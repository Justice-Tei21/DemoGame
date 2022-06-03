
import pygame
import os
from classes import *
import random
import time



import math


#pygame initialization
pygame.init()
pygame.font.init()
pygame.mixer.init()



#some standard values/ could be put in a config file
WIDTH, HEIGHT = 1080, 608
FPS = 60
WHITE = (255, 255, 0)
VEL = 5
BULLET_VEL = 12
MAX_BULLETS = 5
x=0
PLAYER_WIDTH, PLAYER_HEIGHT = 64, 64

#the main window
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.SCALED)




#custom events
player_hit = pygame.USEREVENT + 1
enemy_hit = pygame.USEREVENT + 2
new_enemy_bullet = pygame.USEREVENT +3

#function to make progress bars.  health/ bullet amount
def drawcontainers(i, placementy, placementx, maximum=0, objects=[]):
    offset = 0
    for amount in range(int(maximum-len(objects))):
        screen.blit(i, (offset*32+placementx, placementy))
        offset += 1

#updates the display
def draw_window(green, player_bullet, enemies, current_health, power_up,clock,bullet_con):
    #screen.fill((0, 0, 0, 1))
    global background_pos
    background_mover(background_list, background_pos)
    #screen.blit(background, (0, 0))

    for bullet in player_bullet:
        screen.blit(bullet_image, bullet)
        if power_up:
            pygame.draw.circle(screen, (0, 255, 255), bullet.rect.center, 20.0, 4)


    bullet_con.draw()
    enemies.draw()
    green.draw()


    drawcontainers(bullet_image, 50, 10, MAX_BULLETS, player_bullet)
    drawcontainers(heart_image, 20, 10, current_health)

    #font and everything for checking fps
    a=pygame.font.Font(pygame.font.get_default_font(),20).render(str(int(clock.get_fps())),False,(0,255,255))
    screen.blit(a,(300,0))
    #global x
    #x+=0.1
    #pygame.draw.arc(screen,(0,0,255),screen.get_rect(topleft=(0,0)),math.fabs(math.sin(x)*20),40)

    pygame.display.update()

def handle_bullets(player_bullets, green):

    # /This function is redundant since it is now handled by a class
    # not actually redundant yet since i'm making the class
    for bullet in player_bullets:
        bullet.rect.x += bullet.vel

        if bullet.rect.x + bullet.width >= WIDTH or bullet.rect.x < 0:
            player_bullets.remove(bullet)

def background_mover(background_lis,pos):
    for i, value in enumerate(background_lis,0):
        screen.blit(value,(pos[i],0))
        pos[i]-=10
        if pos[i] <= -WIDTH:
            pos[i] = WIDTH



def scene(difficulty, health=10, enemies_to_kill=20, playerpos=(200, 300)):

    # all of the starting values, will only be called once
    global MAX_BULLETS

    green = Hero(screen,playerpos[0], playerpos[1], VEL+3,space_ship)
    #bullet = Entities(screen, green.x + green.width, green.y + green.height // 2 - 3, 8, 6, 10, bullet_image)
    #yellow_menace = Hostiles(screen, WIDTH - 60, random.randint(2, HEIGHT - 50), 50, 50, 1, enemy_image)
    player_bullets = []


    timer= 0
    player_health = health
    clock = pygame.time.Clock()
    power_up = False
    running = True
    playing = True
    e_BulletHandler = BulletHandler(screen)
    enemyhandler = EnemyManager(screen, green, player_bullets, timer, difficulty, e_BulletHandler)
    active = True

    #the main game loop
    while running:
        timer += 1
        timer = timer % 3600
        clock.tick(FPS)


        #the event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                playing = False

            #pauses game if not active
            if event.type == pygame.WINDOWFOCUSLOST:
                active = False
                print("dead")
            if event.type == pygame.WINDOWFOCUSGAINED:
                active = True
                print("alive again")


            if event.type == pygame.KEYDOWN:
                #spawns bullet
                if event.key == pygame.K_SPACE and len(player_bullets) < MAX_BULLETS:
                    bullet = Entities(screen, green.x + green.width+7, green.y + green.height // 2+3 , 10, bullet_image)
                    e_BulletHandler.player_bullets.append(bullet)
                    player_bullets.append(bullet)

                '''
                            this is a potential powers up
                if event.key == pygame.K_q:
                    power_up= True
                    green.damage+=6
                    # enemyhandler.active = not enemyhandler.active
                    
                '''

                #Ebbe apused the pause function so I removed it
                #if event.key == pygame.K_SPACE:
                #    enemyhandler.active = not enemyhandler.active

                #remove player health
            if event.type == player_hit:
                player_health -=1
                if player_health<=0:
                    running = False
                    playing = False



        if active:
                    # the important methods and functions
            green.update()
            handle_bullets(player_bullets, green)
            draw_window(green, player_bullets, enemyhandler, player_health, power_up, clock,e_BulletHandler,)
            enemyhandler.update(timer)
            e_BulletHandler.update(green)
            if enemyhandler.enemies_killed > enemies_to_kill:
                screen.blit(asset_finder("win screen.png").convert_alpha(), (200, 200))
                pygame.display.update()
                running = False
        #values used for next scene
    return player_health,enemyhandler.enemies_killed, playing,(green.x,green.y)


    #displays total score at the end
def end_credits(kills, lives):

    running = True

    text= f'you had {kills} kills and survived with {lives} lives'
    a = pygame.font.Font(pygame.font.get_default_font(), 20).render(text, False, (0, 255, 255))
    score = f'total score:{kills*lives}'
    b=pygame.font.Font(pygame.font.get_default_font(), 20).render(score, False, (0, 255, 255))
    screen.blit(a, (300, 400))

    pygame.mixer.music.stop()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        screen.blit(a, (300, 40))
        screen.blit(b, (300, 400))



        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE] and running == True:
            running = False

        pygame.display.update()

#a nice intro screne/press space
def intro_screen():

    running= True
    play=False

    Title=asset_finder('titleScreen.png')


    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        screen.fill((0,0,0))


        if time.time()%1>0.5:
            HEIGHT=300
        else:
            HEIGHT=608

        background = pygame.Surface((WIDTH,HEIGHT))

        background.blit(Title, (0, 0))
        screen.blit(background,(0, 0))


        key_pressed=pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE] and running==True:
            play=True
            running=False


        pygame.display.update()


    pygame.mixer.music.play(-1)
    return play


def main():
    #play intro
    run = intro_screen()

    lifes = 10
    total_kills= 0
    ##level_amount= 5   found a better way without numbers
    #gets the levels with attibs
    with open("levels.json", "r") as level_attribs:
        level_attribs = json.load(level_attribs)
    player_pos = (200, 300)
    #plays every level in dict
    for level in level_attribs:       #range(1,level_amount+1)

        if run:
            i = level_attribs[str(level)]
            lifes, enemies_killed ,run, player_pos = scene(i["enemy spawning"], lifes,i["enemies to kill"],(player_pos))
            total_kills += enemies_killed



    #play end credits
    end_credits(total_kills, lifes)


    pygame.quit()


#makes sure files other than this file don't call the main function
if __name__ == '__main__':

    #unsure if other files will
    from images import *

    pygame.display.set_caption('space dust')
    pygame.display.set_icon(icon)

    #images for the background
    background.convert_alpha()
    background_list = [background, background]
    background_pos = [0, WIDTH]
    pygame.mixer.music.load(os.path.join('assets', 'space_opera.mp3'))


    bullet_image.convert_alpha()

    #where the game is played
    main()
