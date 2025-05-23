import math
from PIL import Image, ImageTk
import pygame
from ui import channels, load_sound_effects 

sound_effects = load_sound_effects()

for i in range(pygame.mixer.get_num_channels()):
    pygame.mixer.Channel(i).stop()

class Tower:
    @staticmethod
    def create(x, y, tower_type, tower_info):
        return {
            'x': x,
            'y': y,
            'type': tower_type,
            'damage': tower_info['damage'],
            'range': tower_info['range'],
            'fire_rate': tower_info['fire_rate'],            
            'attack_cooldown': 0,  # Initialize cooldown
            'health': 200,         # Tăng máu cơ bản lên 200
            'max_health': 200,     # Tăng max health lên 200
            'show_range': False,
            'active_projectiles': 0  # Track number of active projectiles
        }

    @staticmethod
    def find_target(tower, enemies, cell_size):
        """Find the closest enemy in range."""
        tower_center_x = tower['x'] * cell_size + cell_size/2
        tower_center_y = tower['y'] * cell_size + cell_size/2
        tower_range = tower['range'] * cell_size
        
        closest_enemy = None
        min_distance = float('inf')
        
        for enemy in enemies:
            dx = enemy['x'] - tower_center_x
            dy = enemy['y'] - tower_center_y
            distance = math.sqrt(dx*dx + dy*dy)
            if distance <= tower_range and distance < min_distance:
                closest_enemy = enemy
                min_distance = distance
        
        return closest_enemy    
    @staticmethod
    def attack(tower, target, dt, projectiles, cell_size, sprite):
        if tower['attack_cooldown'] <= 0:
            # Reset cooldown
            tower['attack_cooldown'] = tower['fire_rate']
            
            # Create projectile with proper velocity
            start_x = tower['x'] * cell_size + cell_size/2
            start_y = tower['y'] * cell_size + cell_size/2
            
            # Calculate direction to target
            dx = target['x'] - start_x
            dy = target['y'] - start_y
            dist = math.sqrt(dx*dx + dy*dy)
            
            # Set speed based on tower type
            if tower['type'] == 'sniper':
                speed = 400  # Faster for sniper
            elif tower['type'] == 'freezer':
                speed = 150  # Slower for freezer
            else:
                speed = 250  # Default speed
            
            if dist > 0:
                dx = dx / dist * speed
                dy = dy / dist * speed

            # Create projectile with all necessary properties
            projectile = {
                'x': start_x,
                'y': start_y,
                'dx': dx,
                'dy': dy,
                'speed': speed,  # Add speed property
                'tower_type': tower['type'],
                'damage': tower['damage'],
                'target_x': target['x'],
                'target_y': target['y'],
                'sprite': sprite,
                'animation_timer': 0,
                'current_frame': 0,
                'initial_x': start_x,
                'initial_y': start_y,
                'tower_range': tower['range'] * cell_size
            }
            projectiles.append(projectile)
            print(f"[DEBUG] Created projectile at ({start_x}, {start_y}) with range {tower['range'] * cell_size} and speed {speed}")
            
            # Play sound effect if available
            try:
                if tower['type'] == 'shooter':
                    sound = sound_effects['tower_attack_fire']
                    channel = channels['tower_attack_fire']
                elif tower['type'] == 'freezer':
                    sound = sound_effects['tower_attack_ice']
                    channel = channels['tower_attack_ice']
                elif tower['type'] == 'sniper':
                    sound = sound_effects['tower_attack_sniper']
                    channel = channels['tower_attack_sniper']
                else:
                    print(f"[ERROR] Unknown tower type: {tower['type']}")
                    return
                
                sound.set_volume(1.0)
                if not channel.get_busy():
                    channel.play(sound)
                    print(f"[SUCCESS] Playing {tower['type']} attack sound")
            except Exception as e:
                print(f"[ERROR] Sound play failed: {e}")
                
            return projectile
        else:
            tower['attack_cooldown'] -= dt
            return None

