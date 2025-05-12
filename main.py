import customtkinter as ctk
from loading_screen import LoadingScreen

def main():
    # Set up the appearance mode and default color theme
    ctk.set_appearance_mode("light")  # Modes: "dark", "light"
    ctk.set_default_color_theme("green")  # Themes: "blue", "green", "dark-blue"
    
    # Create the main window
    root = ctk.CTk()
    root.title("Mê Cung Tower Defense")
    
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate initial window size (80% of screen)
    window_width = int(screen_width * 0.9)
    window_height = int(screen_height * 0.9)
    
    # Calculate center position
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
   
    
    # Set window geometry
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Store window position for fullscreen toggle
    root._window_pos = None
    
    def toggle_fullscreen(event=None):
        if not root.attributes('-fullscreen'):
            # Store current window position and size
            root._window_pos = root.geometry()
            root.attributes('-fullscreen', True)
        else:
            # Restore window position and size
            root.attributes('-fullscreen', False)
            if root._window_pos:
                root.geometry(root._window_pos)
    
    # Bind F11 for fullscreen toggle
    root.bind('<F11>', toggle_fullscreen)
    root.bind('<Escape>', lambda e: root.attributes('-fullscreen', False))
    
    # Create loading screen
    loading_screen = LoadingScreen(root)
    
    # Start the game loop
    root.mainloop()

if __name__ == "__main__":
    main()