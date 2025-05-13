# Mê Cung Tower Defense

## Giới Thiệu
Mê Cung Tower Defense là trò chơi chiến thuật, nơi người chơi xây dựng tháp phòng thủ để ngăn kẻ địch vượt qua mê cung. Trò chơi sử dụng các thuật toán tìm đường thông minh và giao diện trực quan.

## Cấu Trúc Dự Án
- **`main.py`**: Điểm khởi đầu của trò chơi.
- **`game_logic.py`**: Xử lý logic chính, quản lý tháp và kẻ địch.
- **`ui.py`**: Giao diện người dùng.
- **`entities.py`**: Định nghĩa kẻ địch và tháp.
- **`pathfinding.py`**: Thuật toán tìm đường.

## Hướng Dẫn Cài Đặt
1. **Yêu Cầu**:
   - Python 3.10 hoặc mới hơn.
   - Thư viện: `customtkinter`, `pygame`, `Pillow`.
2. **Cài Đặt**:
   ```bash
   pip install customtkinter pygame Pillow
   ```
3. **Chạy Trò Chơi**:
   ```bash
   python main.py
   ```

## Tính Năng Chính
- Thuật toán tìm đường: BFS, DFS, Dijkstra, A*.
- Giao diện trực quan và hiệu ứng âm thanh sống động.

## Cách Chơi
1. **Mục Tiêu**: Xây dựng các tháp phòng thủ để ngăn chặn kẻ địch vượt qua mê cung và bảo vệ căn cứ của bạn.
2. **Xây Dựng Tháp**: Chọn vị trí chiến lược để đặt các tháp, mỗi loại tháp có khả năng đặc biệt:
   - **Shooter Tower**: Tấn công nhanh với sát thương trung bình.
   - **Freeze Tower**: Làm chậm kẻ địch trong phạm vi.
   - **Sniper Tower**: Tầm bắn xa với sát thương cao.
3. **Kẻ Địch**: Đối mặt với nhiều loại kẻ địch:
   - **Normal**: Tốc độ và máu trung bình.
   - **Fast**: Tốc độ cao nhưng máu thấp.
   - **Tank**: Máu cao nhưng di chuyển chậm.
4. **Chiến Thắng**: Tiêu diệt tất cả kẻ địch trước khi chúng đến căn cứ của bạn.

