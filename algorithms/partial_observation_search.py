import heapq
from typing import List, Tuple, Set, Dict
from radar_view import RadarView

class PartialObservationSearch:
    def __init__(self, grid_size: int, view_radius: int = 2):
        """
        Khởi tạo thuật toán tìm đường với quan sát từng phần.
        
        Tham số:
            grid_size: Kích thước của mê cung (giả định mê cung vuông)
            view_radius: Phạm vi quan sát xung quanh agent
        """
        self.grid_size = grid_size
        self.view_radius = view_radius
        self.belief_state = None
        self.reset_belief_state()
        self.radar_view = None

    def reset_belief_state(self):
        """Đặt lại trạng thái niềm tin về môi trường về trạng thái chưa biết."""
        # -1: Chưa biết, 0: Ô trống, 1: Tường
        self.belief_state = [[-1] * self.grid_size for _ in range(self.grid_size)]
        
    def update_observation(self, current_pos: Tuple[int, int], maze: List[List[int]]):
        """
        Cập nhật trạng thái niềm tin dựa trên quan sát hiện tại.
        
        Tham số:
            current_pos: Vị trí hiện tại (x, y)
            maze: Trạng thái thực tế của mê cung
        """
        x, y = current_pos
        for dy in range(-self.view_radius, self.view_radius + 1):
            for dx in range(-self.view_radius, self.view_radius + 1):
                new_x, new_y = x + dx, y + dy
                # Kiểm tra vị trí có nằm trong mê cung không
                if (0 <= new_x < self.grid_size and
                    0 <= new_y < self.grid_size and
                    abs(dx) + abs(dy) <= self.view_radius):  # Kiểm tra khoảng cách Manhattan
                    self.belief_state[new_y][new_x] = maze[new_y][new_x]
        
        # Cập nhật radar view nếu có
        if self.radar_view:
            self.radar_view.update_view(maze, self.belief_state)

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Tính khoảng cách Manhattan giữa hai điểm."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Lấy danh sách các ô kề có thể đi được."""
        x, y = pos
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.grid_size and 
                0 <= ny < self.grid_size and
                self.belief_state[ny][nx] != 1):  # Không phải tường đã biết
                neighbors.append((nx, ny))
        return neighbors

    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int], 
                 maze: List[List[int]]) -> List[Tuple[int, int]]:
        """
        Tìm đường đi sử dụng thuật toán A* với quan sát từng phần.
        
        Tham số:
            start: Vị trí bắt đầu (x, y)
            goal: Vị trí đích (x, y)
            maze: Mê cung thực tế để lấy thông tin quan sát
            
        Trả về:
            Danh sách các vị trí tạo thành đường đi, hoặc None nếu không tìm thấy đường
        """
        # Cập nhật quan sát ban đầu
        self.update_observation(start, maze)
        
        # Hàng đợi ưu tiên lưu (điểm f, điểm g, vị trí hiện tại, đường đi)
        queue = [(0, 0, start, [start])]
        visited = set()
        g_scores = {start: 0}
        
        while queue:
            f_score, g_score, current, path = heapq.heappop(queue)
            
            # Cập nhật quan sát tại vị trí hiện tại
            self.update_observation(current, maze)
            
            if current == goal:
                return path
                
            if current in visited:
                continue
                
            visited.add(current)
            
            for neighbor in self.get_neighbors(current):
                if neighbor in visited:
                    continue
                    
                new_g_score = g_score + 1
                
                if neighbor not in g_scores or new_g_score < g_scores[neighbor]:
                    g_scores[neighbor] = new_g_score
                    f_score = new_g_score + self.heuristic(neighbor, goal)
                    new_path = path + [neighbor]
                    heapq.heappush(queue, (f_score, new_g_score, neighbor, new_path))
        
        return None

    def get_belief_state(self) -> List[List[int]]:
        """Trả về trạng thái niềm tin hiện tại về môi trường."""
        return self.belief_state

def find_path_with_partial_observation(maze: List[List[int]], grid_size: int, 
                                    view_radius: int = 2) -> List[Tuple[int, int]]:
    """
    Hàm wrapper để tìm đường đi qua mê cung với quan sát từng phần.
    
    Tham số:
        maze: Mê cung đầy đủ
        grid_size: Kích thước mê cung
        view_radius: Bán kính quan sát
        
    Trả về:
        Danh sách các vị trí tạo thành đường đi, hoặc None nếu không tìm thấy đường
    """
    searcher = PartialObservationSearch(grid_size, view_radius)
    # Tạo radar view
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ gốc
    searcher.radar_view = RadarView(root, grid_size, 20)  # cell_size = 20
    searcher.radar_view.show()
    
    start = (0, 0)
    goal = (grid_size - 1, grid_size - 1)
    path = searcher.find_path(start, goal, maze)
    
    if path is None:
        searcher.radar_view.hide()
        root.destroy()
    
    return path