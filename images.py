import os
import pygame





def asset_finder(png):
    asset=pygame.image.load(os.path.join('assets', str(png)))
    return asset
STATIC_IMAGE= asset_finder('static.png')
STATIC=pygame.transform.rotate(pygame.transform.scale(STATIC_IMAGE,(50,20)),60)


#pygame.image.load(os.path.join('assets', 'static.png'))

PLAYER=pygame.transform.scale(asset_finder('playerpng.png'),(50,70))
space_ship=pygame.transform.scale((asset_finder('space_ship.png')),(50,50))
background=asset_finder(('starry_background.png'))
icon= asset_finder('icon.png')
bullet_image= pygame.transform.scale(asset_finder(('yellow_bullet.png')),(24,24))
enemy_image =pygame.transform.scale(asset_finder('yellow_enemy.png'),(50,70))
heart_image = asset_finder('heart.png')



