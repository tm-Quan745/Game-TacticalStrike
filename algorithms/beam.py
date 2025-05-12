from collections import deque

def heuristic(a, b):
    """Heuristic function (Manhattan distance)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def beam_search_find_path(maze, grid_size, beam_width=5):
    """Beam Search pathfinding algorithm."""
    start = (0, 0)
    goal = (grid_size - 1, grid_size - 1)
    queue = [[start]]
    visited = {start}

    while queue:
        # Expand all current paths
        all_candidates = []
        for path in queue:
            current = path[-1]
            if current == goal:
                return path
            
            # Check all directions
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                x, y = current[0] + dx, current[1] + dy
                next_pos = (x, y)

                if (0 <= x < grid_size and 0 <= y < grid_size
                    and maze[y][x] == 0 and next_pos not in visited):
                    visited.add(next_pos)
                    new_path = path + [next_pos]
                    all_candidates.append(new_path)

        # Sort by heuristic and keep top-k
        all_candidates.sort(key=lambda path: heuristic(path[-1], goal))
        queue = all_candidates[:beam_width]
    
    return None
