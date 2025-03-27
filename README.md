# Các Thuật Toán Tìm Đường Trong Game Tower Defense

## Cấu Trúc Project

### Thư Mục algorithms/
Chứa các file cài đặt thuật toán và tài liệu chi tiết:

1. **BFS (Breadth-First Search)**
   - Code: `algorithms/bfs.py`
   - Tài liệu: `algorithms/bfs_readme.md`
   - Tìm đường ngắn nhất bằng cách duyệt theo chiều rộng

2. **DFS (Depth-First Search)**
   - Code: `algorithms/dfs.py`
   - Tài liệu: `algorithms/dfs_readme.md`
   - Tìm đường bằng cách duyệt theo chiều sâu

3. **Dijkstra**
   - Code: `algorithms/dijkstra.py`
   - Tài liệu: `algorithms/dijkstra_readme.md`
   - Tìm đường ngắn nhất dựa trên chi phí di chuyển

4. **A* (A-Star)**
   - Code: `algorithms/astar.py`
   - Tài liệu: `algorithms/astar_readme.md`
   - Tìm đường thông minh kết hợp chi phí và heuristic

### File Chính
- `pathfinding.py`: File điều phối các thuật toán
- `game_logic.py`: Xử lý logic game chính
- `ui.py`: Giao diện người dùng
- `entities.py`: Định nghĩa các đối tượng trong game
- `maze_generator.py`: Tạo mê cung ngẫu nhiên

## Tổng Quan Thuật Toán

### 1. BFS (Breadth-First Search)
- Đặc điểm: Tìm đường theo chiều rộng
- Độ phức tạp thời gian: O(V + E)
- Chi tiết: Xem `algorithms/bfs_readme.md`

### 2. DFS (Depth-First Search)
- Đặc điểm: Tìm đường theo chiều sâu
- Độ phức tạp không gian: O(H)
- Chi tiết: Xem `algorithms/dfs_readme.md`

### 3. Dijkstra
- Đặc điểm: Tìm đường dựa trên chi phí
- Độ phức tạp: O((V + E) * log V)
- Chi tiết: Xem `algorithms/dijkstra_readme.md`

### 4. A* (A-Star)
- Đặc điểm: Kết hợp chi phí và heuristic
- Hiệu quả nhất trong thực tế
- Chi tiết: Xem `algorithms/astar_readme.md`

## Đặc Điểm Chung
- Tất cả các thuật toán đều:
  * Chỉ có thể di chuyển theo 4 hướng (lên, xuống, trái, phải)
  * Chỉ có thể đi qua các ô trống (giá trị 0 trong mê cung)
  * Không đi qua các ô đã đi qua (tránh lặp vô hạn)
  * Kiểm tra giới hạn của mê cung (0 ≤ x, y < grid_size)

## Thực Hiện
- Mỗi thuật toán được tách thành file riêng để dễ quản lý
- File readme riêng giải thích chi tiết từng thuật toán
- Có thể dễ dàng thêm thuật toán mới vào hệ thống
- Cấu trúc module hóa giúp dễ bảo trì và nâng cấp

## So Sánh Chi Phí
1. **Chi phí thấp nhất:** DFS (về mặt bộ nhớ)
2. **Cân bằng nhất:** BFS (đảm bảo đường đi ngắn nhất)
3. **Thông minh nhất:** A* (hiệu quả trong thực tế)
4. **Linh hoạt nhất:** Dijkstra (tốt với chi phí khác nhau)

Chi tiết về cài đặt, ưu nhược điểm và độ phức tạp của mỗi thuật toán có thể được tìm thấy trong file readme tương ứng trong thư mục algorithms/.
