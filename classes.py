import random

import pygame
from pygame import draw
from main import *

import json







class Entities(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, width, height, vel, image):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect(midbottom=(self.x,self.y))#pygame.Rect(self.x, self.y, self.width, self.height)
        self.vector = pygame.math.Vector2(self.rect.centerx, self.rect.centery)

class Hostiles(pygame.sprite.Sprite):
    def __init__(self, screene, x, y, width, height, vel, image,HP):
        super().__init__()
        self.screen = screene
        self.x = x
        self.y = y*32
        self.HP = HP
        self.animation_count=0
        self.width = width
        self.height = height
        self.vel = vel
        self.image = image.convert_alpha()
        self.time_of_launch = random.randint(100,800)
        self.new_vel = random.randint(0,self.vel+3)

        self.rect = self.image.get_rect(midbottom=(self.x,self.y))#pygame.Rect(self.x, self.y, self.width, self.height)
        self.targeting= False
        self.vector = pygame.math.Vector2(self.rect.centerx, self.rect.centery)

    def draw(self):
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        animation=[self.image]
        if self.animation_count > len(animation)-1:
            self.animation_count = 0



        self.screen.blit(animation[self.animation_count],(self.x,self.y))
        self.animation_count += 1



    def target(self):




        self.x = self.x + self.vector.x
        print(self.vector)
        self.y = self.y + self.vector.y


    def movement(self, target):

        if self.targeting:
            self.x = self.x + self.vector.x
            self.y = self.y + self.vector.y


        if self.x< WIDTH - 400 and self.targeting == False:
            self.targeting = True
            self.vel=self.new_vel
            self.target_vector = target.vector
            bullet_vector = self.vector
            bullet_vector.y += random.randrange(6,14)+5#//10
            bullet_vector = self.target_vector - bullet_vector
            self.vector = bullet_vector.normalize() * self.vel




        if self.targeting== False:
            self.x-=self.vel



"""
class Bullet(Entities):
    def __init__(self,*args):
        super().__init__(*args)
"""


class Hero(Entities):
    def __init__(self,*args):
        super().__init__(*args)
        self.damage=1
    def player_movement(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_d] and self.x + self.width < WIDTH:  # höger
            self.x = self.x + VEL
        if keys_pressed[pygame.K_w] and self.y > 0:  # upp
            self.y = self.y - VEL
        if keys_pressed[pygame.K_a] and self.x > 0:  # vänster
            self.x = self.x - VEL
        if keys_pressed[pygame.K_s] and self.y + self.height < HEIGHT:  # ner
            self.y = self.y + VEL

        self.rect.x = self.x
        self.rect.y = self.y
        self.vector = pygame.math.Vector2(self.rect.centerx, self.rect.centery)

    def draw(self):
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        animation = [self.image]

        self.screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.player_movement()



class enemyManager:
    def __init__(self,screen,player,bullets,clock,enemy_types=[]):
        self.enemies= []
        self.screen= screen
        self.current_enemy= Hostiles(screen, WIDTH + 60, random.randint(1,17 ), 50, 50, 3, enemy_image,2)
        self.player= player
        self.bullets= bullets
        self.clock = clock
        self.timer_length= 60
        self.enemies_killed = 0


        with open("enemies.json", "r") as enemy_types:
            self.aa = json.load(enemy_types)


    def addEnemy(self):

        yellow_enemy= Hostiles(screen, WIDTH + 60, random.randint(1,17 ), 50, 50, 3, enemy_image,1)
        if self.clock  == 1:
            self.current_enemy= yellow_enemy
            self.enemies.append(self.current_enemy)# remove an indent and everyting turns to hell
    def draw(self):

        for enemy in self.enemies:
            enemy.draw()

    pygame.display.update()
    def move(self):
        for enemy in self.enemies:
            enemy.movement(self.player)

            if enemy.rect.right<0:
                self.enemies.remove(enemy)
    def enemy_collisions(self):
        for enemy in self.enemies:

            if enemy.rect.colliderect(self.player):
                pygame.event.post(pygame.event.Event(player_hit))
                self.enemies.remove(enemy)
            else:
                for bullet in self.bullets:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.HP -= self.player.damage
                        self.killEnemy(enemy)
                        self.bullets.remove(bullet)# remove an indent and everyting turns to hell

    def killEnemy(self,enemy):
        if enemy.HP<1:
            self.enemies.remove(enemy)
            self.enemies_killed+=1
    def update(self,timer):

        self.addEnemy()
        self.move()
        self.inTimer(timer)
        self.enemy_collisions()

    def inTimer(self,timer):
        self.clock = timer
        self.clock = self.clock% self.timer_length


