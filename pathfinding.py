from algorithms.bfs import bfs_find_path
from algorithms.dfs import dfs_find_path
from algorithms.dijkstra import dijkstra_find_path
from algorithms.astar import astar_find_path

def find_path(maze, grid_size, algorithm="BFS"):
    """Find path using the specified algorithm."""
    if algorithm == "BFS":
        return bfs_find_path(maze, grid_size)
    elif algorithm == "DFS":
        return dfs_find_path(maze, grid_size)
    elif algorithm == "Dijkstra":
        return dijkstra_find_path(maze, grid_size)
    elif algorithm == "A*":
        return astar_find_path(maze, grid_size)
    return None