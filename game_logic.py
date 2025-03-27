import random
import time
from tkinter import messagebox, ttk
import tkinter as tk
from maze_generator import generate_maze
from pathfinding import find_path, bfs_find_path  # Import bfs_find_path
from entities import Tower, Enemy, Projectile
from ui import GameUI, Soldier  # Import Soldier class

class MazeTowerDefenseGame:
    def __init__(self, root):
        self.root = root
        
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
        self.start_button = None  # Initialize start_button as None
        
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
        
        # Initialize UI (needs to be imported here to avoid circular imports)
        from ui import GameUI
        self.ui = GameUI(root, self)  # Ensure UI is initialized before calling generate_maze
        
        # Initialize game
        self.generate_maze()  # Generate maze after UI initialization
        self.setup_events()
    
    def setup_events(self):
        self.ui.canvas.bind("<Button-1>", self.on_canvas_click)
        self.ui.canvas.bind("<Motion>", self.on_canvas_hover)
        self.game_loop_id = self.root.after(50, self.game_loop)  # Store the after ID

        # Bind the close event to cancel callbacks
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def toggle_game_speed(self):
        speeds = [1.0, 1.5, 2.0, 0.5]
        current_index = speeds.index(self.game_speed)
        self.game_speed = speeds[(current_index + 1) % len(speeds)]
        self.ui.speed_btn.config(text=f"{self.game_speed}x")
    
    def generate_maze(self):
        # Ensure grid_size is odd
        if self.grid_size % 2 == 0:
            self.grid_size += 1
            print(f"Adjusted grid_size to {self.grid_size} (must be odd).")

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
                    self.maze[y + dy // 2][x + dx // 2] = 0
                    # Mark new cell as path
                    self.maze[new_y][new_x] = 0

                    stack.append((new_x, new_y))
                    moved = True
                    break

            if not moved:
                stack.pop()

        # Ensure there's a path from (0,0) to (grid_size-1, grid_size-1)
        self.maze[self.grid_size - 1][self.grid_size - 1] = 0

        # Make maze more open for better gameplay
        for i in range(1, self.grid_size - 1, 2):
            for j in range(1, self.grid_size - 1, 2):
                if random.random() < 0.6:  # Increased openness
                    self.maze[i][j] = 0

        # Ensure starting and ending areas are more open
        for i in range(2):
            for j in range(2):
                if i > 0 or j > 0:  # Don't change the actual start point
                    self.maze[j][i] = 0
                    self.maze[self.grid_size - 1 - j][self.grid_size - 1 - i] = 0

        # Debug: Print the maze
        print("Generated Maze:")
        for row in self.maze:
            print("".join(["█" if cell == 1 else " " for cell in row]))

        # Check if a path exists
        path = bfs_find_path(self.maze, self.grid_size)  # Use bfs_find_path
        if not path:
            print("Warning: No path found in the generated maze!")

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
        self.update_info_labels()
        if hasattr(self.ui, 'update_info_labels'):
            self.ui.update_info_labels()
        if hasattr(self.ui, 'start_button') and self.ui.start_button:
            self.ui.start_button.config(text="Bắt Đầu Làn Sóng")
        if hasattr(self.ui, 'status_label'):
            self.ui.status_label.config(text="Mê cung mới đã được tạo! Hãy bắt đầu xây tháp.")
        self.play_sound("new_game")

        # Calculate paths
        self.find_paths()
    
    def find_paths(self):
        """Find paths using A* and cache results."""
        if hasattr(self, 'cached_paths') and self.cached_paths:
            self.paths = self.cached_paths  # Use cached paths if available
            return

        # Find a single path using A* algorithm
        path = find_path(self.maze, self.grid_size, "A*")  # Use A* for better performance
        if not path:
            print("Error: No path found!")  # Debug: Check if pathfinding fails
            return

        self.paths = [path]
        self.cached_paths = self.paths  # Cache the paths for reuse

        # Debug: Print the path for verification
        print(f"Path found: {self.paths}")

        # Update path for all enemies
        for enemy in self.enemies:
            enemy['path_index'] = 0
            enemy['path_position'] = 0
            next_pos = self.paths[0][0]
            enemy['target_x'] = next_pos[0] * self.cell_size + self.cell_size / 2
            enemy['target_y'] = next_pos[1] * self.cell_size + self.cell_size / 2
    
    def game_loop(self):
        """Main game loop."""
        try:
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

            # Schedule next frame
            self.game_loop_id = self.root.after(50, self.game_loop)
        except Exception as e:
            print(f"Error in game_loop: {e}")
    
    def update_enemies(self, dt):
        """Update enemy positions and animations."""
        for enemy in self.enemies[:]:
            # Handle spawn delay
            if enemy['spawn_delay'] > 0:
                enemy['spawn_delay'] -= 1 * dt
                continue

            # Update enemy position
            if not Enemy.move(enemy, dt, self.cell_size, self.paths, self.ui.canvas):  # Pass canvas here
                # Remove enemy if it reaches the end of the path
                Enemy.stop_animation(enemy, self.ui.canvas)  # Stop animation before removing
                self.enemies.remove(enemy)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over()
                else:
                    self.ui.update_info_labels()

            # Check if the enemy died
            if enemy['health'] <= 0:
                Enemy.stop_animation(enemy, self.ui.canvas)  # Stop animation before removing
                self.enemies.remove(enemy)
                self.money += enemy['reward']
                self.score += enemy['reward']
                self.ui.update_info_labels()
                self.play_sound("enemy_die")

        # Batch canvas updates for all enemies
        self.ui.canvas.update()
    
    def update_towers(self, dt):
        """Update towers and their interactions with enemies."""
        for tower in self.towers:
            target = Tower.find_target(tower, self.enemies, self.cell_size)
            if target:
                Tower.attack(tower, target, dt, self.projectiles, self.cell_size)
    
    def update_projectiles(self, dt):
        """Update projectile positions and handle collisions."""
        for projectile in self.projectiles[:]:
            if not Projectile.update(projectile, dt):
                self.projectiles.remove(projectile)
                for enemy in self.enemies[:]:
                    # Only check for collisions when the projectile is near the target
                    if (abs(projectile['x'] - projectile['target_x']) < self.cell_size and
                        abs(projectile['y'] - projectile['target_y']) < self.cell_size):
                        enemy['health'] -= projectile['damage']
                        enemy['object'].update_health(enemy['health'])
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
        """Spawn enemies for the current wave."""
        num_enemies = 5 + self.current_wave * 2
        base_health = 50 + self.current_wave * 10
        base_speed = 50 + min(100, self.current_wave * 10)

        for i in range(num_enemies):
            enemy_type = "normal"
            if self.current_wave >= 3:
                r = random.random()
                if r < 0.2:
                    enemy_type = "tank"
                elif r < 0.4:
                    enemy_type = "fast"

            # Ensure sprites are loaded
            if not self.ui.sprites.get("walk_right"):
                print("Error: Sprites not loaded. Cannot create enemies.")
                continue

            # Create enemy with animation support
            enemy = Enemy.create(
                enemy_type,
                self.enemy_types[enemy_type],
                base_health,
                base_speed,
                spawn_delay=0,
                cell_size=self.cell_size,
                sprites=self.ui.sprites
            )

            # Initialize target_x and target_y with the first path point
            if self.paths and len(self.paths[0]) > 0:
                first_point = self.paths[0][0]
                enemy['target_x'] = first_point[0] * self.cell_size + self.cell_size / 2
                enemy['target_y'] = first_point[1] * self.cell_size + self.cell_size / 2

            # Add the 'object' key with a Soldier instance
            try:
                enemy['object'] = Soldier(
                    self.ui.canvas,
                    enemy['x'],
                    enemy['y'],
                    self.ui.sprites,
                    direction="walk_right"
                )
            except ValueError as e:
                print(f"Error creating Soldier: {e}")
                continue

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
                        path = find_path(test_maze, self.grid_size, self.selected_algo.get())
                        print("Maze after tower placement:")
                        for row in test_maze:
                            print(row)
                        print("Path after tower placement:", path)
                        if not path:
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
            info_text += f"Tầm bắn: {tower['range']} ô\n"
            info_text += f"Tốc độ bắn: {100/tower['fire_rate']:.1f}/s\n\n"
            info_text += f"{tower['description']}"
            
            self.ui.tower_info_label.config(text=info_text)
        elif mode == "delete":
            self.ui.tower_info_label.config(text="Chọn tháp để xóa và nhận lại 5$")
        else:
            self.ui.tower_info_label.config(text="Chọn tháp để xem thông tin chi tiết")

    def on_close(self):
        """Cancel scheduled callbacks and close the game."""
        if hasattr(self, 'game_loop_id'):
            self.root.after_cancel(self.game_loop_id)  # Cancel the game loop
        self.root.destroy()  # Close the game window

    def draw_maze(self):
        """Draw the current state of the maze."""
        self.ui.canvas.delete("all")  # Clear the canvas

        # Draw grid cells
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.maze[y][x] == 1:  # Wall
                    self.ui.canvas.create_rectangle(
                        x * self.cell_size, y * self.cell_size,
                        (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                        fill="#8d6e63", outline="#5d4037"
                    )
                else:  # Path
                    self.ui.canvas.create_rectangle(
                        x * self.cell_size, y * self.cell_size,
                        (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                        fill="#e8f5e9", outline="#c8e6c9"
                    )

        # Mark start and end points
        self.ui.canvas.create_rectangle(
            0, 0, self.cell_size, self.cell_size,
            fill="#4caf50", outline="#2e7d32"
        )
        self.ui.canvas.create_text(
            self.cell_size / 2, self.cell_size / 2,
            text="S", fill="white", font=("Arial", 12, "bold")
        )

        self.ui.canvas.create_rectangle(
            (self.grid_size - 1) * self.cell_size, (self.grid_size - 1) * self.cell_size,
            self.grid_size * self.cell_size, self.grid_size * self.cell_size,
            fill="#f44336", outline="#c62828"
        )
        self.ui.canvas.create_text(
            (self.grid_size - 0.5) * self.cell_size, (self.grid_size - 0.5) * self.cell_size,
            text="E", fill="white", font=("Arial", 12, "bold")
        )

    def update_info_labels(self):
        """Update all information labels with the current game state."""
        if hasattr(self.ui, 'money_label') and hasattr(self.ui, 'lives_label') and hasattr(self.ui, 'wave_label') and hasattr(self.ui, 'score_label'):
            self.ui.money_label.config(text=f"Tiền: {self.money}$")
            self.ui.lives_label.config(text=f"Mạng: {self.lives}")
            self.ui.wave_label.config(text=f"Làn sóng: {self.current_wave}")
            self.ui.score_label.config(text=f"Điểm: {self.score}")
        else:
            print("Warning: UI labels have not been initialized yet.")
