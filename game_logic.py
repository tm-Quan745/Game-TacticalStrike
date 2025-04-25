import random
import time
from tkinter import messagebox, ttk
import tkinter as tk
from maze_generator import generate_maze
from pathfinding import find_path
from entities import Tower, Enemy, Projectile
from PIL import Image, ImageTk

class MazeTowerDefenseGame:
    def __init__(self, root):
        self.root = root
        
        # Game parameters
        self.grid_size = 15
        self.cell_size = 48  
        self.maze = []
        self.towers = []
        self.enemies = []
        self.paths = []
        self.projectiles = []
        self.money = 100
        self.lives = 20
        self.current_wave = 0
        self.wave_in_progress = False
        self.selected_algo = tk.StringVar(value="BFS")
        self.score = 0
        self.build_mode = None
        self.game_speed = 1.0

        # Tower info
        self.tower_types = {
            "shooter": {
                "name": "Tháp Bắn",
                "cost": 20,
                "damage": 10,
                "range": 3,
                "fire_rate": 1.0,  # Shoot every second
                "color": "#3498db",
                "description": "Bắn kẻ địch từ xa với tốc độ cao"
            },
            "freezer": {
                "name": "Tháp Đóng Băng",
                "cost": 30,
                "damage": 5,
                "range": 2,
                "fire_rate": 1.5,  # Slower than shooter tower
                "color": "#00bcd4",
                "description": "Làm chậm và gây sát thương nhẹ"
            },
            "sniper": {
                "name": "Tháp Bắn Tỉa",
                "cost": 50,
                "damage": 30,
                "range": 5,
                "fire_rate": 2.0,  # Slowest fire rate but highest damage
                "color": "#9b59b6",
                "description": "Gây sát thương lớn với tầm xa"
            }
        }
        
        # Enemy types
        self.enemy_types = {
            "normal": {
                "color": "#e67e22",
                "speed_factor": 1.0,
                "health_factor": 1.0,
                "reward": 10
            },
            "fast": {
                "color": "#e74c3c",
                "speed_factor": 2.0,
                "health_factor": 0.6,
                "reward": 15
            },
            "tank": {
                "color": "#7f8c8d",
                "speed_factor": 0.6,
                "health_factor": 2.5,
                "reward": 20
            }
        }
        
        try:
            # Load projectile sprites
            sprite_path = "./sprites/"
            shoot_right = Image.open(f"{sprite_path}shoot_right.png")
            shoot_left = Image.open(f"{sprite_path}shoot_left.png")
            
            # Resize projectile sprites
            shoot_right = shoot_right.resize((16, 16), Image.Resampling.LANCZOS) 
            shoot_left = shoot_left.resize((16, 16), Image.Resampling.LANCZOS)
            
            self.projectile_sprites = {
                'shoot_right': ImageTk.PhotoImage(shoot_right),
                'shoot_left': ImageTk.PhotoImage(shoot_left)
            }
            print(f"Loaded projectile sprites from {sprite_path}")
            
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
    
    def toggle_game_speed(self):
        speeds = [1.0, 1.5, 2.0, 0.5]
        current_index = speeds.index(self.game_speed)
        self.game_speed = speeds[(current_index + 1) % len(speeds)]
        self.ui.speed_btn.config(text=f"{self.game_speed}x")
    
    def generate_maze(self):
        self.maze = generate_maze(self.grid_size)
        self.towers = []
        self.enemies = []
        self.projectiles = []
        self.current_wave = 0
        self.lives = 20
        self.money = 100
        self.score = 0
        self.wave_in_progress = False
        self.find_paths()
        if hasattr(self, 'ui'):
            self.ui.draw_maze()
            self.ui.update_info_labels()
            self.ui.canvas.delete("all")
            self.ui.start_button.config(text="Bắt Đầu Làn Sóng", state=tk.NORMAL)
  
        
    
    def find_paths(self):
        # Find a single path using the selected algorithm
        path = find_path(self.maze, self.grid_size, self.selected_algo.get())
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
        dt = (current_time - self.last_update) * self.game_speed
        self.last_update = current_time
        
        # Update game logic
        self.update_enemies(dt)
        self.update_towers(dt)
        self.update_projectiles(dt)
        self.check_wave_end()
        
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
                    self.game_over()
                else:
                    self.ui.update_info_labels()
    
    def update_towers(self, dt):
        for tower in self.towers:
            target = Tower.find_target(tower, self.enemies, self.cell_size)
            if target:
                dx = target['x'] - (tower['x'] * self.cell_size + self.cell_size/2)
                sprite = self.projectile_sprites['shoot_right' if dx > 0 else 'shoot_left']
                Tower.attack(tower, target, dt, self.projectiles, self.cell_size, sprite)
    
    def update_projectiles(self, dt):
        for projectile in self.projectiles[:]:
            if not Projectile.update(projectile, dt):
                self.projectiles.remove(projectile)
                for enemy in self.enemies[:]:
                    if (abs(enemy['x'] - projectile['target_x']) < self.cell_size / 2 and
                        abs(enemy['y'] - projectile['target_y']) < self.cell_size / 2):

                        enemy['health'] -= projectile['damage']

                        if projectile['tower_type'] == 'freezer':
                            enemy['frozen'] = True
                            enemy['freeze_timer'] = 100

                        if enemy['health'] <= 0:
                            self.money += enemy['reward']
                            self.score += enemy['reward']
                            self.enemies.remove(enemy)
                            self.ui.update_info_labels()
                        break

    
    def check_wave_end(self):
        if self.wave_in_progress and not self.enemies:
            self.wave_in_progress = False
            self.current_wave += 1
            self.money += 20 + self.current_wave * 5
            self.ui.update_info_labels()
            self.ui.start_button.config(text="Bắt Đầu Làn Sóng")
    
    def start_wave(self):
        if not self.wave_in_progress:
            self.wave_in_progress = True
            self.spawn_enemies()
            self.ui.start_button.config(text="Làn Sóng Đang Diễn Ra...")
    
    def spawn_enemies(self):
        """Spawn enemies with sprite animations."""
        try:
            if not hasattr(self, 'enemy_sprites'):
                sprite_path = "./sprites/"
                
                # Load sprites
                walk_right = self.ui.load_sprites(f"{sprite_path}walkright.png", 4)
                walk_left = self.ui.load_sprites(f"{sprite_path}walkleft.png", 4) 
                walk_updown = self.ui.load_sprites(f"{sprite_path}walkup.png", 4)
                shoot_right = self.ui.load_sprites(f"{sprite_path}shoot_right.png", 4)
                shoot_left = self.ui.load_sprites(f"{sprite_path}shoot_left.png", 4)
                
                self.enemy_sprites = {
                    'walk_right': walk_right,
                    'walk_left': walk_left,
                    'walk_updown': walk_updown,  # Make sure this matches the direction name used in Enemy.update
                    'shoot_right': shoot_right,
                    'shoot_left': shoot_left
                }
            projectile_sprite = Image.open(f"{sprite_path}grass3.png")
            projectile_sprite = projectile_sprite.resize((16, 16))
            self.enemy_projectile_sprite = ImageTk.PhotoImage(projectile_sprite)
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
        
        num_enemies = 10 + self.current_wave * 5  # Tăng từ 3 lên 10 quân ban đầu
        base_health = 50 + self.current_wave * 8 
        base_speed = 50 + min(80, self.current_wave * 8)
        
        spawn_delay_base = 5  # Giảm từ 15 xuống 5
        
        for i in range(num_enemies):
            enemy_type = "normal"
            if self.current_wave >= 2:
                r = random.random()
                if r < 0.2:  # Tăng tỉ lệ tank từ 15% lên 20%
                    enemy_type = "tank"
                elif r < 0.5:  # Tăng tỉ lệ fast từ 20% lên 30% 
                    enemy_type = "fast"
            
            enemy = Enemy.create(
                enemy_type,
                self.enemy_types[enemy_type],
                base_health,
                base_speed,
                i * spawn_delay_base,  # Spawn quân nhanh hơn
                self.cell_size,
                self.enemy_sprites
            )
            self.enemies.append(enemy)
    
    def game_over(self):
        self.wave_in_progress = False
        messagebox.showinfo("Game Over", f"Game Over! Final Score: {self.score}")
        self.generate_maze()

    def add_tower(self, x, y, tower_type):
        """Add a new tower at the specified position."""
        tower = Tower.create(x, y, tower_type, self.tower_types[tower_type])
        self.towers.append(tower)
        self.maze[y][x] = 2  # Mark cell as containing a tower
    
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
                    self.ui.status_label.config(text="Không thể xây tháp khi làn sóng đang diễn ra!")
                    return
                
                # Build/delete tower based on build_mode
                if hasattr(self, 'build_mode'):
                    if self.build_mode in self.tower_types and self.money >= self.tower_types[self.build_mode]["cost"]:
                        # Check if path still exists after tower placement
                        test_maze = [row[:] for row in self.maze]
                        test_maze[grid_y][grid_x] = 2
                        if not find_path(test_maze, self.grid_size, self.selected_algo.get()):
                            self.ui.status_label.config(text="Không thể xây tháp ở đây vì sẽ chặn hết đường đi!")
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
                self.ui.status_label.config(text="Điểm Xuất Phát (Kẻ địch)")
            elif (grid_x, grid_y) == (self.grid_size-1, self.grid_size-1):
                self.ui.status_label.config(text="Điểm Đích (Bảo vệ đây!)")
            elif self.maze[grid_y][grid_x] == 1:
                self.ui.status_label.config(text="Tường (Không thể xây tháp)")
            elif self.maze[grid_y][grid_x] == 2:
                # Find the tower at this position
                for tower in self.towers:
                    if tower['x'] == grid_x and tower['y'] == grid_y:
                        tower_type = tower['type']
                        tower_info = self.tower_types[tower_type]
                        status = f"{tower_info['name']} | DMG: {tower['damage']} | RNG: {tower['range']}"
                        self.ui.status_label.config(text=status)
                        tower['show_range'] = True
                        # Redraw to show range
                        self.ui.draw_maze()
                        break
            else:
                # Clear previous tower ranges
                for tower in self.towers:
                    tower['show_range'] = False
                
                if hasattr(self, 'build_mode') and self.build_mode in self.tower_types:
                    tower = self.tower_types[self.build_mode]
                    self.ui.status_label.config(text=f"Xây {tower['name']} tại ({grid_x}, {grid_y})")
                else:
                    self.ui.status_label.config(text=f"Ô trống tại ({grid_x}, {grid_y})")

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
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Hướng Dẫn")
        help_window.geometry("400x350")
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        ttk.Button(help_window, text="Đóng", command=help_window.destroy).pack(pady=10)

    def set_build_mode(self, mode):
        self.build_mode = mode
        
        # Update the tower info display
        if mode in self.tower_types:
            tower = self.tower_types[mode]
            info_text = f"{tower['name']}\n\n"
            info_text += f"Sát thương: {tower['damage']}\n"
            info_text += f"Tầm bắn: {tower['range']} ôn\n"
            info_text += f"Tốc độ bắn: {100/tower['fire_rate']:.1f}/s\n\n"
            info_text += f"{tower['description']}"
            
            self.ui.tower_info_label.config(text=info_text)
        elif mode == "delete":
            self.ui.tower_info_label.config(text="Chọn tháp để xóa và nhận lại 5$")
        else:
            self.ui.tower_info_label.config(text="Chọn tháp để xem thông tin chi tiết")
