import pygame as pg
import Node
import time
TILESIZE = 64
GRIDWIDTH = 25
GRIDHEIGHT = 12
WIDTH  = 800 #TILESIZE * GRIDWIDTH
HEIGHT = 600 #TILESIZE * GRIDHEIGHT
# WIDTH = 1200
# HEIGHT = 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)
LIGHTGRAY = (140, 140, 140)

SEARCH_RANGE = 700
# Mob properties
MOB_SIZE = 16
MAX_SPEED = 4
MAX_FORCE = 0.5
font_name = pg.font.match_font('arial')


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, pg.collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, pg.collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def make_point(node):

    return Node.Node(node)


def check_point(maze, point):
    """
    see if the point
    :param point:
    :return:
    """

    #time0 = time.time()
    pt = make_point(point)
    #maze.all_sprites.add(pt)
    #print time.time() - time0
    hit_goal = pg.sprite.spritecollide(pt, maze.enemies, False)



    #print hit_goal
    #maze.all_sprites.remove(pt)
    if hit_goal:
        return 1
    else:
        return 0


def check_vertex(maze, point1, point2):
    """

    :param point1: check if the vertex is in collision
    :param point2:
    :return:
    """

    a = point2[0] - point1[0] + 0.001
    b = point2[1] - point1[1] + 0.001
    m = b / a + 0.001
    rect = [pt.rect for pt in maze.get_obsticals()]

    for obs in rect:

        p1 = obs.topleft
        p2 = obs.topright
        p3 = obs.bottomleft
        p4 = obs.bottomright

        # check y value at p1[0]
        y_at_x1 = m * (p1[0] - point1[0]) + point1[1]
        t_y_at_x1 = (p1[0] - point1[0]) / a

        # checksegments y value at p2[0
        y_at_x2 = m * (p2[0] - point1[0]) + point1[1]
        t_y_at_x2 = (p2[0] - point1[0]) / a

        # check segments x value at p1[1]
        x_at_y1 = (p1[1] - point1[1]) / m + point1[0]
        t_x_at_y1 = (p1[1] - point1[1]) / b

        # check segments x value at p3[1]
        x_at_y3 = (p3[1] - point1[1]) / m + point1[0]
        t_x_at_y3 = (p3[1] - point1[1]) / b



        if ((y_at_x1 >= p1[1]) and (y_at_x1 <= p3[1]) and (t_y_at_x1 >= 0) and (t_y_at_x1 <= 1)):
            return 0

        elif ((y_at_x2 >= p1[1]) and (y_at_x2 <= p3[1]) and (t_y_at_x2 >= 0) and (t_y_at_x2 <= 1)):
            return 0

        elif ((x_at_y1 >= p1[0]) and (x_at_y1 <= p2[0]) and (t_x_at_y1 >= 0) and (t_x_at_y1 <= 1)):
            return 0

        elif ((x_at_y3 >= p1[0]) and (x_at_y3 <= p2[0]) and (t_x_at_y3 >= 0) and (t_x_at_y3 <= 1)):
            return 0


    return 1


def get_obacle_rects(game):
    enemeis = game.get_obsticals()
    rects = []
    for en in enemeis:
        rects.append(en.rect)
    return rects
