from keyboard import read_key
from threading import Thread
from colorama import Fore
import random
import time
import sys
import os

width = 26
height = 16
points = 0
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
            if field[row][col] == PROJECTILE:
                points -= 25

        for row, col in self.positions:
            field[row][col] = ' '

        self.positions = new_pos
        for row, col in self.positions:
            field[row][col] = PLAYER

        draw_field()

class Spawner:
    global projectiles
    projectiles = []
    
    @staticmethod
    def projectile_spawn(spawn_speed):
        for _ in range(int(spawn_speed)):
            spawn_x = random.randint(0, width - 1)

            if field[0][spawn_x] == ' ':
                field[0][spawn_x] = PROJECTILE

                if random.randint(1, 3) == 2:
                    projectiles.append([0, spawn_x, True])
                    field[0][spawn_x] = Fore.RED + f"{PROJECTILE}"
                    draw_field()
                    time.sleep(1)
                    field[0][spawn_x] = Fore.RESET + f"{PROJECTILE}"

                else:
                    projectiles.append([0, spawn_x, False])
        draw_field()

    @staticmethod
    def projectile_move(move_speed, player):
        global points
        for i, pt in enumerate(projectiles):
            new_row = pt[0] + int(move_speed)
            if new_row >= height:
                field[pt[0]][pt[1]] = ' '
                continue

            if field[new_row][pt[1]] == PLAYER:
                field[pt[0]][pt[1]] = ' '
                if pt[2]:
                    points += 15
                    
                else:    
                    points -= 25
                continue

            projectiles[i][0] = new_row
            field[projectiles[i][0]][projectiles[i][1]]

        draw_field()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_field():
    clear_screen()
    for row in field:
        print(Fore.RESET + ''.join(row))
    print(f"Управление: A - влево, D - вправо, Q - выход. | очки: {points}")

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
    input_thread = Thread(target=user_input, args=(player), daemon=True)
    project_thread = Thread(target=projectile_thread, args=(spawner, player, game_time), daemon=True)

    input_thread.start()
    project_thread.start()

    try:
        while True:
            time.sleep(1)
            points += 10
    except KeyboardInterrupt:
        print("Игра завершена.")
        sys.exit()