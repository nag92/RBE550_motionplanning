import pygame as pg

TILESIZE = 64
GRIDWIDTH = 25
GRIDHEIGHT = 12
WIDTH  = 800 #TILESIZE * GRIDWIDTH
HEIGHT = 800 #TILESIZE * GRIDHEIGHT
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
RADIUS = 15
font_name = pg.font.match_font('arial')