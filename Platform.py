import pygame
import pygame as pg
from savereader import *
from savewriter import *
from scorereader import *
from scorewriter import *
import time

'''
Code followed platformer tutorial from: http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py

Laser Sound from: https://www.youtube.com/watch?v=qdgwMnNMylg

Death Sound from: https://www.youtube.com/watch?v=OZdIbJZdSZw

Tile platform: https://karliszabers.itch.io/alienworld-tileset
'''
pygame.init()

pygame.display.set_caption("Space Game")


game_over_sfx = pygame.mixer.Sound('you_lose.wav')
shoot_sfx = pygame.mixer.Sound('laser.wav')
hit_sfx = pygame.mixer.Sound('hit.wav')
death_sfx = pygame.mixer.Sound('death.wav')
win_sfx = pygame.mixer.Sound('win_music.wav')

# load background
mBackg = pygame.image.load('starsBG.png')
mBackg = pygame.transform.scale(mBackg, (1000, 700))

gDisplay = pygame.display.set_mode((1000, 700))

clock = pygame.time.Clock()

# Global constants
current_level_no = 0
total_score = 0.0
current_level_score = 0.0
lives_left = 3
enemies_killed = 0
current_enemies_killed = 0
save_info = {}
save_num = 0
scores_path = "scoresfile.txt"
scores_list = []
is_paused = False
save_done = False
load_done = False
game_over = False


# gameOn = True

# Read and writing saves
# Default dict is used to handle possible errors raised by readSave(), which will cause it to return an empty dictionary
def readSaveFile(save_num):
    global current_level_no
    global lives_left
    global total_score
    global enemies_killed

    save_info = readSave(save_num)
    default_dict = {'game_level': 0, 'lives_left': 3, 'total_score': 0.0, 'enemies_killed': 0}

    try:
        current_level_no = int(save_info["game_level"])
        lives_left = int(save_info["lives_left"])
        total_score = save_info["total_score"]
        enemies_killed = int(save_info["enemies_killed"])

    except(KeyError):
        save_info = default_dict
        current_level_no = int(save_info["game_level"])
        lives_left = int(save_info["lives_left"])
        total_score = save_info["total_score"]
        enemies_killed = int(save_info["enemies_killed"])


# updateSaveInfo() sets the new dict to be saved later
def updateSaveInfo():
    global current_level_no
    global lives_left
    global total_score
    global enemies_killed

    save_info["game_level"] = current_level_no
    save_info["lives_left"] = lives_left
    save_info["total_score"] = total_score
    save_info["enemies_killed"] = enemies_killed


# setSaveInfo() is called when loading a save to update the values with the info loaded from save
def setSaveInfo():
    global current_level_no
    global lives_left
    global total_score
    global enemies_killed

    current_level_no = int(save_info["game_level"])
    lives_left = int(save_info["lives_left"])
    total_score = save_info["total_score"]
    enemies_killed = int(save_info["enemies_killed"])


# resetSaveInfo() is called when returning to start menu from game over screen
def resetSaveInfo():
    global current_level_no
    global lives_left
    global total_score
    global current_level_score
    global enemies_killed
    global current_enmies_killed

    current_level_no = 0
    lives_left = 3
    total_score = 0.0
    current_level_score = 0.0
    enemies_killed = 0
    current_enemies_killed = 0


def text_maker(text, font_a):
    surf = font_a.render(text, True, (255, 255, 255))
    return surf, surf.get_rect()


def startDis():
    text1 = 'Shape Wars: A Space Odyssey'
    text2 = 'Press ENTER to start'
    text3 = 'Press SPACE to choose load a save file'
    font_a = pygame.font.Font('freesansbold.ttf', 50)
    tSurf1, tRec1 = text_maker(text1, font_a)
    tRec1.center = (500, 200)
    tSurf2, tRec2 = text_maker(text2, font_a)
    tRec2.center = (500, 300)
    tSurf3, tRec3 = text_maker(text3, font_a)
    tRec3.center = (500, 400)
    gDisplay.blit(tSurf1, tRec1)
    gDisplay.blit(tSurf2, tRec2)
    gDisplay.blit(tSurf3, tRec3)
    pygame.display.update()


