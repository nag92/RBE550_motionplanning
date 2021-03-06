import random
import pygame as pg
import spacewar_helper as helper
vec = pg.math.Vector2


class Goal(pg.sprite.Sprite):

    def __init__(self,all_sprites,center):

        pg.sprite.Sprite.__init__(self, all_sprites)
        self.group = all_sprites
        self.radius  = 15
        self.image = pg.image.load("./Images/goal.png").convert()#pg.Surface((40, 40))
        #self.image.fill(helper.CYAN)

        self.mass = 10
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 0#random.randrange(-1, 1)
        self.speedx = 0#random.randrange(-1, 1)
        self.x  = vec(center[0], center[1])
        # self.xd = vec(random.randrange(-1, 1), random.randrange(-1, 1))
        self.xd = vec(0, 0)

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
            if block != self:
                self.xd.y = -self.xd.y
                self.xd.x = -self.xd.x

