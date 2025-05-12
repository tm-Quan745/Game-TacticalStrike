from algorithms.bfs import bfs_find_path
from algorithms.astar import astar_find_path
from algorithms.beam import beam_search_find_path

def find_path(maze, grid_size, algorithm="BFS"):
    """Find path using the specified algorithm."""
    if algorithm == "BFS":
        return bfs_find_path(maze, grid_size)
    elif algorithm == "A*":
        return astar_find_path(maze, grid_size)
    elif algorithm == "Beam":
        return beam_search_find_path(maze, grid_size)
    return None