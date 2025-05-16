# BÁO CÁO CUỐI KỲ AI - NHÓM 18

## 1. Mục tiêu
- Phát triển và triển khai các giải thuật tìm đường trong game chiến thuật
- Nghiên cứu cách áp dụng các loại thuật toán khác nhau trong không gian 2D
- Hiểu rõ đặc điểm và cách hoạt động của từng nhóm thuật toán

## 2. Nội dung

### 2.1. Thuật toán Tìm kiếm không có thông tin (Uninformed Search)

#### Thành phần chính của bài toán:

#### Breadth-First Search (BFS):
- Solution: Tìm đường đi ngắn nhất bằng cách khám phá tất cả các nút cùng độ sâu trước
- Đặc điểm:
  + Sử dụng queue để lưu trữ các đường đi cần khám phá
  + Đảm bảo tìm được đường đi ngắn nhất nếu tồn tại
  + Khám phá đều các hướng không phụ thuộc thông tin heuristic

### 2.2. Thuật toán Tìm kiếm có thông tin (Informed Search)

#### A* Search
- Thành phần:
  + Hàm heuristic: Manhattan distance (|x1-x2| + |y1-y2|)
  + f(n) = g(n) + h(n): tổng chi phí đã đi và ước lượng chi phí còn lại
- Solution: 
  + Sử dụng priority queue để luôn xét các nút có f_score thấp nhất trước
  + Kết hợp thông tin thực tế (chi phí đã đi) và dự đoán (heuristic)
  + Đảm bảo tìm được đường đi tối ưu nếu heuristic admissible

### 2.3. Thuật toán Tìm kiếm cục bộ (Local Search)

#### Beam Search
- Thành phần:
  + Beam width: số lượng đường đi được xét tại mỗi bước
  + Hàm đánh giá: Manhattan distance đến đích
- Solution:
  + Giới hạn không gian tìm kiếm bằng beam width
  + Chỉ giữ lại k đường đi tốt nhất tại mỗi bước
  + Tìm kiếm theo chiều rộng có giới hạn

### 2.4. Thuật toán Tìm kiếm ràng buộc (Constraint Search)

#### Backtracking
- Thành phần:
  + Ràng buộc: Không đi vào tường, không vượt biên
  + Không gian tìm kiếm: Cây các trạng thái hợp lệ
- Solution:
  + Thử từng hướng đi có thể
  + Quay lui khi gặp đường cụt
  + Lưu lại toàn bộ hành trình để phân tích

### 2.5. Thuật toán Học tăng cường (Reinforcement Learning)

#### Q-Learning
- Thành phần:
  + Q-table: Lưu giá trị Q(s,a) cho mỗi cặp trạng thái-hành động
  + Reward function: Phần thưởng cho mỗi hành động
  + Tham số học: learning rate, discount factor, epsilon
- Solution:
  + Học tương tác với môi trường qua nhiều episodes
  + Cập nhật Q-table dựa trên phương trình Bellman
  + Cân bằng giữa thăm dò và khai thác qua epsilon-greedy

## 3. Kết luận

### Kết quả đạt được:
1. **Về mặt thuật toán**:
   - Triển khai thành công 5 nhóm thuật toán tìm đường khác nhau
   - Hiểu rõ đặc điểm và phạm vi áp dụng của từng nhóm

2. **Về mặt ứng dụng**:
   - Tích hợp thành công vào game chiến thuật
   - Tạo được visualizer để theo dõi quá trình tìm đường

3. **Về mặt học thuật**:
   - Hiểu sâu về các nhóm thuật toán tìm kiếm khác nhau
   - Nắm được cách áp dụng machine learning vào bài toán tìm đường
   - Phân biệt được đặc điểm và ứng dụng của từng nhóm thuật toán
