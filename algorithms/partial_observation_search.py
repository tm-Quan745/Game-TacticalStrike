import heapq
from typing import List, Tuple, Set, Dict

class PartialObservationSearch:
    def __init__(self, grid_size: int, view_radius: int = 2):
        """
        Initialize the partial observation search algorithm.
        
        Args:
            grid_size: The size of the maze grid (assumes square maze)
            view_radius: How far the agent can see in each direction
        """
        self.grid_size = grid_size
        self.view_radius = view_radius
        self.belief_state = None
        self.reset_belief_state()

    def reset_belief_state(self):
        """Reset the belief state to unknown."""
        # -1: Unknown, 0: Empty, 1: Wall
        self.belief_state = [[-1] * self.grid_size for _ in range(self.grid_size)]
        
    def update_observation(self, current_pos: Tuple[int, int], maze: List[List[int]]):
        """
        Update the belief state based on current observation.
        
        Args:
            current_pos: Current position (x, y)
            maze: The actual maze state
        """
        x, y = current_pos
        for dy in range(-self.view_radius, self.view_radius + 1):
            for dx in range(-self.view_radius, self.view_radius + 1):
                new_x, new_y = x + dx, y + dy
                # Check if the position is within grid bounds
                if (0 <= new_x < self.grid_size and 
                    0 <= new_y < self.grid_size and
                    abs(dx) + abs(dy) <= self.view_radius):  # Manhattan distance check
                    self.belief_state[new_y][new_x] = maze[new_y][new_x]

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Calculate the Manhattan distance heuristic."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring positions."""
        x, y = pos
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.grid_size and 
                0 <= ny < self.grid_size and
                self.belief_state[ny][nx] != 1):  # Not a known wall
                neighbors.append((nx, ny))
        return neighbors

    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int], 
                 maze: List[List[int]]) -> List[Tuple[int, int]]:
        """
        Find a path using partial observation A* search.
        
        Args:
            start: Starting position (x, y)
            goal: Goal position (x, y)
            maze: The actual maze for updating observations
            
        Returns:
            List of positions forming the path, or None if no path is found
        """
        # Update initial observation
        self.update_observation(start, maze)
        
        # Priority queue storing (f_score, g_score, position, path)
        queue = [(0, 0, start, [start])]
        visited = set()
        g_scores = {start: 0}
        
        while queue:
            f_score, g_score, current, path = heapq.heappop(queue)
            
            # Update observation at current position
            self.update_observation(current, maze)
            
            if current == goal:
                return path
                
            if current in visited:
                continue
                
            visited.add(current)
            
            for neighbor in self.get_neighbors(current):
                if neighbor in visited:
                    continue
                    
                new_g_score = g_score + 1
                
                if neighbor not in g_scores or new_g_score < g_scores[neighbor]:
                    g_scores[neighbor] = new_g_score
                    f_score = new_g_score + self.heuristic(neighbor, goal)
                    new_path = path + [neighbor]
                    heapq.heappush(queue, (f_score, new_g_score, neighbor, new_path))
        
        return None

    def get_belief_state(self) -> List[List[int]]:
        """Return the current belief state of the environment."""
        return self.belief_state

def find_path_with_partial_observation(maze: List[List[int]], grid_size: int, 
                                    view_radius: int = 2) -> List[Tuple[int, int]]:
    """
    Wrapper function to find a path through the maze with partial observation.
    
    Args:
        maze: The complete maze grid
        grid_size: Size of the maze
        view_radius: How far the agent can see
        
    Returns:
        List of positions forming the path, or None if no path is found
    """
    searcher = PartialObservationSearch(grid_size, view_radius)
    start = (0, 0)
    goal = (grid_size - 1, grid_size - 1)
    return searcher.find_path(start, goal, maze)