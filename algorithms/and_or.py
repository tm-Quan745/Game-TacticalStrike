import heapq

def and_or_search_find_path(maze, grid_size):
    """And-Or Search algorithm with max depth limit."""
    
    max_depth = grid_size * grid_size 
    
    start = (0, 0)
    goal = (grid_size-1, grid_size-1)
    
    # Priority queue storing (f_score, g_score, position, path, node_type)
    queue = [(0, 0, start, [start], 'OR')]  
    visited = set()
    
    def heuristic(a, b):
        """Hàm heuristic: Khoảng cách Manhattan"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def get_neighbors(position):
        """Lấy các ô kề hợp lệ theo 4 hướng."""
        neighbors = []
        x, y = position
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size and maze[ny][nx] == 0:
                neighbors.append((nx, ny))
        return neighbors
    
    while queue:
        f_score, g_score, current, path, node_type = heapq.heappop(queue)
        
        if current == goal:
            return path
        
        if current in visited:
            continue
        
        if len(path) > max_depth:
            continue
        
        visited.add(current)
        
        neighbors = get_neighbors(current)
        
        if node_type == 'OR':
            # OR node
            for neighbor in neighbors:
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    next_f = g_score + 1 + heuristic(neighbor, goal)
                    heapq.heappush(queue, (next_f, g_score + 1, neighbor, new_path, 'AND'))
        
        elif node_type == 'AND':
            # AND node
            valid_paths = []
            for neighbor in neighbors:
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    next_f = g_score + 1 + heuristic(neighbor, goal)
                    heapq.heappush(queue, (next_f, g_score + 1, neighbor, new_path, 'OR'))
                    valid_paths.append(new_path)
            if not valid_paths:
                continue
    
    return None
