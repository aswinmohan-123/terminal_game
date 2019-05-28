from getkey import getkey, keys
import os
from time import sleep

class game:
    frame_width = 50
    frame_height = 20
    player_initial_x = 25
    player_initial_y = 10
    player_current_position_x = 25
    player_current_position_y = 10
    bullet_position_x = 0
    bullet_position_y = 0
    opponent_spawn_number = 3
    player_object = '+'
    game_speed = 1
    last_direction = 'up'
    commands = [keys.UP, keys.DOWN, keys.LEFT, keys.RIGHT, keys.SPACE]


    def fire_bullet(self):
        self.bullet_position_x = self.player_current_position_x
        self.bullet_position_y = self.player_current_position_y

        while True:
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
            self.render_GUI(x=self.bullet_position_x, y=self.bullet_position_y, game_object='.', extra='bullet')
            sleep(0.05)


    def print_stats(self):
        print("frame_width => %s" % self.frame_width)
        print("frame_height => %s" % self.frame_height)
        print("initial_x => %s" % self.player_initial_x)
        print("initial_y => %s" % self.player_initial_y)
        print("current_x => %s" % self.player_current_position_x)
        print("current_y => %s" % self.player_current_position_y)
        print("opponents => %s" % self.opponent_spawn_number)
        print("speed => %s" % self.game_speed)

    def window_size_set(self):
        self.frame_width = int(input('Enter the width => '))
        self.frame_height = int(input('Enter the height => '))

    def render_GUI(self, x=None, y=None, game_object='+', extra=None):
        os.system('clear')
        if not x and not y:
            x = self.player_current_position_x
            y = self.player_current_position_y
        for h in range(0, self.frame_height):
            for w in range(0, self.frame_width):
                if h > 0 and h < self.frame_height-1:
                    if w == 0 or w == self.frame_width-1: 
                        print('*', end='')
                    else:
                        if h == y and w == x:
                            print(game_object, end='')
                        elif extra and extra == 'bullet' and h == self.player_current_position_y and w == self.player_current_position_x: 
                            print(self.player_object, end='')
                        else:
                            print(' ', end='')
                else:
                    print('*', end='')
            print('')

    def play(self, command):
        render = True
        if command not in self.commands:
            return False
        
        if command == keys.LEFT:
            self.last_direction = 'left'
            self.player_current_position_x -= 1
        elif command == keys.DOWN:
            self.last_direction = 'down'
            self.player_current_position_y += 1
        elif command == keys.RIGHT:
            self.last_direction = 'right'
            self.player_current_position_x += 1
        elif command == keys.UP:
            self.last_direction = 'up'
            self.player_current_position_y -= 1
        elif command == keys.SPACE:
            render = False
            self.fire_bullet()

        if render:
            self.render_GUI()

        return True
        
            

if __name__ == "__main__": 
    g = game()
    g.render_GUI(g.player_initial_x, g.player_initial_y)
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
