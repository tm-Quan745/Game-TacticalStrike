import random
import time
import math
from tkinter import messagebox, ttk
import tkinter as tk
from maze_generator import generate_maze
from pathfinding import find_path
from entities import Tower, Enemy, Projectile,EnemyProjectile
from PIL import Image, ImageTk
import customtkinter as ctk
from ui import channels, load_sound_effects 
import math
from radar_view import RadarView
import pygame
pygame.mixer.init()
for i in range(pygame.mixer.get_num_channels()):
    pygame.mixer.Channel(i).stop()
    
sound_effects = load_sound_effects()
class MazeTowerDefenseGame:
    def __init__(self, root):
        self.enemy_counter = 0  # Counter for generating unique enemy IDs
        self.root = root
        
        # Game parameters
        self.grid_size = 13
        self.cell_size = 45
        self.cols = self.grid_size
        self.rows = self.grid_size  # Add this line to fix the error
        self.initial_money = 100  # Add initial money value
        self.initial_lives = 20   # Add initial lives value
        self.maze = []
        self.towers = []
        self.enemies = []
        self.paths = []
        self.projectiles = []
        self.money = self.initial_money
        self.lives = self.initial_lives
        self.current_wave = 0
        self.wave_in_progress = False
        self.selected_algo = tk.StringVar(value="BFS")
        self.score = 0
        self.radar_view = None
        self.build_mode = None
        self.sprite_path = "./sprites/"
        self.enemy_projectiles = []
        
        # Tower info
        self.tower_types = {
            "shooter": {
                "name": "Tháp Bắn",
                "cost": 25,
                "damage": 15,
                "range": 3,
                "fire_rate": 0.8,  # Bắn nhanh hơn
                "color": "#3498db",
                "description": "Bắn kẻ địch từ xa với tốc độ cao"
            },
            "freezer": {
                "name": "Tháp Đóng Băng",
                "cost": 35,
                "damage": 8,
                "range": 2,
                "fire_rate": 1.2,  # Chậm hơn shooter nhưng hiệu ứng đóng băng
                "color": "#00bcd4",
                "description": "Làm chậm và gây sát thương nhẹ"
            },
            "sniper": {
                "name": "Tháp Bắn Tỉa",
                "cost": 60,
                "damage": 45,
                "range": 4,
                "fire_rate": 2.5,  # Chậm nhất nhưng sát thương cao
                "color": "#9b59b6",
                "description": "Gây sát thương lớn với tầm xa"
            }
        }
        
        # Enemy types
        self.enemy_types = {            "normal": {
                "color": "#e67e22",
                "speed_factor": 1.2,  # Tăng tốc độ cơ bản
                "health_factor": 1.2,
                "damage": 8,
                "reward": 12
            },
            "fast": {
                "color": "#e74c3c",
                "speed_factor": 2.0,  # Tăng tốc độ của fast unit
                "health_factor": 0.7,
                "damage": 12,
                "reward": 18
            },
            "tank": {
                "color": "#7f8c8d",
                "speed_factor": 0.8,  # Tăng tốc độ của tank unit
                "health_factor": 3.0,
                "damage": 15,
                "reward": 25
            }
        }
        
        try:
            # Load projectile sprites
            shoot_right = Image.open(f"{self.sprite_path}shoot_right.png")
            shoot_left = Image.open(f"{self.sprite_path}shoot_left.png")
            projectile_sprite = Image.open(f"{self.sprite_path}grass3.png")
            
            # Resize projectile sprites
            shoot_right = shoot_right.resize((32, 32), Image.Resampling.LANCZOS) 
            shoot_left = shoot_left.resize((32, 32), Image.Resampling.LANCZOS)
            
            self.projectile_sprites = {
                'shoot_right': ImageTk.PhotoImage(shoot_right),
                'shoot_left': ImageTk.PhotoImage(shoot_left)
            }
            print(f"Loaded projectile sprites from {self.sprite_path}")
            self.enemy_projectile_frames = []
            for i in range(4):
                rotated = projectile_sprite.rotate(90 * i)
                self.enemy_projectile_frames.append(ImageTk.PhotoImage(rotated))
        except Exception as e:
            print(f"Error loading projectile sprites: {e}")
            placeholder = Image.new('RGBA', (16, 16), 'yellow')
            self.projectile_sprites = {
                'shoot_right': ImageTk.PhotoImage(placeholder),
                'shoot_left': ImageTk.PhotoImage(placeholder)
            }
        
        
        # Initialize UI (needs to be imported here to avoid circular imports)
        from ui import GameUI
        self.ui = GameUI(root, self)
        
        # Initialize game
        self.generate_maze()
        self.setup_events()
    
    def setup_events(self):
        self.ui.canvas.bind("<Button-1>", self.on_canvas_click)
        self.ui.canvas.bind("<Motion>", self.on_canvas_hover)
        self.root.after(50, self.game_loop)
    
    def generate_maze(self):
        """Generate a new random maze."""
        # Đóng radar view nếu đang mở
        if self.radar_view:
            self.radar_view.hide()
            self.radar_view = None
            
        self.maze = generate_maze(self.grid_size)
        
        # Add start point (top-left)
        self.maze[0][0] = 0
        # Add end point (bottom-right) 
        self.maze[self.grid_size-1][self.grid_size-1] = 0
        
        # Reset game state
        self.towers = []
        self.enemies = []
        self.projectiles = []
        self.money = self.initial_money
        self.lives = self.initial_lives
        self.score = 0
        self.current_wave = 0
        self.wave_in_progress = False
        self.build_mode = None
        self.ui.canvas.delete("all")

        
        # Reset UI
        self.ui.status_label.configure(text="Hãy xây tháp và bắt đầu!")
        self.ui.start_button.configure(text="Bắt Đầu Làn Sóng", state="normal")
        # Find paths for all algorithms
        self.find_paths()
  
        
    
    def find_paths(self):
        # Find a single path using the selected algorithm
        algo = self.selected_algo.get()
        
        # Nếu là Partial, tạo radar view
        if algo == "Partial":
            if not self.radar_view:
                self.radar_view = RadarView(self.root, self.grid_size, 20)
            self.radar_view.show()
        else:
            # Đóng radar view nếu đang mở và chuyển sang thuật toán khác
            if self.radar_view:
                self.radar_view.hide()
                self.radar_view = None
        
        path = find_path(self.maze, self.grid_size, algo)
        if not path:
            return
            
        self.paths = [path]
        
        # Update path for all enemies
        for enemy in self.enemies:
            # Reset path tracking
            enemy['path_index'] = 0
            enemy['path_position'] = 0
            
            # Set initial target position
            next_pos = self.paths[0][0]
            enemy['target_x'] = next_pos[0] * self.cell_size + self.cell_size/2
            enemy['target_y'] = next_pos[1] * self.cell_size + self.cell_size/2
    
    def game_loop(self):
        if not hasattr(self, 'last_update'):
            self.last_update = time.time()
        
        current_time = time.time()
        dt = current_time - self.last_update
        self.last_update = current_time
        
        # Update game logic
        self.update_enemies(dt)
        self.update_towers(dt)
        self.update_projectiles(dt)
        self.check_wave_end()
        self.update_enemy_projectiles(dt)
        self.update_belief_state()  # Cập nhật radar view
        
        # Update UI
        self.ui.draw_maze()
        
        # Schedule next frame
        self.root.after(50, self.game_loop)
    
    def update_enemies(self, dt):
        for enemy in self.enemies[:]:
            if not Enemy.update(enemy, dt, self.cell_size, self.paths, self.ui.canvas, self):  # Pass self (game instance)
                # Enemy reached the end               
                self.lives -= 1
                self.enemies.remove(enemy)
                if self.lives <= 0:
                    channels['gameover'].play(sound_effects['gameover'])
                    self.game_over()
                else:
                    self.ui.update_info_labels()    
    def update_towers(self, dt):
        for tower in self.towers:
            target = Tower.find_target(tower, self.enemies, self.cell_size)
            
            if target and tower['attack_cooldown'] <= 0:
                # For sniper tower, only shoot if no active projectile
                if tower['type'] == 'sniper' and tower['active_projectiles'] > 0:
                    continue
                    
                print(f"[DEBUG] {tower['type']} tower attacking target at position ({target['x']}, {target['y']})")
                Tower.attack(tower, target, dt, self.projectiles, self.cell_size, sprite=None)
                
                # Increment active projectiles for sniper tower
                if tower['type'] == 'sniper':
                    tower['active_projectiles'] += 1
                    
            elif tower['attack_cooldown'] > 0:
                tower['attack_cooldown'] -= dt
                if tower['attack_cooldown'] < 0:
                    tower['attack_cooldown'] = 0    
    def update_projectiles(self, dt):
        to_remove = []
        
        for projectile in self.projectiles[:]:
            # Kiểm tra khoảng cách từ vị trí ban đầu
            dx_from_tower = projectile['x'] - projectile['initial_x']
            dy_from_tower = projectile['y'] - projectile['initial_y']
            dist_from_tower = math.sqrt(dx_from_tower*dx_from_tower + dy_from_tower*dy_from_tower)
            
            # Nếu vượt quá tầm bắn -> xóa ngay lập tức
            if dist_from_tower > projectile['tower_range']:
                print(f"[DEBUG] Removing projectile - Distance {dist_from_tower:.2f} > Range {projectile['tower_range']}")
                if projectile.get('sprite'):
                    self.ui.canvas.delete(projectile['sprite'])
                if projectile['tower_type'] == 'sniper':
                    for tower in self.towers:
                        if tower['type'] == 'sniper':
                            tower['active_projectiles'] -= 1
                to_remove.append(projectile)
                continue
                
            # Tìm mục tiêu gần nhất
            current_target = None
            min_dist = float('inf')
            
            for enemy in self.enemies:
                dx = enemy['x'] - projectile['x']
                dy = enemy['y'] - projectile['y']
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < min_dist:
                    min_dist = dist
                    current_target = enemy
            
            # Cập nhật vị trí nếu còn trong tầm bắn
            if dist_from_tower <= projectile['tower_range']:
                if current_target:
                    # Tính toán hướng di chuyển mới
                    dx = current_target['x'] - projectile['x']
                    dy = current_target['y'] - projectile['y']
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist > 0:
                        projectile['dx'] = (dx / dist) * projectile['speed']
                        projectile['dy'] = (dy / dist) * projectile['speed']
                
                # Di chuyển đạn
                projectile['x'] += projectile['dx'] * dt
                projectile['y'] += projectile['dy'] * dt
                
                # Cập nhật vị trí sprite
                if projectile.get('sprite'):
                    self.ui.canvas.coords(projectile['sprite'], projectile['x'], projectile['y'])
                    
                    # Cập nhật góc xoay sprite
                    angle = math.degrees(math.atan2(projectile['dy'], projectile['dx']))
                    if angle < 0:
                        angle += 360
                    frame_index = int(((angle + 22.5) % 360) // 45)
                    
                    if frame_index != projectile.get('frame_index', -1):
                        projectile['frame_index'] = frame_index
                        if frame_index < len(self.ui.projectile_sprites[projectile['tower_type']]):
                            self.ui.canvas.itemconfig(
                                projectile['sprite'],
                                image=self.ui.projectile_sprites[projectile['tower_type']][frame_index]
                            )
                
                # Kiểm tra va chạm
                if current_target and min_dist < self.cell_size / 2:
                    current_target['health'] -= projectile['damage']
                    
                    if projectile['tower_type'] == 'freezer':
                        current_target['frozen'] = True
                        current_target['freeze_timer'] = 100
                        
                    if current_target['health'] <= 0:
                        self.money += current_target['reward']
                        self.score += current_target['reward']
                        self.enemies.remove(current_target)
                        self.ui.update_info_labels()
                    
                    to_remove.append(projectile)
                    if projectile['tower_type'] == 'sniper':
                        for tower in self.towers:
                            if tower['type'] == 'sniper':
                                tower['active_projectiles'] -= 1
            
        # Xóa các projectile đã đánh dấu
        for proj in to_remove:
            if proj in self.projectiles:
                if proj.get('sprite'):
                    self.ui.canvas.delete(proj['sprite'])
                self.projectiles.remove(proj)

    def update_enemy_projectiles(self, dt):
        to_remove = []
        for projectile in self.enemy_projectiles:
            # Di chuyển
            projectile['x'] += projectile['dx'] * dt
            projectile['y'] += projectile['dy'] * dt

            # Cập nhật vị trí sprite
            self.ui.canvas.coords(projectile['sprite'], projectile['x'], projectile['y'])

            # Animation xoay
            projectile['animation_timer'] += dt
            if projectile['animation_timer'] >= 0.1:
                projectile['animation_timer'] = 0
                projectile['current_frame'] = (projectile['current_frame'] + 1) % len(self.ui.enemy_projectile_frames)
                self.ui.canvas.itemconfig(projectile['sprite'],
                                        image=self.ui.enemy_projectile_frames[projectile['current_frame']])

            # Kiểm tra va chạm với tower
            for tower in self.towers:
                tower_x = tower['x'] * self.cell_size + self.cell_size / 2
                tower_y = tower['y'] * self.cell_size + self.cell_size / 2                
                if abs(projectile['x'] - tower_x) < 15 and abs(projectile['y'] - tower_y) < 15:
                    # Sử dụng damage từ projectile, default là 1 nếu không có
                    damage = projectile.get('damage', 1)  # Giảm default damage xuống 1
                    tower['health'] -= damage
                    
                    # Hiển thị damage
                    damage_text = self.ui.canvas.create_text(
                        tower_x, tower_y - 20,
                        text=str(damage),
                        fill="red",
                        font=("Arial", 12, "bold")
                    )
                    self.root.after(1000, lambda x=damage_text: self.ui.canvas.delete(x))
                    
                    print(f"Enemy deals {damage} damage to tower! Tower health: {tower['health']}")
                    
                    if tower['health'] <= 0:
                        print("Tower destroyed!")
                        self.towers.remove(tower)
                        self.maze[tower['y']][tower['x']] = 0
                        if hasattr(tower, 'sprite'):
                            self.ui.canvas.delete(tower['sprite'])
                    
                    to_remove.append(projectile)
                    self.ui.canvas.delete(projectile['sprite'])
                    break

            # Loại bỏ nếu vượt ra ngoài
            if not (0 <= projectile['x'] <= self.cols * self.cell_size and
                    0 <= projectile['y'] <= self.rows * self.cell_size):
                to_remove.append(projectile)
                self.ui.canvas.delete(projectile['sprite'])

        for proj in to_remove:
            if proj in self.enemy_projectiles:
                self.enemy_projectiles.remove(proj)


    
    def check_wave_end(self):
        if self.wave_in_progress and not self.enemies:
            self.wave_in_progress = False
            self.current_wave += 1
            
            # Tăng phần thưởng theo wave
            wave_bonus = 20 + self.current_wave * 10
            self.money += wave_bonus
            
            # Thông báo hoàn thành wave và chỉ số mới            
            completion_text = f"Hoàn thành làn sóng {self.current_wave-1}!\n"
            completion_text += f"Nhận thưởng: {wave_bonus}$\n"
            completion_text += f"\nLàn sóng tiếp theo:\n"
            completion_text += f"- Số lượng địch: {8 + int(self.current_wave * 4)}\n"
            completion_text += f"- Máu cơ bản: {int(50 * (1 + self.current_wave * 0.2))}\n"
            completion_text += f"- Sát thương đạn: {max(1, int(1 + self.current_wave * 0.5))}\n"
            
            messagebox.showinfo("Hoàn thành làn sóng", completion_text)
            
            self.ui.update_info_labels()
            self.ui.start_button.configure(text="Bắt Đầu Làn Sóng")
    
    def start_wave(self):
        if not self.wave_in_progress:
            self.wave_in_progress = True
            self.spawn_enemies()
            self.ui.start_button.configure(text="Làn Sóng Đang Diễn Ra...")
    
    def spawn_enemies(self):
        """Spawn enemies with sprite animations."""
        try:
            if not hasattr(self, 'enemy_sprites'):
                
                # Load sprites
                walk_right = self.ui.load_sprites(f"{self.sprite_path}walkright.png", 4)
                walk_left = self.ui.load_sprites(f"{self.sprite_path}walkleft.png", 4) 
                walk_updown = self.ui.load_sprites(f"{self.sprite_path}walkup.png", 4)
                shoot_right = self.ui.load_sprites(f"{self.sprite_path}shoot_right.png", 4)
                shoot_left = self.ui.load_sprites(f"{self.sprite_path}shoot_left.png", 4)
                
                self.enemy_sprites = {
                    'walk_right': walk_right,
                    'walk_left': walk_left,
                    'walk_updown': walk_updown,
                    'shoot_right': shoot_right,
                    'shoot_left': shoot_left
                }
        except Exception as e:
            print(f"Error loading sprites: {e}")
            # Create placeholder sprites if loading fails
            placeholder = Image.new('RGBA', (32, 32), 'red')
            placeholder_image = ImageTk.PhotoImage(placeholder)
            self.enemy_sprites = {
                'walk_right': [placeholder_image],
                'walk_left': [placeholder_image], 
                'walk_updown': [placeholder_image],
                'shoot_right': [placeholder_image],
                'shoot_left': [placeholder_image]
            } 
        
        # Tính toán chỉ số tăng theo wave
        wave_multiplier = 1 + (self.current_wave * 0.2)  # Tăng 20% mỗi wave
        num_enemies = 8 + int(self.current_wave * 4)  # Tăng số lượng enemy
        
        # Tăng máu và damage theo cấp số nhân
        base_health = int(50 * wave_multiplier)
        base_damage = int(self.current_wave * 2)  # Damage bonus theo wave        
        # Tăng tốc độ với giới hạn tối đa (về như cũ)
        base_speed = 30 + min(75, self.current_wave * 6)
          # Thêm hệ số tăng tốc ngẫu nhiên (1.0 - 1.3) - chỉ có thể nhanh hơn
        speed_variation = 1.0 + random.random() * 0.3
        base_speed *= speed_variation
        
        # Tính toán spawn delay dựa trên wave
        # Wave đầu: 8s, giảm nhanh ở wave đầu và chậm dần ở các wave sau
        initial_delay = 8.0
        reduction_factor = 0.8 ** self.current_wave  # Giảm theo hàm mũ
        min_delay = 0.5  # Giảm minimum delay xuống 0.5s
        
        spawn_delay_base = max(min_delay, initial_delay * reduction_factor)
        
        # Thêm biến động spawn delay để tạo đợt tấn công dày đặc
        if self.current_wave > 5:  # Từ wave 6 trở đi
            if random.random() < 0.3:  # 30% cơ hội tạo đợt tấn công dày đặc
                spawn_delay_base *= 0.5  # Giảm một nửa thời gian chờ
          # Tỉ lệ xuất hiện enemy đặc biệt tăng theo wave
        tank_chance = min(0.35, 0.15 + self.current_wave * 0.03)
        fast_chance = min(0.45, 0.25 + self.current_wave * 0.04)
        
        print(f"[Wave {self.current_wave}] Spawning {num_enemies} enemies:")
        print(f"Base Health: {base_health}, Base Speed: {base_speed}, Base Damage: {base_damage}")
        print(f"Tank chance: {tank_chance:.2%}, Fast chance: {fast_chance:.2%}")
        print(f"Spawn Delay: {spawn_delay_base:.1f}s")  # Log spawn delay
        
        print(f"[Wave {self.current_wave}] Spawning {num_enemies} enemies:")
        print(f"Base Health: {base_health}, Base Speed: {base_speed}, Base Damage: {base_damage}")
        print(f"Tank chance: {tank_chance:.2%}, Fast chance: {fast_chance:.2%}")
        
        for i in range(num_enemies):
            enemy_type = "normal"
            if self.current_wave >= 1:  # Bắt đầu xuất hiện enemy đặc biệt từ wave 1
                r = random.random()
                if r < tank_chance:
                    enemy_type = "tank"
                elif r < (tank_chance + fast_chance):
                    enemy_type = "fast"
              # Điều chỉnh chỉ số theo loại enemy
            type_data = self.enemy_types[enemy_type]
            enemy_health = int(base_health * type_data['health_factor'])
            enemy_speed = base_speed * type_data['speed_factor']            # Tính toán damage dựa trên wave, bắt đầu từ mức rất thấp
            base_shot_damage = max(1, int(0.5 + self.current_wave * 0.1))  # Bắt đầu từ 0.5, tăng 0.01 mỗi wave
            enemy_damage = type_data['damage'] + base_damage  # Damage cận chiến
            
            # Thêm bonus damage và health cho enemy đặc biệt theo wave
            if enemy_type in ["tank", "fast"]:
                enemy_health += int(self.current_wave * 10)
                enemy_damage += int(self.current_wave * 1.5)  # Thêm damage bonus cho enemy mạnh
                base_shot_damage = int(base_shot_damage * 1.1)  # Enemy đặc biệt gây thêm 10% sát thương đạn
            self.enemy_counter += 1            # Add damage to type_data
            type_data = dict(type_data)  # Create a copy to avoid modifying the original
            type_data['damage'] = enemy_damage
            type_data['shoot_damage'] = base_shot_damage  # Thêm sát thương đạn
            
            enemy = Enemy.create(
                enemy_type,
                type_data,
                enemy_health,
                enemy_speed,
                i * spawn_delay_base,
                self.cell_size,
                self.enemy_sprites,
                self.enemy_counter
            )
            self.enemies.append(enemy)
    
    def game_over(self):
        # Đóng radar view nếu đang mở
        if self.radar_view:
            self.radar_view.hide()
            self.radar_view = None
            
        self.wave_in_progress = False
        messagebox.showinfo("Game Over", f"Game Over! Final Score: {self.score}")
        self.generate_maze()

    def update_belief_state(self):
        """Cập nhật belief_state dựa trên vị trí quân địch và tháp"""
        if not self.radar_view or self.selected_algo.get() != "Partial":
            return
            
        belief_state = [[-1] * self.grid_size for _ in range(self.grid_size)]
        
        # Cập nhật từ vị trí quân địch
        for enemy in self.enemies:
            x, y = int(enemy['x'] / self.cell_size), int(enemy['y'] / self.cell_size)
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    new_x, new_y = x + dx, y + dy
                    if (0 <= new_x < self.grid_size and
                        0 <= new_y < self.grid_size and
                        abs(dx) + abs(dy) <= 2):
                        belief_state[new_y][new_x] = self.maze[new_y][new_x]
                        
        # Cập nhật từ vị trí tháp
        for tower in self.towers:
            x, y = tower['x'], tower['y']
            belief_state[y][x] = self.maze[y][x]  # Tháp luôn nhìn thấy vị trí của nó
        
        self.radar_view.update_view(self.maze, belief_state)

    def add_tower(self, x, y, tower_type):
        """Add a new tower at the specified position."""
        tower = Tower.create(x, y, tower_type, self.tower_types[tower_type])
        self.towers.append(tower)
        self.maze[y][x] = 2  # Mark cell as containing a tower
        self.update_belief_state()  # Cập nhật radar view
    
    def play_sound(self, sound_name):
        # Placeholder for sound effects
        pass
        
    def on_canvas_click(self, event):
        # Convert mouse coordinates to grid coordinates
        grid_x = event.x // self.cell_size
        grid_y = event.y // self.cell_size
        
        if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
            # Check if it's an empty cell and not a path
            if (self.maze[grid_y][grid_x] == 0 and 
                (grid_x, grid_y) != (0, 0) and 
                (grid_x, grid_y) != (self.grid_size-1, self.grid_size-1)):
                
                # Can only build towers before wave starts
                if self.wave_in_progress and self.build_mode in self.tower_types:
                    self.ui.status_label.configure(text="Không thể xây tháp khi làn sóng đang diễn ra!")
                    return
                
                # Build/delete tower based on build_mode
                if hasattr(self, 'build_mode'):
                    if self.build_mode in self.tower_types and self.money >= self.tower_types[self.build_mode]["cost"]:
                        # Check if path still exists after tower placement
                        test_maze = [row[:] for row in self.maze]
                        test_maze[grid_y][grid_x] = 2
                        if not find_path(test_maze, self.grid_size, self.selected_algo.get()):
                            self.ui.status_label.configure(text="Không thể xây tháp ở đây vì sẽ chặn hết đường đi!")
                            return
                        self.add_tower(grid_x, grid_y, self.build_mode)
                        self.money -= self.tower_types[self.build_mode]["cost"]
                        self.play_sound("build")
                    elif self.build_mode == "delete":
                        # Delete tower if exists
                        for tower in self.towers[:]:
                            if tower['x'] == grid_x and tower['y'] == grid_y:
                                self.towers.remove(tower)
                                self.money += 5  # Refund some money
                                self.maze[grid_y][grid_x] = 0  # Mark as empty
                                self.update_belief_state()  # Cập nhật radar view
                                self.play_sound("sell")
                
                # Redraw the maze
                self.ui.draw_maze()
                self.ui.update_info_labels()
                
                # Recalculate paths for enemies
                self.find_paths()
            elif self.maze[grid_y][grid_x] == 2 and self.build_mode == "delete":
                # Delete tower if in delete mode
                for tower in self.towers[:]:
                    if tower['x'] == grid_x and tower['y'] == grid_y:
                        self.towers.remove(tower)
                        self.money += 5  # Refund some money
                        self.maze[grid_y][grid_x] = 0  # Mark as empty
                        self.play_sound("sell")
                
                # Redraw the maze
                self.ui.draw_maze()
                self.ui.update_info_labels()
                
                # Recalculate paths for enemies
                self.find_paths()
    
    def on_canvas_hover(self, event):
        # Convert mouse coordinates to grid coordinates
        grid_x = event.x // self.cell_size
        grid_y = event.y // self.cell_size
        
        # Update the status label with hover information
        if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
            if (grid_x, grid_y) == (0, 0):
                self.ui.status_label.configure(text="Điểm Xuất Phát (Kẻ địch)")
            elif (grid_x, grid_y) == (self.grid_size-1, self.grid_size-1):
                self.ui.status_label.configure(text="Điểm Đích (Bảo vệ đây!)")
            elif self.maze[grid_y][grid_x] == 1:
                self.ui.status_label.configure(text="Tường (Không thể xây tháp)")
            elif self.maze[grid_y][grid_x] == 2:
                # Find the tower at this position
                for tower in self.towers:
                    if tower['x'] == grid_x and tower['y'] == grid_y:
                        tower_type = tower['type']
                        tower_info = self.tower_types[tower_type]
                        status = f"{tower_info['name']} | DMG: {tower['damage']} | RNG: {tower['range']}"
                        self.ui.status_label.configure(text=status)
                        tower['show_range'] = True
                        # Redraw to show range
                        self.ui.draw_maze()
                        break
            
            # Preview tháp trên radar view khi đang trong build mode
            if hasattr(self, 'build_mode') and self.build_mode in self.tower_types:
                if self.maze[grid_y][grid_x] == 0:  # Chỉ preview trên ô trống
                    test_maze = [row[:] for row in self.maze]
                    test_maze[grid_y][grid_x] = 2
                    
                    if self.radar_view and self.selected_algo.get() == "Partial":
                        preview_belief = [[-1] * self.grid_size for _ in range(self.grid_size)]
                        
                        # Copy current vision from enemies
                        for enemy in self.enemies:
                            x, y = int(enemy['x'] / self.cell_size), int(enemy['y'] / self.cell_size)
                            for dy in range(-2, 3):
                                for dx in range(-2, 3):
                                    new_x, new_y = x + dx, y + dy
                                    if (0 <= new_x < self.grid_size and
                                        0 <= new_y < self.grid_size and
                                        abs(dx) + abs(dy) <= 2):
                                        preview_belief[new_y][new_x] = test_maze[new_y][new_x]
                        
                        # Add preview tower
                        preview_belief[grid_y][grid_x] = 2
                        self.radar_view.update_view(test_maze, preview_belief)
            else:
                # Clear previous tower ranges
                for tower in self.towers:
                    tower['show_range'] = False
                
                if hasattr(self, 'build_mode') and self.build_mode in self.tower_types:
                    tower = self.tower_types[self.build_mode]
                    self.ui.status_label.configure(text=f"Xây {tower['name']} tại ({grid_x}, {grid_y})")
                else:
                    self.ui.status_label.configure(text=f"Ô trống tại ({grid_x}, {grid_y})")


    
    def show_help(self):
        help_text = """
        Hướng Dẫn Chơi:
        
        1. Xây tháp bằng cách chọn loại tháp và nhấp vào mê cung
        2. Bắt đầu làn sóng để gọi kẻ địch
        3. Tháp sẽ tự động tấn công kẻ địch trong tầm
        4. Kẻ địch sẽ di chuyển theo đường tìm được bởi thuật toán
        5. Mỗi kẻ địch đến đích sẽ giảm mạng sống
        6. Tiêu diệt kẻ địch để nhận tiền
        7. Hoàn thành làn sóng để nhận thưởng
        
        Mẹo:
        - Xây tháp ở vị trí chiến lược để chặn đường kẻ địch
        - Kết hợp nhiều loại tháp để tối ưu hóa hiệu quả
        - Tháp Bắn Tỉa rất mạnh nhưng đắt, sử dụng hợp lý
        """
        
        help_window = ctk.CTkToplevel(self.root)
        help_window.title("Hướng Dẫn")
        help_window.geometry("400x500")
        
        # Tạo frame chứa nội dung với màu nền sáng
        content_frame = ctk.CTkFrame(help_window, fg_color=("#F5F5F5", "#F5F5F5"))
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tiêu đề với màu xanh lá
        ctk.CTkLabel(content_frame, 
                    text="HƯỚNG DẪN GAME", 
                    font=ctk.CTkFont(size=24, weight="bold"),
                    text_color="#2E7D32").pack(pady=10)
        
        # Nội dung hướng dẫn với màu nền trắng
        text_box = ctk.CTkTextbox(content_frame, 
                                 wrap="word",
                                 fg_color=("#FFFFFF", "#FFFFFF"),
                                 text_color="#1B5E20",
                                 font=ctk.CTkFont(size=14))
        text_box.pack(fill="both", expand=True, padx=10, pady=10)
        text_box.insert("1.0", help_text)
        text_box.configure(state="disabled")
        
        # Nút đóng với màu xanh dương
        ctk.CTkButton(content_frame, 
                     text="Đóng",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     fg_color="#2196F3",
                     hover_color="#1976D2",
                     command=help_window.destroy).pack(pady=10)

    def set_build_mode(self, mode):
        self.build_mode = mode
        
        try:
            # Update the tower info display
            if mode in self.tower_types:
                tower = self.tower_types[mode]
                info_text = f"{tower['name']}\n\n"
                info_text += f"Sát thương: {tower['damage']}\n"
                info_text += f"Tầm bắn: {tower['range']} ô\n"
                info_text += f"Tốc độ bắn: {100/tower['fire_rate']:.1f}/s\n\n"
                info_text += f"{tower['description']}"
                
                if hasattr(self.ui, 'tower_info_label'):
                    self.ui.tower_info_label.configure(text=info_text)
            elif mode == "delete":
                if hasattr(self.ui, 'tower_info_label'):
                    self.ui.tower_info_label.configure(text="Chọn tháp để xóa và nhận lại 5$")
            else:
                if hasattr(self.ui, 'tower_info_label'):
                    self.ui.tower_info_label.configure(text="Chọn tháp để xem thông tin chi tiết")
        except Exception as e:
            print(f"Error updating tower info: {e}")

    def build_tower(self, x, y, tower_type):
        if self.can_build(x, y, tower_type):
            # Create tower with sprite instead of oval
            tower = {
                'x': x,
                'y': y,
                'type': tower_type,
                'damage': self.tower_types[tower_type]['damage'],
                'range': self.tower_types[tower_type]['range'],
                'fire_rate': self.tower_types[tower_type]['fire_rate'],
                'attack_cooldown': 0
            }
            
            # Create image instead of oval
            sprite = self.ui.canvas.create_image(
                x * self.cell_size + self.cell_size/2,
                y * self.cell_size + self.cell_size/2,
                image=self.ui.tower_sprites[tower_type],
                anchor='center',
                tags='tower'
            )
            
            tower['sprite'] = sprite
            self.towers.append(tower)
            
            # Update resources
            self.money -= self.tower_types[tower_type]['cost']
            self.ui.update_info_labels()
            return True
        return False    
    def create_projectile(self, tower, target):
        # Calculate starting position (tower center)
        tower_x = tower['x'] * self.cell_size + self.cell_size/2
        tower_y = tower['y'] * self.cell_size + self.cell_size/2
        
        # Calculate direction to target
        dx = target['x'] - tower_x
        dy = target['y'] - tower_y
        dist = (dx * dx + dy * dy) ** 0.5
        
        # Điều chỉnh tốc độ đạn theo loại tháp
        if tower['type'] == 'sniper':
            speed = 500  # Đạn sniper rất nhanh
        elif tower['type'] == 'freezer':
            speed = 200  # Đạn đóng băng chậm nhất
        else:
            speed = 350  # Tốc độ đạn thường
        
        if dist > 0:
            dx = dx / dist * speed
            dy = dy / dist * speed
            
        # Calculate rotation angle for sprite
        angle = math.degrees(math.atan2(dy, dx))
        if angle < 0:
            angle += 360
            
        frame_index = int(((angle + 22.5) % 360) // 45)
        
        # Create sprite
        sprite = self.ui.canvas.create_image(
            tower_x, tower_y,
            image=self.ui.projectile_sprites[tower['type']][frame_index if frame_index < len(self.ui.projectile_sprites[tower['type']]) else 0],
            tags="projectile"
        )
        
        # Create projectile with all necessary properties
        projectile = {
            'x': tower_x,
            'y': tower_y,
            'dx': dx,
            'dy': dy,
            'tower_type': tower['type'],
            'damage': tower['damage'],
            'target_x': target['x'],
            'target_y': target['y'],
            'sprite': sprite,
            'frame_index': frame_index,
            'initial_x': tower_x,
            'initial_y': tower_y,
            'tower_range': tower['range'] * self.cell_size,
            'speed': speed
        }
        
        return projectile
