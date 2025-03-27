# Thuật Toán BFS (Breadth-First Search)

## Giải Thích Thuật Toán
BFS là thuật toán tìm kiếm theo chiều rộng, khám phá tất cả các nút ở cùng một độ sâu trước khi đi sâu hơn.

## Cách Hoạt Động
1. Khởi tạo:
   - Tạo hàng đợi (queue) với đường đi ban đầu [start]
   - Tạo tập visited để đánh dấu các ô đã thăm
   - Điểm bắt đầu: (0, 0)
   - Điểm đích: (grid_size-1, grid_size-1)

2. Vòng lặp chính:
   - Lấy ra đường đi đầu tiên từ queue (FIFO)
   - Lấy vị trí hiện tại (điểm cuối của đường đi)
   - Nếu đến đích, trả về đường đi

3. Khám phá lân cận:
   - Kiểm tra 4 hướng (lên, phải, xuống, trái)
   - Với mỗi ô lân cận hợp lệ:
     * Trong phạm vi mê cung (0 ≤ x, y < grid_size)
     * Là ô trống (giá trị 0)
     * Chưa thăm (not in visited)
   - Thêm ô hợp lệ vào queue và đánh dấu đã thăm

## Ưu Điểm
- Tìm được đường đi ngắn nhất
- Khám phá đều theo từng lớp
- Phù hợp với mê cung có nhiều đường đi

## Nhược Điểm
- Tốn bộ nhớ do lưu nhiều đường đi
- Phải duyệt nhiều ô không cần thiết

## Độ Phức Tạp
- Thời gian: O(V + E) 
  * V là số ô trong mê cung
  * E là số cạnh có thể đi được
- Không gian: O(V)
  * Cần lưu trữ các đường đi trong queue
  * Cần lưu tập visited