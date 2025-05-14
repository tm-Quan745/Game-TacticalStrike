import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import math
import pygame
pygame.mixer.init()
pygame.mixer.set_num_channels(12)

channels = {
    'enemy_walk': pygame.mixer.Channel(0),
    'enemy_attack': pygame.mixer.Channel(1),
    'tower_attack_fire': pygame.mixer.Channel(2),
    'tower_attack_ice' : pygame.mixer.Channel(3),
    'tower_attack_sniper' : pygame.mixer.Channel(4),
    'tower_explosion': pygame.mixer.Channel(5),
    'gameon' : pygame.mixer.Channel(6),
    'gameover' : pygame.mixer.Channel(7),
    'intro': pygame.mixer.Channel(8)
}

def load_sound_effects():
    
    sounds = {
        'tower_attack_fire': pygame.mixer.Sound('sound_effect/fire_shot.mp3'),
        'tower_attack_ice' : pygame.mixer.Sound('sound_effect/ice_shot.mp3'),
        'tower_attack_sniper': pygame.mixer.Sound('sound_effect/sniper_shot.mp3'),
        'tower_explosion' : pygame.mixer.Sound('sound_effect/tower_destroy.mp3'),
        'enemy_walk': pygame.mixer.Sound('sound_effect/footsteps.mp3'),
        'enemy_attack': pygame.mixer.Sound('sound_effect/AK-47.mp3'),
        'gameon' : pygame.mixer.Sound('sound_effect/game_on.wav'),
        'gameover' : pygame.mixer.Sound('sound_effect/game_over.mp3'),
        'intro': pygame.mixer.Sound('sound_effect/intro.mp3')
    }
    return sounds

for i in range(pygame.mixer.get_num_channels()):
    pygame.mixer.Channel(i).stop()
    