def startMenu():
    # display bkg
    gDisplay.blit(mBackg, (0, 0))

    pygame.mixer.music.stop()
    # play music
    # menuMusic attributed to: HorrorPen https://opengameart.org/users/horrorpen
    pygame.mixer.music.load('menuMusic.mp3')
    pygame.mixer.music.play(-1)

    pygame.display.update()

    # display menu
    startDis()
    pygame.display.update()

    clock.tick(60)
    start = True
    load = False
    scores = False

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameLoop()
                elif event.key == pygame.K_SPACE:
                    start = False
                    load = True
                    loadMenu()
                elif event.key == pygame.K_s:
                    start = False
                    scores = True
                    scoreMenu()

    while load:
        loadMenu()

    while scores:
        scoreMenu()

    pygame.display.update()


def pauseDis():
    global save_done

    top_text = 'PAUSED'
    save_num_text = 'Current save file: ' + str(save_num)
    save_help_text = 'Press S to save to selected save file'
    save_done_text = 'Successfully saved to save file ' + str(save_num)
    font_a = pygame.font.Font('freesansbold.ttf', 50)
    tSurf1, tRec1 = text_maker(top_text, font_a)
    tRec1.center = (500, 200)
    tSurf2, tRec2 = text_maker(save_num_text, font_a)
    tRec2.center = (500, 300)
    tSurf3, tRec3 = text_maker(save_help_text, font_a)
    tRec3.center = (500, 400)
    gDisplay.blit(tSurf1, tRec1)
    gDisplay.blit(tSurf2, tRec2)
    gDisplay.blit(tSurf3, tRec3)
    if save_done:
        tSurf4, tRec4 = text_maker(save_done_text, font_a)
        tRec4.center = (500, 450)
        gDisplay.blit(tSurf4, tRec4)
    pygame.display.update()


def pauseMenu():
    global is_paused
    global save_done
    global save_info
    global save_num
    num_keys = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

    gDisplay.blit(mBackg, (0, 0))
    pauseDis()
    pygame.display.update()
    pause_length = 0
    pause_time = pygame.time.get_ticks()
    while is_paused:
        gDisplay.blit(mBackg, (0, 0))
        pauseDis()
        pygame.display.update()
        pause_length = (pygame.time.get_ticks() - pause_time) / 1000
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    save_done = False
                    is_paused = not is_paused
                elif event.key == pygame.K_s:
                    writeSave(save_info, save_num)
                    save_done = True
                elif event.key in num_keys:
                    save_num = int(event.key) - 48
                    save_done = False

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
    return pause_length


def loadDis():
    global load_done

    top_text = " Select save location 0-9 "
    save_num_text = 'Current save file: ' + str(save_num)
    start_game_text = 'Press ENTER to start'
    load_save_text = 'Press SPACE to load selected save'
    load_done_text = 'Sucessfully loaded save #' + str(save_num)
    font_a = pygame.font.Font('freesansbold.ttf', 50)
    tSurf1, tRec1 = text_maker(top_text, font_a)
    tRec1.center = (500, 200)
    tSurf2, tRec2 = text_maker(save_num_text, font_a)
    tRec2.center = (500, 300)
    tSurf3, tRec3 = text_maker(start_game_text, font_a)
    tRec3.center = (500, 400)
    tSurf4, tRec4 = text_maker(load_save_text, font_a)
    tRec4.center = (500, 500)
    gDisplay.blit(tSurf1, tRec1)
    gDisplay.blit(tSurf2, tRec2)
    gDisplay.blit(tSurf3, tRec3)
    gDisplay.blit(tSurf4, tRec4)
    if load_done:
        tSurf5, tRec5 = text_maker(load_done_text, font_a)
        tRec5.center = (500, 450)
        gDisplay.blit(tSurf5, tRec5)
    pygame.display.update()


def loadMenu():
    global save_num
    global save_info
    global load_done
    num_keys = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

    gDisplay.blit(mBackg, (0, 0))
    loadDis()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                save_info = readSave(save_num)
                setSaveInfo()
                load_done = True
            if event.key == pygame.K_RETURN:
                load_done = False
                gameLoop()
            if event.key in num_keys:
                save_num = int(event.key) - 48
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

