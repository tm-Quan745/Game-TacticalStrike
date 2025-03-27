def dfs_find_path(maze, grid_size):
    """Depth-First Search pathfinding algorithm."""
    start = (0, 0)
    goal = (grid_size-1, grid_size-1)
    stack = [[start]]
    visited = {start}
    
    while stack:
        path = stack.pop()
        current = path[-1]
        
        if current == goal:
            return path
        
        # Check all four directions
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x, y = current[0] + dx, current[1] + dy
            next_pos = (x, y)
            
            if (0 <= x < grid_size and 0 <= y < grid_size
                and maze[y][x] == 0 and next_pos not in visited):  # Only allow empty cells
                stack.append(path + [next_pos])
                visited.add(next_pos)
    
    return None