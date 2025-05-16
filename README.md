<p align="center">
  <img src="https://raw.githubusercontent.com/tm-Quan745/Game-TacticalStrike/Develop/readme_img/logo.png" alt="Logo" width="180"/>
</p>


## 🎮 Giới thiệu trò chơi Tactical Strike
Tactical Strike là một trò chơi thuộc thể loại Tower Defense (thủ thành chiến thuật), được phát triển bằng ngôn ngữ Python kết hợp với thư viện đồ họa Pygame và Tkinter. Trò chơi lấy cảm hứng từ các tựa game nổi tiếng như Plants vs. Zombies và Kingdom Rush, nơi người chơi có nhiệm vụ xây dựng các tháp phòng thủ để ngăn chặn từng đợt tấn công của kẻ địch đang tiến về căn cứ.

Kẻ địch sẽ di chuyển theo các lộ trình cụ thể và người chơi cần vận dụng chiến thuật cùng tư duy logic để bố trí tháp hợp lý, tận dụng các tính năng như gây sát thương, làm chậm hoặc tiêu diệt nhằm bảo vệ căn cứ an toàn.
## 🎯 Mục tiêu của trò chơi
Xây dựng trò chơi chiến thuật giải trí kết hợp tư duy, giúp người chơi vừa chơi vừa học thông qua việc tương tác với các yếu tố chiến thuật và trí tuệ nhân tạo; ứng dụng các thuật toán tìm kiếm trong AI như BFS, A*, Beam Search, Backtracking, Partial Observation, Q-Learning để mô phỏng hành vi di chuyển của kẻ địch.
## 🖥 Giao diện phần mềm
### Giao diện mở đầu

<p align="center">
  <img src="https://raw.githubusercontent.com/tm-Quan745/Game-TacticalStrike/Develop/readme_img/intro.gif" alt="Intro" />
</p>

### Giao diện chính

<p align="center">
  <img src="https://raw.githubusercontent.com/tm-Quan745/Game-TacticalStrike/Develop/readme_img/main.png" alt="Main Game" />
</p>

### Tính năng
### 1. Thay đổi giao diện mê cung

<p align="center">
  <img src="https://raw.githubusercontent.com/tm-Quan745/Game-TacticalStrike/Develop/readme_img/maze_change.gif" alt="Maze Change" />
</p>

### 2. Thay đổi đường đi mê cung

<p align="center">
  <img src="https://raw.githubusercontent.com/tm-Quan745/Game-TacticalStrike/Develop/readme_img/random.gif" alt="Random Maze" />
</p>

### 3. Xây tháp bắn

<p align="center">
  <img src="https://raw.githubusercontent.com/tm-Quan745/Game-TacticalStrike/Develop/readme_img/tower.gif" alt="Tower" />
</p>

### 4. Kẻ địch tấn công và tháp phòng thủ
- Khi kẻ địch ở trong phạm vi tầm bắn của tháp, tháp sẽ tấn công và làm giảm lượng máu của kẻ địch.

- Nếu tháp trong vùng cận chiến thì kẻ địch sẽ tiến hành tấn công vào tháp

<p align="center">
  <img src="https://raw.githubusercontent.com/tm-Quan745/Game-TacticalStrike/Develop/readme_img/shot.gif" alt="Shot" />
</p>



## Các thuật toán áp dụng cho Enemy 
### 1. Uniformed Search : BFS
-	Thuật toán tìm kiếm theo chiều rộng, khám phá đồng thời tất cả các nút ở cùng một độ sâu trước khi đi sâu hơn
-	Sử dụng cấu trúc dữ liệu hàng đợi (queue) theo nguyên tắc FIFO (First In First Out)
-	Đảm bảo tìm được đường đi ngắn nhất trong mê cung không có trọng số

<p align="center">
  <img src="https://raw.githubusercontent.com/tm-Quan745/Game-TacticalStrike/Develop/readme_img/bfs.gif" alt="BFS" />
