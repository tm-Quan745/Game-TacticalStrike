import tkinter as tk
from customtkinter import CTkToplevel, CTkFrame, CTkLabel
from tkinter import TclError

class RadarView:
    def __init__(self, parent, grid_size, cell_size):
        try:
            self.window = CTkToplevel(parent)
            self.window.title("Radar View - Partial Observation")
            self.window.geometry("600x650")
            self.window.attributes('-topmost', True)
            
            self.grid_size = grid_size
            self.cell_size = cell_size
            self.canvas = None
            self.stats_label = None
            
            # Main frame
            main_frame = CTkFrame(self.window)
            main_frame.pack(padx=10, pady=10, fill="both", expand=True)
            
            # Title
            CTkLabel(
                main_frame,
                text="RADAR VIEW",
                font=("Arial", 16, "bold")
            ).pack(pady=(0, 10))
            
            # Info label
            CTkLabel(
                main_frame,
                text="Vùng tối: Chưa khám phá | Vùng sáng: Đã khám phá",
                font=("Arial", 12)
            ).pack(pady=(0, 10))
            
            # Canvas frame
            canvas_frame = CTkFrame(main_frame)
            canvas_frame.pack(padx=10, pady=10)
            
            # Canvas for radar view
            self.canvas = tk.Canvas(
                canvas_frame,
                width=self.grid_size * self.cell_size,
                height=self.grid_size * self.cell_size,
                bg="#1a1a1a",
                highlightthickness=2,
                highlightbackground="#333333"
            )
            self.canvas.pack(padx=10, pady=10)
            
            # Stats frame
            stats_frame = CTkFrame(main_frame)
            stats_frame.pack(fill="x", padx=10, pady=10)
            
            self.stats_label = CTkLabel(
                stats_frame,
                text="Chưa khám phá: 100%",
                font=("Arial", 12)
            )
            self.stats_label.pack()
            
        except TclError as e:
            print(f"Error creating radar view: {e}")
            self.window = None
    
    def update_view(self, maze, belief_state):
        """Update radar view with current belief state"""
        if not self.window or not self.canvas:
            return
            
        try:
            if not self.window.winfo_exists():
                return
                
            # Clear canvas
            self.canvas.delete("all")
            
            # Calculate exploration stats
            total_cells = self.grid_size * self.grid_size
            explored_cells = sum(row.count(0) + row.count(1) for row in belief_state)
            explored_percent = (explored_cells / total_cells) * 100
            
            # Update stats label
            if self.stats_label and self.stats_label.winfo_exists():
                self.stats_label.configure(
                    text=f"Đã khám phá: {explored_percent:.1f}% | Chưa khám phá: {100-explored_percent:.1f}%"
                )
            
            # Draw grid
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    try:
                        if belief_state[y][x] == -1:  # Unexplored
                            fill_color = "#1a1a1a"
                            outline_color = "#333333"
                        else:  # Explored
                            if maze[y][x] == 1:  # Wall
                                fill_color = "#4a4a4a"
                                outline_color = "#666666"
                            else:  # Path
                                fill_color = "#00ff00"
                                outline_color = "#00cc00"
                        
                        self.canvas.create_rectangle(
                            x * self.cell_size, 
                            y * self.cell_size,
                            (x + 1) * self.cell_size, 
                            (y + 1) * self.cell_size,
                            fill=fill_color,
                            outline=outline_color
                        )
                    except TclError:
                        return
            
            # Mark start and end
            try:
                self.canvas.create_rectangle(
                    0, 0, self.cell_size, self.cell_size,
                    fill="#4caf50", outline="#2e7d32"
                )
                self.canvas.create_text(
                    self.cell_size/2, self.cell_size/2,
                    text="S", fill="white", font=("Arial", 12, "bold")
                )
                
                self.canvas.create_rectangle(
                    (self.grid_size-1) * self.cell_size,
                    (self.grid_size-1) * self.cell_size,
                    self.grid_size * self.cell_size,
                    self.grid_size * self.cell_size,
                    fill="#f44336", outline="#c62828"
                )
                self.canvas.create_text(
                    (self.grid_size-0.5) * self.cell_size,
                    (self.grid_size-0.5) * self.cell_size,
                    text="E", fill="white", font=("Arial", 12, "bold")
                )
            except TclError:
                return
                
        except Exception as e:
            print(f"Error updating radar view: {e}")
            return
    
    def show(self):
        """Show the radar window"""
        if not self.window:
            return
            
        try:
            if self.window.winfo_exists():
                self.window.deiconify()
                self.window.lift()
        except TclError as e:
            print(f"Error showing radar view: {e}")
    
    def hide(self):
        """Hide the radar window"""
        if not self.window:
            return
            
        try:
            if self.window.winfo_exists():
                self.window.withdraw()
        except TclError as e:
            print(f"Error hiding radar view: {e}")