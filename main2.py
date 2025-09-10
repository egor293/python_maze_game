import os
import sys
from collections import deque



def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

WALL = '█'    
FLOOR = ' '   
PLAYER = '☺'  
GHOST = 'G'
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

rows = len(maze)
cols = len(maze[0])


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

player_row, player_col = find_player()


def draw_maze():
    clear_screen()
    for row in maze:
        print(''.join(row))
    print("\nУправление: W - вверх, A - влево, S - вниз, D - вправо. Q - выход.")


def ghost_brain(player_pos, ghost_pos):
    queue = deque()
    visited = []


ghost_brain(player_pos = find_player, ghost_pos = find_ghost)
draw_maze()
if __name__ == "__main__":
    while True:
        move = input("Ваш ход: ").lower()
        if move == 'q':
            print("Игра завершена.")
            sys.exit()
    
        new_row, new_col = player_row, player_col
    
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
    
        if new_row < 0 or new_row >= rows or new_col < 0 or new_col >= cols:
            print("Нельзя выйти за пределы лабиринта!")
            continue
    
        if maze[new_row][new_col] == WALL:
            print("Стена! Нельзя пройти.")
            continue
    
        if maze[new_row][new_col] == EXIT:
            clear_screen()
            print("Поздравляем! Вы нашли выход.")
            sys.exit()
    
        maze[player_row][player_col] = FLOOR
        maze[new_row][new_col] = PLAYER
        player_row, player_col = new_row, new_col
    
        draw_maze()