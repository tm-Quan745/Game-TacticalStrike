import tkinter as tk
from game_logic import MazeTowerDefenseGame

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Maze Tower Defense Game")
    game = MazeTowerDefenseGame(root)
    root.mainloop()
