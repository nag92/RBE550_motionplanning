import random
import pygame as pg
import spacewar_helper as helper
vec = pg.math.Vector2


class Enemy(pg.sprite.Sprite):
    def __init__(self,all_sprites,center):

        self.group = all_sprites
        pg.sprite.Sprite.__init__(self, all_sprites)
        self.image = pg.image.load("./Images/obs.png").convert()#pg.Surface((40, 40))
        #self.image.fill(helper.RED)
        self.radius  = 15
        self.mass = 10
        self.rect = self.image.get_rect()

        self.rect.center = center
        self.x = vec(center[0],center[1])
        self.xd = vec(0, 0)#vec(random.randrange(-1, 1), random.randrange(-1, 1))

    def update(self):

        self.x += self.xd
        self.rect.x = self.x.x
        self.rect.y = self.x.y

        if self.rect.bottom >= helper.HEIGHT or self.rect.top <= 0:
            self.xd.y = -self.xd.y
        if self.rect.right >= helper.WIDTH or self.rect.left <= 0:
            self.xd.x = -self.xd.x

        blocks_hit_list = pg.sprite.spritecollide(self, self.group, False)
        for block in blocks_hit_list:
            if block != self :
                self.xd.y = -self.xd.y
                self.xd.x = -self.xd.x
