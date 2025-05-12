import tkinter as tk
from tkinter import ttk, messagebox, font
import random
import math
import time
from collections import deque
import heapq

class MazeTowerDefenseGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Mê Cung Tower Defense")
        self.root.geometry("1000x650")
        
        # Customize appearance
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10, 'bold'))
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        
        # Game parameters
        self.grid_size = 15
        self.cell_size = 36
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
        
        # Tower info with brighter colors
        self.tower_types = {
            "shooter": {
                "name": "Tháp Bắn",
                "cost": 20,
                "damage": 10,
                "range": 3,
                "fire_rate": 20,
                "color": "#2196F3",  # Bright blue
                "description": "Bắn kẻ địch từ xa với tốc độ cao"
            },
            "freezer": {
                "name": "Tháp Đóng Băng",
                "cost": 30,
                "damage": 5,
                "range": 2,
                "fire_rate": 30,
                "color": "#00E5FF",  # Cyan
                "description": "Làm chậm và gây sát thương nhẹ"
            },
            "sniper": {
                "name": "Tháp Bắn Tỉa",
                "cost": 50,
                "damage": 30,
                "range": 5,
                "fire_rate": 50,
                "color": "#E040FB",  # Bright purple
                "description": "Gây sát thương lớn với tầm xa"
            }
        }
        
        # Enemy types with brighter colors
        self.enemy_types = {
            "normal": {
                "color": "#FF9800",  # Orange
                "speed_factor": 1.0,
                "health_factor": 1.0,
                "reward": 10
            },
            "fast": {
                "color": "#F44336",  # Bright red
                "speed_factor": 2.0,
                "health_factor": 0.6,
                "reward": 15
            },
            "tank": {
                "color": "#8BC34A",  # Light green
                "speed_factor": 0.6,
                "health_factor": 2.5,
                "reward": 20
            }
        }
        
        # Initialize UI
        self.setup_ui()
        self.generate_maze()
        self.setup_events()
        
        # Background music (commented out - implement with pygame if desired)
        # self.setup_audio()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Game frame (left)
        game_frame = ttk.Frame(main_frame)
        game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Game title
        title_label = ttk.Label(game_frame, text="MÊ CUNG TOWER DEFENSE", style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        # Maze canvas
        self.canvas = tk.Canvas(game_frame, width=self.grid_size*self.cell_size, 
                               height=self.grid_size*self.cell_size, bg="#f5f5f5", 
                               highlightthickness=1, highlightbackground="#ddd")
        self.canvas.pack(padx=10, pady=10)
        
        # Game status bar
        status_frame = ttk.Frame(game_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Hãy xây tháp và bắt đầu!")
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        speed_frame = ttk.Frame(status_frame)
        speed_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Label(speed_frame, text="Tốc độ:").pack(side=tk.LEFT)
        
        speed_btn = ttk.Button(speed_frame, text="1x", width=3, 
                             command=self.toggle_game_speed)
        speed_btn.pack(side=tk.LEFT, padx=2)
        self.speed_btn = speed_btn
        
        # Control frame (right)
        control_frame = ttk.Frame(main_frame, width=240)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        # Info frame
        info_frame = ttk.LabelFrame(control_frame, text="Thông Tin")
        info_frame.pack(fill=tk.X, pady=5)
        
        self.money_label = ttk.Label(info_frame, text=f"Tiền: {self.money}$")
        self.money_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.lives_label = ttk.Label(info_frame, text=f"Mạng: {self.lives}")
        self.lives_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.wave_label = ttk.Label(info_frame, text=f"Làn sóng: {self.current_wave}")
        self.wave_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.score_label = ttk.Label(info_frame, text=f"Điểm: {self.score}")
        self.score_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Algorithm selection frame
        algo_frame = ttk.LabelFrame(control_frame, text="Thuật Toán Tìm Đường")
        algo_frame.pack(fill=tk.X, pady=5)
        
        algorithms = ["BFS", "A*", "Beam"]
        for algo in algorithms:
            ttk.Radiobutton(algo_frame, text=algo, value=algo, 
                           variable=self.selected_algo, 
                           command=self.find_paths).pack(anchor=tk.W, padx=5, pady=2)
        
        # Tower build frame
        tower_frame = ttk.LabelFrame(control_frame, text="Xây Tháp")
        tower_frame.pack(fill=tk.X, pady=5)
        
        # Tower selection with improved UI
        for tower_key, tower_info in self.tower_types.items():
            tower_btn_frame = ttk.Frame(tower_frame)
            tower_btn_frame.pack(fill=tk.X, padx=5, pady=3)
            
            # Tower icon (a colored square)
            icon_canvas = tk.Canvas(tower_btn_frame, width=20, height=20, 
                                    bg=tower_info["color"], highlightthickness=1, 
                                    highlightbackground="black")
            icon_canvas.pack(side=tk.LEFT, padx=(0, 5))
            
            # Tower info
            tower_info_frame = ttk.Frame(tower_btn_frame)
            tower_info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            ttk.Label(tower_info_frame, text=f"{tower_info['name']} ({tower_info['cost']}$)").pack(anchor=tk.W)
            ttk.Label(tower_info_frame, text=f"DMG: {tower_info['damage']} | RNG: {tower_info['range']}", 
                     font=('Arial', 8)).pack(anchor=tk.W)
            
            ttk.Button(tower_btn_frame, text="Xây", width=6, 
                      command=lambda t=tower_key: self.set_build_mode(t)).pack(side=tk.RIGHT)
        
        # Delete tower option
        delete_frame = ttk.Frame(tower_frame)
        delete_frame.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(delete_frame, text="Xóa Tháp (Hoàn 5$)").pack(side=tk.LEFT)
        ttk.Button(delete_frame, text="Xóa", width=6, 
                  command=lambda: self.set_build_mode("delete")).pack(side=tk.RIGHT)
        
        # Tower info display (shown when hovering)
        self.tower_info_display = ttk.LabelFrame(control_frame, text="Thông Tin Chi Tiết")
        self.tower_info_display.pack(fill=tk.X, pady=5)
        self.tower_info_label = ttk.Label(self.tower_info_display, text="Chọn tháp để xem thông tin chi tiết")
        self.tower_info_label.pack(pady=5, padx=5)
        
        # Game control buttons
        control_btn_frame = ttk.LabelFrame(control_frame, text="Điều Khiển Game")
        control_btn_frame.pack(fill=tk.X, pady=5)
        
        start_button = ttk.Button(control_btn_frame, text="Bắt Đầu Làn Sóng", 
                                 command=self.start_wave)
        start_button.pack(fill=tk.X, padx=5, pady=2)
        self.start_button = start_button
        
        ttk.Button(control_btn_frame, text="Tạo Mê Cung Mới", 
                  command=self.generate_maze).pack(fill=tk.X, padx=5, pady=2)
        
        # Help button
        ttk.Button(control_frame, text="Hướng Dẫn", 
                  command=self.show_help).pack(fill=tk.X, padx=5, pady=10)
        
    def setup_events(self):
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_canvas_hover)
        self.root.after(50, self.game_loop)  # Schedule the game loop to run every 50ms
    
    def toggle_game_speed(self):
        speeds = [1.0, 1.5, 2.0, 0.5]
        current_index = speeds.index(self.game_speed)
        self.game_speed = speeds[(current_index + 1) % len(speeds)]
        # Update speed button
        self.speed_btn.configure(text=f"{self.game_speed}x")
    
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
        # Configure text widget
        text_widget.configure(state=tk.DISABLED)
        
        ttk.Button(help_window, text="Đóng", command=help_window.destroy).pack(pady=10)
    
    def set_build_mode(self, mode):
        self.build_mode = mode
        
        # Update the tower info display
        if mode in self.tower_types:
            tower = self.tower_types[mode]
            info_text = f"{tower['name']}\n\n"
            info_text += f"Sát thương: {tower['damage']}\n"
            info_text += f"Tầm bắn: {tower['range']} ô\n"
            info_text += f"Tốc độ bắn: {100/tower['fire_rate']:.1f}/s\n\n"
            info_text += f"{tower['description']}"
            
            self.tower_info_label.configure(text=info_text)
        elif mode == "delete":
            self.tower_info_label.configure(text="Chọn tháp để xóa và nhận lại 5$")
        else:
            self.tower_info_label.configure(text="Chọn tháp để xem thông tin chi tiết")
    
    def on_canvas_hover(self, event):
        # Convert mouse coordinates to grid coordinates
        grid_x = event.x // self.cell_size
        grid_y = event.y // self.cell_size
        
        # Update the status label with hover information
        if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
            if (grid_x, grid_y) == (0, 0):
                self.status_label.configure(text="Điểm Xuất Phát (Kẻ địch)")
            elif (grid_x, grid_y) == (self.grid_size-1, self.grid_size-1):
                self.status_label.configure(text="Điểm Đích (Bảo vệ đây!)")
            elif self.maze[grid_y][grid_x] == 1:
                self.status_label.configure(text="Tường (Không thể xây tháp)")
            elif self.maze[grid_y][grid_x] == 2:
                # Find the tower at this position
                for tower in self.towers:
                    if tower['x'] == grid_x and tower['y'] == grid_y:
                        tower_type = tower['type']
                        tower_info = self.tower_types[tower_type]
                        status = f"{tower_info['name']} | DMG: {tower['damage']} | RNG: {tower['range']}"
                        self.status_label.configure(text=status)
                        break
            else:
                if hasattr(self, 'build_mode') and self.build_mode in self.tower_types:
                    tower = self.tower_types[self.build_mode]
                    self.status_label.configure(text=f"Xây {tower['name']} tại ({grid_x}, {grid_y})")
                else:
                    self.status_label.configure(text=f"Ô trống tại ({grid_x}, {grid_y})")
    
    def on_canvas_click(self, event):
        # Convert mouse coordinates to grid coordinates
        grid_x = event.x // self.cell_size
        grid_y = event.y // self.cell_size
        
        if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
            # Check if it's an empty cell and not a path
            if (self.maze[grid_y][grid_x] == 0 and 
                (grid_x, grid_y) != (0, 0) and 
                (grid_x, grid_y) != (self.grid_size-1, self.grid_size-1)):
                
                # Build/delete tower based on build_mode
                if hasattr(self, 'build_mode'):
                    if self.build_mode in self.tower_types and self.money >= self.tower_types[self.build_mode]["cost"]:
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
                    self.draw_maze()
                    self.update_info_labels()
                    
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
                self.draw_maze()
                self.update_info_labels()
                
                # Recalculate paths for enemies
                self.find_paths()
    
    def generate_maze(self):
        # Initialize maze with all walls
        self.maze = [[1 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Use DFS algorithm to create the maze
        stack = [(0, 0)]
        self.maze[0][0] = 0  # Start point
        
        # Directions: right, down, left, up
        directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
        
        while stack:
            x, y = stack[-1]
            
            # Shuffle directions
            random.shuffle(directions)
            
            # Find a direction to move
            moved = False
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                
                if (0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size 
                    and self.maze[new_y][new_x] == 1):
                    # Mark middle cell as path
                    self.maze[y + dy//2][x + dx//2] = 0
                    # Mark new cell as path
                    self.maze[new_y][new_x] = 0
                    
                    stack.append((new_x, new_y))
                    moved = True
                    break
            
            if not moved:
                stack.pop()
        
        # Ensure there's a path from (0,0) to (grid_size-1, grid_size-1)
        self.maze[self.grid_size-1][self.grid_size-1] = 0
        
        # Make maze more open for better gameplay
        for i in range(1, self.grid_size-1, 2):
            for j in range(1, self.grid_size-1, 2):
                if random.random() < 0.4:
                    self.maze[i][j] = 0
        
        # Ensure starting and ending areas are more open
        for i in range(2):
            for j in range(2):
                if i > 0 or j > 0:  # Don't change the actual start point
                    self.maze[j][i] = 0
                    self.maze[self.grid_size-1-j][self.grid_size-1-i] = 0
        
        # Reset game
        self.towers = []
        self.enemies = []
        self.projectiles = []
        self.current_wave = 0
        self.lives = 20
        self.money = 100
        self.score = 0
        self.wave_in_progress = False
        
        # Update UI
        self.draw_maze()
        # Update info labels
        self.money_label.configure(text=f"Tiền: {self.money}$")
        self.lives_label.configure(text=f"Mạng: {self.lives}")
        self.wave_label.configure(text=f"Làn sóng: {self.current_wave}")
        self.score_label.configure(text=f"Điểm: {self.score}")
        self.start_button.configure(text="Bắt Đầu Làn Sóng")
        self.status_label.configure(text="Mê cung mới đã được tạo! Hãy bắt đầu xây tháp.")
        self.play_sound("new_game")
        
        # Calculate paths
        self.find_paths()
    
    def draw_maze(self):
        self.canvas.delete("all")
        
        # Draw grid cells
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.maze[y][x] == 1:  # Wall
                    self.canvas.create_rectangle(
                        x * self.cell_size, y * self.cell_size,
                        (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                        fill="#8d6e63", outline="#5d4037"
                    )
                else:  # Path
                    self.canvas.create_rectangle(
                        x * self.cell_size, y * self.cell_size,
                        (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                        fill="#e8f5e9", outline="#c8e6c9"
                    )
        
        # Mark start and end points
        self.canvas.create_rectangle(
            0, 0, self.cell_size, self.cell_size,
            fill="#4caf50", outline="#2e7d32"
        )
        self.canvas.create_text(
            self.cell_size/2, self.cell_size/2,
            text="S", fill="white", font=("Arial", 12, "bold")
        )
        
        self.canvas.create_rectangle(
            (self.grid_size-1) * self.cell_size, (self.grid_size-1) * self.cell_size,
            self.grid_size * self.cell_size, self.grid_size * self.cell_size,
            fill="#f44336", outline="#c62828"
        )
        self.canvas.create_text(
            (self.grid_size-0.5) * self.cell_size, (self.grid_size-0.5) * self.cell_size,
            text="E", fill="white", font=("Arial", 12, "bold")
        )
        
        # Draw towers
        for tower in self.towers:
            x, y = tower['x'], tower['y']
            tower_info = self.tower_types[tower['type']]
            color = tower_info["color"]
            
            # Tower base
            self.canvas.create_rectangle(
                x * self.cell_size + 2, y * self.cell_size + 2,
                (x + 1) * self.cell_size - 2, (y + 1) * self.cell_size - 2,
                fill="#607d8b", outline="#455a64"
            )
            
            # Tower top
            self.canvas.create_oval(
                x * self.cell_size + 6, y * self.cell_size + 6,
                (x + 1) * self.cell_size - 6, (y + 1) * self.cell_size - 6,
                fill=color, outline="black"
            )
            
            # Show range when hovering or selected
            if (hasattr(self, 'build_mode') and self.build_mode == "delete") or tower.get('show_range', False):
                self.canvas.create_oval(
                    x * self.cell_size - tower['range'] * self.cell_size + self.cell_size/2,
                    y * self.cell_size - tower['range'] * self.cell_size + self.cell_size/2,
                    x * self.cell_size + tower['range'] * self.cell_size + self.cell_size/2,
                    y * self.cell_size + tower['range'] * self.cell_size + self.cell_size/2,
                    outline=color, dash=(4, 2)
                )
        
        # Draw projectiles
        for proj in self.projectiles:
            self.canvas.create_oval(
                proj['x'] - 3, proj['y'] - 3,
                proj['x'] + 3, proj['y'] + 3,
                fill=self.tower_types[proj['tower_type']]['color'],
                outline="black"
            )
        
        # Draw enemies
        for enemy in self.enemies:
            if enemy['spawn_delay'] > 0:
                continue
                
            enemy_type = enemy.get('type', 'normal')
            color = self.enemy_types[enemy_type]['color']
            if enemy.get('frozen', False):
                color = "#81d4fa"  # Light blue when frozen
            
            # Enemy body
            self.canvas.create_oval(
                enemy['x'] - 8, enemy['y'] - 8,
                enemy['x'] + 8, enemy['y'] + 8,
                fill=color, outline="black"
            )
            
            # Enemy health bar background
            self.canvas.create_rectangle(
                enemy['x'] - 12, enemy['y'] - 15,
                enemy['x'] + 12, enemy['y'] - 10,
                fill="#e0e0e0", outline="black"
            )
            
            # Enemy health bar
            health_percent = enemy['health'] / enemy['max_health']
            bar_color = "#4caf50" if health_percent > 0.5 else "#ff9800" if health_percent > 0.25 else "#f44336"
            self.canvas.create_rectangle(
                enemy['x'] - 12, enemy['y'] - 15,
                enemy['x'] - 12 + 24 * health_percent, enemy['y'] - 10,
                fill=bar_color, outline=""
            )
            
            # Show damage numbers (optional)
            if 'damage_text' in enemy and enemy['damage_text_timer'] > 0:
                self.canvas.create_text(
                    enemy['x'], enemy['y'] - 20,
                    text=f"-{enemy['damage_text']}",
                    fill="red", font=("Arial", 10, "bold")
                )
    
    def add_tower(self, x, y, tower_type):
        tower_data = self.tower_types[tower_type]
        
        tower = {
            'x': x,
            'y': y,
            'type': tower_type,
            'damage': tower_data['damage'],
            'range': tower_data['range'],
            'cooldown': 0,
            'fire_rate': tower_data['fire_rate'],
            'show_range': False
        }
        
        if tower_type == "freezer":
            tower['freeze_duration'] = 60  # Frames of slowing effect
        
        self.towers.append(tower)
        
        # Mark cell as containing a tower
        self.maze[y][x] = 2
        
        # Recalculate enemy paths
        self.find_paths()
    
    def update_info_labels(self):
        # Update info labels
        self.money_label.configure(text=f"Tiền: {self.money}$")
        self.lives_label.configure(text=f"Mạng: {self.lives}")
        self.wave_label.configure(text=f"Làn sóng: {self.current_wave}")
        self.score_label.configure(text=f"Điểm: {self.score}")
    
    def start_wave(self):
        if not self.wave_in_progress:
            self.current_wave += 1
            self.wave_in_progress = True
            self.spawn_enemies()
            self.update_info_labels()
            # Update wave info
            self.start_button.configure(text=f"Làn {self.current_wave} đang diễn ra...")
            self.status_label.configure(text=f"Làn sóng {self.current_wave} đã bắt đầu!")
            self.play_sound("wave_start")
    
    def spawn_enemies(self):
        # Number of enemies increases with wave
        num_enemies = 5 + self.current_wave * 2
        
        # Basic enemy parameters increase with wave
        base_health = 50 + self.current_wave * 10
        base_speed = 0.1 + min(0.3, self.current_wave * 0.02)  # Cap speed for playability
        
        # Create enemy list
        for i in range(num_enemies):
            # Determine enemy type with probability
            enemy_type = "normal"
            if self.current_wave >= 3:
                r = random.random()
                if r < 0.2:  # 20% chance for tank enemies after wave 3
                    enemy_type = "tank"
                elif r < 0.4:  # 20% chance for fast enemies after wave 3
                    enemy_type = "fast"
            
            # Apply type-specific modifiers
            type_data = self.enemy_types[enemy_type]
            health = base_health * type_data['health_factor']
            speed = base_speed * type_data['speed_factor']
            
            enemy = {
                'x': self.cell_size / 2,  # Starting position
                'y': self.cell_size / 2,
                'health': health,
                'max_health': health,
                'speed': speed,
                'reward': type_data,
                'path_index': 0,
                'path_position': 0,
                'target_x': 0,
                'target_y': 0,
                'spawn_delay': i * 30,  # Stagger spawns
                'frozen': False,
                'freeze_timer': 0,
                'type': enemy_type,
                'damage_text': 0,
                'damage_text_timer': 0
            }
            
            self.enemies.append(enemy)
    
    def find_paths(self):
        # Get the currently selected algorithm
        algorithm = self.selected_algo.get()
        
        # Clear current paths
        self.paths = []
        
        # Calculate new paths based on selected algorithm
        if algorithm == "BFS":
            self.paths = self.bfs_find_path()
        elif algorithm == "DFS":
            self.paths = self.dfs_find_path()
        elif algorithm == "Dijkstra":
            self.paths = self.dijkstra_find_path()
        elif algorithm == "A*":
            self.paths = self.astar_find_path()
        
        # Update path for all enemies
        for enemy in self.enemies:
            # Reset path progress
            enemy['path_index'] = 0
            enemy['path_position'] = 0
            
            # Assign target if paths exist
            if self.paths and len(self.paths) > 0:
                next_pos = self.paths[0][0]
                enemy['target_x'] = next_pos[0] * self.cell_size + self.cell_size/2
                enemy['target_y'] = next_pos[1] * self.cell_size + self.cell_size/2
    
    def bfs_find_path(self):
        # Implementation of Breadth-First Search for path finding
        start = (0, 0)
        end = (self.grid_size-1, self.grid_size-1)
        
        # Create a queue for BFS
        queue = deque([start])
        visited = {start: None}  # Map cell -> previous cell
        
        # Find path
        while queue:
            current = queue.popleft()
            
            # Check if we've reached the end
            if current == end:
                break
                
            # Try all four directions
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy
                
                # Check if the new position is valid
                if (0 <= nx < self.grid_size and 0 <= ny < self.grid_size and 
                    self.maze[ny][nx] == 0 and (nx, ny) not in visited):
                    queue.append((nx, ny))
                    visited[(nx, ny)] = current
        
        # Reconstruct path
        if end not in visited:
            return []  # No path found
            
        path = []
        current = end
        while current != start:
            path.append(current)
            current = visited[current]
        path.append(start)
        path.reverse()
        
        return [path]  # Return as a list of paths
    
    def dfs_find_path(self):
        # Implementation of Depth-First Search for path finding
        start = (0, 0)
        end = (self.grid_size-1, self.grid_size-1)
        
        # Create a stack for DFS
        stack = [start]
        visited = {start: None}  # Map cell -> previous cell
        
        # Find path
        while stack:
            current = stack.pop()
            
            # Check if we've reached the end
            if current == end:
                break
                
            # Try all four directions (in reverse order to prefer right and down)
            for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                nx, ny = current[0] + dx, current[1] + dy
                
                # Check if the new position is valid
                if (0 <= nx < self.grid_size and 0 <= ny < self.grid_size and 
                    self.maze[ny][nx] == 0 and (nx, ny) not in visited):
                    stack.append((nx, ny))
                    visited[(nx, ny)] = current
        
        # Reconstruct path
        if end not in visited:
            return []  # No path found
            
        path = []
        current = end
        while current != start:
            path.append(current)
            current = visited[current]
        path.append(start)
        path.reverse()
        
        return [path]  # Return as a list of paths
    
    def dijkstra_find_path(self):
        # Implementation of Dijkstra's algorithm for path finding
        start = (0, 0)
        end = (self.grid_size-1, self.grid_size-1)
        
        # Priority queue for Dijkstra
        pq = [(0, start)]  # (distance, cell)
        dist = {start: 0}  # Map cell -> distance from start
        prev = {start: None}  # Map cell -> previous cell
        
        # Find path
        while pq:
            d, current = heapq.heappop(pq)
            
            # If we've found a longer path to current, skip
            if d > dist.get(current, float('inf')):
                continue
                
            # Check if we've reached the end
            if current == end:
                break
                
            # Try all four directions
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy
                
                # Check if the new position is valid
                if (0 <= nx < self.grid_size and 0 <= ny < self.grid_size and 
                    self.maze[ny][nx] == 0):
                    
                    # Calculate new distance
                    new_dist = dist[current] + 1
                    
                    # Update if we found a shorter path
                    if new_dist < dist.get((nx, ny), float('inf')):
                        dist[(nx, ny)] = new_dist
                        prev[(nx, ny)] = current
                        heapq.heappush(pq, (new_dist, (nx, ny)))
        
        # Reconstruct path
        if end not in prev:
            return []  # No path found
            
        path = []
        current = end
        while current != start:
            path.append(current)
            current = prev[current]
        path.append(start)
        path.reverse()
        
        return [path]  # Return as a list of paths
    
    def astar_find_path(self):
        # Implementation of A* algorithm for path finding
        start = (0, 0)
        end = (self.grid_size-1, self.grid_size-1)
        
        # Manhattan distance heuristic
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        # Priority queue for A*
        pq = [(0 + heuristic(start, end), 0, start)]  # (f_score, g_score, cell)
        g_score = {start: 0}  # Map cell -> cost from start
        f_score = {start: heuristic(start, end)}  # Map cell -> estimated total cost
        prev = {start: None}  # Map cell -> previous cell
        
        # Find path
        while pq:
            _, g, current = heapq.heappop(pq)
            
            # Check if we've reached the end
            if current == end:
                break
                
            # Try all four directions
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy
                
                # Check if the new position is valid
                if (0 <= nx < self.grid_size and 0 <= ny < self.grid_size and 
                    self.maze[ny][nx] == 0):
                    
                    # Calculate new g score
                    new_g = g_score[current] + 1
                    
                    # Update if we found a better path
                    if new_g < g_score.get((nx, ny), float('inf')):
                        prev[(nx, ny)] = current
                        g_score[(nx, ny)] = new_g
                        f_score[(nx, ny)] = new_g + heuristic((nx, ny), end)
                        heapq.heappush(pq, (f_score[(nx, ny)], new_g, (nx, ny)))
        
        # Reconstruct path
        if end not in prev:
            return []  # No path found
            
        path = []
        current = end
        while current != start:
            path.append(current)
            current = prev[current]
        path.append(start)
        path.reverse()
        
        return [path]  # Return as a list of paths
    
    def game_loop(self):
        # Only update game at the appropriate speed
        if not hasattr(self, 'last_update'):
            self.last_update = time.time()
        
        # Calculate time since last update
        current_time = time.time()
        dt = (current_time - self.last_update) * self.game_speed
        self.last_update = current_time
        
        # Update game logic
        self.update_enemies(dt)
        self.update_towers(dt)
        self.update_projectiles(dt)
        self.check_wave_end()
        
        # Update UI
        self.draw_maze()
        
        # Schedule next frame
        self.root.after(16, self.game_loop)  # ~60 FPS
    
    def update_enemies(self, dt):
        # Update enemy positions and states
        for enemy in self.enemies[:]:
            # Handle spawn delay
            if enemy['spawn_delay'] > 0:
                enemy['spawn_delay'] -= 1 * dt
                continue
            
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
            
            # Update enemy position to move towards target
            dx = enemy['target_x'] - enemy['x']
            dy = enemy['target_y'] - enemy['y']
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist < speed:
                # Reached target, move to next path point
                enemy['x'] = enemy['target_x']
                enemy['y'] = enemy['target_y']
                
                path_idx = enemy['path_index']
                if path_idx < len(self.paths) - 1:
                    # There are still multiple paths to choose from
                    # TODO: Implement logic to choose a path if needed
                    pass
                
                # Move along current path
                if self.paths and path_idx < len(self.paths):
                    path = self.paths[path_idx]
                    pos = enemy['path_position'] + 1
                    
                    if pos < len(path):
                        # Move to next point on current path
                        enemy['path_position'] = pos
                        next_pos = path[pos]
                        enemy['target_x'] = next_pos[0] * self.cell_size + self.cell_size/2
                        enemy['target_y'] = next_pos[1] * self.cell_size + self.cell_size/2
                    else:
                        # Reached the end of path (goal)
                        self.lives -= 1
                        self.update_info_labels()
                        self.enemies.remove(enemy)
                        self.play_sound("life_lost")
                        
                        # Check for game over
                        if self.lives <= 0:
                            self.game_over()
            else:
                # Move towards target
                enemy['x'] += (dx / dist) * speed * dt
                enemy['y'] += (dy / dist) * speed * dt
            
            # Check if the enemy died
            if enemy['health'] <= 0:
                self.enemies.remove(enemy)
                self.money += enemy['reward']
                self.score += enemy['reward']
                self.update_info_labels()
                self.play_sound("enemy_die")
    
    def update_towers(self, dt):
        # Update tower cooldowns and attack enemies
        for tower in self.towers:
            if tower['cooldown'] > 0:
                tower['cooldown'] -= 1 * dt
            else:
                # Find nearest enemy in range
                target = self.find_target_for_tower(tower)
                
                if target:
                    # Attack the enemy
                    self.attack_enemy(tower, target, dt)
    
    def find_target_for_tower(self, tower):
        tx, ty = tower['x'], tower['y']
        tower_range = tower['range']
        closest_dist = float('inf')
        target = None
        
        for enemy in self.enemies:
            # Skip enemies that haven't spawned yet
            if enemy['spawn_delay'] > 0:
                continue
                
            # Calculate distance to enemy
            dx = enemy['x'] - (tx * self.cell_size + self.cell_size/2)
            dy = enemy['y'] - (ty * self.cell_size + self.cell_size/2)
            dist = math.sqrt(dx*dx + dy*dy) / self.cell_size
            
            # Check if enemy is in range
            if dist <= tower_range and dist < closest_dist:
                closest_dist = dist
                target = enemy
        
        return target
    
    def attack_enemy(self, tower, enemy, dt):
        # Reset tower cooldown
        tower['cooldown'] = tower['fire_rate']
        
        # Get tower center coordinates
        tx = tower['x'] * self.cell_size + self.cell_size/2
        ty = tower['y'] * self.cell_size + self.cell_size/2
        
        # Create a projectile animation
        projectile = {
            'x': tx,
            'y': ty,
            'target': enemy,
            'speed': 5.0,
            'damage': tower['damage'],
            'tower_type': tower['type']
        }
        
        # Add special effects based on tower type
        if tower['type'] == 'freezer':
            projectile['freeze'] = True
            projectile['freeze_duration'] = tower['freeze_duration']
        
        self.projectiles.append(projectile)
        self.play_sound("tower_fire")
    
    def update_projectiles(self, dt):
        # Update projectile positions and hit detection
        for projectile in self.projectiles[:]:
            target = projectile['target']
            
            # Check if target still exists
            if target not in self.enemies:
                self.projectiles.remove(projectile)
                continue
            
            # Move projectile towards target
            dx = target['x'] - projectile['x']
            dy = target['y'] - projectile['y']
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist < projectile['speed'] * dt:
                # Hit the target
                self.hit_enemy(target, projectile)
                self.projectiles.remove(projectile)
            else:
                # Move towards target
                projectile['x'] += (dx / dist) * projectile['speed'] * dt
                projectile['y'] += (dy / dist) * projectile['speed'] * dt
    
    def hit_enemy(self, enemy, projectile):
        # Apply damage to enemy
        enemy['health'] -= projectile['damage']
        
        # Show damage text
        enemy['damage_text'] = projectile['damage']
        enemy['damage_text_timer'] = 20
        
        # Apply special effects
        if 'freeze' in projectile and projectile['freeze']:
            enemy['frozen'] = True
            enemy['freeze_timer'] = projectile['freeze_duration']
    
    def check_wave_end(self):
        # Check if wave is complete (no more enemies)
        if self.wave_in_progress and not self.enemies:
            self.wave_in_progress = False
            
            # Give bonus money for completing wave
            bonus = 20 + self.current_wave * 5
            self.money += bonus
            self.score += bonus * 2
            self.update_info_labels()
            
            # Update UI
            self.start_button.configure(text="Bắt Đầu Làn Sóng")
            self.status_label.configure(text=f"Đã hoàn thành làn {self.current_wave}! Nhận {bonus}$ tiền thưởng.")
            self.play_sound("wave_complete")
    
    def game_over(self):
        # Show game over message
        messagebox.showinfo("Game Over", f"Bạn đã thua! Điểm số: {self.score}")
        
        # Reset game
        self.generate_maze()
    
    def play_sound(self, sound_name):
        # Placeholder for sound effects - would be implemented with pygame
        # Example: self.sounds[sound_name].play()
        pass

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = MazeTowerDefenseGame(root)
    root.mainloop()