import tkinter as tk
from tkinter import ttk
from ui import GameUI
from game_logic import MazeTowerDefenseGame

def main():
    root = tk.Tk()
    root.title("Mê Cung Tower Defense")
    
    # Configure styles
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 10, 'bold'))
    style.configure('TLabel', font=('Arial', 10))
    style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
    
    # Create game instance
    game = MazeTowerDefenseGame(root)
    
    # Start game loop
    root.mainloop()

if __name__ == "__main__":
    main()