class Enemy:
    @staticmethod
    def create(enemy_type, type_data, base_health, base_speed, spawn_delay, cell_size, sprites, enemy_id=None):
        """Create a new enemy instance with animation support."""
        health = base_health * type_data['health_factor']
        speed = base_speed * type_data['speed_factor']        # Initialize enemy with all required fields
        enemy = {
            'id': enemy_id,  # Unique ID for enemy
            'x': cell_size / 2,  # Starting position
            'y': cell_size / 2,
            'health': health,
            'max_health': health,
            'speed': speed,
            'reward': type_data['reward'],
            'path_index': 0,
            'path_position': 0,
            'target_x': 0,
            'target_y': 0,
            'spawn_delay': spawn_delay,
            'frozen': False,
            'freeze_timer': 0,
            'type': enemy_type,
            'animation_frames': sprites,
            'current_frame': 0,
            'direction': "walk_right",            
            'can_shoot': True,  # Enemy có thể bắn
            'shoot_cooldown': 0,  # Thời gian chờ giữa các lần bắn            
            'shoot_rate': 0.15,  # Thời gian giữa các lần bắn (0.15 giây)
            'shoot_range': cell_size * 3,  # Tầm bắn của enemy            
            'shoot_damage': 1,  # Tăng sát thương đạn lên 1
            'animation_speed': 100,
            'canvas_image': None,
            # Add missing fields            
            'damage_text': 0,
            'damage_text_timer': 0,
            'attack_damage': 3,  # Tăng sát thương cận chiến lên 3
            'attack_range': cell_size * 1.5,  # Tầm đánh tháp
            'attack_cooldown': 0,  # Thời gian hồi đánh
            'attack_rate': 1.0,  # Tốc độ đánh (giây)
        }
    
        return enemy

    @staticmethod
    def update(enemy, dt, cell_size, paths, canvas, game):
        """Update enemy position and animation."""
        # Handle spawn delay
        if enemy['spawn_delay'] > 0:
            enemy['spawn_delay'] -= 1 * dt
            return True
        
        # Handle freeze effect
        if enemy['frozen']:
            enemy['freeze_timer'] -= 1 * dt
            if enemy['freeze_timer'] <= 0:
                enemy['frozen'] = False
        
        # Update damage text timer
        if enemy['damage_text_timer'] > 0:
            enemy['damage_text_timer'] -= 1 * dt
        
        # Tính speed dựa trên trạng thái
        speed = enemy['speed']
        if enemy['frozen']:
            speed *= 0.5
        
        # Kiểm tra tower trong tầm đánh
        has_tower_in_range = False
        for tower in game.towers:
            tower_x = tower['x'] * cell_size + cell_size/2
            tower_y = tower['y'] * cell_size + cell_size/2
            dx = tower_x - enemy['x']
            dy = tower_y - enemy['y']
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist <= enemy['attack_range']:
                channels['enemy_walk'].stop()
                if not channels['enemy_attack'].get_busy():
                    channels['enemy_attack'].play(sound_effects['enemy_attack'])
                has_tower_in_range = True
                if enemy['attack_cooldown'] <= 0:
                    tower['health'] -= enemy['attack_damage']
                    enemy['attack_cooldown'] = enemy['attack_rate']
                    
                    canvas.create_text(
                        tower_x, tower_y - 10,
                        text=f"-{enemy['attack_damage']}",
                        fill="red", 
                        font=("Arial", 10, "bold"),
                        tags="damage_text"
                    )                    
                    if tower['health'] <= 0:
                        # Phát âm thanh nổ trước khi dừng các âm thanh khác
                        channels['tower_explosion'].play(sound_effects['tower_explosion'])
                        # Sau đó mới dừng các âm thanh khác
                        channels['enemy_walk'].stop()
                        channels['enemy_attack'].stop()
                        # Xóa tower và cập nhật maze
                        game.towers.remove(tower)
                        game.maze[tower['y']][tower['x']] = 0
                break

        if enemy['attack_cooldown'] > 0:
            enemy['attack_cooldown'] -= dt
        if has_tower_in_range:
            # Tọa độ pixel chính xác của tower (nếu tower lưu theo lưới)
            tower_px_x = tower['x'] * cell_size + cell_size / 2
            dx = tower_px_x - enemy['x']

            # Bắn trái/phải dựa vào tọa độ pixel thật
            enemy['direction'] = 'shoot_right' if dx >= 0 else 'shoot_left'
        
        # Di chuyển nếu không đang tấn công tower
        if not has_tower_in_range:

            # Lấy vị trí target từ path
            if paths and paths[0]:
                current_path = paths[0]
                next_point = current_path[enemy['path_position']]
                enemy['target_x'] = next_point[0] * cell_size + cell_size/2
                enemy['target_y'] = next_point[1] * cell_size + cell_size/2
                
                # Calculate movement vector
                dx = enemy['target_x'] - enemy['x']
                dy = enemy['target_y'] - enemy['y']
                dist = math.sqrt(dx*dx + dy*dy)
                
                if dist < speed * dt:
                    # Đã đến điểm tiếp theo
                    enemy['x'] = enemy['target_x']        
                    enemy['y'] = enemy['target_y']
                    enemy['path_position'] += 1
                    
                    # Kiểm tra đã đến đích chưa
                    if enemy['path_position'] >= len(current_path):
                        return False
                else:
                    # Di chuyển theo hướng
                    if not channels['enemy_walk'].get_busy():
                        channels['enemy_walk'].play(sound_effects['enemy_walk'])

                    enemy['x'] += (dx / dist) * speed * dt
                    enemy['y'] += (dy / dist) * speed * dt

                if has_tower_in_range:
                    # Set shooting direction based on tower position
                    enemy['direction'] = 'shoot_right' if dx > 0 else 'shoot_left'
                # Update animation direction
                if abs(dx) > abs(dy):
                    enemy['direction'] = 'walk_right' if dx > 0 else 'walk_left'
                else:
                    enemy['direction'] = 'walk_updown'



                    
         # Handle shooting
                      # Handle shooting - chỉ bắn khi đang trong trạng thái shoot
        enemy['shoot_cooldown'] = enemy.get('shoot_cooldown', 0) - dt
        
        # Kiểm tra tower trong tầm đánh và xác định hướng bắn
        nearest_tower = None
        min_dist = float('inf')
        for tower in game.towers:
            tower_x = tower['x'] * cell_size + cell_size/2
            tower_y = tower['y'] * cell_size + cell_size/2
            dx = tower_x - enemy['x']
            dy = tower_y - enemy['y']
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist <= enemy.get('attack_range', cell_size * 3) and dist < min_dist:
                min_dist = dist
                nearest_tower = tower
                # Cập nhật hướng bắn dựa trên vị trí tower
                enemy['direction'] = 'shoot_right' if dx >= 0 else 'shoot_left'
        
        # Bắn khi có tower trong tầm và hết cooldown
        if nearest_tower and enemy['shoot_cooldown'] <= 0:
            tower_x = nearest_tower['x'] * cell_size + cell_size/2
            tower_y = nearest_tower['y'] * cell_size + cell_size/2            # Tạo một đạn đi thẳng đến tower
            base_damage = enemy.get('attack_damage', 5)
            
            # Tạo đạn nhắm thẳng vào tower
            projectile = EnemyProjectile.create(
                enemy['x'], enemy['y'],
                tower_x,  # Nhắm trực tiếp vào tower
                tower_y,
                base_damage
            )
            
            projectile['sprite'] = canvas.create_image(
                enemy['x'], enemy['y'],
                image=game.ui.enemy_projectile_frames[0],
                anchor='center',
                tags='enemy_projectile'
            )
            
            game.enemy_projectiles.append(projectile)
            
            # Reset cooldown với tốc độ bắn nhanh hơn
            enemy['shoot_cooldown'] = enemy.get('shoot_rate', 0.3)  # Giảm cooldown xuống 0.3s

        # Create or update enemy sprite with unique tag
        enemy_tag = f"enemy_{enemy['id']}"
        current_anim = enemy['animation_frames'].get(enemy['direction'])
        if current_anim and len(current_anim) > 0:
            if not enemy.get('canvas_image'):
                # Delete any existing sprite with this tag first
                canvas.delete(enemy_tag)
                enemy['canvas_image'] = canvas.create_image(
                    enemy['x'], enemy['y'],
                    image=current_anim[0],
                    anchor='center',
                    tags=(enemy_tag, 'enemy')  # Add both unique and group tags
                )
            else:
                # Update animation frame
                frame_index = (enemy['current_frame'] + 1) % len(current_anim)
                enemy['current_frame'] = frame_index
                frame = current_anim[frame_index]
                canvas.itemconfig(enemy['canvas_image'], image=frame)
                canvas.coords(enemy['canvas_image'], enemy['x'], enemy['y'])

        return True

