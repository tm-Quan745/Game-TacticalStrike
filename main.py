import customtkinter as ctk
from game_logic import MazeTowerDefenseGame

def main():
    # Set up the appearance mode and default color theme
    ctk.set_appearance_mode("light")  # Modes: "dark", "light"
    ctk.set_default_color_theme("green")  # Themes: "blue", "green", "dark-blue"
    
    # Create the main window
    root = ctk.CTk()
    root.title("Mê Cung Tower Defense")
    root.geometry("1200x800")  # Set initial window size
    
    # Create game instance
    game = MazeTowerDefenseGame(root)
    
    # Start the game loop
    root.mainloop()

if __name__ == "__main__":
    main()