class GameUI:
    def __init__(self, root, game):
        self.enemy_id_counter = 0  # Counter for generating unique enemy IDs
        self.root = root
        self.game = game

        # Create default sprites for error cases
        default_proj = Image.new('RGBA', (16, 16), '#FF0000')
        self.default_frame = ImageTk.PhotoImage(default_proj)
        
        # Theme tracking
        self.current_theme = 0
        self.themes = [
            {
                'wall': "./sprites/wall.png",
                'floor': "./sprites/floor.png",
                'name': "Default"
            },
            {
                'wall': "./sprites/brownwall.png",
                'floor': "./sprites/floorgrass.png",
                'name': "Nature"
            },
            {
                'wall': "./sprites/ForestTree.png",
                'floor': "./sprites/ForestLand.png",
                'name': "Forest"
            },
            {
                'wall': "./sprites/water.png",
                'floor': "./sprites/sand.png",
                'name': "Beach"
            }
        ]
        
        # Create default sprites for error cases
        default_proj = Image.new('RGBA', (16, 16), '#FF0000')
        self.default_frame = ImageTk.PhotoImage(default_proj)
        
        # Load initial sprites
        try:
            # Load initial theme sprites
            self.load_theme_sprites(self.current_theme)
              # Add tower sprites loading
            shooter_tower = Image.open("./sprites/shooter_tower.png")  # Tháp bắn
            freezer_tower = Image.open("./sprites/freezer_tower.png")  # Tháp đóng băng
            sniper_tower = Image.open("./sprites/sniper_tower.png")   # Tháp bắn tỉa
            # Add projectile sprites loading
            ice = Image.open("./sprites/bulletice.png")
            sniper = Image.open("./sprites/bulletsniper.png")
            bullet = Image.open("./sprites/bulletfire.png")
            enemy_projectile = Image.open("./sprites/proj_enemy.png")
        
            # Resize sprites
            shooter_tower = shooter_tower.resize((48, 48), Image.Resampling.LANCZOS)
            freezer_tower = freezer_tower.resize((48, 48), Image.Resampling.LANCZOS)
            sniper_tower = sniper_tower.resize((48, 48), Image.Resampling.LANCZOS)
            bullet = bullet.resize((16, 16), Image.Resampling.LANCZOS)
            ice = ice.resize((16, 16), Image.Resampling.LANCZOS)
            sniper = sniper.resize((16, 16), Image.Resampling.LANCZOS)
            enemy_projectile = enemy_projectile.resize((16, 16), Image.Resampling.LANCZOS)            
            self.tower_sprites = {
                'shooter': ImageTk.PhotoImage(shooter_tower),
                'freezer': ImageTk.PhotoImage(freezer_tower),
                'sniper': ImageTk.PhotoImage(sniper_tower)
            }# Create projectile sprites with 8 directional rotations
            self.projectile_sprites = {
                'shooter': [],
                'freezer': [],
                'sniper': []
            }
            
                # Create 8 rotation frames (every 45 degrees) for each projectile type
            angles = [0, 45, 90, 135, 180, 225, 270, 315]
            projectiles = {'shooter': bullet, 'freezer': ice, 'sniper': sniper}
            for tower_type, base_sprite in projectiles.items():
                frames = []
                for angle in angles:
                    rotated = base_sprite.copy()
                    rotated = rotated.rotate(angle)
                    frames.append(ImageTk.PhotoImage(rotated))
                self.projectile_sprites[tower_type] = frames            # Enemy projectile frames
            self.enemy_projectile_frames = []
            try:
                rotated = enemy_projectile
                for i in range(4):  # Create 4 rotation frames
                    self.enemy_projectile_frames.append(ImageTk.PhotoImage(rotated))
                    rotated = rotated.rotate(90)
            except Exception as e:
                print(f"Warning: Error creating enemy projectile frames: {e}")
                self.enemy_projectile_frames = [self.default_frame] * 4
            
            # Load tower sprites
            tower_size = (60, 60)  # Kích thước tower
            
            shooter = Image.open("./sprites/shooter_tower.png")
            shooter = shooter.resize(tower_size, Image.Resampling.LANCZOS)
            self.shooter_sprite = ImageTk.PhotoImage(shooter)
            
            freezer = Image.open("./sprites/freezer_tower.png")
            freezer = freezer.resize(tower_size, Image.Resampling.LANCZOS)
            self.freezer_sprite = ImageTk.PhotoImage(freezer)
            
            sniper = Image.open("./sprites/sniper_tower.png") 
            sniper = sniper.resize(tower_size, Image.Resampling.LANCZOS)
            self.sniper_sprite = ImageTk.PhotoImage(sniper)
            
            # Dictionary để map loại tower với sprite tương ứng
            self.tower_sprites = {
                "shooter": self.shooter_sprite,
                "freezer": self.freezer_sprite,
                "sniper": self.sniper_sprite
            }
            
            # Create tower animation frames (optional)
            self.tower_animation_frames = {
                "shooter": [ImageTk.PhotoImage(shooter_tower.resize(tower_size).rotate(angle)) 
                            for angle in range(0, 360, 45)],
                "freezer": [ImageTk.PhotoImage(freezer_tower.resize(tower_size).rotate(angle)) 
                            for angle in range(0, 360, 45)],
                "sniper": [ImageTk.PhotoImage(sniper_tower.resize(tower_size).rotate(angle)) 
                            for angle in range(0, 360, 45)]
            }
            
            # Load start and end point sprites
            castle = Image.open("./sprites/castle.png")
            camp = Image.open("./sprites/camp.png")
            
            # Resize to fit cell size
            point_size = (self.game.cell_size, self.game.cell_size)
            self.start_sprite = ImageTk.PhotoImage(camp.resize(point_size, Image.Resampling.LANCZOS))
            self.end_sprite = ImageTk.PhotoImage(castle.resize(point_size, Image.Resampling.LANCZOS))
                
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
                                font=ctk.CTkFont(family="Minecraft", size=24, weight="bold"),
                                text_color="#2E7D32")
        title_label.pack(pady=(10, 10))
        
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
                                      font=ctk.CTkFont(family="Minecraft", size=14),
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
        
        # Theme selection button
        self.theme_button = ctk.CTkButton(
            buttons_frame,
            text=f"Theme: {self.themes[self.current_theme]['name']}",
            font=ctk.CTkFont(family="Minecraft", size=14, weight="bold"),
            fg_color="#9C27B0",
            hover_color="#7B1FA2",
            command=self.change_theme
        )
        self.theme_button.pack(fill=tk.X, padx=5, pady=5)
        
        # Algorithm selection button
        self.algorithm_button = ctk.CTkButton(
            buttons_frame, 
            text=f"Thuật Toán: {self.game.selected_algo.get()}",
            font=ctk.CTkFont(family="Minecraft", size=14, weight="bold"),
            fg_color="#673AB7",
            hover_color="#512DA8",
            command=self.show_algorithm_selector
        )
        self.algorithm_button.pack(fill=tk.X, padx=5, pady=5)
        
        # Start wave button
        self.start_button = ctk.CTkButton(
            buttons_frame,
            text="Bắt Đầu Làn Sóng",
            font=ctk.CTkFont(family="Minecraft", size=14, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#388E3C",
            command=self.game.start_wave
        )
        self.start_button.pack(fill=tk.X, padx=5, pady=5)
        
        # New maze button
        ctk.CTkButton(
            buttons_frame,
            text="Tạo Mê Cung Mới",
            font=ctk.CTkFont(family="Minecraft", size=14, weight="bold"),
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
            font=ctk.CTkFont(family="Minecraft", size=18, weight="bold"),
            text_color="#2E7D32"
        )
        info_title.pack(pady=5)
        
        # Game info labels
        self.timeline_label = ctk.CTkLabel(
            info_frame,
            text=f"Thời gian đến đích: {self.game.wave_start_time}s",
            font=ctk.CTkFont(family="Minecraft", size=14),
            text_color="#1B5E20"
        )
        self.timeline_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.money_label = ctk.CTkLabel(
            info_frame,
            text=f"Tiền: {self.game.money}$",
            font=ctk.CTkFont(family="Minecraft", size=14),
            text_color="#1B5E20"
        )
        self.money_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.lives_label = ctk.CTkLabel(
            info_frame,
            text=f"Mạng: {self.game.lives}",
            font=ctk.CTkFont(family="Minecraft", size=14),
            text_color="#1B5E20"
        )
        self.lives_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.wave_label = ctk.CTkLabel(
            info_frame,
            text=f"Làn sóng: {self.game.current_wave}",
            font=ctk.CTkFont(family="Minecraft", size=14),
            text_color="#1B5E20"
        )
        self.wave_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.score_label = ctk.CTkLabel(
            info_frame,
            text=f"Điểm: {self.game.score}",
            font=ctk.CTkFont(family="Minecraft", size=14),
            text_color="#1B5E20"
        )
        self.score_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Tower frame
        tower_frame = ctk.CTkFrame(control_scroll, fg_color=("#E3F2FD", "#E3F2FD"))
        tower_frame.pack(fill=tk.X, pady=5, padx=5)
        
        tower_title = ctk.CTkLabel(
            tower_frame,
            text="Xây Tháp",
            font=ctk.CTkFont(family="Minecraft", size=18, weight="bold"),
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
                font=ctk.CTkFont(family="Minecraft", size=13, weight="bold"),
                text_color="#1B5E20"
            ).pack(anchor=tk.W)
            
            ctk.CTkLabel(
                info_frame,
                text=f"Giá: {tower_info['cost']}$",
                font=ctk.CTkFont(family="Minecraft", size=12),
                text_color="#1B5E20"
            ).pack(anchor=tk.W)
            
            # Stats frame
            stats_frame = ctk.CTkFrame(info_frame, fg_color=("#FFFFFF", "#FFFFFF"))
            stats_frame.pack(fill=tk.X, pady=2)
            
            # Stats with icons
            ctk.CTkLabel(
                stats_frame,
                text=f"💥 {tower_info['damage']} | 🎯 {tower_info['range']} | ⚡ {100/tower_info['fire_rate']:.1f}/s",
                font=ctk.CTkFont(family="Minecraft", size=11),
                text_color="#666666"
            ).pack(anchor=tk.W)
            
            # Build button
            ctk.CTkButton(
                tower_container,
                text="Xây",
                width=60,
                height=32,
                font=ctk.CTkFont(family="Minecraft", size=13),
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
            font=ctk.CTkFont(family="Minecraft", size=12),
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
            font=ctk.CTkFont(family="Minecraft", size=14),
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
        self.timeline_label.configure(text=f"Thời gian đến đích: {self.game.timeline:.2f}s")
        self.money_label.configure(text=f"Tiền: {self.game.money}$")
        self.lives_label.configure(text=f"Mạng: {self.game.lives}")
        self.wave_label.configure(text=f"Làn sóng: {self.game.current_wave}")
        self.score_label.configure(text=f"Điểm: {self.game.score}")
    def draw_maze(self):
        """Draw the current state of the maze."""
        # Delete all existing elements except enemies
        self.canvas.delete("terrain", "health_bar", "projectile", "tower", "damage_text")

        # Draw grid cells using sprites
        for y in range(self.game.grid_size):
            for x in range(self.game.grid_size):
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
                    self.canvas.create_rectangle(
                        x * self.game.cell_size, y * self.game.cell_size,
                        (x + 1) * self.game.cell_size, (y + 1) * self.game.cell_size,
                        fill="#8d6e63" if self.game.maze[y][x] == 1 else "#e8f5e9",
                        outline="#5d4037" if self.game.maze[y][x] == 1 else "#c8e6c9",
                        tags="terrain"
                    )
        
        # Replace rectangle markers with sprites for start and end points
        self.canvas.create_image(
            self.game.cell_size/2,  # Center of first cell
            self.game.cell_size/2,
            image=self.start_sprite,
            anchor='center',
            tags="terrain"
        )
        
        self.canvas.create_image(
            (self.game.grid_size - 0.5) * self.game.cell_size,  # Center of last cell
            (self.game.grid_size - 0.5) * self.game.cell_size,
            image=self.end_sprite,
            anchor='center',
            tags="terrain"
        )
        
        # Draw towers with sprites
        for tower in self.game.towers:
            x, y = tower['x'], tower['y']
            tower_type = tower['type']
            
            # Create tower sprite
            self.canvas.create_image(
                x * self.game.cell_size + self.game.cell_size/2,
                y * self.game.cell_size + self.game.cell_size/2,
                image=self.tower_sprites[tower_type],
                anchor='center',
                tags="tower"
            )
            
            # Show range when hovering or selected
            if (hasattr(self.game, 'build_mode') and 
                self.game.build_mode == "delete") or tower.get('show_range', False):
                # Set color based on tower type
                if tower_type == 'shooter':
                    color = 'red'  # Xanh cho shooter tower
                elif tower_type == 'freezer':
                    color = '#00bcd4'  # Xanh nhạt cho freezer tower
                elif tower_type == 'sniper':
                    color = '#9b59b6'  # Tím cho sniper tower
                else:
                    color = '#666666'  # Màu mặc định
                    
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

        # Draw enemies with their sprites and health bars
        for enemy in self.game.enemies:
            if enemy['spawn_delay'] <= 0:
                enemy_id = enemy.get('id', id(enemy))  # Gán ID duy nhất nếu chưa có 
                tag = f"enemy_{enemy_id}"

                # Xoá sprite cũ
                self.canvas.delete(tag)
                
                # Get current animation based on direction
                current_anim = enemy.get('animation_frames', {}).get(enemy['direction'], [])
                if current_anim and len(current_anim) > 0:
                    # Use current frame from animation
                    frame_index = enemy['current_frame'] % len(current_anim)
                    frame = current_anim[frame_index]
                    
                    # Vẽ frame mới, gán tag riêng
                    self.canvas.create_image(
                        enemy['x'],
                        enemy['y'],
                        image=frame,
                        anchor='center',
                        tags=(tag, 'enemy')
                    )
                
                # Draw enemy health bar
                health_ratio = enemy['health'] / enemy['max_health']
                bar_width = 20
                bar_height = 4
                
                # Health bar background
                self.canvas.create_rectangle(
                    enemy['x'] - bar_width/2,
                    enemy['y'] - 25,
                    enemy['x'] + bar_width/2,
                    enemy['y'] - 25 + bar_height,
                    fill="red",
                    tags="health_bar"
                )
                
                # Current health bar
                self.canvas.create_rectangle(
                    enemy['x'] - bar_width/2,
                    enemy['y'] - 25,
                    enemy['x'] - bar_width/2 + bar_width * health_ratio,
                    enemy['y'] - 25 + bar_height,
                    fill="green",
                    tags="health_bar"
                )
                
                # Show damage text above health bar
                if enemy['damage_text_timer'] > 0:
                    self.canvas.create_text(
                        enemy['x'],
                        enemy['y'] - 25,
                        text=str(enemy['damage_text']),
                        fill="red",
                        font=("Minecraft", 10, "bold"),
                        tags="damage_text"
                    )

        # Draw tower projectiles with rotation animation
        for proj in self.game.projectiles:
            # Calculate rotation frame based on projectile direction
            angle = math.atan2(proj['dy'], proj['dx'])
            frame_index = int(((angle + math.pi) / (2 * math.pi) * 8) % 8)
            
            # Create image with correct rotation frame
            self.canvas.create_image(
                proj['x'], proj['y'],
                image=self.projectile_sprites[proj['tower_type']][frame_index],
                tags="projectile"
            )

        # Draw enemy projectiles
        for projectile in self.game.enemy_projectiles:
            self.canvas.create_image(
                projectile['x'],
                projectile['y'],
                image=self.enemy_projectile_frames[projectile['current_frame']],
                anchor='center',
                tags="projectile"
            )

        # Layer ordering
        self.canvas.tag_raise("enemy")        # Enemy sprites in middle
        self.canvas.tag_raise("health_bar")   # Health bars above enemies
        self.canvas.tag_raise("projectile")   # Projectiles on top
        self.canvas.tag_raise("damage_text")  # Damage text highest
    
    
    def load_sprites(self, sheet_path, num_frames, target_size=(32, 32)):
        """Load sprite sheet, split into frames, and resize each frame to target_size."""
        try:
            sheet = Image.open(sheet_path).convert("RGBA")
            print(f"Loading sprite sheet: {sheet_path}")

            frame_width = sheet.width // num_frames
            frame_height = sheet.height

            frames = []

            for i in range(num_frames):
                frame = sheet.crop((i * frame_width, 0, (i + 1) * frame_width, frame_height))
                
                # Resize từng frame sau khi crop (đảm bảo rõ nét và đúng tỉ lệ)
                frame = frame.resize(target_size, Image.Resampling.LANCZOS)

                frames.append(ImageTk.PhotoImage(frame))

            return frames

        except Exception as e:
            print(f"Error loading sprite sheet {sheet_path}: {e}")
            placeholder = Image.new('RGBA', target_size, 'red')
            return [ImageTk.PhotoImage(placeholder)]

    
    def show_algorithm_selector(self):
        """Show algorithm selection window"""
        algo_window = ctk.CTkToplevel(self.root)
        algo_window.title("Chọn Thuật Toán Tìm Đường")
        algo_window.geometry("400x500")
        algo_window.grab_set()
        
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
            "A*": {
                "name": "A* (A-Star)",
                "desc": "Tìm đường thông minh kết hợp chi phí và heuristic",
                "color": "#FF9800"
            },
            "Beam":{
                "name": "Beam Search",
                "desc": "Tìm đường theo chiều rộng nhưng chỉ giữ số lượng giới hạn các lựa chọn tốt nhất ở mỗi bước",
                "color": "#705446"
            },
            "Q-Learning": {
                "name": "Q-Learning",
                "desc": "Học tăng cường để tìm đường tối ưu trực tiếp trên map hiện tại",
                "color": "#2196F3"
            },
            "Partial": {
                "name": "Partial Observation Search",
                "desc": "Thuật toán tìm đường dựa trên quan sát từng phần của mê cung, phù hợp với thực tế khi người chơi chỉ nhìn thấy phần xung quanh",
                "color": "#9C27B0"
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
                        text_color="#666666",
                        anchor="w",
                        justify="left",
                        wraplength=280).pack(anchor="w", fill="x")

            
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
        # Close window first to prevent hanging
        window.destroy()
        
        self.game.selected_algo.set(algorithm)
        algo_name = self.game.selected_algo.get()
        algo_color = {
            "BFS": "#4CAF50",
            "A*": "#FF9800",
            "Beam": "#705446",
            "Partial": "#9C27B0",
            "Q-Learning": "#2196F3"
        }.get(algorithm, "#FFFFFF")
        self.update_algorithm_button(algo_name, algo_color)
        print(f"Selected algorithm: {algo_name}")
        
        # Find paths after UI updates
        self.game.find_paths()
        
    def update_algorithm_button(self, algo_name, algo_color):
        """Update the algorithm button's text and color based on the selected algorithm"""
        self.algorithm_button.configure(  
            text=f"Thuật Toán: {algo_name}",
            fg_color=algo_color  
        )

    def load_theme_sprites(self, theme_index):
        """Load sprites for the current theme"""
        theme = self.themes[theme_index]
        try:
            # Load wall sprite
            wall = Image.open(theme['wall'])
            wall = wall.resize((self.game.cell_size, self.game.cell_size), Image.Resampling.LANCZOS)
            
            # Load floor sprite  
            floor = Image.open(theme['floor'])
            floor = floor.resize((self.game.cell_size, self.game.cell_size), Image.Resampling.LANCZOS)
            
            # Update tile sprites
            self.tile_sprites = {
                'grass': ImageTk.PhotoImage(wall),
                'land': ImageTk.PhotoImage(floor)
            }
            
            # Redraw maze with new sprites
            self.draw_maze()
            
        except Exception as e:
            print(f"Error loading theme sprites: {e}")
            # Create default colored sprites if loading fails
            placeholder = Image.new('RGBA', (self.game.cell_size, self.game.cell_size), '#8d6e63')
            placeholder2 = Image.new('RGBA', (self.game.cell_size, self.game.cell_size), '#e8f5e9')
            self.tile_sprites = {
                'grass': ImageTk.PhotoImage(placeholder),
                'land': ImageTk.PhotoImage(placeholder2)
            }
    
    def change_theme(self):
        """Change to the next available theme"""
        self.current_theme = (self.current_theme + 1) % len(self.themes)
        self.load_theme_sprites(self.current_theme)
        self.theme_button.configure(text=f"Theme: {self.themes[self.current_theme]['name']}")




