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
            'target': None
        }

    @staticmethod
    def find_target(tower, enemies, cell_size):
        """Find the closest enemy in range."""
        tower_center_x = tower['x'] * cell_size + cell_size / 2
        tower_center_y = tower['y'] * cell_size + cell_size / 2
        tower_range = tower['range'] * cell_size
        
        closest_enemy = None
        min_distance = float('inf')
        
        for enemy in enemies:
            soldier = enemy.get("soldier")  # Safely access the Soldier object
            if not soldier:
                continue  # Skip if Soldier object is missing
            
            dx = soldier.x - tower_center_x
            dy = soldier.y - tower_center_y
            distance = math.sqrt(dx * dx + dy * dy)
            
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
            tower_center_x = tower['x'] * cell_size + cell_size / 2
            tower_center_y = tower['y'] * cell_size + cell_size / 2
            
            # Safely access enemy position
            target_x = enemy.get('x', tower_center_x)
            target_y = enemy.get('y', tower_center_y)
            
            projectile = {
                'x': tower_center_x,
                'y': tower_center_y,
                'target_x': target_x,
                'target_y': target_y,
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
    def create(enemy_type, type_data, base_health, base_speed, spawn_delay, cell_size, sprites):
        """Create a new enemy instance with animation support."""
        def safe_load_sprites(sprites, key, default=[]):
            return sprites[key] if key in sprites else default

        health = base_health * type_data['health_factor']
        speed = base_speed * type_data['speed_factor']

        # Initialize animation frames with safe loading
        animation_frames = {
            "walk_right": safe_load_sprites(sprites, "walk_right"),
            "walk_left": safe_load_sprites(sprites, "walk_left"),
            "walk_up": safe_load_sprites(sprites, "walk_up"),
        }

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
            'damage_text_timer': 0,
            'animation_frames': animation_frames,
            'current_frame': 0,
            'direction': "walk_right",
            'animation_speed': 100,  # Animation speed in ms
            'canvas_image': None,  # Canvas image reference
            'animation_id': None,  # Store the after() ID
        }

    @staticmethod
    def update(enemy, dt, cell_size, paths, canvas):
        """Update enemy position, state, and animation."""
        # Handle spawn delay
        if enemy['spawn_delay'] > 0:
            enemy['spawn_delay'] -= dt
            return True

        # Calculate movement
        dx = enemy['target_x'] - enemy['x']
        dy = enemy['target_y'] - enemy['y']
        distance = (dx**2 + dy**2) ** 0.5

        if distance <= enemy['speed'] * dt:
            # Move to exact target and update path
            enemy['x'], enemy['y'] = enemy['target_x'], enemy['target_y']

            if paths and enemy['path_position'] + 1 < len(paths[0]):
                enemy['path_position'] += 1
                next_point = paths[0][enemy['path_position']]
                enemy['target_x'] = next_point[0] * cell_size + cell_size / 2
                enemy['target_y'] = next_point[1] * cell_size + cell_size / 2
            else:
                return False  # Enemy reached end
        else:
            # Move smoothly
            enemy['x'] += (dx / distance) * enemy['speed'] * dt
            enemy['y'] += (dy / distance) * enemy['speed'] * dt

        # Debug: Print current direction and movement deltas
        print(f"Before update: Direction={enemy.get('direction', 'N/A')}, dx={dx}, dy={dy}")

        # Updated direction logic
        if abs(dx) > abs(dy):
            enemy['direction'] = "walk_right" if dx > 0 else "walk_left"
        else:
            enemy['direction'] = "walk_updown"  # Shared sprite for upward and downward movement

        # Debug: Print updated direction
        print(f"Enemy moving {enemy['direction']} - Target: ({enemy['target_x']}, {enemy['target_y']})")

        # Synchronize animation with movement
        if enemy['direction'] in enemy['animation_frames']:
            frames = enemy['animation_frames'][enemy['direction']]
            if frames:  # Ensure frames are not empty
                # Correct frame index calculation
                enemy['current_frame'] = (enemy['current_frame'] + 1) % len(frames)
                frame = frames[enemy['current_frame']]
                canvas.itemconfig(enemy['canvas_image'], image=frame)
            else:
                print(f"Warning: No frames available for direction '{enemy['direction']}'")
        else:
            print(f"Warning: Direction '{enemy['direction']}' not found in animation frames")

        # Debug: Log movement
        print(f"Enemy moving {enemy['direction']} from ({enemy['x']}, {enemy['y']}) to ({enemy['target_x']}, {enemy['target_y']})")

        # Update canvas position
        canvas.coords(enemy['canvas_image'], enemy['x'], enemy['y'])
        return True

    @staticmethod
    def update_animation(enemy, canvas):
        """Update the enemy's animation frame."""
        try:
            if not canvas.winfo_exists():
                return  # Exit if the canvas no longer exists

            if enemy['direction'] in enemy['animation_frames']:
                frames = enemy['animation_frames'][enemy['direction']]
                if frames:  # Ensure frames are not empty
                    enemy['current_frame'] = (enemy['current_frame'] + 1) % len(frames)
                    frame = frames[enemy['current_frame']]

                    if enemy['canvas_image']:
                        canvas.itemconfig(enemy['canvas_image'], image=frame)
                    else:
                        enemy['canvas_image'] = canvas.create_image(
                            enemy['x'], enemy['y'], image=frame, anchor="center"
                        )

                    # Schedule the next animation frame
                    enemy['animation_id'] = canvas.after(enemy['animation_speed'], Enemy.update_animation, enemy, canvas)
                else:
                    print(f"Warning: No frames loaded for '{enemy['direction']}'")
            else:
                print(f"Warning: No animation frames for direction '{enemy['direction']}'")
        except Exception as e:
            print(f"Error in update_animation: {e}")

    @staticmethod
    def stop_animation(enemy, canvas):
        """Stop the animation by canceling the after() call."""
        if enemy.get('animation_id'):
            canvas.after_cancel(enemy['animation_id'])
            enemy['animation_id'] = None
        if enemy.get('canvas_image'):
            canvas.delete(enemy['canvas_image'])
            enemy['canvas_image'] = None

    @staticmethod
    def move(enemy, dt, cell_size, paths, canvas):
        """Move the enemy along the path."""
        if enemy['spawn_delay'] > 0:
            enemy['spawn_delay'] -= dt
            return True

        # Debug: Print full path and current path position
        if 'debug_printed' not in enemy:
            print(f"Full enemy path: {paths[0] if paths else 'No path'}")
            enemy['debug_printed'] = True

        # Calculate movement vector
        dx = enemy['target_x'] - enemy['x']
        dy = enemy['target_y'] - enemy['y']
        distance = math.sqrt(dx * dx + dy * dy)

        # Debug: Print current position, target, and distance
        print(f"Enemy position: ({enemy['x']}, {enemy['y']}), Target: ({enemy['target_x']}, {enemy['target_y']}), Distance: {distance}")

        # Check if the enemy has reached the target
        if distance < 1:  # Reduced epsilon to avoid getting stuck
            # Debug: Print path progress
            print(f"Enemy reached target at path position: {enemy['path_position']}")

            if paths and len(paths[0]) > enemy['path_position'] + 1:
                enemy['path_position'] += 1
                next_point = paths[0][enemy['path_position']]
                enemy['target_x'] = next_point[0] * cell_size + cell_size / 2
                enemy['target_y'] = next_point[1] * cell_size + cell_size / 2
                # Debug: Print next target
                print(f"Next target: ({enemy['target_x']}, {enemy['target_y']})")
            else:
                # Reached the end of the path
                print("Enemy reached the end of the path.")  # Debug
                return False
        else:
            # Move towards the target
            enemy['x'] += (dx / distance) * enemy['speed'] * dt
            enemy['y'] += (dy / distance) * enemy['speed'] * dt
            # Debug: Print updated position
            print(f"Updated position: ({enemy['x']}, {enemy['y']})")

        # Debug: Print canvas to ensure it is passed correctly
        print(f"Moving enemy {enemy} on canvas {canvas}")

        # Update canvas position
        if enemy['canvas_image']:
            canvas.coords(enemy['canvas_image'], enemy['x'], enemy['y'])
            canvas.update_idletasks()  # Force UI update

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