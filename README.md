# Các Thuật Toán Tìm Đường Trong Game Tower Defense

## 1. Thuật Toán BFS (Breadth-First Search)
### Trạng thái ban đầu:
- Điểm xuất phát: (0, 0)
- Điểm đích: (grid_size-1, grid_size-1)
- Hàng đợi (queue) chứa đường đi ban đầu [start]
- Tập visited chỉ chứa điểm xuất phát
- Tìm đường theo chiều rộng, khám phá tất cả các ô liền kề trước khi đi sâu hơn

### Trạng thái đích:
- Tìm được đường đi ngắn nhất từ điểm xuất phát đến đích
- Trả về danh sách các tọa độ tạo thành đường đi
- Nếu không tìm được đường đi, trả về None

## 2. Thuật Toán DFS (Depth-First Search)
### Trạng thái ban đầu:
- Điểm xuất phát: (0, 0)
- Điểm đích: (grid_size-1, grid_size-1)
- Ngăn xếp (stack) chứa đường đi ban đầu [start]
- Tập visited chỉ chứa điểm xuất phát
- Tìm đường theo chiều sâu, ưu tiên đi sâu vào một hướng trước

### Trạng thái đích:
- Tìm được một đường đi từ điểm xuất phát đến đích (không nhất thiết là ngắn nhất)
- Trả về danh sách các tọa độ tạo thành đường đi
- Nếu không tìm được đường đi, trả về None

## 3. Thuật Toán Dijkstra
### Trạng thái ban đầu:
- Điểm xuất phát: (0, 0)
- Điểm đích: (grid_size-1, grid_size-1)
- Hàng đợi ưu tiên chứa (chi_phí=0, vị_trí=start, đường_đi=[start])
- Tập visited rỗng
- Chi phí di chuyển giữa các ô liền kề là 1

### Trạng thái đích:
- Tìm được đường đi ngắn nhất từ điểm xuất phát đến đích dựa trên chi phí
- Trả về danh sách các tọa độ tạo thành đường đi có tổng chi phí nhỏ nhất
- Nếu không tìm được đường đi, trả về None

## 4. Thuật Toán A* (A-Star)
### Trạng thái ban đầu:
- Điểm xuất phát: (0, 0)
- Điểm đích: (grid_size-1, grid_size-1)
- Hàng đợi ưu tiên chứa (f_score, g_score=0, vị_trí=start, đường_đi=[start])
- f_score = g_score + heuristic (Manhattan distance)
- Tập visited rỗng
- Sử dụng heuristic là khoảng cách Manhattan đến đích

### Trạng thái đích:
- Tìm được đường đi tốt nhất từ điểm xuất phát đến đích
- Trả về danh sách các tọa độ tạo thành đường đi tối ưu
- Nếu không tìm được đường đi, trả về None

## Đặc Điểm Chung
- Tất cả các thuật toán đều:
  * Chỉ có thể di chuyển theo 4 hướng (lên, xuống, trái, phải)
  * Chỉ có thể đi qua các ô trống (giá trị 0 trong mê cung)
  * Không đi qua các ô đã đi qua (tránh lặp vô hạn)
  * Kiểm tra giới hạn của mê cung (0 ≤ x, y < grid_size)

## Chi Phí Thuật Toán

### 1. BFS (Breadth-First Search)
- **Độ phức tạp thời gian:** O(V + E)
  * V: số lượng ô trong mê cung (grid_size * grid_size)
  * E: số lượng cạnh có thể đi được giữa các ô
- **Độ phức tạp không gian:** O(V)
  * Cần lưu trữ hàng đợi và tập visited
- **Ưu điểm:** Tìm được đường đi ngắn nhất
- **Nhược điểm:** Tốn nhiều bộ nhớ do phải lưu tất cả các trạng thái

### 2. DFS (Depth-First Search)
- **Độ phức tạp thời gian:** O(V + E)
  * V: số lượng ô trong mê cung
  * E: số lượng cạnh có thể đi được
- **Độ phức tạp không gian:** O(H)
  * H: độ sâu tối đa của đường đi
  * Thường tốt hơn BFS về mặt bộ nhớ
- **Ưu điểm:** Tốn ít bộ nhớ hơn BFS
- **Nhược điểm:** Không đảm bảo tìm được đường đi ngắn nhất

### 3. Dijkstra
- **Độ phức tạp thời gian:** O((V + E) * log V)
  * Do sử dụng hàng đợi ưu tiên (priority queue)
- **Độ phức tạp không gian:** O(V)
  * Cần lưu trữ khoảng cách và đường đi
- **Ưu điểm:** Tìm được đường đi ngắn nhất, xử lý tốt với chi phí khác nhau
- **Nhược điểm:** Chậm hơn BFS khi tất cả các cạnh có chi phí bằng nhau

### 4. A* (A-Star)
- **Độ phức tạp thời gian:** O((V + E) * log V)
  * Tương tự Dijkstra nhưng thường nhanh hơn trong thực tế
- **Độ phức tạp không gian:** O(V)
  * Cần lưu trữ f_score, g_score và đường đi
- **Ưu điểm:** Thường tìm đường nhanh hơn Dijkstra nhờ heuristic
- **Nhược điểm:** Phụ thuộc vào chất lượng của hàm heuristic

## So Sánh Chi Phí
1. **Chi phí thấp nhất:** DFS (về mặt bộ nhớ)
2. **Cân bằng nhất:** BFS (thời gian và bộ nhớ tương đối, đảm bảo đường đi ngắn nhất)
3. **Thông minh nhất:** A* (hiệu quả trong thực tế nhờ heuristic)
4. **Linh hoạt nhất:** Dijkstra (tốt cho mê cung có chi phí di chuyển khác nhau)
