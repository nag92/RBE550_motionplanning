import pygame as pg
from random import randint, uniform
# from queue import Queue
import collections
vec = pg.math.Vector2
import spacewar_helper as helper

class Player(pg.sprite.Sprite):
    def __init__(self,all_sprites):

        groups = all_sprites
        pg.sprite.Sprite.__init__(self, groups)
        self.image = pg.Surface((30, 30))
        self.image.fill(helper.GREEN)
        self.rect = self.image.get_rect()
        self.pos = vec(helper.WIDTH / 2, helper.HEIGHT / 2)
        self.rect.center = self.pos
        self.vel = vec(0, 0)

    def update(self):
        self.vel = vec(0, 0)
        self.move_8way()
        self.pos += self.vel
        self.rect.center = self.pos
        # prevent sprite from moving off screen
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > helper.WIDTH:
            self.pos.x = helper.WIDTH
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.y > helper.HEIGHT:
            self.pos.y = helper.HEIGHT

    def move_8way(self):
        keystate = pg.key.get_pressed()
        if keystate[pg.K_UP]:
            self.vel.y = -10
        if keystate[pg.K_DOWN]:
            self.vel.y = 10
        if keystate[pg.K_LEFT]:
            self.vel.x = -10
        if keystate[pg.K_RIGHT]:
            self.vel.x = 10

    def update_vel(self,x,y):
        self.vel.y = y
        self.vel.x = x


