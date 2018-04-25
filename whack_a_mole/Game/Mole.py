import random
import pygame as pg
import whack_a_mole_helper as helper

class Mole(pg.sprite.Sprite):
    def __init__(self,all_sprites,center):
        pg.sprite.Sprite.__init__(self, all_sprites)
        self.group = all_sprites
        self.radius  = 15
        self.image = pg.image.load("mole.png").convert().convert_alpha()#
        #self.image.fill(helper.CYAN)

        self.mass = 10
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 0#random.randrange(-1, 1)
        self.speedx = 0#random.randrange(-1, 1)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.bottom >= helper.HEIGHT or self.rect.top <= 0:
            self.speedy = -self.speedy
        if self.rect.right >= helper.WIDTH or self.rect.left <= 0:
            self.speedx = -self.speedx

        blocks_hit_list = pg.sprite.spritecollide(self, self.group, False)
        for block in blocks_hit_list:
            if block != self:
                self.speedy = -self.speedy
                self.speedx = -self.speedx

