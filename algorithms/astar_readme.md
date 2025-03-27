# Thuật Toán A* (A-Star)

## Giải Thích Thuật Toán
A* là thuật toán tìm đường đi kết hợp giữa Dijkstra và heuristic để tìm đường đi tối ưu. Thuật toán sử dụng hàm f(n) = g(n) + h(n) để đánh giá các đường đi.

## Các Thành Phần Chính
- g(n): Chi phí thực tế từ điểm xuất phát đến điểm hiện tại
- h(n): Ước lượng chi phí từ điểm hiện tại đến đích (heuristic)
- f(n): Tổng chi phí ước tính của đường đi qua điểm hiện tại

## Cách Hoạt Động
1. Khởi tạo:
   - Tạo hàng đợi ưu tiên với (f_score, g_score=0, vị_trí=start, đường_đi=[start])
   - Tạo tập visited để đánh dấu các ô đã thăm
   - Điểm bắt đầu: (0, 0)
   - Điểm đích: (grid_size-1, grid_size-1)
   - Tính h(start) bằng khoảng cách Manhattan

2. Vòng lặp chính:
   - Lấy ra điểm có f_score thấp nhất từ priority queue
   - Kiểm tra nếu đã đến đích
   - Bỏ qua nếu đã thăm vị trí này
   - Đánh dấu vị trí hiện tại đã thăm

3. Khám phá lân cận:
   - Kiểm tra 4 hướng (lên, phải, xuống, trái)
   - Với mỗi ô lân cận hợp lệ:
     * Trong phạm vi mê cung (0 ≤ x, y < grid_size)
     * Là ô trống (giá trị 0)
     * Chưa thăm (not in visited)
   - Tính:
     * g_score mới = g_score hiện tại + 1
     * h_score = khoảng cách Manhattan đến đích
     * f_score = g_score mới + h_score
   - Thêm vào priority queue

## Hàm Heuristic
- Sử dụng khoảng cách Manhattan: |x1 - x2| + |y1 - y2|
- Không được ước lượng cao hơn chi phí thực tế
- Càng chính xác càng hiệu quả
- Phải nhanh để tính toán

## Ưu Điểm
- Thường tìm đường nhanh hơn Dijkstra nhờ heuristic
- Đảm bảo tìm được đường đi tối ưu
- Khám phá ít ô hơn Dijkstra và BFS
- Hiệu quả với mê cung lớn

## Nhược Điểm
- Phụ thuộc vào chất lượng của hàm heuristic
- Phức tạp trong cài đặt
- Tốn bộ nhớ để lưu f_score và g_score

## Độ Phức Tạp
- Thời gian: O((V + E) * log V)
  * V là số ô trong mê cung
  * E là số cạnh có thể đi được
  * Thường nhanh hơn Dijkstra trong thực tế
- Không gian: O(V)
  * Cần lưu trữ f_score, g_score và đường đi

## So Sánh với Các Thuật Toán Khác
1. So với BFS:
   - A* thông minh hơn trong việc chọn hướng đi
   - A* thường khám phá ít ô hơn
   - Cả hai đều đảm bảo đường đi tối ưu

2. So với DFS:
   - A* đảm bảo đường đi tối ưu, DFS không
   - A* tốn nhiều bộ nhớ hơn
   - A* có tính dự đoán hơn

3. So với Dijkstra:
   - A* sử dụng thêm thông tin heuristic
   - A* thường tìm đường nhanh hơn
   - Cả hai đều đảm bảo đường đi tối ưu
   - A* là phiên bản thông minh hơn của Dijkstra

## Ứng Dụng Thực Tế
- Game và trò chơi điện tử
- Hệ thống định tuyến GPS
- Robot tự hành
- Lập kế hoạch đường đi cho AI