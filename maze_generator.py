import random
from pathfinding import bfs_find_path

def generate_maze(grid_size, debug=False):
    """Generate a maze using a randomized DFS algorithm."""
    # Ensure grid_size is odd
    if grid_size % 2 == 0:
        grid_size += 1

    # Initialize maze with all walls
    maze = [[1 for _ in range(grid_size)] for _ in range(grid_size)]
    stack = [(0, 0)]
    maze[0][0] = 0  # Start point

    # Directions: right, down, left, up
    directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]

    while stack:
        x, y = stack[-1]
        random.shuffle(directions)
        moved = False

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < grid_size and 0 <= new_y < grid_size and maze[new_y][new_x] == 1:
                maze[y + dy // 2][x + dx // 2] = 0
                maze[new_y][new_x] = 0
                stack.append((new_x, new_y))
                moved = True
                break

        if not moved:
            stack.pop()

    # Ensure there's a path from (0,0) to (grid_size-1, grid_size-1)
    maze[grid_size - 1][grid_size - 1] = 0

    # Make maze more open for better gameplay
    for i in range(1, grid_size - 1, 2):
        for j in range(1, grid_size - 1, 2):
            if random.random() < 0.3:  # Reduced randomness to maintain structure
                maze[i][j] = 0

    # Ensure starting and ending areas are more open
    for i in range(2):
        for j in range(2):
            if i > 0 or j > 0:
                maze[j][i] = 0
                maze[grid_size - 1 - j][grid_size - 1 - i] = 0

    # Validate the maze to ensure a valid path exists
    path = bfs_find_path(maze, grid_size)
    if not path:
        return generate_maze(grid_size, debug)  # Regenerate maze if no valid path

    # Debug: Print the maze if debug mode is enabled
    if debug:
        pass  # Debugging output removed

    return maze