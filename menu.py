import pygame
import time

pygame.init()

#load music
pygame.mixer.music.load('menuMusic.mp3')

#load background
mBackg = pygame.image.load('starsBG.png')
mBackg = pygame.transform.scale(mBackg, (1000,700))

gDisplay = pygame.display.set_mode((1000,700))

pygame.display.set_caption('Main Menu')

clock = pygame.time.Clock()

#gameOn = True

def text_maker(text, font_a):
    surf = font_a.render(text, True, (255,255,255))
    return surf, surf.get_rect()

def menu_dis ():
    text1 = 'Shape Wars: A Space Odyssey'
    text2 = 'Press ENTER to Start'
    font_a =  pygame.font.Font('freesansbold.ttf', 50)
    tSurf1, tRec1 = text_maker(text1, font_a)
    tRec1.center = (500, 200)
    tSurf2, tRec2 = text_maker(text2, font_a)
    tRec2.center = (500, 300)
    gDisplay.blit(tSurf1, tRec1)
    gDisplay.blit(tSurf2, tRec2)
    pygame.display.update()


def startMenu():


    #display bkg
    gDisplay.blit(mBackg, (0,0))
    #play music
    pygame.mixer.music.play(-1)

    pygame.display.update()

    #display menu
    menu_dis()
    pygame.display.update()


    clock.tick(60)
    start = True

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    quit()

    pygame.display.update()


#while gameOn:

    #for event in pygame.event.get():

        #if event.type == pygame.QUIT:
            #gameOn = False




    #pygame.display.update()

    #clock.tick(60)


#quit()

startMenu()
pygame.quit()
quit()