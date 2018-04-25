import pygame as pg
from Player import Player
from Mole import Mole
import whack_a_mole_helper as helper
import random
import time
class WhackAMole():

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((helper.WIDTH, helper.HEIGHT), pg.DOUBLEBUF | pg.HWSURFACE)
        self.clock = pg.time.Clock()
        self.all_sprites = pg.sprite.Group()
        self.moles = pg.sprite.Group()
        self.mole = Mole(self.all_sprites, (0,0))
        self.player = Player(self.all_sprites)
        self.time0 = time.time()
        self.locations = [ (0.50 * helper.WIDTH - 100, 0.25 * helper.HEIGHT - 100),
                           (0.50 * helper.WIDTH - 100, 0.50 * helper.HEIGHT - 100),
                           (0.50 * helper.WIDTH - 100, 0.90 * helper.HEIGHT - 100),

                           (0.25 * helper.WIDTH - 100, 0.25 * helper.HEIGHT - 100),
                           (0.25 * helper.WIDTH - 100, 0.50 * helper.HEIGHT - 100),
                           (0.25 * helper.WIDTH - 100, 0.9 * helper.HEIGHT - 100),

                           (0.90 * helper.WIDTH - 100, 0.25 * helper.HEIGHT - 100),
                           (0.90 * helper.WIDTH - 100, 0.50 * helper.HEIGHT - 100),
                           (0.90 * helper.WIDTH - 100, 0.90 * helper.HEIGHT - 100)
                         ]

        self.running = True

    # def update_score(self):
    #
    #
    #     for hit in hit_enemies:
    #         self.score-=10
    #
    #     for hit in hit_goal:
    #         self.score+=10
    #         hit.kill()
    #
    #     helper.draw_text(self.screen, str(self.score), 18, helper.WIDTH / 2, 10)

    def keypress(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                if event.key == pg.K_SPACE:
                    paused = not self.paused

    def update(self):

        if self.running:
            self.clock.tick(helper.FPS)
            now = pg.time.get_ticks()

            self.keypress()

            if time.time() -  self.time0 >= 3:
                self.mole.rect.center = self.locations[ random.randint(0, len(self.locations)-1)]
                self.time0 = time.time()

            #self.update_score()
            self.all_sprites.update()
            self.screen.fill(helper.DARKGRAY)

            # draw_grid()
            self.all_sprites.draw(self.screen)

            pg.display.flip()

mole = WhackAMole()
while 1:
    mole.update()