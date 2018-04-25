import FinalProject.Game.SpaceWar
import RRT.RRT as rrt
import A_star.ANA as Astar
import Queue
import time

game = FinalProject.Game.SpaceWar.SpaceWar()
import queue
import csv
import matplotlib.pyplot as plt
import math
import numpy as np
import threading
import FinalProject.Motion_Controller.Cursor as Cursor
import FinalProject.Motion_Controller.Potential_Function as PF
import FinalProject.Game.spacewar_helper as sw_helper
import pygame as pg

path = []


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def get_object(player, goals):
    max_d = 100000000000
    next_goal = None

    for goal in goals:
        distance = dist(player.center, goal.rect.center)
        if distance < max_d:
            max_d = distance
            next_goal = goal

    return next_goal


def find_path(game):
    global path
    path = []
    states = []
    alpha = 0.5

    with open("right_down.csv", "w") as file:
        writer1 = csv.writer(file)
        writer1.writerow(['x', 'y', 'xd', 'yd', 'xdd', 'ydd'])
        while len(game.get_goals()) > 0:
            goal = get_object(game.get_player(), game.get_goals())
            F_p = move_8way()
            state = cursor.move(alpha * F_p)
            states.append(state)
            game.move_player(state[3], state[4])
            writer1.writerow([state[0][0], state[1][0], state[3][0],state[4][0], F_p[0] / 1,F_p[1]])
            print "yo"

def run(game, cursor):
    global path
    (x, y) = game.player.rect.center
    cursor.set_state(np.array([[x], [y], [0], [0], [0], [0]]))

    while 1:
        # game.player.update_vel(5,-5)
        game.update()
        (x, y) = game.player.rect.center
        cursor.set_state(np.array([[x], [y], [0], [0], [0], [0]]))



def move_8way():
    F_x = 0
    F_y = 0
    mag = 80
    keystate = pg.key.get_pressed()
    if keystate[pg.K_UP]:
        F_y = mag
    if keystate[pg.K_DOWN]:
        F_y = -mag
    if keystate[pg.K_LEFT]:
        F_x = mag
    if keystate[pg.K_RIGHT]:
        F_x = -mag

    return np.array([F_x, F_y, 0])


if __name__ == "__main__":
    game = FinalProject.Game.SpaceWar.SpaceWar((500,500),1,0)
    cursor = Cursor.Cursor(1, 0.01)
    update = True

    t2 = threading.Thread(target=run, args=(game, cursor))
    t2.start()

    t1 = threading.Thread(target=find_path, args=(game,))
    t1.start()