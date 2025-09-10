import os
import sys

# Функция для очистки терминала
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Кастомные символы для более красивого вида
WALL = '█'    # Стена
FLOOR = ' '   # Пол (можно изменить на '·' для точек, но оставим пробел для чистоты)
PLAYER = '☺'  # Игрок (улыбающееся лицо)
EXIT = '🚪'    # Выход (дверь, если консоль поддерживает Unicode; иначе можно заменить на 'E')

# Представление лабиринта как списка списков с кастомными символами
maze = [
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
    [WALL, PLAYER, FLOOR, FLOOR, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, WALL, WALL, FLOOR, WALL, FLOOR, WALL, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, FLOOR, WALL, WALL, WALL, WALL, FLOOR, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, FLOOR, WALL, FLOOR, FLOOR, WALL, FLOOR, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, FLOOR, WALL, FLOOR, WALL, WALL, FLOOR, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, FLOOR, FLOOR, FLOOR, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, EXIT, WALL],
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
]

# Размеры лабиринта
rows = len(maze)
cols = len(maze[0])

# Найти начальную позицию игрока
def find_player():
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == PLAYER:
                return r, c
    return None

player_row, player_col = find_player()

# Функция для отрисовки лабиринта
def draw_maze():
    clear_screen()
    for row in maze:
        print(''.join(row))
    print("\nУправление: W - вверх, A - влево, S - вниз, D - вправо. Q - выход.")

# Основной игровой цикл
draw_maze()
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

    # Проверка границ
    if new_row < 0 or new_row >= rows or new_col < 0 or new_col >= cols:
        print("Нельзя выйти за пределы лабиринта!")
        continue

    # Проверка на стену
    if maze[new_row][new_col] == WALL:
        print("Стена! Нельзя пройти.")
        continue

    # Проверка на выход
    if maze[new_row][new_col] == EXIT:
        clear_screen()
        print("Поздравляем! Вы нашли выход.")
        sys.exit()

    # Перемещение игрока
    maze[player_row][player_col] = FLOOR
    maze[new_row][new_col] = PLAYER
    player_row, player_col = new_row, new_col

    draw_maze()