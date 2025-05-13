import tkinter as tk
from customtkinter import CTkToplevel, CTkFrame, CTkLabel

class RadarWindow:
    def __init__(self, parent, grid_size, cell_size):
        self.window = CTkToplevel(parent)
        self.window.title("Radar View - Partial Observation")
        self.window.geometry("600x600")
        self.window.attributes('-topmost', True)  # Luôn hiển thị trên cùng
        
        self.grid_size = grid_size
        self.cell_size = cell_size
        
        # Frame chứa canvas
        self.frame = CTkFrame(self.window)
        self.frame.pack(padx=10, pady=10)

        # Canvas để vẽ radar (sử dụng tk.Canvas vì nó ổn định hơn cho việc vẽ)
        self.canvas = tk.Canvas(
            self.frame,
            width=self.grid_size*self.cell_size,
            height=self.grid_size*self.cell_size,
            bg="#1a1a1a",  # Nền tối
            highlightthickness=2,
            highlightbackground="#333333"
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Label thông tin
        self.info_label = CTkLabel(
            self.window,
            text="Vùng tối: Chưa khám phá | Vùng sáng: Đã khám phá",
            font=("Arial", 12)
        )
        self.info_label.pack(pady=5)
        
        # Belief state for radar view
        self.belief_state = [[-1 for _ in range(grid_size)] for _ in range(grid_size)]
        
    def update_view(self, maze, belief_state):
        """Cập nhật hiển thị radar với belief state mới"""
        self.belief_state = belief_state
        self.draw_radar(maze)
        
    def draw_radar(self, maze):
        """Vẽ mê cung với vùng sáng/tối dựa trên belief state"""
        self.canvas.delete("all")
        
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                # Vẽ các ô với màu sắc phù hợp
                if self.belief_state[y][x] == -1:  # Chưa khám phá
                    fill_color = "#1a1a1a"  # Tối đen
                    outline_color = "#333333"
                else:  # Đã khám phá
                    if maze[y][x] == 1:  # Tường
                        fill_color = "#4a4a4a"  # Xám đậm
                        outline_color = "#666666"
                    else:  # Đường đi
                        fill_color = "#00ff00"  # Xanh sáng
                        outline_color = "#00cc00"
                
                self.canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill=fill_color, outline=outline_color
                )
        
        # Đánh dấu điểm bắt đầu và kết thúc
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
    
    def show(self):
        """Hiển thị cửa sổ radar"""
        self.window.deiconify()
        self.window.lift()  # Đưa cửa sổ lên trên cùng
    
    def hide(self):
        """Ẩn cửa sổ radar"""
        self.window.withdraw()