import pygame as pg
from Player import Player
from Objects import Objects
import spacewar_helper as helper

class SpaceWar():

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((helper.WIDTH, helper.HEIGHT), pg.DOUBLEBUF | pg.HWSURFACE)
        self.clock = pg.time.Clock()
        self.all_sprites = pg.sprite.Group()

        self.enemies = pg.sprite.Group()
        self.goals = pg.sprite.Group()
        self.player = Player(self.all_sprites)
        self.path = pg.Rect(0, 0, 0, 0)
        for i in xrange(10):
            self.enemies.add( Objects(self.all_sprites,False) )
            self.goals.add(Objects(self.all_sprites, True))

        self.paused = False
        self.show_vectors = False
        self.last_update = 0
        self.running = True
        self.score = 0

    def move_player(self,vx,vy):
        self.player.update_vel(vx,vy)

    def check_collisilion_obsticals(self):
        pass


    def check_collisilion_goals(self):
        pass

    def get_goals(self):
        return self.goals.sprites()
        pass

    def get_obsticals(self):
        return  self.enemies.sprites()
        pass

    def get_player(self):
        return self.player.rect
        pass

    def draw_line(self,points):
        self.path = pg.draw.lines(self.screen,helper.GREEN,  False, points, 1)
        pg.display.flip()

    def update_score(self):
        hits = pg.sprite.spritecollide(self.player, self.goals, True, pg.sprite.collide_circle)
        for hit in hits:
            self.score+=10
            hit.kill()

        helper.draw_text(self.screen, str(self.score), 18, helper.WIDTH / 2, 10)


    def keypress(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                if event.key == pg.K_SPACE:
                    paused = not self.paused
                if event.key == pg.K_v:
                    show_vectors = not self.show_vectors

    def update(self):

        if self.running:
            self.clock.tick(helper.FPS)
            now = pg.time.get_ticks()


            self.keypress()
            if not self.paused:
                self.all_sprites.update()
            self.screen.fill(helper.DARKGRAY)

            # draw_grid()
            self.all_sprites.draw(self.screen)
            self.update_score()
            if self.show_vectors:
                for sprite in self.all_sprites:
                    sprite.draw_vectors()
            pg.display.flip()
