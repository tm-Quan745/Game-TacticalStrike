def is_safe(maze, x, y, visited, grid_size):
    """Không được vượt ra khỏi mê cung"""
    return (0 <= x < grid_size and
            0 <= y < grid_size and
            maze[y][x] == 0 and
            (x, y) not in visited)

def backtracking_search(maze, x, y, goal, path, visited, grid_size):
    if (x, y) == goal:
        path.append((x, y))
        return True

    visited.add((x, y))
    path.append((x, y))  

    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_x, new_y = x + dx, y + dy
        if is_safe(maze, new_x, new_y, visited, grid_size):
            if backtracking_search(maze, new_x, new_y, goal, path, visited, grid_size):
                return True

    visited.remove((x, y))
    # path.pop()
    return False

def backtracking_find_path(maze, grid_size):
    """Backtracking CSP pathfinding algorithm"""
    start = (0, 0)
    goal = (grid_size - 1, grid_size - 1)
    path = []
    visited = set()

    if maze[start[1]][start[0]] == 1 or maze[goal[1]][goal[0]] == 1:
        return None  # Start or goal is blocked

    backtracking_search(maze, start[0], start[1], goal, path, visited, grid_size)
    return path 
