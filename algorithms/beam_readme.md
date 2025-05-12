## Thuật Toán Beam Search

### Giải Thích Thuật Toán
Beam Search là thuật toán tìm kiếm theo chiều rộng nhưng giới hạn số lượng các lựa chọn tốt nhất ở mỗi bước, thay vì mở rộng tất cả các nhánh.

### Cách Hoạt Động
1. **Khởi tạo**:
   - Tạo một danh sách các đường đi khả thi ban đầu.
   - Đặt giới hạn beam (k) – số lượng nhánh con tốt nhất cần giữ lại ở mỗi bước.
   - Điểm bắt đầu: (0, 0).
   - Điểm đích: (grid_size-1, grid_size-1).

2. **Vòng lặp chính**:
   - Khám phá các ô lân cận và đánh giá bằng hàm heuristic.
   - Lọc các đường đi tốt nhất dựa trên giá trị của hàm đánh giá.
   - Giới hạn số lượng các đường đi trong beam (chỉ giữ lại k đường đi tốt nhất).

3. **Đến đích**:
   - Nếu một trong các đường đi đạt đến đích, thuật toán dừng lại và trả về đường đi.

### Ưu Điểm
- Tìm kiếm hiệu quả hơn so với BFS khi không cần khám phá toàn bộ không gian trạng thái.
- Giảm thiểu độ phức tạp tính toán bằng cách giữ lại chỉ một số lượng hạn chế các lựa chọn.
- Dễ dàng điều chỉnh với tham số beam để kiểm soát độ sâu và chi phí bộ nhớ.

### Nhược Điểm
- Không đảm bảo tìm được đường đi ngắn nhất.
- Phụ thuộc vào hàm đánh giá, nếu hàm không tốt, thuật toán có thể dẫn đến kết quả không chính xác.

### Độ Phức Tạp
- Thời gian: O(k * E).
- Không gian: O(k * V).
