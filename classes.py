import random
import time

import pygame

import weapon
from images import asset_finder
from main import WIDTH,HEIGHT, player_hit,enemy_hit, new_enemy_bullet


import json



#basic entity class, Not sure if it's used
class Entities:  # base class for all entities/ only used for the player
    def __init__(self, screene, x, y, vel, image):
        #super().__init__()   for if you want to use sprite class
        self.screen = screene
        self.x = x
        self.y = y

        self.vel = vel
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))
        self.vector = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        self.height = self.rect.height
        self.width = self.rect.width



#the class of the enemy
class Hostiles:
    def __init__(self, screen, x, y, vel, image, hp, special, bullet_con): #  lägg till bullet list
        # super().__init__()
        self.screen = screen
        self.x = x
        self.y = y*32
        self.HP = hp
        self.animation_count = 0
        self.vel = vel[0]
        self.image = asset_finder(image).convert_alpha()
        self.time_of_launch = random.randint(100, 800)
        self.new_vel = random.randint(vel[1][0], vel[1][1])
        self.bullet_con = bullet_con


        self.special = special  # the state of the class
        actions = {"shoot": self.shot_everything, "target": self.target, "march": self.marching_on}
        self.special_action = actions[special]

        self.rect = self.image.get_rect(midleft=(self.x, self.y))  # pygame.Rect(self.x, self.y, self.width, self.height)
        self.targeting = False
        #self.vector = pygame.math.Vector2(self.rect.centerx, self.rect.centery)



    def draw(self):
        # mix mellan draw och update metoderna
        #self.rect.move(int(self.vector.x),int(self.vector.y))
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        self.screen.blit(self.image, (self.rect.x, self.rect.y))



    def movement(self, target):

        if self.targeting:
            #self.target()
            self.special_action()

        elif self.x < WIDTH - 400 and self.targeting == False:

            self.targeting = True
            self.vel = self.new_vel


            #values used for targeting special
            if self.special == "target":
                own_vector = pygame.Vector2(self.x,self.y)



                bullet_vector = pygame.Vector2(target.x,target.y)
                self.vector = bullet_vector - own_vector
                self.vector.scale_to_length(self.vel)

                #init shooting values
            if self.special== "shoot":
                self.shooting= True
                self.timer = time.time()

        if not self.targeting:
            #self.rect = self.rect.move(self.move_rect)
            pygame.draw.rect(self.screen,(211,211,222),self.rect)
            self.x-=self.vel


                            # the three states
    def shot_everything(self):

            #bang bang
        curr_time = time.time()
        if curr_time - self.timer > 2:

            self.timer = curr_time
            image = pygame.Surface((50,50))
            image.fill((255,0,0))
            self.bullet_con.addbullet(self.rect.center)
            


    def target(self):
            #target locked

        self.x = self.x + self.vector.x

        self.y = self.y + self.vector.y


    def marching_on(self):
            #it's a long way to tipperary
        self.x-=self.vel


#the players class
class Hero(Entities):
    def __init__(self,*args):
        super().__init__(*args)
        self.damage=1


        # the players movement and barriers
    def player_movement(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_d] and self.x + self.width < WIDTH:  # höger
            self.x = self.x + self.vel
        if keys_pressed[pygame.K_w] and self.y > 0:  # upp
            self.y = self.y - self.vel
        if keys_pressed[pygame.K_a] and self.x > 0:  # vänster
            self.x = self.x - self.vel
        if keys_pressed[pygame.K_s] and self.y + self.height < HEIGHT:  # ner
            self.y = self.y + self.vel

        self.rect.x = self.x
        self.rect.y = self.y
        #self.vector = pygame.math.Vector2(self.x, self.y)


    def draw(self):
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        #eeanimation = [self.image]  # there is no animation

        self.screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.player_movement()


