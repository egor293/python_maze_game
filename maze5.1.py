import os
import sys
from queue import Queue
import random
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

WALL = '█'    
FLOOR = ' '   
PLAYER = '☺'  
GHOST = '☻'
LANDMINE = '*'
EXIT = '🚪'    

maze = [
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
    [WALL, PLAYER, FLOOR, FLOOR, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, WALL, WALL, FLOOR, WALL, FLOOR, WALL, WALL, WALL, FLOOR, WALL, WALL, WALL, WALL, FLOOR, WALL],
    [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, FLOOR, WALL],
    [WALL, FLOOR, WALL, WALL, WALL, WALL, FLOOR, WALL, WALL, WALL, FLOOR, WALL, FLOOR, WALL, FLOOR, WALL],
    [WALL, FLOOR, WALL, FLOOR, GHOST, WALL, FLOOR, WALL, FLOOR, FLOOR, FLOOR, WALL, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, FLOOR, WALL, FLOOR, WALL, WALL, FLOOR, WALL, FLOOR, WALL, FLOOR, WALL, WALL, WALL, WALL, WALL],
    [WALL, FLOOR, FLOOR, FLOOR, WALL, FLOOR, FLOOR, FLOOR, FLOOR, WALL, FLOOR, FLOOR, FLOOR, WALL, WALL, WALL],
    [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, FLOOR, FLOOR, WALL, FLOOR, WALL, FLOOR, EXIT, WALL],
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
]

rows = len(maze) - 1
cols = len(maze[0]) - 1

# rows = 12
# cols = 24


# def generate_maze(rows, cols):
#     maze = [[WALL for _ in range(cols)] for _ in range(rows)]
#     start_r, start_c = 1, 1

#     def is_valid(nr, nc):
#         return 0 < nr < rows-1 and 0 < nc < cols-1

#     def carve_passages_from(r, c):
#         directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
#         random.shuffle(directions)

#         for dr, dc in directions:
#             nr, nc = r + dr, c + dc
#             if is_valid(nr, nc) and maze[nr][nc] == WALL:
#                 maze[nr][nc] = FLOOR
#                 maze[r + dr//2][c + dc//2] = FLOOR 
#                 carve_passages_from(nr, n)   
#         maze[start_r][start_c] = FLOOR
#         carve_passages_from(start_r, start_c)

#         maze[start_r][start_c] = PLAYER

#         while True:
#             er, ec = random.randint(1, rows-2), random.randint(1, cols-2)
#             if maze[er][ec] == FLOOR and (er, ec) != (start_r, start_c):
#                 maze[er][ec] = EXIT
#                 break

#         while True:
#             gr, gc = random.randint(1, rows-2), random.randint(1, cols-2)
#             if maze[gr][gc] == FLOOR and maze[gr][gc] != EXIT:
#                 maze[gr][gc] = GHOST
#                 break

#     return maze

def restart(rows, cols):
    player_pos = find_player()
    ghost_pos = find_ghost()
    maze[player_pos[0]][player_pos[1]] = FLOOR
    maze[ghost_pos[0]][ghost_pos[1]] = FLOOR

    player_placed = False
    ghost_placed = False

    while is_possible() == False:
        for i in range(rows):
            for j in range(cols):
                if maze[i][j] == FLOOR and random.randint(1, 10) == 5 and player_placed == False:
                    maze[i][j] = PLAYER
                    player_placed = True
                if maze[i][j] == FLOOR and random.randint(1, 10) == 5 and ghost_placed == False:
                    maze[i][j] = GHOST
                    ghost_placed = True
    
    
def is_possible():
    def dfc(entity_pos):
        queue = Queue()
        queue.put([entity_pos])
        visited = set()
        visited.add(entity_pos)

        while not queue.empty():
            path = queue.get()
            x, y = path[-1]

            if (x, y) == (rows - 1, cols - 1):
                return len(path)
                
            for dx, dy in [(1,0), (0,1), (-1,0), (0,-1)]:
                next_x, next_y = x + dx, y + dy
                if (0 <= next_x < rows and 0 <= next_y < cols and 
                    maze[next_x][next_y] != WALL and (next_x, next_y) not in visited):
                    visited.add((next_x, next_y))
                    new_path = list(path)
                    new_path.append((next_x, next_y))
                    queue.put(new_path)
    try:
        if dfc(find_player()) < dfc(find_ghost()):
            return True
    except:
        return False
        
        
        






