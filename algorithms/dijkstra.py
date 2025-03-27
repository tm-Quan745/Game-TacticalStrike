import heapq

def dijkstra_find_path(maze, grid_size):
    """Dijkstra's pathfinding algorithm."""
    start = (0, 0)
    goal = (grid_size-1, grid_size-1)
    
    # Priority queue storing (cost, position, path)
    queue = [(0, start, [start])]
    visited = set()
    
    while queue:
        cost, current, path = heapq.heappop(queue)
        
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
                next_cost = cost + 1
                heapq.heappush(queue, (next_cost, next_pos, path + [next_pos]))
    
    return None