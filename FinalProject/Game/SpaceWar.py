import pygame as pg
from Player import Player
from Enemy import Enemy
from Goal import Goal
from Node import Node
import spacewar_helper as helper

class SpaceWar():

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((helper.WIDTH, helper.HEIGHT), pg.DOUBLEBUF | pg.HWSURFACE)
        self.clock = pg.time.Clock()
        self.all_sprites = pg.sprite.Group()
        self.RRT = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.goals = pg.sprite.Group()
        self.nodes = pg.sprite.Group()
        self.player = Player(self.all_sprites)
        self.segments = []
        for i in xrange(5):
            self.enemies.add(Enemy(self.all_sprites))
        for i in xrange(3):
            self.goals.add(Goal(self.all_sprites))

        self.paused = False
        self.show_vectors = False
        self.last_update = 0
        self.running = True
        self.score = 0

    def move_player(self,vx,vy):
        self.player.update_vel(vx,vy)

    def check_collisilion_obsticals(self):
        pass

    def add_node(self,pt):
        pt = Node(pt)
        self.RRT.add(pt)
        self.nodes.add(pt)

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

    def draw_line(self,start,finish):
        self.segments.append((start, finish))

    def draw_path(self,points):
        pg.draw.lines(self.screen, helper.MAGENTA,False, points, 1)
        pg.display.flip()

    def update_line(self):

        for pts in self.segments:
            pg.draw.line(self.screen, helper.MAGENTA , pts[0],pts[1], 1)


    def update_score(self):
        hit_goal = pg.sprite.spritecollide(self.player, self.goals, False)
        hit_enemies = pg.sprite.spritecollide(self.player, self.enemies, False)

        for hit in hit_enemies:
            self.score-=10


        for hit in hit_goal:
            self.score+=10
            #hit.kill()

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
            self.RRT.draw(self.screen)

            self.update_score()
            self.update_line()
            if self.show_vectors:
                for sprite in self.all_sprites:
                    sprite.draw_vectors()
            pg.display.flip()
