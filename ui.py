import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

class GameUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        # Load tile sprites
        try:
            grass = Image.open("./sprites/grass.png")
            land = Image.open("./sprites/land.png")
            # Add tower sprites loading
            shooter_tower = Image.open("./sprites/grass4.jpg")  # Tháp bắn
            freezer_tower = Image.open("./sprites/grass5.jpg")  # Tháp đóng băng
            sniper_tower = Image.open("./sprites/grass6.jpg")   # Tháp bắn tỉa
            # Add projectile sprites loading
            ice = Image.open("./sprites/grass2.png")
            sniper = Image.open("./sprites/grass3.png")
            bullet = Image.open("./sprites/land1.jpg")
            enemy_projectile = Image.open("./sprites/grass4.jpg")
            
            
            # Resize sprites
            grass = grass.resize((game.cell_size, game.cell_size), Image.Resampling.LANCZOS)
            land = land.resize((game.cell_size, game.cell_size), Image.Resampling.LANCZOS)
            shooter_tower = shooter_tower.resize((48, 48), Image.Resampling.LANCZOS)
            freezer_tower = freezer_tower.resize((48, 48), Image.Resampling.LANCZOS)
            sniper_tower = sniper_tower.resize((48, 48), Image.Resampling.LANCZOS)
            bullet = bullet.resize((16, 16), Image.Resampling.LANCZOS)
            ice = ice.resize((16, 16), Image.Resampling.LANCZOS)
            sniper = sniper.resize((16, 16), Image.Resampling.LANCZOS)
            enemy_projectile = enemy_projectile.resize((16, 16), Image.Resampling.LANCZOS)
            self.tile_sprites = {
                'grass': ImageTk.PhotoImage(grass),
                'land': ImageTk.PhotoImage(land),
            }
            
            self.tower_sprites = {
                'shooter': ImageTk.PhotoImage(shooter_tower),
                'freezer': ImageTk.PhotoImage(freezer_tower),
                'sniper': ImageTk.PhotoImage(sniper_tower)
            }
            
            self.projectile_sprites = {
                'shooter': ImageTk.PhotoImage(bullet),
                'freezer': ImageTk.PhotoImage(ice),
                'sniper': ImageTk.PhotoImage(sniper)
            }
            
            self.enemy_projectile_frames = []
            rotated_bullet = enemy_projectile
            for i in range(4):  # Create 4 rotation frames
                self.enemy_projectile_frames.append(ImageTk.PhotoImage(rotated_bullet))
                rotated_bullet = rotated_bullet.rotate(90)
            
        except Exception as e:
            print(f"Error loading sprites: {e}")
            self.tile_sprites = {
                'grass': None,
                'land': None,
            }
            # Create placeholder images for towers
            placeholder = Image.new('RGBA', (48, 48), 'gray')
            self.tower_sprites = {
                'shooter': ImageTk.PhotoImage(placeholder),
                'freezer': ImageTk.PhotoImage(placeholder),
                'sniper': ImageTk.PhotoImage(placeholder)
            }
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.root, fg_color=("#FFFFFF", "#FFFFFF"))
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Game frame (left)
        game_frame = ctk.CTkFrame(main_frame, fg_color=("#F0F8FF", "#F0F8FF"))
        game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Game title
        title_label = ctk.CTkLabel(game_frame, text="MÊ CUNG TOWER DEFENSE",
                                font=ctk.CTkFont(size=24, weight="bold"),
                                text_color="#2E7D32")
        title_label.pack(pady=(0, 10))
        
        # Maze canvas
        self.canvas = tk.Canvas(game_frame,
                            width=self.game.grid_size * self.game.cell_size,
                            height=self.game.grid_size * self.game.cell_size,
                            bg="#E8F5E9",
                            highlightthickness=1,
                            highlightbackground="#81C784")
        self.canvas.pack(padx=10, pady=10)
        
        # Game status bar
        status_frame = ctk.CTkFrame(game_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = ctk.CTkLabel(status_frame, 
                                      text="Hãy xây tháp và bắt đầu!",
                                      font=ctk.CTkFont(size=14),
                                      text_color="#1B5E20")
        self.status_label.pack(side=tk.LEFT, padx=10)

        # Control container (right side)
        control_container = ctk.CTkFrame(main_frame, fg_color=("#F1F8E9", "#F1F8E9"))
        control_container.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Create scrollable frame
        control_scroll = ctk.CTkScrollableFrame(
            control_container,
            width=300,
            fg_color=("#F1F8E9", "#F1F8E9"),
            orientation="vertical"
        )
        control_scroll.pack(fill=tk.BOTH, expand=True)

        # Game buttons frame
        buttons_frame = ctk.CTkFrame(control_scroll, fg_color=("#E8F5E9", "#E8F5E9"))
        buttons_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Algorithm selection button
        self.algorithm_button = ctk.CTkButton(
            buttons_frame, 
            text=f"Thuật Toán: {self.game.selected_algo.get()}",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#673AB7",
            hover_color="#512DA8",
            command=self.show_algorithm_selector
        )
        self.algorithm_button.pack(fill=tk.X, padx=5, pady=5)
        
        # Start wave button
        self.start_button = ctk.CTkButton(
            buttons_frame,
            text="Bắt Đầu Làn Sóng",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#388E3C",
            command=self.game.start_wave
        )
        self.start_button.pack(fill=tk.X, padx=5, pady=5)
        
        # New maze button
        ctk.CTkButton(
            buttons_frame,
            text="Tạo Mê Cung Mới",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2196F3",
            hover_color="#1976D2",
            corner_radius=10,
            command=self.game.generate_maze
        ).pack(fill=tk.X, padx=5, pady=5)
        
        # Info frame
        info_frame = ctk.CTkFrame(control_scroll, fg_color=("#E8F5E9", "#E8F5E9"))
        info_frame.pack(fill=tk.X, pady=5, padx=5)
        
        info_title = ctk.CTkLabel(
            info_frame,
            text="Thông Tin",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#2E7D32"
        )
        info_title.pack(pady=5)
        
        # Game info labels
        self.money_label = ctk.CTkLabel(
            info_frame,
            text=f"Tiền: {self.game.money}$",
            font=ctk.CTkFont(size=14),
            text_color="#1B5E20"
        )
        self.money_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.lives_label = ctk.CTkLabel(
            info_frame,
            text=f"Mạng: {self.game.lives}",
            font=ctk.CTkFont(size=14),
            text_color="#1B5E20"
        )
        self.lives_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.wave_label = ctk.CTkLabel(
            info_frame,
            text=f"Làn sóng: {self.game.current_wave}",
            font=ctk.CTkFont(size=14),
            text_color="#1B5E20"
        )
        self.wave_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.score_label = ctk.CTkLabel(
            info_frame,
            text=f"Điểm: {self.game.score}",
            font=ctk.CTkFont(size=14),
            text_color="#1B5E20"
        )
        self.score_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Tower frame
        tower_frame = ctk.CTkFrame(control_scroll, fg_color=("#E3F2FD", "#E3F2FD"))
        tower_frame.pack(fill=tk.X, pady=5, padx=5)
        
        tower_title = ctk.CTkLabel(
            tower_frame,
            text="Xây Tháp",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1565C0"
        )
        tower_title.pack(pady=5)
        
        # Tower selection with images
        for tower_key, tower_info in self.game.tower_types.items():
            # Create frame for each tower
            tower_container = ctk.CTkFrame(tower_frame, fg_color=("#FFFFFF", "#FFFFFF"))
            tower_container.pack(fill=tk.X, padx=5, pady=3)
            
            # Left frame for image
            image_frame = ctk.CTkFrame(tower_container, width=48, height=48)
            image_frame.pack(side=tk.LEFT, padx=5, pady=5)
            
            # Create label with tower image
            image_label = ctk.CTkLabel(
                image_frame, 
                text="",
                image=self.tower_sprites[tower_key]
            )
            image_label.pack(expand=True)
            
            # Right frame for info and button
            info_frame = ctk.CTkFrame(tower_container, fg_color=("#FFFFFF", "#FFFFFF"))
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            # Tower name and cost
            ctk.CTkLabel(
                info_frame,
                text=f"{tower_info['name']}",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#1B5E20"
            ).pack(anchor=tk.W)
            
            ctk.CTkLabel(
                info_frame,
                text=f"Giá: {tower_info['cost']}$",
                font=ctk.CTkFont(size=12),
                text_color="#1B5E20"
            ).pack(anchor=tk.W)
            
            # Stats frame
            stats_frame = ctk.CTkFrame(info_frame, fg_color=("#FFFFFF", "#FFFFFF"))
            stats_frame.pack(fill=tk.X, pady=2)
            
            # Stats with icons
            ctk.CTkLabel(
                stats_frame,
                text=f"💥 {tower_info['damage']} | 🎯 {tower_info['range']} | ⚡ {100/tower_info['fire_rate']:.1f}/s",
                font=ctk.CTkFont(size=11),
                text_color="#666666"
            ).pack(anchor=tk.W)
            
            # Build button
            ctk.CTkButton(
                tower_container,
                text="Xây",
                width=60,
                height=32,
                font=ctk.CTkFont(size=13),
                fg_color=tower_info["color"],
                hover_color="#424242",
                command=lambda t=tower_key: self.game.set_build_mode(t)
            ).pack(side=tk.RIGHT, padx=5, pady=5)
            
            # Bind hover events
            def show_description(event, info=tower_info):
                self.status_label.configure(text=info['description'])
            
            def hide_description(event):
                self.status_label.configure(text="Hãy xây tháp và bắt đầu!")
            
            tower_container.bind('<Enter>', show_description)
            tower_container.bind('<Leave>', hide_description)
        
        # Delete button frame
        delete_frame = ctk.CTkFrame(tower_frame, fg_color=("#FFEBEE", "#FFEBEE"))
        delete_frame.pack(fill=tk.X, padx=5, pady=3)
        
        delete_icon = ctk.CTkLabel(
            delete_frame,
            text="🗑️",
            font=ctk.CTkFont(size=20),
            text_color="#D32F2F"
        )
        delete_icon.pack(side=tk.LEFT, padx=10)
        
        ctk.CTkLabel(
            delete_frame,
            text="Xóa Tháp\nHoàn lại 5$",
            font=ctk.CTkFont(size=12),
            text_color="#D32F2F"
        ).pack(side=tk.LEFT, padx=5)
        
        ctk.CTkButton(
            delete_frame,
            text="Xóa",
            width=60,
            font=ctk.CTkFont(size=13),
            fg_color="#F44336",
            hover_color="#D32F2F",
            command=lambda: self.game.set_build_mode("delete")
        ).pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Help button at the bottom
        ctk.CTkButton(
            control_scroll,
            text="Hướng Dẫn",
            font=ctk.CTkFont(size=14),
            fg_color="#03A9F4",
            hover_color="#0288D1",
            corner_radius=10,
            command=self.game.show_help
        ).pack(fill=tk.X, padx=5, pady=10)
        
        tower_frame = ctk.CTkFrame(control_scroll, fg_color=("#E3F2FD", "#E3F2FD"))
        tower_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Add tower info label here
        self.tower_info_label = ctk.CTkLabel(
            tower_frame,
            text="",
            width=200,
            wraplength=180,
            justify="left"
        )
        self.tower_info_label.pack(pady=10)
    
    def update_info_labels(self):
        """Update all information labels with current game state."""
        self.money_label.configure(text=f"Tiền: {self.game.money}$")
        self.lives_label.configure(text=f"Mạng: {self.game.lives}")
        self.wave_label.configure(text=f"Làn sóng: {self.game.current_wave}")
        self.score_label.configure(text=f"Điểm: {self.game.score}")
    
    def draw_maze(self):
        """Draw the current state of the maze."""
        self.canvas.delete("terrain", "health_bar", "projectile", "tower")

        # Draw grid cells using sprites
        for y in range(self.game.grid_size):
            for x in range(self.game.grid_size):
                # Wall cells use grass sprite, path cells use land sprite
                sprite = self.tile_sprites['grass'] if self.game.maze[y][x] == 1 else self.tile_sprites['land']
                if sprite:
                    self.canvas.create_image(
                        x * self.game.cell_size, 
                        y * self.game.cell_size,
                        image=sprite,
                        anchor='nw',
                        tags="terrain"
                    )
                else:
                    # Fallback to colored rectangles if sprites failed to load
                    self.canvas.create_rectangle(
                        x * self.game.cell_size, y * self.game.cell_size,
                        (x + 1) * self.game.cell_size, (y + 1) * self.game.cell_size,
                        fill="#8d6e63" if self.game.maze[y][x] == 1 else "#e8f5e9",
                        outline="#5d4037" if self.game.maze[y][x] == 1 else "#c8e6c9",
                        tags="terrain"
                    )
        
        # Mark start and end points
        self.canvas.create_rectangle(
            0, 0, self.game.cell_size, self.game.cell_size,
            fill="#4caf50", outline="#2e7d32",
            tags="terrain"
        )
        self.canvas.create_text(
            self.game.cell_size/2, self.game.cell_size/2,
            text="S", fill="white", font=("Arial", 12, "bold"),
            tags="terrain"
        )
        
        self.canvas.create_rectangle(
            (self.game.grid_size-1) * self.game.cell_size,
            (self.game.grid_size-1) * self.game.cell_size,
            self.game.grid_size * self.game.cell_size,
            self.game.grid_size * self.game.cell_size,
            fill="#f44336", outline="#c62828",
            tags="terrain"
        )
        self.canvas.create_text(
            (self.game.grid_size-0.5) * self.game.cell_size,
            (self.game.grid_size-0.5) * self.game.cell_size,
            text="E", fill="white", font=("Arial", 12, "bold"),
            tags="terrain"
        )
        
        # Draw towers with tag
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
                fill="#607d8b", outline="#455a64",
                tags="tower"
            )
            
            # Tower top
            self.canvas.create_oval(
                x * self.game.cell_size + 6,
                y * self.game.cell_size + 6,
                (x + 1) * self.game.cell_size - 6,
                (y + 1) * self.game.cell_size - 6,
                fill=color, outline="black",
                tags="tower"
            )
            
            # Show range when hovering or selected
            if (hasattr(self.game, 'build_mode') and 
                self.game.build_mode == "delete") or tower.get('show_range', False):
                self.canvas.create_oval(
                    x * self.game.cell_size - tower['range'] * self.game.cell_size + self.game.cell_size/2,
                    y * self.game.cell_size - tower['range'] * self.game.cell_size + self.game.cell_size/2,
                    x * self.game.cell_size + tower['range'] * self.game.cell_size + self.game.cell_size/2,
                    y * self.game.cell_size + tower['range'] * self.game.cell_size + self.game.cell_size/2,
                    outline=color, dash=(4, 2),
                    tags="tower"
                )
            
            # Draw tower health bar
            health_ratio = tower['health'] / tower['max_health']
            bar_width = self.game.cell_size - 4
            bar_height = 4
            
            # Health bar background
            self.canvas.create_rectangle(
                x * self.game.cell_size + 2,
                y * self.game.cell_size - 6,
                (x + 1) * self.game.cell_size - 2,
                y * self.game.cell_size - 2,
                fill="red",
                tags="tower"
            )
            
            # Current health
            self.canvas.create_rectangle(
                x * self.game.cell_size + 2,
                y * self.game.cell_size - 6,
                x * self.game.cell_size + 2 + bar_width * health_ratio,
                y * self.game.cell_size - 2,
                fill="green",
                tags="tower"
            )
        
        # Vẽ thanh máu phía trên sprites
        for enemy in self.game.enemies:
            if enemy['spawn_delay'] <= 0:
                # Vẽ thanh máu với tag health_bar
                health_ratio = enemy['health'] / enemy['max_health']
                bar_width = 20
                bar_height = 4
                
                # Background của thanh máu
                self.canvas.create_rectangle(
                    enemy['x'] - bar_width/2,
                    enemy['y'] - 20,  # Đẩy thanh máu lên cao hơn
                    enemy['x'] + bar_width/2,
                    enemy['y'] - 20 + bar_height,
                    fill="red",
                    tags="health_bar"
                )
                
                # Thanh máu hiện tại
                self.canvas.create_rectangle(
                    enemy['x'] - bar_width/2,
                    enemy['y'] - 20,  # Đẩy máu lên cao hơn
                    enemy['x'] - bar_width/2 + bar_width * health_ratio,
                    enemy['y'] - 20 + bar_height,
                    fill="green",
                    tags="health_bar"
                )
                
                # Hiển thị damage text cao hơn thanh máu
                if enemy['damage_text_timer'] > 0:
                    self.canvas.create_text(
                        enemy['x'],
                        enemy['y'] - 25,  # Đẩy text damage lên cao hơn
                        text=str(enemy['damage_text']),
                        fill="red",
                        font=("Arial", 10, "bold"),
                        tags="damage_text"
                    )
        
        # Draw projectiles as simple dots with trails
        for proj in self.game.projectiles:
            # Draw main projectile
            self.canvas.create_oval(
                proj['x'] - 4, proj['y'] - 4,
                proj['x'] + 4, proj['y'] + 4,
                fill="red", outline="darkred",
                tags="projectile"
            )
            
            # Simple trail effect
            self.canvas.create_line(
                proj['x'], proj['y'],
                proj['x'] - proj['dx'] * 3,
                proj['y'] - proj['dy'] * 3,
                fill=self.game.tower_types[proj['tower_type']]['color'],
                width=2,
                tags="projectile"
            )

        # Sắp xếp các layer theo thứ tự
        self.canvas.tag_raise("enemy")      # Sprite enemy ở giữa
        self.canvas.tag_raise("health_bar") # Thanh máu phía trên sprite
        self.canvas.tag_raise("damage_text") # Text damage cao nhất
    
    def load_sprites(self, sheet_path, num_frames):
        """Load sprite sheet and split into frames."""        
        try:
            sheet = Image.open(sheet_path)
            print(f"Loading sprite sheet: {sheet_path}")
            
            # Resize để projectile sprite nhỏ hơn
            if 'shoot' in sheet_path:
                new_width = sheet.width // 3  # Giảm kích thước projectile
                new_height = sheet.height // 3
            else:
                new_width = sheet.width // 2
                new_height = sheet.height // 2
                
            sheet = sheet.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Tính toán kích thước frame mới
            frame_width = new_width // num_frames
            frame_height = new_height
            frames = []
            
            for i in range(num_frames):
                frame = sheet.crop((i * frame_width, 0, (i + 1) * frame_width, frame_height))
                frames.append(ImageTk.PhotoImage(frame))
            
            return frames
        except Exception as e:
            print(f"Error loading sprite sheet {sheet_path}: {e}")
            placeholder = Image.new('RGBA', (16, 16), 'red')
            return [ImageTk.PhotoImage(placeholder)]
    
    def show_algorithm_selector(self):
        """Show algorithm selection window"""
        algo_window = ctk.CTkToplevel(self.root)
        algo_window.title("Chọn Thuật Toán Tìm Đường")
        algo_window.geometry("400x500")
        
        # Content frame
        content_frame = ctk.CTkFrame(algo_window, fg_color=("#F5F5F5", "#F5F5F5"))
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        ctk.CTkLabel(content_frame,
                    text="CHỌN THUẬT TOÁN",
                    font=ctk.CTkFont(size=24, weight="bold"),
                    text_color="#1565C0").pack(pady=10)
        
        algorithms = {
            "BFS": {
                "name": "Breadth-First Search",
                "desc": "Tìm đường ngắn nhất bằng cách duyệt theo chiều rộng",
                "color": "#4CAF50"
            },
            "DFS": {
                "name": "Depth-First Search",
                "desc": "Tìm đường bằng cách duyệt theo chiều sâu",
                "color": "#2196F3"
            },
            "Dijkstra": {
                "name": "Dijkstra",
                "desc": "Tìm đường ngắn nhất dựa trên chi phí di chuyển",
                "color": "#9C27B0"
            },
            "A*": {
                "name": "A* (A-Star)",
                "desc": "Tìm đường thông minh kết hợp chi phí và heuristic",
                "color": "#FF9800"
            }
        }
        
        for algo_key, algo_info in algorithms.items():
            # Algorithm container
            algo_container = ctk.CTkFrame(content_frame, fg_color=("#FFFFFF", "#FFFFFF"))
            algo_container.pack(fill="x", padx=10, pady=5)
            
            # Algorithm info
            info_frame = ctk.CTkFrame(algo_container, fg_color=("#FFFFFF", "#FFFFFF"))
            info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)
            
            ctk.CTkLabel(info_frame,
                        text=algo_info["name"],
                        font=ctk.CTkFont(size=14, weight="bold"),
                        text_color="#1B5E20").pack(anchor="w")
            
            ctk.CTkLabel(info_frame,
                        text=algo_info["desc"],
                        font=ctk.CTkFont(size=12),
                        text_color="#666666").pack(anchor="w")
            
            # Select button
            def make_select_command(algo):
                return lambda: self.select_algorithm(algo, algo_window)
            
            ctk.CTkButton(algo_container,
                         text="Chọn",
                         width=60,
                         font=ctk.CTkFont(size=13),
                         fg_color=algo_info["color"],
                         hover_color="#424242",
                         command=make_select_command(algo_key)).pack(side="right", padx=10, pady=5)
    
    def select_algorithm(self, algorithm, window):
        """Select an algorithm and update the UI"""
        self.game.selected_algo.set(algorithm)
        self.game.find_paths()
        window.destroy()