from keyboard import read_key
from threading import Thread
import random
import time
import sys
import os

width = 26
height = 16
PLAYER = '█'
PROJECTILE = '*'
base_move_speed = 1
base_spawn_speed = 1
field = [[' ' for _ in range(width)] for _ in range(height)]

class Player:
    def __init__(self):
        self.positions = [(height - 1, width // 2 - 1), (height - 1, width // 2), (height - 1, width // 2 + 1)]

    def place_player(self):
        for row, col in self.positions:
            field[row][col] = PLAYER

    def find_player(self):
        return self.positions

    def move_player(self, move):
        move = move.lower()
        if move == 'q':
            print("Игра завершена.")
            sys.exit()

        dx = 0
        if move == 'a':
            dx = -1
        elif move == 'd':
            dx = 1
        else:
            return

        new_pos = [(row, col + dx) for row, col in self.positions]
        for row, col in new_pos:
            if col < 0 or col >= width:
                return  
            if field[row][col] == PROJECTILE:
                print("Вы были поражены снарядом! Игра окончена.")
                sys.exit()

        for row, col in self.positions:
            field[row][col] = ' '

        self.positions = new_pos
        for row, col in self.positions:
            field[row][col] = PLAYER

        draw_field()

class Spawner:
    @staticmethod
    def projectile_spawn(spawn_speed):
        for _ in range(int(spawn_speed)):
            spawn_x = random.randint(0, width - 1)
            if field[0][spawn_x] == ' ':
                field[0][spawn_x] = PROJECTILE

    @staticmethod
    def projectile_move(move_speed, player):
        for row in range(height - 1, -1, -1):
            for col in range(width):
                if field[row][col] == PROJECTILE:
                    next_row = row + int(move_speed)
                    if next_row >= height:
                        field[row][col] = ' '
                        continue
                    if field[next_row][col] == PLAYER:
                        print("Вы были поражены снарядом! Игра окончена.")
                        sys.exit()
                    field[row][col] = ' '
                    field[next_row][col] = PROJECTILE

        draw_field()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_field():
    clear_screen()
    for row in field:
        print(''.join(row))
    print("Управление: A - влево, D - вправо, Q - выход.")

def user_input(player):
    while True:
        key = read_key()
        player.move_player(key)
        time.sleep(0.1) 

def projectile_thread(spawner, player, game_time):
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time

        spawn_speed = base_spawn_speed * (1.05 ** (elapsed_time / 10))
        move_speed = base_move_speed * (1.05 ** (elapsed_time / 10))
        
        spawner.projectile_spawn(spawn_speed)
        spawner.projectile_move(move_speed, player)
        time.sleep(0.5 / move_speed) 

if __name__ == "__main__":
    player = Player()
    spawner = Spawner()
    player.place_player()
    draw_field()

    game_time = 0
    input_thread = Thread(target=user_input, args=(player,), daemon=True)
    project_thread = Thread(target=projectile_thread, args=(spawner, player, game_time), daemon=True)

    input_thread.start()
    project_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Игра завершена.")
        sys.exit()