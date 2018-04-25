import pygame as pg
from random import randint, uniform
# from queue import Queue
import collections
vec = pg.math.Vector2
import spacewar_helper as helper

class Player(pg.sprite.Sprite):
    def __init__(self,all_sprites):

        self.group = all_sprites
        self.radius  = 15
        pg.sprite.Sprite.__init__(self, self.group)
        self.image = pg.image.load("./Images/Player.png").convert()#pg.Surface((30, 30))
        #self.image.fill(helper.GREEN)
        self.rect = self.image.get_rect()
        self.x = vec(helper.WIDTH / 2 - 100, helper.HEIGHT / 1.5 - 100)
        self.rect.center = self.x
        self.xd = vec(0, 0)


    def update(self):

        #self.xd = vec(0, 0)
        #self.move_8way()
        #self.x += self.xd
        self.rect.center = self.x
        # prevent sprite from moving off screen
        if self.x.x < 0:
            self.x.x = 0
        if self.x.x > helper.WIDTH:
            self.x.x = helper.WIDTH
        if self.x.y < 0:
            self.x.y = 0
        if self.x.y > helper.HEIGHT:
            self.x.y = helper.HEIGHT


    def update_vel(self,x,y):
        self.x.y = y
        self.x.x = x
        #self.rect.center = self.x

