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
EXIT = '⍇'    
lifes = 3

# maze = [
#     [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
#     [WALL, PLAYER, FLOOR, FLOOR, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
#     [WALL, WALL, WALL, FLOOR, WALL, FLOOR, WALL, WALL, WALL, FLOOR, WALL, WALL, WALL, WALL, FLOOR, WALL],
#     [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, FLOOR, WALL],
#     [WALL, FLOOR, WALL, WALL, WALL, WALL, FLOOR, WALL, WALL, WALL, FLOOR, WALL, FLOOR, WALL, FLOOR, WALL],
#     [WALL, FLOOR, WALL, FLOOR, GHOST, WALL, FLOOR, WALL, FLOOR, FLOOR, FLOOR, WALL, FLOOR, FLOOR, FLOOR, WALL],
#     [WALL, FLOOR, WALL, FLOOR, WALL, WALL, FLOOR, WALL, FLOOR, WALL, FLOOR, WALL, WALL, WALL, WALL, WALL],
#     [WALL, FLOOR, FLOOR, FLOOR, WALL, FLOOR, FLOOR, FLOOR, FLOOR, WALL, FLOOR, FLOOR, FLOOR, WALL, WALL, WALL],
#     [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, FLOOR, FLOOR, WALL, FLOOR, WALL, FLOOR, EXIT, WALL],
#     [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
# ]

def generate_maze(rows, cols):
    def is_valid(nr, nc):
        return 0 < nr < rows-1 and 0 < nc < cols-1

    def carve_passages_from(maze, r, c):
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc) and maze[nr][nc] == WALL:
                maze[nr][nc] = FLOOR
                maze[r + dr//2][c + dc//2] = FLOOR
                carve_passages_from(maze, nr, nc)

    def find_path(maze, start, goal):
        queue = Queue()
        queue.put([start])
        visited = set()
        visited.add(start)
        while not queue.empty():
            path = queue.get()
            x, y = path[-1]
            if (x, y) == goal:
                return path
            for dx, dy in [(1,0), (0,1), (-1,0), (0,-1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < rows and 0 <= ny < cols and 
                    maze[nx][ny] != WALL and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.put(path + [(nx, ny)])
        return None

    while True:
        maze = [[WALL for _ in range(cols)] for _ in range(rows)]
        start_r, start_c = 1, 1
        maze[start_r][start_c] = FLOOR
        carve_passages_from(maze, start_r, start_c)


        while True:
            er, ec = random.randint(1, rows-2), random.randint(1, cols-2)
            if maze[er][ec] == FLOOR and (er, ec) != (start_r, start_c):
                maze[er][ec] = EXIT
                break


        while True:
            gr, gc = random.randint(1, rows-2), random.randint(1, cols-2)
            if maze[gr][gc] == FLOOR and maze[gr][gc] != EXIT and (gr, gc) != (start_r, start_c):
                maze[gr][gc] = GHOST
                break

        maze[start_r][start_c] = PLAYER

        player_pos = (start_r, start_c)
        exit_pos = (er, ec)
        ghost_pos = (gr, gc)
        path_player_to_exit = find_path(maze, player_pos, exit_pos)
        path_ghost_to_player = find_path(maze, ghost_pos, player_pos)


        if path_player_to_exit and path_ghost_to_player:

            player_path = path_player_to_exit
            ghost_path = find_path(maze, ghost_pos, player_pos)
            player_step = 0
            ghost_step = 0
            player_current = player_pos
            ghost_current = ghost_pos
            safe = True
            while player_step < len(player_path):

                player_current = player_path[player_step]

                ghost_path_now = find_path(maze, ghost_current, player_current)
                if ghost_path_now and len(ghost_path_now) > 1:
                    ghost_current = ghost_path_now[1]

                if ghost_current == player_current:
                    safe = False
                    break
                player_step += 1

                if player_current == exit_pos:
                    break
            if safe:
                return maze

rows = 12
cols = 24
maze = generate_maze(rows, cols)

class Player:
    def move(player_row, player_col, lifes):
        new_row, new_col = player_row, player_col
        move = input("Ваш ход: ").lower()
        
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

        if move == 'q':
            print("Игра завершена.")
            sys.exit()


        if new_row < 0 or new_row >= rows or new_col < 0 or new_col >= cols:
            print("Нельзя выйти за пределы лабиринта!")
            return  


        if maze[new_row][new_col] == WALL:
            print("Стена! Нельзя пройти.")
            return 

        if (new_row, new_col) in landmines:
            lifes -= 1
            if lifes == 0:
                print("Вы наступили на мину и потеряли все жизни! Игра окончена.")
                start(rows, cols)
                return
            print(f"Вы наступили на мину! Осталось жизней: {lifes}")

        if maze[new_row][new_col] == EXIT:
            clear_screen()
            print("Поздравляем! Вы нашли выход.")
            start(rows, cols)
            return

        maze[new_row][new_col] = PLAYER
        maze[player_row][player_col] = FLOOR

        draw_maze()
        move_ghost()


def start(rows, cols):
    global maze
    maze = generate_maze(rows, cols)
    place_mines(rows, cols)
    draw_maze()


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


place_mines(rows, cols)
if __name__ == "__main__":
    while True:
        pos = find_player()
        if pos is None:
            print("Игрок не найден. Перезапуск игры.")
            start(rows, cols)
            pos = find_player()
            if pos is None:
                print("Ошибка: игрок не найден после перезапуска.")
                break
        player_row, player_col = pos
        Player.move(player_row, player_col, lifes)

