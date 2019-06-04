from getkey import getkey, keys
import os
from time import sleep
import random

class game:
    game_move = 0 
    game_score = 0
    player_energy = 50
    player_life = 1
    frame_width = 50
    frame_height = 20
    player_x = 25
    player_y = 10
    bullet_position_x = 0
    bullet_position_y = 0
    opponent_spawn_number = 1
    opponent_object = '@'
    player_object = '+'
    food_object = '$'
    opponent_positions = []
    food_positions = []
    max_food = 1
    game_speed = 1
    last_direction = 'up'
    bullet_object = '.'
    infinity = 100
    commands = [keys.UP, keys.DOWN, keys.LEFT, keys.RIGHT, keys.SPACE, 'l']


    def opponent_position_update(self):
        new_opponent_positions = []
        for opponent in self.opponent_positions:
            opponent_x, opponent_y = opponent
            if self.player_x > opponent_x:
                opponent_x += 1
            else:
                opponent_x -= 1
            if self.player_y > opponent_y:
                opponent_y += 1
            else:
                opponent_y -= 1
            new_opponent_positions.append((opponent_x, opponent_y))
        self.opponent_positions = new_opponent_positions


    def check_death(self):
        if self.player_energy < 1:
            self.player_life -= 1
            self.player_energy = 50
        for opponent in self.opponent_positions:
            opponent_x, opponent_y = opponent
            if self.player_x == opponent_x and self.player_y == opponent_y:
                self.opponent_positions.remove(opponent)
                self.player_life -= 1
        for food in self.food_positions:
            food_x, food_y = food
            if self.player_x == food_x and self.player_y == food_y:
                self.food_positions.remove(food)
                self.player_energy += 10

    def fire_bullet(self):
        self.bullet_position_x = self.player_x
        self.bullet_position_y = self.player_y
        self.player_energy -= 5

        while True:
            flag = False
            if self.bullet_position_x < 0 or self.bullet_position_x > self.frame_width:
                break
            elif self.bullet_position_y < 0 or self.bullet_position_y > self.frame_height:
                break
            if self.last_direction == 'left':
                self.bullet_position_x -= 1
            elif self.last_direction == 'right':
                self.bullet_position_x += 1
            elif self.last_direction == 'up':
                self.bullet_position_y -= 1
            elif self.last_direction == 'down':
                self.bullet_position_y += 1
            if self.opponent_positions:
                for opponent in self.opponent_positions:
                    if opponent[0] == self.bullet_position_x and opponent[1] == self.bullet_position_y:
                        self.game_score += 1
                        self.bullet_position_x = self.infinity
                        self.bullet_position_y = self.infinity
                        self.opponent_positions.remove(opponent)
                        flag = True
            self.render_GUI(x=self.bullet_position_x, y=self.bullet_position_y, game_object=self.bullet_object, extra='bullet')
            if flag:
                break
            sleep(0.05)


    def print_stats(self):
        print("frame_width => %s" % self.frame_width)
        print("frame_height => %s" % self.frame_height)
        print("current_x => %s" % self.player_x)
        print("current_y => %s" % self.player_y)
        print("opponents => %s" % self.opponent_spawn_number)
        print("speed => %s" % self.game_speed)

    def window_size_set(self):
        self.frame_width = int(input('Enter the width => '))
        self.frame_height = int(input('Enter the height => '))

    def render_GUI(self, x=None, y=None, game_object='+', extra=None):
        os.system('clear')
        if not x and not y:
            x = self.player_x
            y = self.player_y
        for h in range(0, self.frame_height):
            for w in range(0, self.frame_width):
                if self.player_life < 1:
                    if w == self.frame_width//2 - 5 and h == self.frame_height//2:
                        print("GAME OVER", end='')
                    else:
                        print(" ", end='')
                else:
                    if h > 0 and h < self.frame_height-1:
                        if w == 0 or w == self.frame_width-1: 
                            print('*', end='')
                        else:
                            if h == y and w == x:
                                print(game_object, end='')
                            elif extra and extra == 'bullet' and h == self.player_y and w == self.player_x: 
                                print(self.player_object, end='')
                            elif self.opponent_positions:
                                flag = True
                                for opponent in self.opponent_positions:
                                    if w == opponent[0] and h == opponent[1]:
                                        print(self.opponent_object, end='')
                                    else:
                                        print(' ', end='')
                            elif self.food_positions:
                                for food in self.food_positions:
                                    if w == food[0] and h == food[1]:
                                        print(self.food_object, end='')
                                    else:
                                        print(' ', end='')
                            else:
                                print(' ', end='')

                        if w == self.frame_width-1 and h == 1:
                            print("   Score => %d" % self.game_score, end='')
                        if w == self.frame_width-1 and h == 2:
                            print("   Life => %d" % self.player_life, end='')
                        if w == self.frame_width-1 and h == 3:
                            print("   Energy => %d" % self.player_energy, end='')
                    else:
                        print('*', end='')
                        if w == self.frame_width-1 and h == 0:
                            print("   Game Move => %d" % self.game_move, end='')
                        
            print('')

    def play(self, command):
        render = True
        if command not in self.commands:
            return False
        
        if command == keys.LEFT:
            self.last_direction = 'left'
            self.player_x -= 1
        elif command == keys.DOWN:
            self.last_direction = 'down'
            self.player_y += 1
        elif command == keys.RIGHT:
            self.last_direction = 'right'
            self.player_x += 1
        elif command == keys.UP:
            self.last_direction = 'up'
            self.player_y -= 1
        elif command == keys.SPACE:
            render = False
            self.game_move += 1
            self.fire_bullet()
        elif command == 'l':
            self.game_move += 1
            data = [(random.randint(1, self.frame_width), random.randint(1, self.frame_height)) for i in range(0, self.opponent_spawn_number)]
            self.opponent_positions = data

        if render:
            if len(self.food_positions) < self.max_food:
                self.food_positions.append((random.randint(1, self.frame_width), random.randint(1, self.frame_height)))
            self.game_move += 1
            self.player_energy -= 1
            self.opponent_position_update()
            self.render_GUI()
            self.check_death()

        return True
        
            

if __name__ == "__main__": 
    g = game()
    g.render_GUI(g.player_x, g.player_y)
    print('Game keys are A S D W and E for exit')
    while True:
        try:
            command = getkey()
            if command == 'e':
                break
            elif command == 'k':
                g.print_stats()
            elif command == 'p':
                g.window_size_set()
            else:
                if not g.play(command):
                    break
        except KeyboardInterrupt:
            break
    
    print('Exiting the Game')
