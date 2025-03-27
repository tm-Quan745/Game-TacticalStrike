from collections import deque
import heapq
import math

def validate_maze(maze, grid_size):
    """Validate the maze structure."""
    if len(maze) != grid_size or any(len(row) != grid_size for row in maze):
        raise ValueError("Invalid maze dimensions!")

def bfs_find_path(maze, grid_size):
    """Breadth-First Search for pathfinding."""
    validate_maze(maze, grid_size)
    start = (0, 0)
    end = (grid_size - 1, grid_size - 1)

    if maze[start[1]][start[0]] != 0 or maze[end[1]][end[0]] != 0:
        return None

    queue = [(start, [start])]
    visited = set()

    while queue:
        current, path = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            return path

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size and maze[ny][nx] == 0:
                queue.append(((nx, ny), path + [(nx, ny)]))

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
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x, y = current[0] + dx, current[1] + dy
            next_pos = (x, y)
            
            if (0 <= x < grid_size and 0 <= y < grid_size
                and maze[y][x] == 0 and next_pos not in visited):
                stack.append(path + [next_pos])
                visited.add(next_pos)
    
    return None

def dijkstra_find_path(maze, grid_size):
    """Dijkstra's pathfinding algorithm."""
    start = (0, 0)
    goal = (grid_size-1, grid_size-1)
    
    queue = [(0, start, [start])]
    visited = set()
    
    while queue:
        cost, current, path = heapq.heappop(queue)
        
        if current == goal:
            return path
        
        if current in visited:
            continue
        
        visited.add(current)
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x, y = current[0] + dx, current[1] + dy
            next_pos = (x, y)
            
            if (0 <= x < grid_size and 0 <= y < grid_size
                and maze[y][x] == 0 and next_pos not in visited):
                next_cost = cost + 1
                heapq.heappush(queue, (next_cost, next_pos, path + [next_pos]))
    
    return None

def astar_find_path(maze, grid_size):
    """A* algorithm for pathfinding."""
    validate_maze(maze, grid_size)
    start = (0, 0)
    end = (grid_size - 1, grid_size - 1)

    if maze[start[1]][start[0]] != 0 or maze[end[1]][end[0]] != 0:
        return None

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = [(0 + heuristic(start, end), 0, start, [start])]
    g_score = {start: 0}

    while open_set:
        _, current_g, current, path = heapq.heappop(open_set)

        if current == end:
            return path

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)

            if 0 <= nx < grid_size and 0 <= ny < grid_size and maze[ny][nx] == 0:
                tentative_g = current_g + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor, path + [neighbor]))

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