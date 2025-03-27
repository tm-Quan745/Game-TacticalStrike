import heapq

def astar_find_path(maze, grid_size):
    """A* pathfinding algorithm."""
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    start = (0, 0)
    goal = (grid_size-1, grid_size-1)
    
    # Priority queue storing (f_score, g_score, position, path)
    queue = [(heuristic(start, goal), 0, start, [start])]
    visited = set()
    
    while queue:
        f_score, g_score, current, path = heapq.heappop(queue)
        
        if current == goal:
            return path
        
        if current in visited:
            continue
        
        visited.add(current)
        
        # Check all four directions
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x, y = current[0] + dx, current[1] + dy
            next_pos = (x, y)
            
            if (0 <= x < grid_size and 0 <= y < grid_size
                and maze[y][x] == 0 and next_pos not in visited):  # Only allow empty cells
                next_g = g_score + 1
                next_f = next_g + heuristic(next_pos, goal)
                heapq.heappush(queue, (next_f, next_g, next_pos, path + [next_pos]))
    
    return None