# from algorithms.bfs import bfs_find_path
# from algorithms.astar import astar_find_path
# from algorithms.beam import beam_search_find_path
# from algorithms.and_or import and_or_search_find_path

# def find_path(maze, grid_size, algorithm="BFS"):
#     """Find path using the specified algorithm."""
#     if algorithm == "BFS":
#         return bfs_find_path(maze, grid_size)
#     elif algorithm == "A*":
#         return astar_find_path(maze, grid_size)
#     elif algorithm == "Beam":
#         return beam_search_find_path(maze, grid_size)
#     elif algorithm == "And-Or":
#         return and_or_search_find_path(maze, grid_size)

#     return None
from algorithms.bfs import bfs_find_path
from algorithms.astar import astar_find_path
from algorithms.beam import beam_search_find_path
from algorithms.and_or import and_or_search_find_path

def find_path(maze, grid_size, algorithm="BFS"):
    """Find path using the specified algorithm."""
    if algorithm == "BFS":
        path = bfs_find_path(maze, grid_size)
    elif algorithm == "A*":
        path = astar_find_path(maze, grid_size)
    elif algorithm == "Beam":
        path = beam_search_find_path(maze, grid_size)
    elif algorithm == "And-Or":
        path = and_or_search_find_path(maze, grid_size)
    else:
        path = None
    
    # In đường đi tìm được (nếu có)
    if path:
        print(f"Đường đi tìm được bằng thuật toán {algorithm}: {path}")
    else:
        print(f"Không tìm thấy đường đi bằng thuật toán {algorithm}")
    
    return path