</p>

### 2. Informed Search : A*
-	Thuật toán tìm đường đi kết hợp giữa Dijkstra và heuristic để tìm đường đi tối ưu
-	Sử dụng hàm f(n) = g(n) + h(n) để đánh giá các đường đi
-	Kết hợp chi phí thực tế g(n) và ước lượng chi phí heuristic h(n)
-	Hiệu quả hơn BFS nhờ khả năng dự đoán hướng đi

<p align="center">
  <img src="https://raw.githubusercontent.com/tm-Quan745/Game-TacticalStrike/Develop/readme_img/astar.gif" alt="A*" />
</p>

### 3. Local Search : Beam Search
-	Cải tiến của BFS nhằm giảm không gian tìm kiếm
-	Chỉ giữ lại k đường đi tốt nhất tại mỗi bước (beam width)
-	Sử dụng heuristic để đánh giá và chọn lọc đường đi tiềm năng
-	Cân bằng giữa tốc độ và chất lượng giải pháp

<p align="center">
  <img src="https://raw.githubusercontent.com/tm-Quan745/Game-TacticalStrike/Develop/readme_img/beam.gif" alt="Beam Search" />
</p>

### 4. Partial Observation
Thuật toán Partial Observation Search là một biến thể của thuật toán A* được thiết kế để hoạt động trong môi trường chỉ được quan sát một phần. Thay vì biết toàn bộ bản đồ ngay từ đầu, agent chỉ có thể "nhìn thấy" một phần môi trường xung quanh nó trong một bán kính nhất định.

<p align="center">
  <img src="https://raw.githubusercontent.com/tm-Quan745/Game-TacticalStrike/Develop/readme_img/partial.gif" alt="Partial Observation" />
</p>


### 5. Constraint Satisfaction Problem : Backtracking
-	Cải tiến của BFS nhằm giảm không gian tìm kiếm
-	Chỉ giữ lại k đường đi tốt nhất tại mỗi bước (beam width)
-	Sử dụng heuristic để đánh giá và chọn lọc đường đi tiềm năng
-	Cân bằng giữa tốc độ và chất lượng giải pháp

<p align="center">
  <img src="https://raw.githubusercontent.com/tm-Quan745/Game-TacticalStrike/Develop/readme_img/backtracking.gif" alt="Backtracking" />
</p>

### 6. Reinforcement Learning : Q - Learning
Q-Learning là thuật toán học tăng cường, học từ trải nghiệm để tìm đường đi tối ưu. Thuật toán duy trì một bảng Q-table lưu trữ giá trị của mỗi hành động tại mỗi trạng thái, và cập nhật liên tục các giá trị này dựa trên phần thưởng nhận được.

<p align="center">
  <img src="https://raw.githubusercontent.com/tm-Quan745/Game-TacticalStrike/Develop/readme_img/qlearning.gif" alt="Q-Learning" />
</p>

## 🌓 So sánh hiệu năng thuật toán

| Thuật Toán         | Loại Tìm Kiếm        | Tính Chất Chính                               | Ưu Điểm                                              | Nhược Điểm                                              |
|--------------------|----------------------|------------------------------------------------|-------------------------------------------------------|----------------------------------------------------------|
| BFS                | Không có thông tin   | Duyệt theo chiều rộng                         | Tìm đường đi ngắn nhất, đơn giản                     | Tốn RAM, mở rộng nhiều node dư thừa                     |
| A*                 | Có thông tin (Heuristic) | Kết hợp chi phí thực tế + dự đoán          | Tối ưu, nhanh hơn BFS, tránh đường nguy hiểm        | Tốn bộ nhớ, phụ thuộc vào hàm heuristic                 |
| Beam Search        | Local     | Giữ lại `k` đường tốt nhất tại mỗi bước      | Nhanh, tiết kiệm bộ nhớ, phù hợp kẻ địch nhanh       | Không tối ưu, kết quả phụ thuộc beam width              |
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
