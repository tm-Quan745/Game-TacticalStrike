![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)

## 🎮 Giới thiệu trò chơi Tactical Strike
Tactical Strike là một trò chơi thuộc thể loại Tower Defense (thủ thành chiến thuật), được phát triển bằng ngôn ngữ Python kết hợp với thư viện đồ họa Pygame và Tkinter. Trò chơi lấy cảm hứng từ các tựa game nổi tiếng như Plants vs. Zombies và Kingdom Rush, nơi người chơi có nhiệm vụ xây dựng các tháp phòng thủ để ngăn chặn từng đợt tấn công của kẻ địch đang tiến về căn cứ.

Kẻ địch sẽ di chuyển theo các lộ trình cụ thể, và người chơi cần vận dụng chiến thuật cùng tư duy logic để bố trí tháp hợp lý, tận dụng các tính năng như gây sát thương, làm chậm, hoặc tiêu diệt nhằm bảo vệ căn cứ an toàn.
## 🎯 Mục tiêu của trò chơi
Xây dựng trò chơi chiến thuật giải trí kết hợp tư duy, giúp người chơi vừa chơi vừa học thông qua việc tương tác với các yếu tố chiến thuật và trí tuệ nhân tạo; ứng dụng các thuật toán tìm kiếm trong AI như BFS, A*, Beam Search, Backtracking, Partial Observation, Q-Learning để mô phỏng hành vi di chuyển của kẻ địch.
## 🖥 Giao diện phần mềm
### Giao diện chính
### Tính năng
### 1. Thay đổi giao diện mê cung
### 2. Thay đổi đường đi mê cung
### 3. Xây tháp bắn
<p align="center">
  <img src="https://media.giphy.com/media/your-gif-link.gif" alt="Maze Change" />
</p>

## Các thuật toán áp dụng cho Enemy 
### 1. Uniformed Search
-	Thuật toán tìm kiếm theo chiều rộng, khám phá đồng thời tất cả các nút ở cùng một độ sâu trước khi đi sâu hơn
-	Sử dụng cấu trúc dữ liệu hàng đợi (queue) theo nguyên tắc FIFO (First In First Out)
-	Đảm bảo tìm được đường đi ngắn nhất trong mê cung không có trọng số

### 2. Informed Search
-	Thuật toán tìm đường đi kết hợp giữa Dijkstra và heuristic để tìm đường đi tối ưu
-	Sử dụng hàm f(n) = g(n) + h(n) để đánh giá các đường đi
-	Kết hợp chi phí thực tế g(n) và ước lượng chi phí heuristic h(n)
-	Hiệu quả hơn BFS nhờ khả năng dự đoán hướng đi

### 3. Local Search
-	Cải tiến của BFS nhằm giảm không gian tìm kiếm
-	Chỉ giữ lại k đường đi tốt nhất tại mỗi bước (beam width)
-	Sử dụng heuristic để đánh giá và chọn lọc đường đi tiềm năng
-	Cân bằng giữa tốc độ và chất lượng giải pháp

### 4. Partial Observation
Thuật toán Partial Observation Search là một biến thể của thuật toán A* được thiết kế để hoạt động trong môi trường chỉ được quan sát một phần. Thay vì biết toàn bộ bản đồ ngay từ đầu, agent chỉ có thể "nhìn thấy" một phần môi trường xung quanh nó trong một bán kính nhất định.

### 5. Constraint Satisfaction Problem
-	Cải tiến của BFS nhằm giảm không gian tìm kiếm
-	Chỉ giữ lại k đường đi tốt nhất tại mỗi bước (beam width)
-	Sử dụng heuristic để đánh giá và chọn lọc đường đi tiềm năng
-	Cân bằng giữa tốc độ và chất lượng giải pháp

### 6. Reinforcement Learning
Q-Learning là thuật toán học tăng cường, học từ trải nghiệm để tìm đường đi tối ưu. Thuật toán duy trì một bảng Q-table lưu trữ giá trị của mỗi hành động tại mỗi trạng thái, và cập nhật liên tục các giá trị này dựa trên phần thưởng nhận được.

## 🌓 So sánh hiệu năng thuật toán

| Thuật Toán         | Loại Tìm Kiếm        | Tính Chất Chính                               | Ưu Điểm                                              | Nhược Điểm                                              |
|--------------------|----------------------|------------------------------------------------|-------------------------------------------------------|----------------------------------------------------------|
| BFS                | Không có thông tin   | Duyệt theo chiều rộng                         | Tìm đường đi ngắn nhất, đơn giản                     | Tốn RAM, mở rộng nhiều node dư thừa                     |
| A*                 | Có thông tin (Heuristic) | Kết hợp chi phí thực tế + dự đoán          | Tối ưu, nhanh hơn BFS, tránh đường nguy hiểm        | Tốn bộ nhớ, phụ thuộc vào hàm heuristic                 |
| Beam Search        | Heuristic cắt tỉa     | Giữ lại `k` đường tốt nhất tại mỗi bước      | Nhanh, tiết kiệm bộ nhớ, phù hợp kẻ địch nhanh       | Không tối ưu, kết quả phụ thuộc beam width              |
| Partial Observation| Quan sát từng phần    | Agent chỉ thấy vùng xung quanh                | Mô phỏng thực tế, di chuyển tự nhiên                 | Có thể sai đường, tính toán chậm hơn                    |
| Backtracking       | Quay lui              | Duyệt từng đường có thể, quay lại nếu sai     | Đơn giản, dễ lập trình                                | Dễ lặp, không hiệu quả với mê cung lớn                  |
| Q-Learning         | Học tăng cường        | Học từ trải nghiệm qua nhiều lần thử          | Tự học, thích nghi môi trường                       | Cần huấn luyện lâu, phụ thuộc thiết kế reward           |



## 🛠 Thực thi phần mềm

Đảm bảo đã cài đặt ![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white) hoặc phiên bản mới hơn.

Cài đặt các thư viện cần thiết bằng lệnh: 
```bash
  pip install customtkinter
```
Chạy file main.py ở command line: 

```bash
  python main.py
```


## 📗 Tài liệu tham khảo

[1] Smith, J. (2018), Artificial Intelligence: Principles and Applications, Oxford University Press.

[2]	Russell, S. J., & Norvig, P. (2021), Artificial intelligence: A modern approach (4th ed.), Pearson.

[3] [Python Software Foundation. (2025). *Tkinter — Python interface to Tcl/Tk*. Python 3.13.3 documentation](https://docs.python.org/3/library/tkinter.html)

## 👤Thành viên

- Trần Minh Quận : https://github.com/tm-Quan745
- Lê Thị Thanh Tâm : https://github.com/ltaamlee
- Nguyễn Hoàng Thạch : https://github.com/Thach45