def place_mines(rows, cols):
    global landmines
    clear_screen()
    landmines = []
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == FLOOR and random.randint(1, 15) == 4:
                landmines.append((i, j))
    print('landmines: ', landmines)
    for i in landmines:
        maze[i[0]][i[1]] = LANDMINE
        draw_maze()
        time.sleep(0.15)
    for i in landmines:
        maze[i[0]][i[1]] = FLOOR
        draw_maze()
        time.sleep(0.15)
       


def find_player():
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == PLAYER:
                return r, c
    return None

def find_ghost():
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == GHOST:
                return r, c
    return None

def ghost_pathfinder(maze, player_pos, ghost_pos):
    queue = Queue()
    queue.put([ghost_pos])
    
    visited = set()
    visited.add(ghost_pos)
    
    while not queue.empty():
        path = queue.get()
        x, y = path[-1]
        
        if (x, y) == player_pos:
            if len(path) > 1:
                return path[1]  
            else:
                return ghost_pos 
        
        for dx, dy in [(1,0), (0,1), (-1,0), (0,-1)]:
            next_x, next_y = x + dx, y + dy
            if (0 <= next_x < rows and 0 <= next_y < cols and 
                maze[next_x][next_y] != WALL and (next_x, next_y) not in visited):
                visited.add((next_x, next_y))
                new_path = list(path)
                new_path.append((next_x, next_y))
                queue.put(new_path)
    
    return ghost_pos  

def move_ghost():
    player_pos = find_player()
    ghost_pos = find_ghost()
    
    if player_pos and ghost_pos:
        next_ghost_pos = ghost_pathfinder(maze, player_pos, ghost_pos)
        maze[ghost_pos[0]][ghost_pos[1]] = FLOOR
        maze[next_ghost_pos[0]][next_ghost_pos[1]] = GHOST
        if next_ghost_pos == player_pos or ghost_pos == player_pos:
            print('Игра завершена, вас поймал призрак.')
            draw_maze()
            sys.exit()

def draw_maze():
    clear_screen()
    for row in maze:
        print(''.join(row))
    print("\nУправление: W - вверх, A - влево, S - вниз, D - вправо. Q - выход.")

# maze = generate_maze(rows, cols)
# draw_maze()
place_mines(rows, cols)
if __name__ == "__main__":
    player_row, player_col = find_player()
    
    while True:
        
        draw_maze()
        move = input("Ваш ход: ").lower()
        new_row, new_col = player_row, player_col

        if move == 'q':
            print("Игра завершена.")
            restart(rows, cols)
        
        if move == 'w':
            new_row -= 1
        elif move == 's':
            new_row += 1
        elif move == 'a':
            new_col -= 1
        elif move == 'd':
            new_col += 1
        else:
            print("Неверный ввод. Используйте WASD или Q для выхода.")
            continue

        if (new_row, new_col) in landmines:
            print("Игра завершена. Вы наступили на мину.")
            restart(rows, cols)
        
        if new_row < 0 or new_row >= rows or new_col < 0 or new_col >= cols:
            print("Нельзя выйти за пределы лабиринта!")
            continue
        
        if maze[new_row][new_col] == WALL:
            print("Стена! Нельзя пройти.")
            continue
        
        if maze[new_row][new_col] == EXIT:
            clear_screen()
            print("Поздравляем! Вы нашли выход.")
            restart(rows, cols)
            # generate_maze(rows, cols)
        
        maze[player_row][player_col] = FLOOR
        maze[new_row][new_col] = PLAYER
        player_row, player_col = new_row, new_col
        
        move_ghost()
