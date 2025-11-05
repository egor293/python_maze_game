from keyboard import read_key
from threading import Thread, Lock
from colorama import Fore, init
import random
import time
import sys
import os

init(autoreset=True) 

width = 26
height = 16
points = 0
PLAYER = '█'
projectiles = []
base_move_speed = 1
base_spawn_speed = 1
field_lock = Lock()
field = [[' ' for _ in range(width)] for _ in range(height)]


class Projectile:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.char = '*'
        self.color = Fore.RESET
        self.speed = 1
        self.bonus = -15
        self.destroy_on_hit = True

    def move(self):
        self.row += self.speed
        return self.row < height

    def render(self):
        return self.color + self.char

    def on_hit_player(self):
        global points
        points += self.bonus
        return self.destroy_on_hit



class FastProjectile(Projectile):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.char = '•'
        self.color = Fore.YELLOW
        self.speed = 2
        self.bonus = -10


class BonusProjectile(Projectile):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.char = '♦'
        self.color = Fore.GREEN
        self.bonus = 45
        self.destroy_on_hit = False 


class BombProjectile(Projectile):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.char = '☼'
        self.color = Fore.RED
        self.bonus = -50
        self.speed = 1

    def on_hit_player(self):
        global points
        points -= 50
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                r, c = self.row + dr, self.col + dc
                if 0 <= r < height and 0 <= c < width:
                    field[r][c] = ' '
        return True


class Player:
    def __init__(self):
        self.positions = [(height - 1, width // 2 - 1), (height - 1, width // 2), (height - 1, width // 2 + 1)]

    def place_player(self):
        for row, col in self.positions:
            field[row][col] = PLAYER

    def move_player(self, move):
        global points
        move = move.lower()
        if move == 'q':
            print("Игра завершена.")
            sys.exit()

        newx = 0
        if move == 'a':
            newx = -1
        elif move == 'd':
            newx = 1
        else:
            return

        new_pos = [(row, col + newx) for row, col in self.positions]

        for row, col in new_pos:
            if col < 0 or col >= width:
                return

        for row, col in new_pos:
            proj = next((p for p in projectiles if p.row == row and p.col == col), None)
            if proj:
                should_remove = proj.on_hit_player()
                if should_remove:
                    projectiles[:] = [p for p in projectiles if p != proj]

        self.clear_player()
        self.positions = new_pos
        self.render_player()

        draw_field()

    def render_player(self):
        for row, col in self.positions:
            safe_set_field(row, col, PLAYER)

    def clear_player(self):
        for row, col in self.positions:
            safe_set_field(row, col, ' ')


class Spawner:
    def __init__(self):
        self.projectile_types = [
            (Projectile, 60),      # Обычный — 60%
            (FastProjectile, 20),  # Быстрый — 20%
            (BonusProjectile, 15), # Бонус — 15%
            (BombProjectile, 5),   # Бомба — 5%
        ]

    def spawn(self, spawn_speed):
            for _ in range(int(spawn_speed)):
                col = random.randint(0, width - 1)
                if safe_get_field(0, col) != ' ':
                    continue
                
                rand = random.randint(1, 100)
                cumulative = 0
                chosen_class = Projectile
                for proj_class, probability in self.projectile_types:
                    cumulative += probability
                    if rand <= cumulative:
                        chosen_class = proj_class
                        break
                    
                projectile = chosen_class(0, col)
                safe_set_field(0, col, projectile.render())
                projectiles.append(projectile)
    
                draw_field()


def move_projectiles(player):
    global points
    to_remove = []

    for proj in projectiles[:]:
        safe_set_field(proj.row, proj.col, ' ')

        if not proj.move():
            to_remove.append(proj)
            continue

        if not (0 <= proj.row < height and 0 <= proj.col < width):
            to_remove.append(proj)
            continue

        player_hit = False
        for player_row, player_col in player.positions:
            if proj.row == player_row and proj.col == player_col:
                player_hit = True
                break

        if player_hit:
            should_remove = proj.on_hit_player()
            
            if should_remove:
                to_remove.append(proj)
            else:
                safe_set_field(proj.row, proj.col, proj.render())
            
            player.render_player()
            draw_field()
            continue

        safe_set_field(proj.row, proj.col, proj.render())

    for proj in to_remove:
        if proj in projectiles:
            projectiles.remove(proj)

    draw_field()


def safe_set_field(row, col, char):
    with field_lock:
        if 0 <= row < height and 0 <= col < width:
            field[row][col] = char

def safe_get_field(row, col):
    with field_lock:
        if 0 <= row < height and 0 <= col < width:
            return field[row][col]
        return ' '

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_field():
    clear_screen()
    with field_lock: 
        display_field = [row[:] for row in field]  
    
    for row in display_field:
        print(''.join(row))
    print(f"Управление: A - влево, D - вправо, Q - выход. | очки: {points}")
    draw_types()

def draw_types():
    print("Типы снарядов: ", end='')
    types = [
        Projectile(0, 0),
        FastProjectile(0, 0),
        BonusProjectile(0, 0),
        BombProjectile(0, 0),
    ]
    for type in types:
        temp = type
        print(f"{temp.render()}", end='  ')
    print()

def user_input(player):
    while True:
        key = read_key()
        player.move_player(key)
        time.sleep(0.05)

def game_loop(spawner, player):
    global points
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time

        spawn_speed = base_spawn_speed * (1.05 ** (elapsed_time / 10))
        move_speed = base_move_speed * (1.05 ** (elapsed_time / 10))

        spawner.spawn(spawn_speed)
        move_projectiles(player)
        if points < 0:
            print("Игра завершена!")
            sys.exit()

        time.sleep(0.5 / move_speed)    


if __name__ == "__main__":
    player = Player()
    spawner = Spawner()
    player.place_player()
    draw_field()

    input_thread = Thread(target=user_input, args=(player,), daemon=True)
    game_thread = Thread(target=game_loop, args=(spawner, player), daemon=True)

    input_thread.start()
    game_thread.start()

    try:
        while True:
            time.sleep(1)
            points += 5 
    except KeyboardInterrupt:
        print("Игра завершена.")
        sys.exit()