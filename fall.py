import sys 
import random

width = 20
height = 16
PLAYER = '█'
PROJECTILE = '*'
spawn_speed = 1
move_speed = 1
field = [[' ' for _ in range(width + 1)] for _ in range(height + 1)]

def draw_field():
    for i in field:
        print(''.join(i))
    print(Player.find_player())
    print("\nУправление: A - влево, D - вправо. Q - выход.")

class Player:
    def place_player():
        for i in range(3):
            field[height][(width // 2) - 2 + i] = PLAYER
        return None
    
    def find_player():
        positions = []
        for i in range(height + 1):
            for j in range(width):
                if field[i][j] == PLAYER:
                    positions.append((i, j))
        return positions if len(positions) > 0 else None
    
    def move_player(move):
        player_pos = Player.find_player()
        new_pos = []
        move.lower()

        if move == 'q':
            print("Игра завершена.")
            sys.exit()

        elif move == 'a':
            for i in range(len(player_pos)):
                field[player_pos[i][0]][player_pos[i][1]] = ' '
                new_pos.append((player_pos[i][0], player_pos[i][1] - 1))
            draw_field()  

        elif move == 'd':
            for i in range(len(player_pos)):
                field[player_pos[i][0]][player_pos[i][1]] = ' '
                new_pos.append((player_pos[i][0], player_pos[i][1] + 1))
            draw_field() 

        for i in range(len(new_pos)):
            field[new_pos[i][0]][new_pos[i][1]] = PLAYER
            draw_field()

class Spawner:

    def projectile_spawn(spawn_speed):
        for i in range(spawn_speed):
            spawn_x = random.randint(0, width)
            field[0][spawn_x] = PROJECTILE
            draw_field()
    
    def projectile_move(move_speed):
        field[height - 1] = field[height]
        field.pop(height)
        field.insert(0, [' ' for _ in range(width)])
        draw_field()
        
if __name__ == "__main__":
    Player.place_player()
    draw_field()
    while True:
        Player.move_player(move = input('Ваш ход: ').lower())
        Spawner.projectile_spawn(spawn_speed)
        Spawner.projectile_move(move_speed)