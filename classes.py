import random

import pygame
from pygame import draw
from main import *


class Entities:
    def __init__(self, screen, x, y, width, height, vel, image,damage):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.damage = damage
        self.vel = vel
        self.image = image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.vector = pygame.math.Vector2(self.rect.centerx, self.rect.centery)


class Hostiles:
    def __init__(self, screene, x, y, width, height, vel, image,HP):
        self.screen = screene
        self.x = x
        self.y = y
        self.HP = HP
        self.animation_count=0
        self.width = width
        self.height = height
        self.vel = vel
        self.image = image
        self.time_of_launch = random.randint(100,800)
        self.new_vel = random.randint(0,self.vel+3)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
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

    def death(self):
        if self.HP <1:
            pass





class Hero(Entities):

    def player_movement(self):
        keys_pressed=pygame.key.get_pressed()

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

class Bullet(Entities):
    pass




class enemyManager:
    def __init__(self,screen):