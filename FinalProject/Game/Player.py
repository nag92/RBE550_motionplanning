import pygame as pg
from random import randint, uniform
# from queue import Queue
import collections
vec = pg.math.Vector2
import spacewar_helper as helper

class Player(pg.sprite.Sprite):
    def __init__(self,all_sprites):

        groups = all_sprites
        self.radius  = 15

        pg.sprite.Sprite.__init__(self, groups)
        self.image = pg.image.load("./Images/Player.png").convert()#pg.Surface((30, 30))
        #self.image.fill(helper.GREEN)
        self.rect = self.image.get_rect()
        self.x = vec(helper.WIDTH / 2 - 50, helper.HEIGHT / 2 - 75)
        self.rect.center = self.x
        self.xd = vec(0, 0)


    def update(self):
        #self.xd = vec(0, 0)
        #self.move_8way()
        self.x += self.xd
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

    def move_8way(self):
        keystate = pg.key.get_pressed()
        if keystate[pg.K_UP]:
            self.xd.y = -10
        if keystate[pg.K_DOWN]:
            self.xd.y = 10
        if keystate[pg.K_LEFT]:
            self.xd.x = -10
        if keystate[pg.K_RIGHT]:
            self.xd.x = 10

    def update_vel(self,x,y):
        self.xd.y = y
        self.xd.x = x


