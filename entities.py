import math

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
            'target': None
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
    def attack(tower, enemy, dt, projectiles, cell_size):
        """Attack an enemy and create a projectile."""
        if tower['last_fire'] <= 0:
            tower['last_fire'] = tower['fire_rate']
            
            # Create projectile
            tower_center_x = tower['x'] * cell_size + cell_size/2
            tower_center_y = tower['y'] * cell_size + cell_size/2
            
            projectile = {
                'x': tower_center_x,
                'y': tower_center_y,
                'target_x': enemy['x'],
                'target_y': enemy['y'],
                'speed': 300,  # Increase projectile speed significantly
                'damage': tower['damage'],
                'tower_type': tower['type']
            }
            
            projectiles.append(projectile)
            return True
        else:
            tower['last_fire'] = max(0, tower['last_fire'] - dt)  # Use dt directly for consistent timing
            return False

class Enemy:
    @staticmethod
    def create(enemy_type, type_data, base_health, base_speed, spawn_delay, cell_size):
        """Create a new enemy instance."""
        health = base_health * type_data['health_factor']
        speed = base_speed * type_data['speed_factor']
        
        return {
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
            'damage_text': 0,
            'damage_text_timer': 0
        }

    @staticmethod
    def update(enemy, dt, cell_size, paths):
        """Update enemy position and state."""
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
        
        # Calculate the actual speed based on freeze state
        speed = enemy['speed']
        if enemy['frozen']:
            speed *= 0.5  # 50% slower when frozen
        
        # Calculate movement vector
        dx = enemy['target_x'] - enemy['x']
        dy = enemy['target_y'] - enemy['y']
        dist = math.sqrt(dx*dx + dy*dy)
        
        # Move towards target using normalized direction and speed
        if dist <= (speed * dt):  # Check if we would reach or pass the target
            # Reached target, move to next path point
            enemy['x'] = enemy['target_x']
            enemy['y'] = enemy['target_y']
            
            # Since we're using a single path, just move along it
            if not paths or len(paths) == 0:
                return False
                
            current_path = paths[0]  # Use the primary path
            next_position = enemy['path_position'] + 1
            
            if next_position < len(current_path):
                # Move to next point on path
                enemy['path_position'] = next_position
                next_point = current_path[next_position]
                enemy['target_x'] = next_point[0] * cell_size + cell_size/2
                enemy['target_y'] = next_point[1] * cell_size + cell_size/2
                return True
            else:
                # Reached the end of path
                return False
        else:
            # Move towards target
            enemy['x'] += (dx / dist) * speed * dt
            enemy['y'] += (dy / dist) * speed * dt
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