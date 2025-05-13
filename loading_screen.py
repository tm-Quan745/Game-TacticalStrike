import customtkinter as ctk
from PIL import Image, ImageTk
from game_logic import MazeTowerDefenseGame
from ui import channels, load_sound_effects 
import pygame

sound_effects = load_sound_effects()

for i in range(pygame.mixer.get_num_channels()):
    pygame.mixer.Channel(i).stop()


channels['intro'].set_volume(0.5)
if not channels['intro'].get_busy():

    channels['intro'].play(sound_effects['intro'])
    
class LoadingScreen:
    def __init__(self, root):
        self.root = root
        self.fade_step = 0
        self.button_pulse = True
        self.setup_loading_screen()
        
    def setup_loading_screen(self):
        # Main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="MÊ CUNG TOWER DEFENSE",
            font=ctk.CTkFont(family="Minecraft", size=36, weight="bold"),
            text_color="#A5D6A7"  # Nhạt ban đầu
        )
        self.title_label.pack(pady=(100, 20))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Tower Defense phòng thủ mê cung",
            font=ctk.CTkFont(family="Minecraft", size=18),
            text_color="#1B5E20"
        )
        subtitle_label.pack(pady=(0, 50))
        
        # Start button
        self.start_button = ctk.CTkButton(
            self.main_frame,
            text="Bắt Đầu Chơi",
            font=ctk.CTkFont(family="Minecraft", size=24, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#388E3C",
            width=200,
            height=60,
            command=self.start_game
        )
        self.start_button.pack(pady=20)
        
        # Help button
        help_button = ctk.CTkButton(
            self.main_frame,
            text="Hướng Dẫn",
            font=ctk.CTkFont(family="Minecraft", size=18),
            fg_color="#2196F3",
            hover_color="#1976D2",
            width=150,
            height=40,
            command=self.show_help
        )
        help_button.pack(pady=10)
        
        # Exit button
        exit_button = ctk.CTkButton(
            self.main_frame,
            text="Thoát",
            font=ctk.CTkFont(family="Minecraft", size=18),
            fg_color="#F44336",
            hover_color="#D32F2F",
            width=150,
            height=40,
            command=self.root.quit
        )
        exit_button.pack(pady=10)
        
        # Start animations
        self.fade_in_title()
        self.pulse_button()
        
    def fade_in_title(self):
        # Fade màu từ nhạt đến đậm xanh (#A5D6A7 → #2E7D32)
        steps = [
            "#A5D6A7", "#81C784", "#66BB6A", "#4CAF50", "#388E3C", "#2E7D32"
        ]
        if self.fade_step < len(steps):
            color = steps[self.fade_step]
            self.title_label.configure(text_color=color)
            self.fade_step += 1
            self.root.after(200, self.fade_in_title)
        
    def pulse_button(self):
        # Hiệu ứng nhấp nháy nút
        if self.button_pulse:
            self.start_button.configure(fg_color="#66BB6A")
        else:
            self.start_button.configure(fg_color="#4CAF50")
        self.button_pulse = not self.button_pulse
        self.root.after(600, self.pulse_button)
        
    def start_game(self):
        # Show spinner trước khi vào game
        loading_label = ctk.CTkLabel(
            self.main_frame,
            text="Đang khởi động trò chơi",
            font=ctk.CTkFont(family="Minecraft", size=18),
            text_color="#1B5E20"
        )
        loading_label.pack(pady=20)
        
        self.animate_spinner(loading_label, 0)
        
    def animate_spinner(self, label, count):
        dots = "." * (count % 4)
        label.configure(text=f"Đang khởi động trò chơi{dots}")
        if count < 10:
            self.root.after(300, lambda: self.animate_spinner(label, count + 1))
        else:
            self.main_frame.destroy()
            self.game = MazeTowerDefenseGame(self.root)
            channels['intro'].fadeout(1000)

        
    def show_help(self):
        help_window = ctk.CTkToplevel(self.root)
        help_window.title("Hướng Dẫn")
        help_window.geometry("600x400")
        help_window.grab_set()
        
        help_text = """
        HƯỚNG DẪN CHƠI:
        
        1. Xây tháp phòng thủ trên mê cung
        2. Ngăn chặn kẻ địch di chuyển từ điểm Bắt đầu (S) đến điểm Kết thúc (E)
        3. Mỗi tháp có sức mạnh và khả năng riêng:
           - Tháp Bắn: Tấn công cơ bản, tốc độ bắn nhanh
           - Tháp Đóng Băng: Làm chậm kẻ địch
           - Tháp Bắn Tỉa: Sát thương cao, tầm bắn xa
        
        4. Kiếm tiền bằng cách tiêu diệt kẻ địch
        5. Nâng cấp và xây thêm tháp để phòng thủ hiệu quả
        6. Sống sót qua các làn sóng tấn công để giành chiến thắng!
        
        Chúc may mắn!
        """
        
        help_label = ctk.CTkLabel(
            help_window,
            text=help_text,
            font=ctk.CTkFont(family="Minecraft", size=14),
            justify="left"
        )
        help_label.pack(padx=20, pady=20)
