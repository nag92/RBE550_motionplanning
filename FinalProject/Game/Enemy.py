import random
import pygame as pg
import spacewar_helper as helper

class Enemy(pg.sprite.Sprite):
    def __init__(self,all_sprites):

        self.group = all_sprites
        pg.sprite.Sprite.__init__(self, all_sprites)
        self.image = pg.image.load("./Images/obs.png").convert()#pg.Surface((40, 40))
        #self.image.fill(helper.RED)
        self.radius  = 15
        self.mass = 10
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(helper.WIDTH - self.rect.width)
        self.rect.y = random.randrange(helper.HEIGHT - self.rect.height)
        self.rect.x = random.randrange(helper.WIDTH - self.rect.width)
        self.rect.y = random.randrange(helper.HEIGHT - self.rect.height)
        self.speedy = random.randrange(-2, 2)
        self.speedx = random.randrange(-2, 2)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.bottom >= helper.HEIGHT or self.rect.top <= 0:
            self.speedy = -self.speedy
        if self.rect.right >= helper.WIDTH or self.rect.left <= 0:
            self.speedx = -self.speedx

        blocks_hit_list = pg.sprite.spritecollide(self, self.group, False)
        for block in blocks_hit_list:
            if block != self :
                self.speedy = -self.speedy
                self.speedx = -self.speedx
