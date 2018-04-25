import random
import pygame as pg
import spacewar_helper as helper

class Obsticals(pg.sprite.Sprite):
    def __init__(self,all_sprites, center, size):

        self.group = all_sprites
        pg.sprite.Sprite.__init__(self, all_sprites)
        self.image = pg.Surface(size)
        self.image.fill(helper.CYAN)
        self.mass = 10
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 0
        self.speedx = 0


