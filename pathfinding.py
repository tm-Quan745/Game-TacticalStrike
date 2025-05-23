import time

from algorithms.bfs import bfs_find_path
from algorithms.astar import astar_find_path
from algorithms.beam import beam_search_find_path
from algorithms.partial_observation_search import find_path_with_partial_observation
from algorithms.qlearning import qlearning_find_path
from algorithms.backtracking import backtracking_find_path

def find_path(maze, grid_size, algorithm="BFS"):
    """Find path using the specified algorithm."""
    if algorithm == "BFS":
        path = bfs_find_path(maze, grid_size)
    elif algorithm == "A*":
        path = astar_find_path(maze, grid_size)
    elif algorithm == "Beam":
        path = beam_search_find_path(maze, grid_size)
    elif algorithm == "Partial":
        path = find_path_with_partial_observation(maze, grid_size)
    elif algorithm == "Backtracking":
        path = backtracking_find_path(maze, grid_size)
    elif algorithm == "Q-Learning":
        print("Đang áp dụng Q-learning cho map hiện tại...")
        path = qlearning_find_path(maze, grid_size)
    else:
        path = None
    
    # In đường đi tìm được (nếu có)
    if path:
        print(f"Đường đi tìm được bằng thuật toán {algorithm}: {path}")
    else:
        print(f"Không tìm thấy đường đi bằng thuật toán {algorithm}")
    
    return path