'''
def scoreMenu():
    global scores_list

    gDisplay.blit(mBackg, (0, 0))
    pygame.display.update()
    scores_list = readScores(scores_path)
    print(scores_list)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                startMenu()

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

'''
def gameOverDis():
    global total_score
    global current_level_score
    global enemies_killed
    global current_enemies_killed
    global current_level_no


    end_text = "Game Over"
    end_text_2 = "Press SPACE to return to Start"
    end_text_3 = "Final score: " + str(int(total_score + current_level_score))
    end_text_4 = "Enemies killed: " + str(enemies_killed + current_enemies_killed)
    end_text_5 = "Level reached: " + str(current_level_no)
    font_a = pygame.font.Font('freesansbold.ttf', 50)
    tSurf1, tRec1 = text_maker(end_text, font_a)
    tRec1.center = (500, 200)
    tSurf2, tRec2 = text_maker(end_text_2, font_a)
    tRec2.center = (500, 300)
    tSurf3, tRec3 = text_maker(end_text_3, font_a)
    tRec3.center = (500, 400)
    tSurf4, tRec4 = text_maker(end_text_4, font_a)
    tRec4.center = (500, 500)
    tSurf5, tRec5 = text_maker(end_text_5, font_a)
    tRec5.center = (500, 600)
    gDisplay.blit(tSurf1, tRec1)
    gDisplay.blit(tSurf2, tRec2)
    gDisplay.blit(tSurf3, tRec3)
    gDisplay.blit(tSurf4, tRec4)
    gDisplay.blit(tSurf5, tRec5)
    pygame.display.update()


def gameOverMenu():
    global total_score
    global current_level_score
    global enemies_killed
    global current_enemies_killed
    global game_over



    gDisplay.blit(mBackg, (0, 0))
    gameOverDis()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_over = False
            pygame.mixer.stop()
            resetSaveInfo()
            startMenu()
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit()


'''
=========================================================Colors
'''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREY = (169, 169, 169)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (53, 22, 0)

BULLET_IMG = pg.Surface((15, 9))
BULLET_IMG.fill(pg.Color('aquamarine2'))

# Screen dimensions, DO NOT CHANGE FROM 1000 to 700
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Set the height and width of the screen
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)


def message_to_screen(msg, color, x_displace=0, y_displace=0, font_size=0):
    nice_font = pygame.font.Font('freesansbold.ttf', font_size)
    textSurface = nice_font.render(msg, True, color)
    textSurf, textRect = textSurface, textSurface.get_rect()
    textRect.center = (SCREEN_WIDTH / 2) + x_displace, (SCREEN_HEIGHT / 2) + y_displace
    screen.blit(textSurf, textRect)


class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pygame.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assuming black works as the transparent color
        image.set_colorkey(BLACK)

        # Return the image
        return image


global look_forward
look_forward = True


