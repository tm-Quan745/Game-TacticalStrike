import random

def generate_maze(grid_size):
    # Initialize maze with all walls
    maze = [[1 for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Use DFS algorithm to create the maze
    stack = [(0, 0)]
    maze[0][0] = 0  # Start point
    
    # Directions: right, down, left, up
    directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
    
    while stack:
        x, y = stack[-1]
        
        # Shuffle directions
        random.shuffle(directions)
        
        # Find a direction to move
        moved = False
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            if (0 <= new_x < grid_size and 0 <= new_y < grid_size 
                and maze[new_y][new_x] == 1):
                # Mark middle cell as path
                maze[y + dy//2][x + dx//2] = 0
                # Mark new cell as path
                maze[new_y][new_x] = 0
                
                stack.append((new_x, new_y))
                moved = True
                break
        
        if not moved:
            stack.pop()
    
    # Ensure there's a path from (0,0) to (grid_size-1, grid_size-1)
    maze[grid_size-1][grid_size-1] = 0
    
    # Make maze more open for better gameplay
    for i in range(1, grid_size-1, 2):
        for j in range(1, grid_size-1, 2):
            if random.random() < 0.4:
                maze[i][j] = 0
    
    # Ensure starting and ending areas are more open
    for i in range(2):
        for j in range(2):
            if i > 0 or j > 0:  # Don't change the actual start point
                maze[j][i] = 0
                maze[grid_size-1-j][grid_size-1-i] = 0
    
    return maze