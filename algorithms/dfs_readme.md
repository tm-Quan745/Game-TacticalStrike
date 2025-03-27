# Thuật Toán DFS (Depth-First Search)

## Giải Thích Thuật Toán
DFS là thuật toán tìm kiếm theo chiều sâu, ưu tiên khám phá càng sâu càng tốt theo một nhánh trước khi quay lui.

## Cách Hoạt Động
1. Khởi tạo:
   - Tạo ngăn xếp (stack) với đường đi ban đầu [start]
   - Tạo tập visited để đánh dấu các ô đã thăm
   - Điểm bắt đầu: (0, 0)
   - Điểm đích: (grid_size-1, grid_size-1)

2. Vòng lặp chính:
   - Lấy ra đường đi cuối cùng từ stack (LIFO)
   - Lấy vị trí hiện tại (điểm cuối của đường đi)
   - Nếu đến đích, trả về đường đi

3. Khám phá lân cận:
   - Kiểm tra 4 hướng (lên, phải, xuống, trái)
   - Với mỗi ô lân cận hợp lệ:
     * Trong phạm vi mê cung (0 ≤ x, y < grid_size)
     * Là ô trống (giá trị 0)
     * Chưa thăm (not in visited)
   - Thêm ô hợp lệ vào stack và đánh dấu đã thăm

## Đặc Điểm Quan Trọng
- Sử dụng LIFO (Last In First Out)
- Đi sâu vào một nhánh trước khi thử nhánh khác
- Sử dụng đệ quy tự nhiên hoặc stack để lưu trữ

## Ưu Điểm
- Tốn ít bộ nhớ hơn BFS
- Tốt cho mê cung có ít nhánh rẽ
- Dễ cài đặt với đệ quy

## Nhược Điểm
- Không đảm bảo đường đi ngắn nhất
- Có thể bị mắc kẹt trong nhánh sâu
- Không hiệu quả với mê cung rộng

## Độ Phức Tạp
- Thời gian: O(V + E)
  * V là số ô trong mê cung
  * E là số cạnh có thể đi được
- Không gian: O(H)
  * H là độ sâu tối đa của đường đi
  * Thường tốt hơn BFS về mặt bộ nhớ

## So Sánh với BFS
- BFS tìm đường ngắn nhất, DFS không đảm bảo
- DFS tiêu tốn ít bộ nhớ hơn BFS
- BFS khám phá theo lớp, DFS khám phá theo nhánh
- DFS có thể tìm đường nhanh hơn trong một số trường hợp đặc biệt