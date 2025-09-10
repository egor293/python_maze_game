import os
import sys
import random
from collections import deque

# Функция для очистки терминала
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Кастомные символы для более красивого вида
WALL = '█'    # Стена
FLOOR = ' '   # Пол (можно изменить на '·' для точек, но оставим пробел для чистоты)
PLAYER = '☺'  # Игрок (улыбающееся лицо)
EXIT = '🚪'    # Выход (дверь, если консоль поддерживает Unicode; иначе можно заменить на 'E')

# Параметры лабиринта
HEIGHT = 11  # Высота лабиринта
WIDTH = 17   # Ширина лабиринта

# Функция для создания пустого лабиринта (стены по краям, пол внутри)
def create_empty_maze(width, height):
    maze = [[WALL for _ in range(width)] for _ in range(height)]
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            maze[r][c] = FLOOR
    return maze

# Рекурсивный алгоритм разделения для генерации лабиринта
def generate_maze(maze, top, bottom, left, right):
    if bottom - top < 3 or right - left < 3:
        return
    # Выбор позиции горизонтальной и вертикальной стены
    h_wall = random.randint(top + 1, bottom - 2)
    v_wall = random.randint(left + 1, right - 2)
    # Рисуем горизонтальную стену
    for c in range(left, right):
        maze[h_wall][c] = WALL
    # Рисуем вертикальную стену
    for r in range(top, bottom):
        maze[r][v_wall] = WALL
    # Создаем проходы (3 из 4 случайных)
    passages = [
        (h_wall, random.randint(left, v_wall - 1)),  # Левый горизонтальный
        (h_wall, random.randint(v_wall + 1, right - 1)),  # Правый горизонтальный
        (random.randint(top, h_wall - 1), v_wall),  # Верхний вертикальный
        (random.randint(h_wall + 1, bottom - 1), v_wall),  # Нижний вертикальный
    ]
    # Выбираем один проход, который не откроем
    no_open_index = random.randint(0, 3)
    for i in range(4):
        if i != no_open_index:
            r, c = passages[i]
            maze[r][c] = FLOOR
    # Рекурсия для четырех секций
    generate_maze(maze, top, h_wall, left, v_wall)
    generate_maze(maze, top, h_wall, v_wall + 1, right)
    generate_maze(maze, h_wall + 1, bottom, left, v_wall)
    generate_maze(maze, h_wall + 1, bottom, v_wall + 1, right)

# Функция для проверки проходимости лабиринта (BFS)
def is_solvable(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    visited = [[False] * cols for _ in range(rows)]
    queue = deque([start])
    visited[start[0]][start[1]] = True
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
    
    while queue:
        r, c = queue.popleft()
        if (r, c) == end:
            return True
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and maze[nr][nc] != WALL:
                visited[nr][nc] = True
                queue.append((nr, nc))
    return False

# Генерация лабиринта с проверкой проходимости
def generate_solvable_maze():
    while True:
        maze = create_empty_maze(WIDTH, HEIGHT)
        generate_maze(maze, 0, HEIGHT, 0, WIDTH)
        start = (1, 1)
        end = (HEIGHT - 2, WIDTH - 2)
        maze[start[0]][start[1]] = FLOOR  # Убедимся, что старт чист
        maze[end[0]][end[1]] = FLOOR      # Убедимся, что конец чист
        if is_solvable(maze, start, end):
            maze[start[0]][start[1]] = PLAYER
            maze[end[0]][end[1]] = EXIT
            return maze

maze = generate_solvable_maze()

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