class Player(pygame.sprite.Sprite):

    # This class represents the bar at the bottom that the player controls.

    def __init__(self):
        # Constructor function

        # Call the parent's constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        width = 30
        height = 50
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # This holds all the images for the animated walk left/right
        # of our player
        self.walking_frames_l = []
        self.walking_frames_r = []

        # What direction is the player facing?
        self.direction = "R"

        # Player Health
        self.health = 3

        # List of sprites we can bump against
        self.level = None

        sprite_sheet = SpriteSheet("astronaut.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(20, 3, 40, 50)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(80, 3, 40, 50)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(140, 3, 40, 50)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(200, 3, 40, 50)
        self.walking_frames_r.append(image)

        # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(20, 3, 40, 50)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(80, 3, 40, 50)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(140, 3, 40, 50)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(200, 3, 40, 50)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

    def update(self):
        # Move the player.
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x
        pos = self.rect.x + self.level.world_shift
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

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
        # Calculate effect of gravity.
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
        self.direction = "L"
        look_forward = False

    def go_right(self):
        # Called when the user hits the right arrow.
        self.change_x = 6
        self.direction = "R"
        look_forward = True

    def stop(self):
        # Called when the user lets off the keyboard.
        self.change_x = 0

    def collide(self, enemy, enemy_list):
        if self.rect.colliderect(enemy.rect):  # Tests if the player is touching an enemy
            self.rect.x -= 50  # Pushes player to left if hit
            self.health = self.health - 1
            hit_sfx.play()


class Bullet(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = BULLET_IMG
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.math.Vector2(pos)
        self.vel = pg.math.Vector2(450, 0)
        self.damage = 10

        # List of sprites we can bump against
        self.level = None

    def update(self, dt):

        global current_enemies_killed
        global current_level_score

        # Add the velocity to the position vector to move the sprite.
        self.pos += self.vel * dt
        self.rect.center = self.pos  # Update the rect pos.
        if self.rect.right <= 0 or self.rect.left <= -20:
            self.kill()

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            self.kill()

        block_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        for block in block_hit_list:
            self.kill()
            block.kill()
            current_enemies_killed += 1
            current_level_score += 100


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        # Create enemies

        super().__init__()

        width = 50
        height = 50
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # This holds all the images for the animated walk left/right
        # of our player
        self.walking_frames_l = []
        self.walking_frames_r = []

        # What direction is the player facing?
        self.direction = "R"

        # List of sprites we can bump against
        self.level = None

        sprite_sheet = SpriteSheet("alien.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(0, 0, 45, 60)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(45, 0, 45, 60)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(90, 0, 45, 60)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(135, 0, 45, 60)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(180, 0, 45, 60)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(225, 0, 45, 60)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(265, 0, 45, 60)
        self.walking_frames_r.append(image)

        # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(0, 0, 45, 60)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(45, 0, 45, 60)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(90, 0, 45, 60)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(135, 0, 45, 60)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(180, 0, 45, 60)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(225, 0, 45, 60)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(265, 0, 45, 60)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # set movement counter
        self.counter = 0

    # Set the position of the enemy
    def setPosition(self, x, y):
        self.rect.left = x
        self.rect.top = y

    def move(self):
        # enemy movement, paces left and right
        # distance sets how far
        # speed sets how fast
        distance = 70
        speed = 2

        if self.counter >= 0 and self.counter <= distance:
            self.direction = "R"
            self.rect.x += speed
        elif self.counter >= distance and self.counter <= distance * 2:
            self.direction = "L"
            self.rect.x -= speed
        else:
            self.counter = 0

        self.counter += 1

        # Move left/right
        # self.rect.x += self.change_x
        pos = self.rect.x
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:  # need to include left direction of enemy
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]


class Platform(pygame.sprite.Sprite):
    # Platform the user can jump on

    def __init__(self, width, height):
        """
        Platform constructor. Assumes constructed with user passing in
        an array of 5 numbers like what's defined at the top of this code.
        """
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BROWN)
        
        pltfrm = pygame.image.load('plt_tile.png')
        
        self.rect = self.image.get_rect()
        self.image.blit(pltfrm, self.rect)

class Level():

    def __init__(self, player):

        # Constructor.

        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        # Background image
        self.background = None

        # How far this world has been scrolled left/right
        self.world_shift = 0

        # local enemy list to add
        self.enemy_to_spawn = []

        #countdown timer for each level
        self.level_time = 14

    # Update everythign on this level
    def update(self):
        # Update everything in this level.
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        # Draw everything on this level.

        # Draw the background
        screen.fill(BROWN)
        screen.blit(self.background, (0,0))

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        for enemy in self.enemy_list:
            enemy.move()
            self.player.collide(enemy, self.enemy_list)  # Checks if enemy is touching player

    def shift_world(self, shift_x):

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        # function to kill and respawn all enemies upon death or restart

    def respawnEnemies(self):
        for enemy in self.enemy_list:
            enemy.kill()

        for i in range(0, len(self.enemy_to_spawn), 2):
            newEn = Enemy()
            newEn.setPosition(self.enemy_to_spawn[i], self.enemy_to_spawn[i + 1])
            self.enemy_list.add(newEn)


# Create platforms for the level
class Level_00(Level):
    # Definition for level 0.

    def __init__(self, player):
        # Call the parent constructor
        Level.__init__(self, player)

        # Set the background
        self.background = pygame.image.load("background-purple.png").convert()

        self.level_limit = -1400
        self.level_limit_back = 200

        # spawn enemies
        enemy_1 = Enemy()
        enemy_1.setPosition(775, 440)
        self.enemy_to_spawn.append(enemy_1.rect.x)
        self.enemy_to_spawn.append(enemy_1.rect.y)
        self.enemy_list.add(enemy_1)

        # Array with width, height, x, and y of platform
        level = [
        	[1500, 30, 0, -10],  # roof
        	[1500, 30, 1500, -10],  # roof
            [30, 1000, 0, 0],  # left blocking
            [500, 30, 0, 670],  # ground

            [70, 70, 500, 650],  #
            [70, 70, 700, 550],  #
            [70, 70, 750, 550],  #

            [210, 70, 500, 600],  #

            [210, 70, 800, 500],  #
            [70, 70, 1000, 550],  #
            [210, 70, 1000, 600],  #
            [210, 70, 1120, 380],  #
            [210, 30, 1400, 550],
            [210, 30, 1650, 470],
            [210, 30, 1800, 370],

            [2000, 30, 1210, 670],  # #bottom
        ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


# Create platforms for the level
class Level_01(Level):
    # Definition for level 2.

    def __init__(self, player):
        # Call the parent constructor
        Level.__init__(self, player)

        # Set the background
        self.background = pygame.image.load("background-purple.png").convert()
        
        self.level_limit = -1300
        self.level_limit_back = 200

        # spawn enemies
        enemy_1 = Enemy()
        enemy_1.setPosition(825, 360)
        self.enemy_to_spawn.append(enemy_1.rect.x)
        self.enemy_to_spawn.append(enemy_1.rect.y)
        self.enemy_list.add(enemy_1)
        enemy_2 = Enemy()
        enemy_2.setPosition(700, 640)
        self.enemy_to_spawn.append(enemy_2.rect.x)
        self.enemy_to_spawn.append(enemy_2.rect.y)
        self.enemy_list.add(enemy_2)

        # Array with width, height, x, and y of platform
        level = [
        	[1500, 30, 0, -10],  # roof
        	[1500, 30, 1500, -10],  # roof
            [30, 1000, 0, 0],  # Left blocking
            [500, 30, 0, 670],  # beg ground

            [30, 150, 500, 550],  # A
            [50, 30, 450, 550],  # B
            [150, 30, 250, 430],  # C

            [150, 30, 600, 350],  # D
            [150, 30, 850, 420],  # E
            [150, 30, 1000, 550],  # F
            [150, 30, 1120, 280],  # G

            [250, 30, 1300, 400],  # H
            [30, 150, 1550, 400],  # I
            [200, 30, 1550, 540],  # J
            [30, 150, 1750, 540],  # K

            [2000, 30, 1750, 670]  # end ground
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
        # Call the parent constructor
        Level.__init__(self, player)

        # Set the background
        self.background = pygame.image.load("background-purple.png").convert()

        self.level_limit = -1500
        self.level_limit_back = 200

        # spawn enemies
        enemy_1 = Enemy()
        enemy_1.setPosition(1450, 340)
        self.enemy_to_spawn.append(enemy_1.rect.x)
        self.enemy_to_spawn.append(enemy_1.rect.y)
        self.enemy_list.add(enemy_1)
        enemy_2 = Enemy()
        enemy_2.setPosition(1305, 640)
        self.enemy_to_spawn.append(enemy_2.rect.x)
        self.enemy_to_spawn.append(enemy_2.rect.y)
        self.enemy_list.add(enemy_2)
        enemy_3 = Enemy()
        enemy_3.setPosition(1435, 640)
        self.enemy_to_spawn.append(enemy_3.rect.x)
        self.enemy_to_spawn.append(enemy_3.rect.y)
        self.enemy_list.add(enemy_3)
        enemy_4 = Enemy()
        enemy_4.setPosition(1560, 640)
        self.enemy_to_spawn.append(enemy_4.rect.x)
        self.enemy_to_spawn.append(enemy_4.rect.y)
        self.enemy_list.add(enemy_4)

        # Array with width, height, x, and y of platform
        level = [
        	[1500, 30, 0, -10],  # roof
        	[1500, 30, 1500, -10],  # roof
            [30, 1000, 0, 0],  # Left blocking
            [500, 30, 0, 670],  # beg ground

            [150, 30, 250, 550],  # A
            [30, 30, 500, 450],  # B
            [300, 30, 600, 350],  # C
            [250, 30, 870, 670],  # D
            [200, 450, 1120, 550],  # E

            [150, 30, 1475, 400],  # F
            [150, 30, 1475, 250],  # G
            [30, 300, 1750, 500],  # H

            [2000, 30, 1750, 670]  # end ground
        ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


class Level_03(Level):
    # Definition for level 3.

    def __init__(self, player):
        # Call the parent constructor
        Level.__init__(self, player)

        # Set the background
        self.background = pygame.image.load("background-purple.png").convert()

        self.level_limit = -1400
        self.level_limit_back = 200

        # spawn enemies
        '''enemy_1 = Enemy()
        enemy_1.setPosition(1475, 290)
        self.enemy_to_spawn.append(enemy_1)
        self.enemy_list.add(enemy_1)
        enemy_2 = Enemy()
        enemy_2.setPosition(1475, 450)
        self.enemy_to_spawn.append(enemy_2)
        self.enemy_list.add(enemy_2)
        enemy_3 = Enemy()
        enemy_3.setPosition(1475, 550)
        self.enemy_to_spawn.append(enemy_3)
        self.enemy_list.add(enemy_3)
        enemy_4 = Enemy()
        enemy_4.setPosition(1475, 650)
        self.enemy_to_spawn.append(enemy_4)
        self.enemy_list.add(enemy_4)'''

        # Array with width, height, x, and y of platform
        level = [
        	[1500, 30, 0, -10],  # roof
        	[1500, 30, 1500, -10],  # roof
            [30, 1000, 0, 0],  # Left blocking
            [500, 30, 0, 670],  # beg ground
            [50, 30, 550, 550],  # A
            [50, 30, 650, 450],  # B
            [50, 30, 750, 350],  # C
            [50, 30, 850, 250],  # D
            [50, 30, 950, 150],  # E
            [50, 30, 1050, 250],  # F
            [50, 30, 1150, 350],  # G
            [50, 30, 1250, 450],  # H
            [50, 30, 1350, 550],  # I
            [50, 30, 1450, 450],  # J
            [50, 30, 1550, 350],  # K
            [50, 30, 1650, 450],  # L
            [30, 300, 1750, 500],  # M
            [2000, 30, 1750, 670]  # end ground
        ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


class Level_04(Level):
    # Definition for level 4.

    def __init__(self, player):
        # Call the parent constructor
        Level.__init__(self, player)

        # Set the background
        self.background = pygame.image.load("background-purple.png").convert()

        self.level_limit = -1400
        self.level_limit_back = 200

        # spawn enemies
        enemy_1 = Enemy()
        enemy_1.setPosition(975, 610)
        self.enemy_to_spawn.append(enemy_1.rect.x)
        self.enemy_to_spawn.append(enemy_1.rect.y)
        self.enemy_list.add(enemy_1)
        '''enemy_2 = Enemy()
        enemy_2.setPosition(1475, 450)
        self.enemy_to_spawn.append(enemy_2)
        self.enemy_list.add(enemy_2)
        enemy_3 = Enemy()
        enemy_3.setPosition(1475, 550)
        self.enemy_to_spawn.append(enemy_3)
        self.enemy_list.add(enemy_3)
        enemy_4 = Enemy()
        enemy_4.setPosition(1475, 650)
        self.enemy_to_spawn.append(enemy_3)
        self.enemy_list.add(enemy_4)'''

        # Array with width, height, x, and y of platform
        level = [
        	[1500, 30, 0, -10],  # roof
        	[1500, 30, 1500, -10],  # roof
            [30, 1000, 0, 0],  # Left blocking
        	[1500, 30, 0, 670],  # beg ground
        	[1500, 30, 1500, 670],  # beg ground

            [30, 60, 300, 640],  # A
            [30, 90, 400, 610],  # B
            [30, 120, 500, 580],  # C
            [30, 150, 600, 550],  # D
            [30, 180, 700, 520],  # E
            [30, 180, 800, 520],  # F
            [30, 150, 900, 550],  # G
            # enemy
            [30, 150, 1250, 550],  # H
            [30, 90, 1350, 610],  # I

            [50, 100, 1500, 600],  # J
            [50, 140, 1550, 560],  # K
            [50, 180, 1600, 520],  # L
            [50, 220, 1650, 480],  # M
            [50, 260, 1700, 440],  # N

        ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


def gameLoop():
    # Load required global variables
    global current_level_no
    global lives_left
    global enemies_killed
    global current_enemies_killed
    global total_score
    global current_level_score
    global is_paused
    global game_over

    # load and play game music
    # gameMusic attributed to: http://cynicmusic.com http://pixelsphere.org
    pygame.mixer.music.stop()
    pygame.mixer.music.load('gameMusic.mp3')
    pygame.mixer.music.play(-1)
    playsound = False


    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append(Level_00(player))
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
    level_list.append(Level_03(player))
    level_list.append(Level_04(player))

    # Set the current level
    current_level = level_list[current_level_no]

    # Start time of the level initialization
    starting_time = pygame.time.get_ticks()

    active_sprite_list = pygame.sprite.Group()
    enemy_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()
    player.level = current_level

    # set player position
    player.rect.x = 340
    position_scroll = 0
    player.rect.y = 500  # SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    # Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # clock for shoot
    Sentinel = 0
    look_forward = True
    dt = clock.tick(60) / 1000

    #valuable booleans for restart and end game
    endgame = False
    mScreen = False
    pause_length = 0

    # Preliminarily update save info
    updateSaveInfo()

    # -------- Main Program Loop -----------
    while not done:
        if not is_paused and not game_over:
            # boolean to restart current level
            restart_level = False

            #current level time
            current_time = (pygame.time.get_ticks()- starting_time)/ 1000
            countdown_time = current_level.level_time - current_time + pause_length


            if mScreen:
                player.jump()
            for event in pygame.event.get():

                # if window closed, quit
                if event.type == pygame.QUIT:
                    done = True

                # interpret event of keys being pressed
                if event.type == pygame.KEYDOWN and (mScreen == False and is_paused == False):
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        player.go_left()
                        look_forward = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player.go_right()
                        look_forward = True
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        player.jump()
                    if event.key == pygame.K_SPACE:
                        shoot_sfx.play()
                        Sentinel = 1
                        if look_forward == True:
                            pos = [player.rect.x + 40,
                                   player.rect.y + 30]
                            bullet = Bullet(pos)
                            bullet.vel = pg.math.Vector2(450, 0)
                            bullet.level = current_level
                            bullet_list.add(bullet)

                        elif look_forward == False:
                            pos = [player.rect.x,
                                   player.rect.y + 30]
                            bullet = Bullet(pos)
                            bullet.vel = pg.math.Vector2(-450, 0)
                            bullet.level = current_level
                            bullet_list.add(bullet)

                    if event.key == pygame.K_r:
                        restart_level = True
                    if event.key == pygame.K_p:
                        is_paused = not is_paused
                        pause_time = pygame.time.get_ticks()


                # if at end game screen, press q to quit and r to restart level
                elif event.type == pygame.KEYDOWN and mScreen == True:
                    if event.key == pygame.K_q:
                        done = True
                    if event.key == pygame.K_r:
                        restart_level = True
                        mScreen = False
                        starting_time = pygame.time.get_ticks()
                        current_time = (pygame.time.get_ticks()- starting_time)/ 1000
                        countdown_time = current_level.level_time - current_time
                        pygame.mixer.music.play(-1)
                        endgame = False

                # interpret event of keys being released
                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and player.change_x < 0:
                        player.stop()
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and player.change_x > 0:
                        player.stop()

            # Update the player.
            active_sprite_list.update()
            if Sentinel == 1:
                bullet_list.update(dt)

            # Update items in the level
            current_level.update()

            # If the player gets near the right side, shift the world left (-x)
            if player.rect.right >= 500:
                diff = player.rect.right - 500
                player.rect.right = 500
                position_scroll += diff
                current_level.shift_world(-diff)

            # If the player gets near the left side, shift the world right (+x)
            if player.rect.left <= 120:
                diff = 120 - player.rect.left
                player.rect.left = 120
                position_scroll -= diff
                current_level.shift_world(diff)

            # Player Death
            if player.health == 0 or player.rect.y >= 650 or (countdown_time < 0 and endgame == False):
                death_sfx.play()
                lives_left -= 1
                updateSaveInfo()
                player.health = 3
                restart_level = True
                if lives_left <= 0:
                	pygame.mixer.music.stop()
                	pygame.mixer.stop()
                	game_over = True
                	game_over_sfx.play()

            # if r is pressed, return block to initial level position
            if restart_level == True:
                if position_scroll != 0:
                    current_level.shift_world(position_scroll)
                    position_scroll = 0
                    player.rect.x = 120
                    player.rect.y = 500  # SCREEN_HEIGHT - player.rect.height
                    bullet_list = pygame.sprite.Group()
                    current_level.respawnEnemies()
                    starting_time = pygame.time.get_ticks()
                    pause_length = 0

            # If the player gets to the end of the level, go to the next level, if at end of last level, print you win
            current_position = player.rect.x + current_level.world_shift
            if current_position < current_level.level_limit:
                if current_level_no < len(level_list) - 1:
                    player.rect.x = 120
                    current_level_no += 1
                    current_level = level_list[current_level_no]
                    player.level = current_level
                    position_scroll = 0
                    bullet_list = pygame.sprite.Group()
                    updateSaveInfo()
                    starting_time = pygame.time.get_ticks()
                    pause_length = 0
                else:
                    mScreen = True
                    updateSaveInfo()

                    # make sure game over sound only plays once
                    if playsound == 0:
                        playsound = 1

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
            if Sentinel == 1:
                bullet_list.draw(screen)

            if mScreen:
                # stop looking for ways to kill character
                endgame = True

                pygame.mixer.music.stop()
                message_to_screen("You win! Yuhhhhh", RED, 0, -50, 25)
                message_to_screen('To quit: press q', GREY, 0, -30, 16)
                message_to_screen('To restart level: press r', GREY, 0, -15, 16)
                if playsound == 1:
                    win_sfx.play()
                    playsound += 1
                # winMusic attributed to: p0ss https://opengameart.org/users/p0ss
                #pygame.mixer.music.stop()
                #pygame.mixer.music.load('winMusic.mp3')
                #pygame.mixer.music.play(-1)
                player.stop()
            else:
                message_to_screen("Countdown: " + str(countdown_time)[:4], RED, -10, -225,30)
                message_to_screen("Level " + str((current_level_no)), RED, -400, -300, 24)
                message_to_screen("If stuck, press r to restart level", RED, -307, -275, 18)
                message_to_screen("Press P to pause", RED, -368, -250, 18)
                message_to_screen("Lives left: " + str(lives_left), RED, -390, -225, 18)
                message_to_screen("Total score: " + str(int(total_score + current_level_score)), RED, -383, -200, 18)
                message_to_screen("Enemies killed: " + str(enemies_killed + current_enemies_killed), RED, -366, -175,
                                  18)
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

            # Limit to 60 frames per second
            clock.tick(60)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

        elif is_paused:
            player.stop()
            pause_length += pauseMenu()

        # If game_over, display game over menu
        elif game_over == True:
            # gameOverMusic attributed to: t4ngr4m https://opengameart.org/users/t4ngr4m
            #pygame.mixer.music.stop()
            # play music
            #pygame.mixer.music.load('gameOverMusic.mp3')
            #pygame.mixer.music.play(-1)
            gameOverMenu()

    pygame.quit()
    quit()
'''
Killer Panda Update
                              _,add8ba,
                            ,d888888888b,
                           d8888888888888b                        _,ad8ba,_
                          d888888888888888)                     ,d888888888b,
                          I8888888888888888 _________          ,8888888888888b
                __________`Y88888888888888P"""""""""""baaa,__ ,888888888888888,
            ,adP"""""""""""9888888888P""^                 ^""Y8888888888888888I
         ,a8"^           ,d888P"888P^                           ^"Y8888888888P'
       ,a8^            ,d8888'                                     ^Y8888888P'
      a88'           ,d8888P'                                        I88P"^
    ,d88'           d88888P'                                          "b,
   ,d88'           d888888'                                            `b,
  ,d88'           d888888I                                              `b,
  d88I           ,8888888'            ___                                `b,
 ,888'           d8888888          ,d88888b,              ____            `b,
 d888           ,8888888I         d88888888b,           ,d8888b,           `b
,8888           I8888888I        d8888888888I          ,88888888b           8,
I8888           88888888b       d88888888888'          8888888888b          8I
d8886           888888888       Y888888888P'           Y8888888888,        ,8b
88888b          I88888888b      `Y8888888^             `Y888888888I        d88,
Y88888b         `888888888b,      `""""^                `Y8888888P'       d888I
`888888b         88888888888b,                           `Y8888P^        d88888
 Y888888b       ,8888888888888ba,_          _______        `""^        ,d888888
 I8888888b,    ,888888888888888888ba,_     d88888888b               ,ad8888888I
 `888888888b,  I8888888888888888888888b,    ^"Y888P"^      ____.,ad88888888888I
  88888888888b,`888888888888888888888888b,     ""      ad888888888888888888888'
  8888888888888698888888888888888888888888b_,ad88ba,_,d88888888888888888888888
  88888888888888888888888888888888888888888b,`"""^ d8888888888888888888888888I
  8888888888888888888888888888888888888888888baaad888888888888888888888888888'
  Y8888888888888888888888888888888888888888888888888888888888888888888888888P
  I888888888888888888888888888888888888888888888P^  ^Y8888888888888888888888'
  `Y88888888888888888P88888888888888888888888888'     ^88888888888888888888I
   `Y8888888888888888 `8888888888888888888888888       8888888888888888888P'
    `Y888888888888888  `888888888888888888888888,     ,888888888888888888P'
     `Y88888888888888b  `88888888888888888888888I     I888888888888888888'
       "Y8888888888888b  `8888888888888888888888I     I88888888888888888'
         "Y88888888888P   `888888888888888888888b     d8888888888888888'
            ^""""""""^     `Y88888888888888888888,    888888888888888P'
                             "8888888888888888888b,   Y888888888888P^
                              `Y888888888888888888b   `Y8888888P"^
                                "Y8888888888888888P     `""""^
                                  `"YY88888888888P'

'''

startMenu()
