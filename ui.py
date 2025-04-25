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
            # Add projectile sprites loading
            ice = Image.open("./sprites/grass2.png")
            sniper = Image.open("./sprites/grass3.png")
            bullet = Image.open("./sprites/land1.jpg")
            # Resize sprites
            grass = grass.resize((game.cell_size, game.cell_size), Image.Resampling.LANCZOS)
            land = land.resize((game.cell_size, game.cell_size), Image.Resampling.LANCZOS)
            bullet = bullet.resize((16, 16), Image.Resampling.LANCZOS)
            ice = ice.resize((16, 16), Image.Resampling.LANCZOS)
            sniper = sniper.resize((16, 16), Image.Resampling.LANCZOS)

            self.tile_sprites = {
                'grass': ImageTk.PhotoImage(grass),
                'land': ImageTk.PhotoImage(land),
            }
            
            self.projectile_sprites = {
                'shooter': ImageTk.PhotoImage(bullet),
                'freezer': ImageTk.PhotoImage(ice),
                'sniper': ImageTk.PhotoImage(sniper)
            }
        except Exception as e:
            print(f"Error loading sprites: {e}")
            self.tile_sprites = {
                'grass': None,
                'land': None,
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
        
        # Maze canvas - keeping tk.Canvas
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
        
        # Control frame (right)
        control_frame = ctk.CTkFrame(main_frame, fg_color=("#F1F8E9", "#F1F8E9"))
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        # Info frame with bright colors
        info_frame = ctk.CTkFrame(control_frame, fg_color=("#E8F5E9", "#E8F5E9"))
        info_title = ctk.CTkLabel(info_frame, text="Thông Tin",
                               font=ctk.CTkFont(size=18, weight="bold"),
                               text_color="#2E7D32")
        info_title.pack(pady=5)
        info_frame.pack(fill=tk.X, pady=5)
        
        self.money_label = ctk.CTkLabel(info_frame, text=f"Tiền: {self.game.money}$",
                                    font=ctk.CTkFont(size=14),
                                    text_color="#1B5E20")
        self.money_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.lives_label = ctk.CTkLabel(info_frame, text=f"Mạng: {self.game.lives}",
                                     font=ctk.CTkFont(size=14),
                                     text_color="#1B5E20")
        self.lives_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.wave_label = ctk.CTkLabel(info_frame, text=f"Làn sóng: {self.game.current_wave}",
                                    font=ctk.CTkFont(size=14),
                                    text_color="#1B5E20")
        self.wave_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.score_label = ctk.CTkLabel(info_frame, text=f"Điểm: {self.game.score}",
                                     font=ctk.CTkFont(size=14),
                                     text_color="#1B5E20")
        self.score_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Game buttons with bright colors
        self.start_button = ctk.CTkButton(control_frame, text="Bắt Đầu Làn Sóng",
                                      font=ctk.CTkFont(size=14, weight="bold"),
                                      fg_color="#4CAF50",
                                      hover_color="#388E3C",
                                      command=self.game.start_wave)
        self.start_button.pack(fill=tk.X, padx=5, pady=5)
        
        ctk.CTkButton(control_frame, text="Tạo Mê Cung Mới",
                   font=ctk.CTkFont(size=14, weight="bold"),
                   fg_color="#2196F3",
                   hover_color="#1976D2",
                   corner_radius=10,
                   command=self.game.generate_maze).pack(fill=tk.X, padx=5, pady=5)
        
        # Tower buttons with bright colors
        tower_frame = ctk.CTkFrame(control_frame, fg_color=("#E3F2FD", "#E3F2FD"))
        tower_title = ctk.CTkLabel(tower_frame, text="Xây Tháp",
                                font=ctk.CTkFont(size=18, weight="bold"),
                                text_color="#1565C0")
        tower_title.pack(pady=5)
        tower_frame.pack(fill=tk.X, pady=5)
        
        for tower_key, tower_info in self.game.tower_types.items():
            tower_btn = ctk.CTkButton(tower_frame, 
                                    text=f"{tower_info['name']} ({tower_info['cost']}$)",
                                    font=ctk.CTkFont(size=13),
                                    fg_color=tower_info["color"],
                                    hover_color="#424242",
                                    command=lambda t=tower_key: self.game.set_build_mode(t))
            tower_btn.pack(fill=tk.X, padx=5, pady=2)
        
        # Delete button with red color
        ctk.CTkButton(tower_frame, text="Xóa Tháp",
                   font=ctk.CTkFont(size=13),
                   fg_color="#F44336",
                   hover_color="#D32F2F",
                   command=lambda: self.game.set_build_mode("delete")).pack(fill=tk.X, padx=5, pady=2)
        
        # Help button with nice blue color
        ctk.CTkButton(control_frame, text="Hướng Dẫn",
                   font=ctk.CTkFont(size=14),
                   fg_color="#03A9F4",
                   hover_color="#0288D1",
                   corner_radius=10,
                   command=self.game.show_help).pack(fill=tk.X, padx=5, pady=10)
    
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