import pygame
from savereader import *

'''
Code followed platformer tutorial from:
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
'''
# Global constants
global current_level_no
current_level_no = 1
total_score = 0
lives_left = 3
enemies_killed = 0
save_info = {}

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen dimensions, DO NOT CHANGE FROM 1000 to 700
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Set the height and width of the screen
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)

def message_to_screen(msg,color,x_displace=0, y_displace =0):
    nice_font = pygame.font.Font('freesansbold.ttf',24)
    textSurface = nice_font.render(msg,True,color)
    textSurf, textRect = textSurface, textSurface.get_rect()
    textRect.center = (SCREEN_WIDTH/2) + x_displace, (SCREEN_HEIGHT/2) + y_displace
    screen.blit(textSurf, textRect)

global look_forward
look_forward = True

class Player(pygame.sprite.Sprite):

    #This class represents the bar at the bottom that the player controls.

    def __init__(self):
        #Constructor function

        # Call the parent's constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # List of sprites we can bump against
        self.level = None


    def update(self):
        # Move the player.
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

    def calc_grav(self):
        #Calculate effect of gravity.
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        # Called when user hits the up arrow.

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        # Called when the user hits the left arrow.
        self.change_x = -6
        look_forward = False

    def go_right(self):
        # Called when the user hits the right arrow.
        self.change_x = 6
        look_forward = True

    def stop(self):
        # Called when the user lets off the keyboard.
        self.change_x = 0




class Shoot(Player):

    def __init__(self):

        super().__init__()

        # Create an image of the block, and fill it with a color.
        width = 2
        height = 5
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of shot
        self.change_x = 30
        self.change_y = 0

        # List of sprites we can bump against
        self.level = None

        def Fire(self):
            # Called when user hits the A key.
            if look_forward == True:
                x = False # PLACEHOLDER




class Platform(pygame.sprite.Sprite):
    # Platform the user can jump on

    def __init__(self, width, height):
        """
        Platform constructor. Assumes constructed with user passing in
        an array of 5 numbers like what's defined at the top of this code.
        """
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()


class Level():


    def __init__(self, player):

        # Constructor.

        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        # How far this world has been scrolled left/right
        self.world_shift = 0

    # Update everythign on this level
    def update(self):
        # Update everything in this level.
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        # Draw everything on this level.

        # Draw the background
        screen.fill(BLUE)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x


# Create platforms for the level
class Level_01(Level):
    # Definition for level 1.

    def __init__(self, player):
        # Create level 1.

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000
        self.level_limit_back = 200

        # Array with width, height, x, and y of platform
        level = [[210, 70, 500, 600],
                 [210, 70, 800, 500],
                 [210, 70, 1000, 600],
                 [210, 70, 1120, 380],
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


# Create platforms for the level
class Level_02(Level):
    # Definition for level 2.

    def __init__(self, player):
        # Create level 2.

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000
        self.level_limit_back = 200

        # Array with type of platform, and x, y location of the platform.
        level = [[210, 30, 450, 570],
                 [210, 30, 850, 420],
                 [210, 30, 1000, 520],
                 [210, 30, 1120, 280],
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


def main():
    pygame.init()

    #

    pygame.display.set_caption("Space Game")

    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))

    # Set the current level

    # ***This information will hopefully come from a save state after the use of our start screen ***
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    position_scroll = 0
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    # Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        restart_level = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.go_left()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.go_right()
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.jump()
                if event.key == pygame.K_SPACE:
                    shoot =  Shoot()
                    shoot.rect.x
                    shoot.fire()
                if event.key == pygame.K_r:
                    restart_level = True

            if event.type == pygame.KEYUP:
                if  (event.key == pygame.K_LEFT or event.key == pygame.K_a) and player.change_x < 0:
                    player.stop()
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and player.change_x > 0:
                    player.stop()

        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            position_scroll+= diff
            current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            position_scroll -= diff
            current_level.shift_world(diff)

        if restart_level == True:
            if position_scroll != 0:
                current_level.shift_world(position_scroll)
                position_scroll = 0
                player.rect.x = 120


        # If the player gets to the end of the level, go to the next level, if at end of last level, print you win
        mScreen = False
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            if current_level_no < len(level_list) - 1:
                player.rect.x = 120
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
                position_scroll = 0
            else:
                mScreen = True
            

        '''
        print(current_level_no, 'Boo')
        print(current_position)
        if current_position > current_level.level_limit_back and current_level_no != 0:
            player.rect.x = 120
            if current_level_no < len(level_list) - 1:
                current_level_no -= 1
                print(current_level_no)
                current_level = level_list[current_level_no]
                player.level = current_level
        '''

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        if mScreen:
            message_to_screen("You win! Yuhhhhh", RED)
        else:
            message_to_screen("Level " + str((current_level_no + 1)),RED, -400 ,-300)
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()


    pygame.quit()


if __name__ == "__main__":
    main()

# Reading and writing saves
def readSaveFile():

    save_info = readSave()

    current_level_no = save_info["game_level"]
    lives_left = save_info["lives_left"]
    total_score = save_info["total_score"]
    enemies_killed = save_info["enemies_killed"]



def writeSaveFile():

    writeSaveFile(save_info)

