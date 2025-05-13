import customtkinter as ctk
from loading_screen import LoadingScreen
from ui import channels, load_sound_effects 
sound_effects = load_sound_effects()

def main():
    # Set up the appearance mode and default color theme
    ctk.set_appearance_mode("light")  # Modes: "dark", "light"
    ctk.set_default_color_theme("green")  # Themes: "blue", "green", "dark-blue"
    
    # Create the main window
    root = ctk.CTk()
    root.title("Mê Cung Tower Defense")
    root.geometry("800x600")  # Set initial window size
    
    # Create loading screen
    loading_screen = LoadingScreen(root)
    
    # Start the game loop
    root.mainloop()

if __name__ == "__main__":
    main()