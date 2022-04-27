import pygame

import classes
from images import asset_finder
from json import load


class SpecialTrait:
    def __init__(self,type):

        self.type = type

        self.gettrait()

    def target(self):
        pass
        #launces towards a target

    def march(self,x):
        x-=4
        #goes in a straight line

    def shoot(self,weapontype, xpos,ypos): # takes the center y and the left x of the rect
        #shoots a bullet towards the left
        Bullet(weapontype,xpos,ypos)

    def gettrait(self):
        things = {"target": self.target, "march": self.march, "shoot": self.shoot}
        return things[self.type]

class Bullet:
    def __init__(self,attrib_list,x,y):
        self.x = x
        self.y = y
        self.damage= attrib_list["damage"]
        self._types = attrib_list["type"]


        direction = {"right": 1, "left": -1}
        self.speed = attrib_list["speed"]* direction[attrib_list["direction"]]

        self.sprite= asset_finder(attrib_list["sprite"])


        _typesDict={"beam":2000, "bullet":self.sprite.get_width()}
        self.rect= pygame.Rect(self.x,self.y,_typesDict[self._types],self.sprite.get_height())

        if attrib_list["direction"]== "left":
            self.rect.right=self.rect.left-5

    def move(self):
        self.x += self.speed

        self.rect.x = self.x



class Weapon():
    def __init__(self,weapon_json,player):
        self.bullets=[]
        self.player = player




        with open("weapons.json") as armory:
            self._armory = load(armory)
            self._current_weapon= self._armory[weapon_json]




    def addBullet(self):
        if self._current_weapon["direction"]== "left":
            _pos= self.player.rect.right
        else:
            _pos= self.player.rect.left
        self.bullets.append(Bullet(self._current_weapon,_pos,self.player.y))


    def changeWeapon(self,new_weapon):
        self._current_weapon= self._armory[new_weapon]

    def draw(self):
        for bullet in self.bullets:
            bullet.move()
    def update(self):
        pass



