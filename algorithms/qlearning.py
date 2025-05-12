import numpy as np
import random
import json

class QLearningPathFinder:
    def __init__(self, maze, grid_size):
        self.maze = maze
        self.grid_size = grid_size
        self.q_table = {}
        self.learning_rate = 0.1
        self.gamma = 0.95
        self.epsilon = 1.0
        self.episodes = 2000
        
    def get_state(self, pos):
        """Lấy state hiện tại"""
        return (pos[0], pos[1])
        
    def get_valid_moves(self, x, y):
        """Kiểm tra các hướng đi hợp lệ từ vị trí x,y"""
        valid_moves = []
        possible_moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left
        
        for i, (dx, dy) in enumerate(possible_moves):
            new_x, new_y = x + dx, y + dy
            # Kiểm tra biên và tường
            if (0 <= new_x < self.grid_size and
                0 <= new_y < self.grid_size and
                self.maze[new_y][new_x] != 1):
                valid_moves.append(i)  # Lưu index của hướng đi hợp lệ
                
        return valid_moves
        
    def get_actions(self, state):
        """Lấy các action có thể thực hiện được"""
        x, y = state
        valid_indices = self.get_valid_moves(x, y)
        actions = []
        possible_moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        
        for i in valid_indices:
            actions.append(possible_moves[i])
        return actions
        
    def get_reward(self, state, action, next_state):
        """Tính reward cho mỗi action"""
        # Đạt đích - phần thưởng lớn nhất
        if next_state == (self.grid_size-1, self.grid_size-1):
            return 1000
            
        # Tính khoảng cách Manhattan đến đích
        goal_x = goal_y = self.grid_size - 1
        old_dist = abs(goal_x - state[0]) + abs(goal_y - state[1])
        new_dist = abs(goal_x - next_state[0]) + abs(goal_y - next_state[1])
        
        # Phần thưởng dựa trên tiến triển
        if new_dist < old_dist:
            # Khuyến khích đi theo đường thẳng/chéo về đích
            dx = abs(next_state[0] - state[0])
            dy = abs(next_state[1] - state[1])
            if dx + dy == 1:  # Đi thẳng
                return 50
            return 20  # Đi gần đích hơn
        elif new_dist > old_dist:
            return -50  # Phạt nặng nếu đi xa đích
            
        # Phạt nhẹ cho việc đứng yên hoặc đi quanh quẩn
        if next_state == state:
            return -100
            
        return -1  # Chi phí di chuyển cơ bản
        
    def train(self):
        print("Đang huấn luyện Q-learning cho map hiện tại...")
        
        for episode in range(self.episodes):
            state = (0, 0)  # Start
            total_reward = 0
            
            while state != (self.grid_size-1, self.grid_size-1):
                # Khởi tạo Q-values
                if str(state) not in self.q_table:
                    self.q_table[str(state)] = [0] * 4  # 4 hướng đi
                    # Set giá trị âm lớn cho các hướng không đi được
                    valid_moves = self.get_valid_moves(state[0], state[1])
                    for i in range(4):
                        if i not in valid_moves:
                            self.q_table[str(state)][i] = float('-inf')
                
                # Lấy các action có thể từ state hiện tại
                actions = self.get_actions(state)
                if not actions:
                    break
                
                # Epsilon-greedy
                if random.random() < self.epsilon:
                    action = random.choice(actions)
                else:
                    # Chọn action từ các hướng đi hợp lệ
                    valid_moves = self.get_valid_moves(state[0], state[1])
                    if valid_moves:  # Nếu có hướng đi hợp lệ
                        action_idx = max(valid_moves, key=lambda i: self.q_table[str(state)][i])
                        action = [(0, -1), (1, 0), (0, 1), (-1, 0)][action_idx]
                    else:
                        action = random.choice(actions)  # Fallback nếu không có hướng hợp lệ
                
                # Thực hiện action
                next_state = (state[0] + action[0], state[1] + action[1])
                reward = self.get_reward(state, action, next_state)
                total_reward += reward
                
                # Cập nhật Q-table
                if str(next_state) not in self.q_table:
                    self.q_table[str(next_state)] = [0] * 4
                
                action_idx = [(0, -1), (1, 0), (0, 1), (-1, 0)].index(action)
                next_max = max(self.q_table[str(next_state)])
                
                self.q_table[str(state)][action_idx] = (1 - self.learning_rate) * \
                    self.q_table[str(state)][action_idx] + \
                    self.learning_rate * (reward + self.gamma * next_max)
                
                state = next_state
                
            # Giảm epsilon
            self.epsilon = max(0.01, self.epsilon * 0.995)
            
            if episode % 100 == 0:
                print(f"Episode {episode}/{self.episodes}, Total Reward: {total_reward}")
                
        print("Huấn luyện hoàn tất!")
        self.save_and_display_qtable()
        self.visualize_path()
        
    def visualize_path(self):
        """Hiển thị đường đi của quân địch dựa trên Q-table"""
        import tkinter as tk
        
        window = tk.Toplevel()
        window.title("Q-Learning Path Visualization")
        
        # Tạo canvas để vẽ path
        cell_size = 30
        canvas = tk.Canvas(window,
                         width=self.grid_size*cell_size,
                         height=self.grid_size*cell_size)
        canvas.pack()
        
        # Vẽ ma trận
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                x1 = x * cell_size
                y1 = y * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                # Vẽ nền cho từng ô
                if self.maze[y][x] == 1:  # Tường
                    canvas.create_rectangle(x1, y1, x2, y2, fill='gray')
                else:  # Đường đi
                    canvas.create_rectangle(x1, y1, x2, y2, fill='white')
                    
                # Vẽ lưới
                canvas.create_rectangle(x1, y1, x2, y2, outline='black')
        
        # Tìm và vẽ đường đi từ Q-table
        current = (0, 0)
        path = [current]
        
        while current != (self.grid_size-1, self.grid_size-1):
            if str(current) not in self.q_table:
                break
                
            # Tìm hướng đi tốt nhất
            valid_moves = self.get_valid_moves(current[0], current[1])
            if not valid_moves:
                break
                
            q_values = self.q_table[str(current)]
            best_move_idx = max(valid_moves, key=lambda i: q_values[i])
            
            # Di chuyển đến vị trí mới
            moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
            dx, dy = moves[best_move_idx]
            current = (current[0] + dx, current[1] + dy)
            path.append(current)
            
            # Tránh lặp vô tận
            if len(path) > self.grid_size * self.grid_size:
                break
        
        # Vẽ đường đi
        for i in range(len(path)-1):
            x1 = path[i][0] * cell_size + cell_size/2
            y1 = path[i][1] * cell_size + cell_size/2
            x2 = path[i+1][0] * cell_size + cell_size/2
            y2 = path[i+1][1] * cell_size + cell_size/2
            
            # Vẽ mũi tên chỉ hướng đi
            canvas.create_line(x1, y1, x2, y2, fill='red', width=2, arrow=tk.LAST)
            # Đánh số thứ tự các bước
            canvas.create_text(x1, y1, text=str(i), fill='blue')
            
        if len(path) > 1:
            # Đánh dấu điểm cuối cùng
            last_x = path[-1][0] * cell_size + cell_size/2
            last_y = path[-1][1] * cell_size + cell_size/2
            canvas.create_text(last_x, last_y, text=str(len(path)-1), fill='blue')
        
    def save_and_display_qtable(self):
        """Lưu và hiển thị Q-table"""
        # Tạo cửa sổ mới để hiển thị Q-table
        import tkinter as tk
        from tkinter import ttk
        
        window = tk.Toplevel()
        window.title("Q-Learning Table")
        window.geometry("800x600")
        
        # Tạo Text widget để hiển thị Q-table
        text = tk.Text(window, wrap=tk.NONE)
        text.pack(expand=True, fill='both')
        
        # Tạo scrollbars
        v_scroll = ttk.Scrollbar(window, orient='vertical', command=text.yview)
        h_scroll = ttk.Scrollbar(window, orient='horizontal', command=text.xview)
        text.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        v_scroll.pack(side='right', fill='y')
        h_scroll.pack(side='bottom', fill='x')
        
        # Format và hiển thị Q-table
        text.insert('1.0', "Q-Learning Table:\n\n")
        for state in sorted(self.q_table.keys()):
            text.insert('end', f"State {state}:\n")
            values = self.q_table[state]
            move_names = ["Lên", "Phải", "Xuống", "Trái"]
            current_pos = eval(state)  # Convert string '(x, y)' to tuple
            text.insert('end', f"Vị trí ({current_pos[0]}, {current_pos[1]}):\n")
            
            # Lấy các hướng đi hợp lệ
            valid_moves = self.get_valid_moves(current_pos[0], current_pos[1])
            
            for i in range(4):
                if i in valid_moves:
                    if values[i] != float('-inf'):
                        text.insert('end', f"  Đi {move_names[i]}: {values[i]:.2f}\n")
                else:
                    text.insert('end', f"  Đi {move_names[i]}: [Tường]\n")
            text.insert('end', "\n")
            
        # Lưu vào file
        import time
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"qtable_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Q-Learning Table\n")
            f.write("===============\n\n")
            for state in sorted(self.q_table.keys()):
                f.write(f"State {state}:\n")
                values = self.q_table[state]
                current_pos = eval(state)
                f.write(f"Vị trí ({current_pos[0]}, {current_pos[1]}):\n")
                
                valid_moves = self.get_valid_moves(current_pos[0], current_pos[1])
                for i in range(4):
                    if i in valid_moves:
                        if values[i] != float('-inf'):
                            f.write(f"  Đi {move_names[i]}: {values[i]:.2f}\n")
                    else:
                        f.write(f"  Đi {move_names[i]}: [Tường]\n")
                f.write("\n")
                
        text.insert('end', f"\nĐã lưu Q-table vào file: {filename}")
        
    def find_path(self):
        """Tìm đường đi tối ưu dựa trên Q-table đã học"""
        path = [(0, 0)]
        current = (0, 0)
        
        while current != (self.grid_size-1, self.grid_size-1):
            if str(current) not in self.q_table:
                return None
                
            # Lấy các hướng đi hợp lệ
            valid_moves = self.get_valid_moves(current[0], current[1])
            if not valid_moves:
                return None
            
            # Chọn hướng đi tốt nhất từ các hướng hợp lệ
            best_move_idx = max(valid_moves,
                              key=lambda i: self.q_table[str(current)][i])
            
            # Chuyển đổi index thành vector di chuyển
            possible_moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
            dx, dy = possible_moves[best_move_idx]
            
            # Di chuyển
            new_x = current[0] + dx
            new_y = current[1] + dy
            current = (new_x, new_y)
            path.append(current)
            
            # Tránh lặp vô tận
            if len(path) > self.grid_size * self.grid_size:
                return None
            
        return path

def qlearning_find_path(maze, grid_size):
    finder = QLearningPathFinder(maze, grid_size)
    finder.train()  # Train trên map hiện tại
    return finder.find_path()