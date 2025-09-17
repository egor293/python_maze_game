import random
rows = 12
cols = 24
WALL = '█'    
FLOOR = ' '   
PLAYER = '☺'  
GHOST = '☻'
EXIT = '🚪'  
def generate_maze(rows, cols):
    directions = ['w', 'a', 's', 'd']
    maze = [[WALL]*cols]*rows
    stack = [(1, 1)]
    while stack:
        col, row = stack.pop()
        direction = random.choice(directions)
        if (col, row) == (11, 23):
            maze[11, 23] = EXIT
            return maze

        if direction == 'w' and row > 1 and row < rows:
            if (col, row - 1) not in stack:
                stack.append((col, row))
                maze[col, row - 1] = FLOOR
        if direction == 'a' and col > 1 and col < cols:
            if (col - 1, row) not in stack:
                stack.append((col, row))
                maze[col - 1, row] = FLOOR
        if direction == 's' and row > 1 and row < rows:
            if (col, row + 1) not in stack:
                stack.append((col, row))
                maze[col, row + 1] = FLOOR
        if direction == 'd' and col > 1 and col < cols:
            if (col + 1, row) not in stack:
                stack.append((col, row))
                maze[col + 1, row] = FLOOR
        
                # redo
    return maze
print(generate_maze(rows, cols))
