import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from entities import Enemy  # Import the Enemy class
import os  # Import os for handling file paths

class Soldier:
    def __init__(self, canvas, x, y, sprites, direction="walk_right", max_health=100):
        self.canvas = canvas
        self.x, self.y = x, y
        self.sprites = sprites
        self.frames = self.sprites.get(direction, [])
        if not self.frames:
            raise ValueError(f"Error: No frames found for direction '{direction}'. Check sprite loading.")
        self.current_frame = 0
        self.tk_image = self.frames[0]
        self.image = self.canvas.create_image(x, y, image=self.tk_image, anchor="nw")
        self.animation_speed = 100  # Animation speed in ms
        self.direction = direction
        self.max_health = max_health
        self.current_health = max_health
        self.animation_id = None  # Store the after() ID

        # Health bar
        self.health_bar_bg = self.canvas.create_rectangle(
            x, y - 10, x + 36, y - 5, fill="red", outline=""
        )
        self.health_bar_fg = self.canvas.create_rectangle(
            x, y - 10, x + 36, y - 5, fill="green", outline=""
        )

        self.update_animation()

    def update_animation(self):
        """Update the animation frame without affecting position."""
        if not self.canvas.winfo_exists():
            return  # Exit if the canvas no longer exists
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.tk_image = self.frames[self.current_frame]
        self.canvas.itemconfig(self.image, image=self.tk_image)
        self.animation_id = self.canvas.after(self.animation_speed, self.update_animation)

    def stop_animation(self):
        """Stop the animation by canceling the after() call."""
        if self.animation_id:
            self.canvas.after_cancel(self.animation_id)
            self.animation_id = None

    def __del__(self):
        """Ensure animation is stopped when the object is destroyed."""
        self.stop_animation()

    def move(self, dx, dy):
        """Move the Soldier and update its position on the canvas."""
        # Calculate new position
        new_x = self.x + dx
        new_y = self.y + dy

        # Constrain new position within canvas bounds
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if new_x < 0:
            new_x = 0
        elif new_x > canvas_width - 36:  # Assuming sprite width is 36
            new_x = canvas_width - 36

        if new_y < 0:
            new_y = 0
        elif new_y > canvas_height - 36:  # Assuming sprite height is 36

            new_y = canvas_height - 36

        # Automatically update direction based on movement
        if dx > 0:
            self.set_direction("walk_right")
        elif dx < 0:
            self.set_direction("walk_left")
        elif dy != 0:
            self.set_direction("walk_up")

        # Update position
        dx = new_x - self.x
        dy = new_y - self.y
        self.x = new_x
        self.y = new_y

        # Move the canvas elements
        self.canvas.move(self.image, dx, dy)
        self.canvas.move(self.health_bar_bg, dx, dy)
        self.canvas.move(self.health_bar_fg, dx, dy)

        # Trigger canvas redraw
        self.canvas.update()

    def set_direction(self, direction):
        """Set the direction and update the animation frames."""
        if self.direction != direction:
            self.direction = direction
            self.frames = self.sprites[direction]
            self.current_frame = 0  # Reset animation frame to avoid glitches

    def update_health(self, health):
        """Update the health bar position and size."""
        self.current_health = max(0, min(health, self.max_health))  # Clamp health
        health_ratio = self.current_health / self.max_health
        new_width = 36 * health_ratio

        # Update the position and size of the health bar
        self.canvas.coords(
            self.health_bar_bg,
            self.x, self.y - 10,
            self.x + 36, self.y - 5
        )
        self.canvas.coords(
            self.health_bar_fg,
            self.x, self.y - 10,
            self.x + new_width, self.y - 5
        )

    def smooth_move(self, dx, dy):
        """Smoothly move the Soldier in small steps."""
        steps = 10
        step_x, step_y = dx / steps, dy / steps

        def move_step(i=0):
            if i < steps:
                self.move(step_x, step_y)
                self.canvas.after(30, lambda: move_step(i + 1))  # 30ms per step

        move_step()

class GameUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.sprites = {}
        self.start_button = None  # Initialize start_button as None
        self.setup_ui()
        self.load_sprites()

    def load_sprites(self):
        """Load sprite sheets and split them into frames."""
        def load_sprites(sheet_path, num_frames):
            try:
                sheet = Image.open(sheet_path)
                frame_width = sheet.width // num_frames
                frame_height = sheet.height
                return [ImageTk.PhotoImage(sheet.crop((i * frame_width, 0, (i + 1) * frame_width, frame_height))) for i in range(num_frames)]
            except FileNotFoundError:
                print(f"Error: Sprite file not found: {sheet_path}")
                # Create a placeholder sprite (solid color)
                placeholder = Image.new("RGBA", (36, 36), (255, 0, 0, 255))  # Red square
                return [ImageTk.PhotoImage(placeholder) for _ in range(num_frames)]

        NUM_FRAMES = 4
        sprite_dir = os.path.join(os.getcwd(), "sprites")  # Assuming sprites are in a "sprites" folder
        self.sprites = {
            "walk_right": load_sprites(os.path.join(sprite_dir, "Linh_move.png"), NUM_FRAMES),
            "walk_left": load_sprites(os.path.join(sprite_dir, "Linh_moveleft.png"), NUM_FRAMES),
            "walk_up": load_sprites(os.path.join(sprite_dir, "Linh_moveupdown.png"), NUM_FRAMES),
            "shoot_right": load_sprites(os.path.join(sprite_dir, "Linh_shoot.png"), NUM_FRAMES),
            "shoot_left": load_sprites(os.path.join(sprite_dir, "Linh_shootleft.png"), NUM_FRAMES),
        }
        # Validate that all sprites are loaded
        for key, frames in self.sprites.items():
            if not frames:
                print(f"Warning: No frames loaded for '{key}'. Using placeholder sprites.")

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
        """Draw the current state of the maze, including static elements."""
        # Clear only static elements (e.g., maze grid)
        self.canvas.delete("maze")  # Use a tag to delete only maze-related elements
        
        # Draw grid cells
        for y in range(self.game.grid_size):
            for x in range(self.game.grid_size):
                if self.game.maze[y][x] == 1:  # Wall
                    self.canvas.create_rectangle(
                        x * self.game.cell_size, y * self.game.cell_size,
                        (x + 1) * self.game.cell_size, (y + 1) * self.game.cell_size,
                        fill="#8d6e63", outline="#5d4037", tags="maze"
                    )
                else:  # Path
                    self.canvas.create_rectangle(
                        x * self.game.cell_size, y * self.game.cell_size,
                        (x + 1) * self.game.cell_size, (y + 1) * self.game.cell_size,
                        fill="#e8f5e9", outline="#c8e6c9", tags="maze"
                    )
        
        # Mark start and end points
        self.canvas.create_rectangle(
            0, 0, self.game.cell_size, self.game.cell_size,
            fill="#4caf50", outline="#2e7d32", tags="maze"
        )
        self.canvas.create_text(
            self.game.cell_size/2, self.game.cell_size/2,
            text="S", fill="white", font=("Arial", 12, "bold"), tags="maze"
        )
        
        self.canvas.create_rectangle(
            (self.game.grid_size-1) * self.game.cell_size,
            (self.game.grid_size-1) * self.game.cell_size,
            self.game.grid_size * self.game.cell_size,
            self.game.grid_size * self.game.cell_size,
            fill="#f44336", outline="#c62828", tags="maze"
        )
        self.canvas.create_text(
            (self.game.grid_size-0.5) * self.game.cell_size,
            (self.game.grid_size-0.5) * self.game.cell_size,
            text="E", fill="white", font=("Arial", 12, "bold"), tags="maze"
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
        
        # Draw enemies after all static elements
        self.draw_enemies()
        
        # Draw projectiles
        for proj in self.game.projectiles:
            self.canvas.create_oval(
                proj['x'] - 3, proj['y'] - 3,
                proj['x'] + 3, proj['y'] + 3,
                fill="yellow", outline="orange"
            )

    def draw_enemies(self):
        """Draw enemies with animations."""
        for enemy in self.game.enemies:
            if enemy['canvas_image'] is None:
                # Initialize the canvas image for the enemy
                enemy['canvas_image'] = self.canvas.create_image(
                    enemy['x'], enemy['y'], image=enemy['animation_frames'][enemy['direction']][0], anchor="nw"
                )
            else:
                # Update the position of the enemy
                self.canvas.coords(enemy['canvas_image'], enemy['x'], enemy['y'])
            # Update the animation frame
            Enemy.update_animation(enemy, self.canvas)