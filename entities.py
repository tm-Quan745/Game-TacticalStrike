import math
from PIL import Image, ImageTk

class Tower:
    @staticmethod
    def create(x, y, tower_type, tower_info):
        """Create a new tower instance."""
        return {
            'x': x,
            'y': y,
            'type': tower_type,
            'damage': tower_info['damage'],
            'range': tower_info['range'],
            'fire_rate': tower_info['fire_rate'],
            'last_fire': 0,
            'target': None,
            'health': 100,
            'max_health': 100
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
    def attack(tower, enemy, dt, projectiles, cell_size, sprite=None):  # Add sprite parameter
        """Attack an enemy and create a projectile."""
        if tower['last_fire'] <= 0:
            tower['last_fire'] = tower['fire_rate']
            
            # Create projectile with sprite
            tower_center_x = tower['x'] * cell_size + cell_size/2
            tower_center_y = tower['y'] * cell_size + cell_size/2
            
            projectile = {
                'x': tower_center_x,
                'y': tower_center_y,
                'target_x': enemy['x'],
                'target_y': enemy['y'],
                'speed': 300,  # Increase projectile speed significantly
                'damage': tower['damage'],
                'tower_type': tower['type'],
                'sprite': sprite  # Add sprite to projectile data
            }
            
            projectiles.append(projectile)
            return True
        else:
            tower['last_fire'] = max(0, tower['last_fire'] - dt)  # Use dt directly for consistent timing
            return False

class Enemy:
    @staticmethod
    def create(enemy_type, type_data, base_health, base_speed, spawn_delay, cell_size, sprites):
        """Create a new enemy instance with animation support."""
        health = base_health * type_data['health_factor']
        speed = base_speed * type_data['speed_factor']

        # Initialize enemy with all required fields
        enemy = {
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

                # Update animation direction
                if abs(dx) > abs(dy):
                    enemy['direction'] = 'walk_right' if dx > 0 else 'walk_left'
                else:
                    enemy['direction'] = 'walk_updown'

        # Luôn cập nhật animation ngay cả khi đứng im
        current_anim = enemy['animation_frames'].get(enemy['direction'])
        if current_anim and len(current_anim) > 0:
            
            if not enemy.get('canvas_image'):
                enemy['canvas_image'] = canvas.create_image(
                    enemy['x'], enemy['y'],
                    image=current_anim[0],
                    anchor='center',
                    tags='enemy'
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
    def update(projectile, dt):
        """Update projectile position."""
        dx = projectile['target_x'] - projectile['x']
        dy = projectile['target_y'] - projectile['y']
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < projectile['speed']:
            return False  # Projectile hit target
        
        # Move towards target
        projectile['x'] += (dx / dist) * projectile['speed'] * dt
        projectile['y'] += (dy / dist) * projectile['speed'] * dt
        return True