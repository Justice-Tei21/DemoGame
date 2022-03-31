import time

import pygame
import os
from images import *
from classes import *
import random





pygame.init()

WIDTH, HEIGHT = 1080, 608
FPS = 60
WHITE = (255, 255,0)
VEL = 5
BULLET_VEL = 11
MAX_BULLETS = 5

PLAYER_WIDTH, PLAYER_HEIGHT = 64, 64

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Smoke')
pygame.display.set_icon(icon)


player_hit = pygame.USEREVENT + 1
enemy_hit= pygame.USEREVENT +2

def drawcontainers(image, offset,placementy, placementx, maximum=0,objects=[]):
    offset=0
    for amount in range(int(maximum-len(objects))):
        screen.blit(image,(offset*32+placementx,placementy))
        offset += 1

def draw_window(green, player_bullet, enemies,current_health):
    #screen.fill(WHITE)
    screen.blit(background, (0, 0))


    enemies.draw()
    green.draw()
    for bullet in player_bullet:
        screen.blit(bullet_image, bullet)

    drawcontainers(bullet_image,0,50,10,MAX_BULLETS,player_bullet)
    drawcontainers(heart_image,20,20,10,current_health)
    pygame.display.update()


def handle_bullets(player_bullets, green):
    #This function is redundant since it is now handled by a class

    for bullet in player_bullets:
        bullet.rect.x += bullet.vel

        if green.rect.colliderect(bullet):

            player_bullets.remove(bullet)

        if bullet.rect.x + bullet.width >= WIDTH or bullet.rect.x < 0:
            bullet.vel = -bullet.vel



def main(frequency):
    global MAX_BULLETS

    green = Hero(screen,200, 300, PLAYER_WIDTH, PLAYER_HEIGHT,VEL+3,space_ship)
    #bullet = Entities(screen, green.x + green.width, green.y + green.height // 2 - 3, 8, 6, 10, bullet_image)
    #yellow_menace = Hostiles(screen, WIDTH - 60, random.randint(2, HEIGHT - 50), 50, 50, 1, enemy_image)
    player_bullets = []
    enemies_alive = []
    timer= 0
    player_health = 10
    clock = pygame.time.Clock()
    RUNNING = True
    enemyhandler = enemyManager(screen, green, player_bullets,timer,[["yellow",frequency]])


    while RUNNING:
        timer +=1
        timer = timer%FPS
        clock.tick(FPS)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and len(player_bullets) < MAX_BULLETS:
                    bullet = Entities(screen, green.x + green.width, green.y + green.height // 2 - 3, 8, 6, 10,
                                      bullet_image)
                    player_bullets.append(bullet)
                if event.key == pygame.K_q:
                    MAX_BULLETS+=1
            if event.type == player_hit:
                player_health -=1

        green.update()

        handle_bullets(player_bullets, green)
        draw_window(green, player_bullets, enemyhandler,player_health)
        enemyhandler.update(timer)
        if enemyhandler.enemies_killed>20:
            RUNNING=False
            pygame.quit()
            print('you win')


    return enemies_alive, player_health




def intro_screen():

    running= True
    play=False

    Title=asset_finder('titleScreen.png')

    skull1= asset_finder('Skull1.jpg').set_colorkey((136,0,27))
    skull2= asset_finder('Skull2.jpg').set_colorkey((136,0,27))
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



if __name__ == '__main__':
    run = intro_screen()
    if run:
        a = main(["yellow",60])
        pygame.quit()