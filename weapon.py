import pygame

import classes
from images import asset_finder
from json import load


class Bullet:
    def __init__(self, attrib_list, x, y):
        self.x = x
        self.y = y
        self.damage = attrib_list["damage"]
        self._types = attrib_list["type"]
        self.direction = attrib_list["direction"]
        self.sprite = asset_finder(attrib_list["sprite"])

        # chooses which direction the bullet will travel#
        direction = {"right": 1, "left": -1}
        self.speed = attrib_list["speed"] * direction[attrib_list["direction"]]

        # chooses how wide a bullet hitbox will be#
        _typesDict = {"beam": 2000, "bullet": self.sprite.get_width()}
        self.rect = pygame.Rect(self.x, self.y, _typesDict[self._types], self.sprite.get_height())

        if attrib_list["direction"] == "left":
            self.rect.right = self.rect.left-5

    def movement(self):
        self.x += self.speed

        self.rect.x = self.x


class Weapon:
    def __init__(self, weapon_json, player):
        self.bullets = []
        self.player = player

        with open("weapons.json") as armory:
            self._armory = load(armory)
            self._current_weapon = self._armory[weapon_json]


    def move(self):
        for bullet in self.bullets:
            bullet.movement()

    def FireBullet(self):

        self.bullets.append(Bullet(self._current_weapon, self.player.x, self.player.y))


    def changeWeapon(self,new_weapon):
        self._current_weapon= self._armory[new_weapon]

    def draw(self):
        for bullet in self.bullets:
            bullet.move()
    def update(self):
        pass



