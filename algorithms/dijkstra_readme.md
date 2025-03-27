# Thuật Toán Dijkstra

## Giải Thích Thuật Toán
Dijkstra là thuật toán tìm đường đi ngắn nhất dựa trên chi phí di chuyển giữa các điểm. Trong trường hợp mê cung, chi phí di chuyển giữa các ô liền kề là 1.

## Cách Hoạt Động
1. Khởi tạo:
   - Tạo hàng đợi ưu tiên (priority queue) với (chi_phí=0, vị_trí=start, đường_đi=[start])
   - Tạo tập visited để đánh dấu các ô đã thăm
   - Điểm bắt đầu: (0, 0)
   - Điểm đích: (grid_size-1, grid_size-1)

2. Vòng lặp chính:
   - Lấy ra đường đi có chi phí thấp nhất từ priority queue
   - Kiểm tra nếu đã đến đích
   - Bỏ qua nếu đã thăm vị trí này
   - Đánh dấu vị trí hiện tại đã thăm

3. Khám phá lân cận:
   - Kiểm tra 4 hướng (lên, phải, xuống, trái)
   - Với mỗi ô lân cận hợp lệ:
     * Trong phạm vi mê cung (0 ≤ x, y < grid_size)
     * Là ô trống (giá trị 0)
     * Chưa thăm (not in visited)
   - Tính chi phí mới = chi phí hiện tại + 1
   - Thêm vào priority queue với chi phí mới

## Đặc Điểm Quan Trọng
- Sử dụng priority queue để luôn xét đường đi có chi phí thấp nhất trước
- Đảm bảo tìm được đường đi ngắn nhất
- Có thể mở rộng để xử lý chi phí di chuyển khác nhau

## Ưu Điểm
- Tìm được đường đi ngắn nhất
- Hiệu quả với mê cung có chi phí di chuyển khác nhau
- Có thể tối ưu hóa cho nhiều loại chi phí khác nhau

## Nhược Điểm
- Chậm hơn BFS khi tất cả các cạnh có chi phí bằng nhau
- Tốn bộ nhớ để lưu chi phí và priority queue
- Phức tạp hơn BFS và DFS trong cài đặt

## Độ Phức Tạp
- Thời gian: O((V + E) * log V)
  * V là số ô trong mê cung
  * E là số cạnh có thể đi được
  * log V do sử dụng priority queue
- Không gian: O(V)
  * Cần lưu trữ chi phí và đường đi
  * Cần lưu priority queue

## So Sánh với BFS/DFS
- Dijkstra tổng quát hơn BFS, có thể xử lý chi phí khác nhau
- BFS là trường hợp đặc biệt của Dijkstra khi mọi chi phí bằng nhau
- Dijkstra chậm hơn BFS trong mê cung đơn giản
- Dijkstra đảm bảo đường đi ngắn nhất như BFS
- Dijkstra tốn nhiều bộ nhớ hơn DFS