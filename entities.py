import math
from PIL import Image, ImageTk

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
            'health': 100,         # Add base health
            'max_health': 100,     # Add max health
            'show_range': False
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
    def attack(tower, target, dt, projectiles, cell_size, sprite=None):
        tower['attack_cooldown'] -= dt
        if tower['attack_cooldown'] <= 0:
            # Reset cooldown
            tower['attack_cooldown'] = tower['fire_rate']
            
            # Create projectile with proper velocity
            start_x = tower['x'] * cell_size + cell_size/2
            start_y = tower['y'] * cell_size + cell_size/2
            
            projectile = Projectile.create(
                start_x, start_y,
                target['x'], target['y'],
                tower['damage'],
                tower['type'],
                target  # Pass target enemy reference
            )
            projectiles.append(projectile)

class Enemy:
    @staticmethod
    def create(enemy_type, type_data, base_health, base_speed, spawn_delay, cell_size, sprites, enemy_id=None):
        """Create a new enemy instance with animation support."""
        health = base_health * type_data['health_factor']
        speed = base_speed * type_data['speed_factor']

        # Initialize enemy with all required fields
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
            'animation_speed': 100,
            'canvas_image': None,
            # Add missing fields
            'damage_text': 0,
            'damage_text_timer': 0,
            'attack_damage': 5,  # Sát thương khi tấn công tháp
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
                      # Handle shooting - chỉ bắn khi đang trong trạng thái shoot
        enemy['shoot_cooldown'] = enemy.get('shoot_cooldown', 0) - dt
        if enemy['shoot_cooldown'] <= 0 and ('shoot_left' in enemy['direction'] or 'shoot_right' in enemy['direction']):
            # Find nearest tower to shoot at
            nearest_tower = None
            min_dist = float('inf')
            for tower in game.towers:
                dx = tower['x'] * cell_size - enemy['x']
                dy = tower['y'] * cell_size - enemy['y']
                dist = (dx**2 + dy**2)**0.5
                if dist < min_dist and dist <= enemy['attack_range']:  # Chỉ tìm tower trong tầm tấn công
                    min_dist = dist
                    nearest_tower = tower
                    
            if nearest_tower:  # Nếu có tower trong tầm
                projectile = EnemyProjectile.create(
                    enemy['x'], enemy['y'],
                    nearest_tower['x'] * cell_size + cell_size/2,
                    nearest_tower['y'] * cell_size + cell_size/2,
                    1  # Damage value
                )
                projectile['sprite'] = canvas.create_image(
                    enemy['x'], enemy['y'],
                    image=game.ui.enemy_projectile_frames[0],
                    anchor='center'
                )
                game.enemy_projectiles.append(projectile)
                enemy['shoot_cooldown'] = 2  # Reset cooldown
        
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
            'damage': damage,
            'sprite': None,
            'animation_timer': 0,
            'current_frame': 0,
        }
