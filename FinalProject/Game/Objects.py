import random
import pygame as pg
import spacewar_helper as helper

class Objects(pg.sprite.Sprite):
    def __init__(self,all_sprites,is_goal=True):

        pg.sprite.Sprite.__init__(self, all_sprites)
        self.image = pg.Surface((40, 40))
        self.goal = is_goal
        if self.goal:
            self.image.fill(helper.CYAN)
        else:
            self.image.fill(helper.RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(helper.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(-1, 2)
        self.speedx = random.randrange(-1, 1)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > helper.HEIGHT + 10 or self.rect.left < -25 or self.rect.right > helper.WIDTH + 20:
            self.rect.x = random.randrange(helper.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)