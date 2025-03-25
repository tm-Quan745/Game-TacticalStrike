from collections import deque
import heapq
import math

def bfs_find_path(maze, grid_size):
    """Breadth-First Search pathfinding algorithm."""
    start = (0, 0)
    goal = (grid_size-1, grid_size-1)
    queue = deque([[start]])
    visited = {start}
    
    while queue:
        path = queue.popleft()
        current = path[-1]
        
        if current == goal:
            return path
        
        # Check all four directions
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x, y = current[0] + dx, current[1] + dy
            next_pos = (x, y)
            
            if (0 <= x < grid_size and 0 <= y < grid_size
                and maze[y][x] == 0 and next_pos not in visited):  # Only allow empty cells
                queue.append(path + [next_pos])
                visited.add(next_pos)
    
    return None

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

def astar_find_path(maze, grid_size):
    """A* pathfinding algorithm."""
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    start = (0, 0)
    goal = (grid_size-1, grid_size-1)
    
    # Priority queue storing (f_score, position, path)
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