import pygame as pg
from random import randint, uniform
# from queue import Queue
import collections
vec = pg.math.Vector2
import spacewar_helper as helper

class Node(pg.sprite.Sprite):
    def __init__(self,node):

        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((20, 20))
        self.image.fill(helper.YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = node