class Projectile:
    @staticmethod
    def create(start_x, start_y, target_x, target_y, damage, tower_type, target_enemy,sprite=None):
        return {
            'x': start_x,
            'y': start_y,
            'dx': 0,
            'dy': 0,
            'target_x': target_x,
            'target_y': target_y,
            'damage': damage,
            'tower_type': tower_type,
            'target_enemy': target_enemy,  # Track target enemy
            'speed': 8,  # Increased speed
            'sprite': None
        }

    @staticmethod
    def update(projectile, dt):
        if projectile['target_enemy']:
            # Update target position to enemy's current position
            projectile['target_x'] = projectile['target_enemy']['x']
            projectile['target_y'] = projectile['target_enemy']['y']
            
            # Calculate new direction to enemy
            dx = projectile['target_x'] - projectile['x']
            dy = projectile['target_y'] - projectile['y']
            length = (dx**2 + dy**2)**0.5
            
            if length > 0:
                # Update velocity to track enemy
                projectile['dx'] = (dx/length) * projectile['speed']
                projectile['dy'] = (dy/length) * projectile['speed']
        
        # Move projectile
        projectile['x'] += projectile['dx'] * dt * 60
        projectile['y'] += projectile['dy'] * dt * 60
        
        # Check if hit target
        dist = ((projectile['target_x'] - projectile['x'])**2 + 
                (projectile['target_y'] - projectile['y'])**2)**0.5
        return dist > 5
    
class EnemyProjectile:    
    @staticmethod
    def create(x, y, target_x, target_y, damage):
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx**2 + dy**2)
        speed = 150  # pixels/second

        return {
            'x': x,
            'y': y,
            'target_x': target_x,
            'target_y': target_y,
            'dx': (dx / dist) * speed,
            'dy': (dy / dist) * speed,
            'damage': min(1, damage),  # Đảm bảo damage không vượt quá 1
            'sprite': None,
            'animation_timer': 0,
            'current_frame': 0,
        }
