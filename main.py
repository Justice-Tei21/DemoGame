
import pygame
import os
from classes import *
import random
import time
from images import *


pygame.init()
pygame.font.init()


WIDTH, HEIGHT = 1080, 608
FPS = 60
WHITE = (255, 255, 0)
VEL = 5
BULLET_VEL = 12
MAX_BULLETS = 5

PLAYER_WIDTH, PLAYER_HEIGHT = 64, 64

screen = pygame.display.set_mode((WIDTH, HEIGHT))


pygame.display.set_caption('Smoke')
pygame.display.set_icon(icon)


player_hit = pygame.USEREVENT + 1
enemy_hit = pygame.USEREVENT + 2
new_enemy_bullet = pygame.USEREVENT +3


def drawcontainers(image, placementy, placementx, maximum=0, objects=[]):
    offset = 0
    for amount in range(int(maximum-len(objects))):
        screen.blit(image, (offset*32+placementx, placementy))
        offset += 1


def draw_window(green, player_bullet, enemies, current_health, power_up,clock):
    #screen.fill((0, 0, 0, 1))
    screen.blit(background, (0, 0))

    for bullet in player_bullet:
        screen.blit(bullet_image, bullet)
        if power_up:
            pygame.draw.circle(screen, (0, 255, 255), bullet.rect.center, 20.0, 4)
    enemies.draw()
    green.draw()

    drawcontainers(bullet_image, 50, 10, MAX_BULLETS, player_bullet)
    drawcontainers(heart_image, 20, 10, current_health)
    a=pygame.font.Font(pygame.font.get_default_font(),20).render(str(int(clock.get_fps())),False,(0,0,0))
    screen.blit(a,(300,0))
    pygame.display.update()

bullet_image.convert_alpha()
def handle_bullets(player_bullets, green):

    # This function is redundant since it is now handled by a class
    # not actually redundant yet since i'm making the class
    for bullet in player_bullets:
        bullet.rect.x += bullet.vel

        if bullet.rect.x + bullet.width >= WIDTH or bullet.rect.x < 0:
            player_bullets.remove(bullet)


def scene(difficulty, health=10, enemies_to_kill=20, playerpos=(200, 300)):


    global MAX_BULLETS

    green = Hero(screen,playerpos[0], playerpos[1], VEL+3,space_ship)
    #bullet = Entities(screen, green.x + green.width, green.y + green.height // 2 - 3, 8, 6, 10, bullet_image)
    #yellow_menace = Hostiles(screen, WIDTH - 60, random.randint(2, HEIGHT - 50), 50, 50, 1, enemy_image)
    player_bullets = []


    timer= 0
    player_health = health
    clock = pygame.time.Clock()
    power_up = False
    RUNNING = True
    playing = True
    enemyhandler = enemyManager(screen, green, player_bullets, timer, difficulty)
    e_BulletHandler= BulletHandler()
    active = True
    while RUNNING:
        timer +=1
        timer = timer%3600
        clock.tick(FPS)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                playing= False

            if event.type == pygame.WINDOWFOCUSLOST:
                active = False
                print("dead")
            if event.type == pygame.WINDOWFOCUSGAINED:
                active = True
                print("alive again")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and len(player_bullets) < MAX_BULLETS:
                    bullet = Entities(screen, green.x + green.width+7, green.y + green.height // 2+3 , 10, bullet_image)
                    e_BulletHandler.player_bullets.append(bullet)
                    player_bullets.append(bullet)

                if event.key == pygame.K_q:
                    power_up= True
                    green.damage+=6
                    # enemyhandler.active = not enemyhandler.active

                #if event.key == pygame.K_SPACE:
                #    enemyhandler.active = not enemyhandler.active
            if event.type == player_hit:
                player_health -=1
                if player_health<=0:
                    RUNNING=False
                    pygame.quit()
        if active:
            green.update()
            handle_bullets(player_bullets, green)
            draw_window(green, player_bullets, enemyhandler, player_health, power_up, clock)
            enemyhandler.update(timer)
            if enemyhandler.enemies_killed > enemies_to_kill:
                screen.blit(asset_finder("win screen.png").convert_alpha(), (200, 200))
                pygame.display.update()
                RUNNING = False

    return player_health,enemyhandler.enemies_killed, playing,(green.x,green.y)


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


        Background=pygame.Surface((WIDTH,HEIGHT))

        Background.blit(Title, (0, 0))
        screen.blit(Background,(0, 0))


        key_pressed=pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE] and running==True:
            play=True
            running=False


        pygame.display.update()



    return play


def main():
    run = intro_screen()

    lifes = 10
    total_kills= 0
    level_amount= 5

    with open("levels.json", "r") as level_attribs:
        level_attribs = json.load(level_attribs)
    player_pos = (200, 300)
    for level in range(1,level_amount+1):

        if run:
            i = level_attribs[str(level)]
            lifes, enemies_killed ,run, player_pos = scene(i["enemy spawning"], lifes,i["enemies to kill"],(player_pos))
            total_kills += enemies_killed
    print(f"you had {total_kills} kills and survived with {lifes}, lives")
    print("total score:" + str(total_kills * lifes))



    pygame.quit()



if __name__ == '__main__':
    print(pygame.font.get_fonts())
    main()