# adds and removes enemies and handles all of their physics and events
class EnemyManager:
    def __init__(self, screen, player, bullets, clock, enemy_types, bullet_list):
        self.enemies = []
        self.screen = screen
        self.player = player
        self.bullets = bullets
        self.clock = clock
        self.timer_length = 601
        self.enemies_killed = 0
        self.enemy_types = enemy_types
        self.active = True
        self.bullet_con = bullet_list


            #takes the attribs from the dict and
        with open("enemies.json", "r") as enemy_list:
            self.enemy_attribs = []
            enemy_json_file = json.load(enemy_list)
            for ship in enemy_types:
                # print(self.enemy_types)
                # print(ship)
                aa = enemy_json_file[str(ship[0])]
                speeds = aa["movement"]
                sprite = aa["sprite"]
                hp = aa["health"]
                special = aa["special"]
                # print(ship[1])
                # aa = Hostiles(screen, WIDTH+60, random.randint(1, 17), speeds, sprite, hp, special)
                self.enemy_attribs.append([speeds, sprite, hp, ship[1], special])

    #  creates an enemy of a certain type and adds it to the current list
    def addenemy(self):


            #item is a type of enemy, like green or blueship
        for item in self.enemy_attribs:  # maybe use enemy_type

            if self.clock % item[3] == 0:
                an_enemy = Hostiles(self.screen, WIDTH, random.randint(1, 17), item[0], item[1],
                                    item[2], item[4], self.bullet_con)

                self.enemies.append(an_enemy)

    def draw(self):
        #blits every enemy
        for enemy in self.enemies:
            enemy.draw()

    def move(self):

            #excecutes movement method
        for enemy in self.enemies:
            enemy.movement(self.player)

            #takes life if too far right
            if enemy.rect.right < 0:
                pygame.event.post(pygame.event.Event(player_hit))
                self.enemies.remove(enemy)

        #handles collision and events
    def enemy_collisions(self):
        for enemy in self.enemies:

            if enemy.rect.colliderect(self.player):
                pygame.event.post(pygame.event.Event(player_hit))
                self.enemies.remove(enemy)
            else:
                for bullet in self.bullets:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.HP -= self.player.damage
                        self.killenemy(enemy)
                        self.bullets.remove(bullet)
        #removes enemy from list. garbage collector removes from memory
    def killenemy(self, enemy):
        if enemy.HP < 1:
            self.enemies.remove(enemy)
            self.enemies_killed += 1


    def update(self, timer):
        if self.active:  #this was part of ebbe's exploit
            self.addenemy()
            self.move()
            self.intimer(timer)
        self.enemy_collisions() #this was the main crux of his exploit

    def intimer(self, timer):
        self.clock += 1
        self.clock %= 3600


#class Bullet(Entities):

#    def move(self):
#        self.x += self.vel



#deal with the enemy bullets
class BulletHandler:
    def __init__(self, screen):
        self.enemybullets = []
        self.player_bullets = [] #don't think this is used
        self.screen = screen
        self.image = asset_finder("static.png").convert_alpha()



        #add bullet to the enemy bullet list
    def addbullet(self, position):
        self.enemybullets.append(self.image.get_rect(center=(position)))

        #checks if a bullet collides and checks for proper protocol
    def collision(self,player,bullet):
        #for bullet in self.enemybullets:

            #start the playerhit event
        if bullet.colliderect(player.rect):
            pygame.event.post(pygame.event.Event(player_hit))
            self.enemybullets.remove(bullet)

            #deletes bullet for reuse
        if bullet.x + bullet.width >= WIDTH or bullet.x < 0:
            self.enemybullets.remove(bullet)


    #moves the bullet
    @staticmethod
    def move(bullet):
        bullet.x -= 12

        #sepatrate from the update becauseof how blit works
    def draw(self):
        for bullet in self.enemybullets:
            self.screen.blit(self.image, bullet.topleft)

        #bullet updater
    def update(self, player):
        for bullet in self.enemybullets:
            self.move(bullet)
            self.collision(player, bullet)

