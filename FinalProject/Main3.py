import FinalProject.Game.SpaceWar
import math
import numpy as np
import threading
import FinalProject.Motion_Controller.Cursor as Cursor
import pygame as pg
from FinalProject.DMP.Python.Mod_DMP_runner import  Mod_DMP_runner
import matplotlib.pyplot as plt


full_path = "/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_DMP/"

def get_DMP(player,goal):

    dx = player[0] - goal[0]
    dy = player[1] - goal[1]
    theta = math.atan2( dy, dx )

    # 0 = right/left, 1 = up/down
    axis = abs(dx) > abs(dy)
    sign_x = np.sign(dx) == 1
    sign_y = np.sign(dy) == 1

    if axis:
        if not sign_x:
            file = "right"
        else:
            file="left"
    else:
        if  sign_y:
            file = "up"
        else:
            file="down"

    return full_path + file


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def get_goal(player, goals):
    max_d = 100000000000
    next_goal = None

    for goal in goals:
        distance = dist(cursor.state, goal.rect.center)
        if distance < max_d:
            max_d = distance
            next_goal = goal

    return next_goal

def run(game, cursor):

    tau = 3
    dt = 0.001

    (x, y) = game.player.rect.center
    cursor.set_state(np.array([[np.array([x])], [np.array([y])], [0], [0], [0], [0]]))
    X = []
    Y = []
    runner_y = []
    runner_x = []
    count = 0
    while len(game.get_goals()) > 0:

        goal = get_goal(game.get_player(), game.get_goals())
        print goal.rect.center
        dmp_file = get_DMP(cursor.state,goal.rect.center)
        print dmp_file
        my_runner_x = None
        my_runner_y = None
        print cursor.state[1]
        runner_y.append(Mod_DMP_runner(dmp_file + "_y.xml", np.asscalar(cursor.state[1]) , goal.rect.centery))
        runner_x.append(Mod_DMP_runner(dmp_file + "_x.xml", np.asscalar(cursor.state[0]) , goal.rect.centerx))
        err_x = 0
        err_y = 0

        print "next"
        for i in np.arange(0, (tau / dt) + 1):

            (x_t, xd_t, xdd_t) =runner_x[count].step(tau, dt, error=err_x)
            (y_t, yd_t, ydd_t) = runner_y[count].step(tau, dt, error=err_y)

            # f = avoid_obstacles(np.array([x_t,y_t]),np.array([xd_t,yd_t]) ,my_runner_y.g)
            # print "obs", np.array([[obstacles[0]],[obstacles[1]]])
            up = 20 * (np.array([[x_t], [y_t], [0]]) - cursor.state[0:3])
            uv = 20 * (np.array([[xd_t], [yd_t], [0]]) - cursor.state[3:])

            F = np.array([[xdd_t], [ydd_t], [0]]) - up - uv
            #cursor.set_state(np.array([[x_t], [y_t], [0], [0], [0], [0]]))
            cursor.move(F)
            err_x = np.asscalar(0.1 * abs(cursor.state[0] - x_t))[0]
            err_y = np.asscalar(0.1 * abs(cursor.state[1] - y_t))[0]
            X.append(cursor.state[0])
            Y.append(cursor.state[1])
            game.move_player(cursor.state[0], cursor.state[1])
            game.update()

        print "yp"
        count += 1
    time_step = np.arange(0, (1 / .001) + 1)
    # plt.plot(X, Y)
    plt.plot(time_step,Y)
    # plt.plot(time_step, F_x)
    # plt.plot(time_step,F_y)
    plt.show()


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
    game = FinalProject.Game.SpaceWar.SpaceWar((700,700),2,0)
    cursor = Cursor.Cursor(1, 0.01)
    update = True

    t2 = threading.Thread(target=run, args=(game, cursor))
    t2.start()
