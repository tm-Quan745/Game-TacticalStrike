import tkinter as tk
from tkinter import ttk

class GameUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.setup_ui()
    
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
        self.canvas = tk.Canvas(game_frame, 
                              width=self.game.grid_size * self.game.cell_size,
                              height=self.game.grid_size * self.game.cell_size,
                              bg="#f5f5f5",
                              highlightthickness=1,
                              highlightbackground="#ddd")
        self.canvas.pack(padx=10, pady=10)
        
        # Game status bar
        status_frame = ttk.Frame(game_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Hãy xây tháp và bắt đầu!")
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        speed_frame = ttk.Frame(status_frame)
        speed_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Label(speed_frame, text="Tốc độ:").pack(side=tk.LEFT)
        
        self.speed_btn = ttk.Button(speed_frame, text="1x", width=3,
                                  command=self.game.toggle_game_speed)
        self.speed_btn.pack(side=tk.LEFT, padx=2)
        
        # Control frame (right)
        control_frame = ttk.Frame(main_frame, width=240)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        # Info frame
        info_frame = ttk.LabelFrame(control_frame, text="Thông Tin")
        info_frame.pack(fill=tk.X, pady=5)
        
        self.money_label = ttk.Label(info_frame, text=f"Tiền: {self.game.money}$")
        self.money_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.lives_label = ttk.Label(info_frame, text=f"Mạng: {self.game.lives}")
        self.lives_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.wave_label = ttk.Label(info_frame, text=f"Làn sóng: {self.game.current_wave}")
        self.wave_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.score_label = ttk.Label(info_frame, text=f"Điểm: {self.game.score}")
        self.score_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Algorithm selection frame
        algo_frame = ttk.LabelFrame(control_frame, text="Thuật Toán Tìm Đường")
        algo_frame.pack(fill=tk.X, pady=5)
        
        algorithms = ["BFS", "DFS", "Dijkstra", "A*"]
        for algo in algorithms:
            ttk.Radiobutton(algo_frame, text=algo, value=algo,
                           variable=self.game.selected_algo,
                           command=self.game.find_paths).pack(anchor=tk.W, padx=5, pady=2)
        
        # Tower build frame
        tower_frame = ttk.LabelFrame(control_frame, text="Xây Tháp")
        tower_frame.pack(fill=tk.X, pady=5)
        
        # Tower selection with improved UI
        for tower_key, tower_info in self.game.tower_types.items():
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
            
            ttk.Label(tower_info_frame,
                     text=f"{tower_info['name']} ({tower_info['cost']}$)").pack(anchor=tk.W)
            ttk.Label(tower_info_frame,
                     text=f"DMG: {tower_info['damage']} | RNG: {tower_info['range']}",
                     font=('Arial', 8)).pack(anchor=tk.W)
            
            ttk.Button(tower_btn_frame, text="Xây", width=6,
                      command=lambda t=tower_key: self.game.set_build_mode(t)).pack(side=tk.RIGHT)
        
        # Delete tower option
        delete_frame = ttk.Frame(tower_frame)
        delete_frame.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(delete_frame, text="Xóa Tháp (Hoàn 5$)").pack(side=tk.LEFT)
        ttk.Button(delete_frame, text="Xóa", width=6,
                  command=lambda: self.game.set_build_mode("delete")).pack(side=tk.RIGHT)
        
        # Tower info display (shown when hovering)
        self.tower_info_display = ttk.LabelFrame(control_frame, text="Thông Tin Chi Tiết")
        self.tower_info_display.pack(fill=tk.X, pady=5)
        self.tower_info_label = ttk.Label(self.tower_info_display,
                                        text="Chọn tháp để xem thông tin chi tiết")
        self.tower_info_label.pack(pady=5, padx=5)
        
        # Game control buttons
        control_btn_frame = ttk.LabelFrame(control_frame, text="Điều Khiển Game")
        control_btn_frame.pack(fill=tk.X, pady=5)
        
        self.start_button = ttk.Button(control_btn_frame, text="Bắt Đầu Làn Sóng",
                                     command=self.game.start_wave)
        self.start_button.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(control_btn_frame, text="Tạo Mê Cung Mới",
                  command=self.game.generate_maze).pack(fill=tk.X, padx=5, pady=2)
        
        # Help button
        ttk.Button(control_frame, text="Hướng Dẫn",
                  command=self.game.show_help).pack(fill=tk.X, padx=5, pady=10)
    
    def update_info_labels(self):
        """Update all information labels with current game state."""
        self.money_label.config(text=f"Tiền: {self.game.money}$")
        self.lives_label.config(text=f"Mạng: {self.game.lives}")
        self.wave_label.config(text=f"Làn sóng: {self.game.current_wave}")
        self.score_label.config(text=f"Điểm: {self.game.score}")
    
    def draw_maze(self):
        """Draw the current state of the maze, including towers, enemies, and projectiles."""
        self.canvas.delete("all")
        
        # Draw grid cells
        for y in range(self.game.grid_size):
            for x in range(self.game.grid_size):
                if self.game.maze[y][x] == 1:  # Wall
                    self.canvas.create_rectangle(
                        x * self.game.cell_size, y * self.game.cell_size,
                        (x + 1) * self.game.cell_size, (y + 1) * self.game.cell_size,
                        fill="#8d6e63", outline="#5d4037"
                    )
                else:  # Path
                    self.canvas.create_rectangle(
                        x * self.game.cell_size, y * self.game.cell_size,
                        (x + 1) * self.game.cell_size, (y + 1) * self.game.cell_size,
                        fill="#e8f5e9", outline="#c8e6c9"
                    )
        
        # Mark start and end points
        self.canvas.create_rectangle(
            0, 0, self.game.cell_size, self.game.cell_size,
            fill="#4caf50", outline="#2e7d32"
        )
        self.canvas.create_text(
            self.game.cell_size/2, self.game.cell_size/2,
            text="S", fill="white", font=("Arial", 12, "bold")
        )
        
        self.canvas.create_rectangle(
            (self.game.grid_size-1) * self.game.cell_size,
            (self.game.grid_size-1) * self.game.cell_size,
            self.game.grid_size * self.game.cell_size,
            self.game.grid_size * self.game.cell_size,
            fill="#f44336", outline="#c62828"
        )
        self.canvas.create_text(
            (self.game.grid_size-0.5) * self.game.cell_size,
            (self.game.grid_size-0.5) * self.game.cell_size,
            text="E", fill="white", font=("Arial", 12, "bold")
        )
        
        # Draw towers
        for tower in self.game.towers:
            x, y = tower['x'], tower['y']
            tower_info = self.game.tower_types[tower['type']]
            color = tower_info["color"]
            
            # Tower base
            self.canvas.create_rectangle(
                x * self.game.cell_size + 2,
                y * self.game.cell_size + 2,
                (x + 1) * self.game.cell_size - 2,
                (y + 1) * self.game.cell_size - 2,
                fill="#607d8b", outline="#455a64"
            )
            
            # Tower top
            self.canvas.create_oval(
                x * self.game.cell_size + 6,
                y * self.game.cell_size + 6,
                (x + 1) * self.game.cell_size - 6,
                (y + 1) * self.game.cell_size - 6,
                fill=color, outline="black"
            )
            
            # Show range when hovering or selected
            if (hasattr(self.game, 'build_mode') and 
                self.game.build_mode == "delete") or tower.get('show_range', False):
                self.canvas.create_oval(
                    x * self.game.cell_size - tower['range'] * self.game.cell_size + self.game.cell_size/2,
                    y * self.game.cell_size - tower['range'] * self.game.cell_size + self.game.cell_size/2,
                    x * self.game.cell_size + tower['range'] * self.game.cell_size + self.game.cell_size/2,
                    y * self.game.cell_size + tower['range'] * self.game.cell_size + self.game.cell_size/2,
                    outline=color, dash=(4, 2)
                )
        
        # Draw enemies
        for enemy in self.game.enemies:
            if enemy['spawn_delay'] <= 0:
                enemy_type = enemy['type']
                enemy_info = self.game.enemy_types[enemy_type]
                color = enemy_info["color"]
                
                # Enemy body
                self.canvas.create_oval(
                    enemy['x'] - 10, enemy['y'] - 10,
                    enemy['x'] + 10, enemy['y'] + 10,
                    fill=color, outline="black"
                )
                
                # Health bar
                health_ratio = enemy['health'] / enemy['max_health']
                bar_width = 20
                bar_height = 4
                self.canvas.create_rectangle(
                    enemy['x'] - bar_width/2,
                    enemy['y'] - 15,
                    enemy['x'] + bar_width/2,
                    enemy['y'] - 15 + bar_height,
                    fill="red"
                )
                self.canvas.create_rectangle(
                    enemy['x'] - bar_width/2,
                    enemy['y'] - 15,
                    enemy['x'] - bar_width/2 + bar_width * health_ratio,
                    enemy['y'] - 15 + bar_height,
                    fill="green"
                )
                
                # Show damage text
                if enemy['damage_text_timer'] > 0:
                    self.canvas.create_text(
                        enemy['x'], enemy['y'] - 20,
                        text=str(enemy['damage_text']),
                        fill="red", font=("Arial", 10, "bold")
                    )
        
        # Draw projectiles
        for proj in self.game.projectiles:
            self.canvas.create_oval(
                proj['x'] - 3, proj['y'] - 3,
                proj['x'] + 3, proj['y'] + 3,
                fill="yellow", outline="orange"
            )