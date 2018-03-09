import pygame as pg
from Player import Player
from Enemy import Enemy
from Goal import Goal
from Node import Node
from Obstical import Obsticals
import spacewar_helper as helper
import random

class SpaceWar():

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((helper.WIDTH, helper.HEIGHT), pg.DOUBLEBUF | pg.HWSURFACE)
        self.clock = pg.time.Clock()
        self.all_sprites = pg.sprite.Group()
        self.RRT = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.obsticals = pg.sprite.Group()
        self.goals = pg.sprite.Group()
        self.nodes = pg.sprite.Group()
        self.player = Player(self.all_sprites)
        self.segments = []

        self.make_obsticals()
        obs_rects = helper.get_obacle_rects(self)
        temp = pg.Rect((0, 0), (30, 30))
        for i in xrange(3):
            hit = 0
            while not hit:
                temp.centerx = random.randrange(helper.WIDTH  - 15)
                temp.centery = random.randrange(helper.HEIGHT - 15)
                hit = temp.collidelist(obs_rects)

            self.enemies.add(Enemy(self.all_sprites,temp.center))


        for i in xrange(5):
            hit = 0
            while not hit:
                temp.centerx = random.randrange(helper.WIDTH - 15)
                temp.centery = random.randrange(helper.HEIGHT - 15)
                hit = temp.collidelist(obs_rects)

            self.goals.add(Goal(self.all_sprites,temp.center))


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
        self.nodes.add(pt)
        self.all_sprites.add(pt)

    def check_collisilion_goals(self):
        pass

    def get_goals(self):

        return self.goals.sprites()

    def get_obsticals(self):

        return  self.obsticals.sprites()

    def get_enemies(self):

        return  self.enemies.sprites()

    def get_player(self):

        return self.player.rect

    def draw_line(self,start,finish):
        self.segments.append((start, finish))


    def draw_path(self,points):

        for pt in xrange(len(points)-1):
            self.draw_line(points[pt],points[pt+1])


    def update_line(self):

        for pts in self.segments:
            pg.draw.line(self.screen, helper.MAGENTA , pts[0],pts[1], 1)
        self.segments = []

    def update_score(self):

        hit_goal = pg.sprite.spritecollide(self.player, self.goals, False)
        hit_enemies = pg.sprite.spritecollide(self.player, self.enemies, False)

        for hit in hit_enemies:
            self.score-=10

        for hit in hit_goal:
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

    def make_obsticals(self):
        centers = [(400,300), (50,600), (150,375),(175,300)] #[(400,300), (350,150), (150,175),(175,300),(80,100),(500,500),(10,400), (400,10),(400,400),(700,500),(500,300)]
        sizes =   [ (100,100),(80,100), (100,20), (100,170)]#[ (100,100),(80,100), (100,20), (100,170),(95,95),(100,80),(80,100), (75,135),(80,80),(100,100),(100,250)]

        for center, size in zip(centers,sizes):
            self.obsticals.add(Obsticals(self.all_sprites,center,size))

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

            pg.display.flip()
