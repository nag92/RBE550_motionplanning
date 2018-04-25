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
from FinalProject.DMP.Python.Mod_DMP_runner import  Mod_DMP_runner
import matplotlib.pyplot as plt
import time
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


def run(game):
    global path
    path = []
    states = []
    alpha = 0.5

    name_x = "/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_DMP/right_x.xml"
    name_y = "/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_DMP/right_y.xml"
    n_rfs = 200
    start = game.get_player().center
    goal = game.get_goals()[0].rect.center
    # start = 0

    tau = 1
    dt = .001
    # goal = 1

    my_runner_y = Mod_DMP_runner(name_y, start[1], goal[1])
    my_runner_x = Mod_DMP_runner(name_x, start[0], goal[0])
    X = []
    Y = []
    X_r = []
    Y_r = []
    dt_x = dt
    dt_y = dt
    err_y = 0.0
    err_x = 0.0
    (x, y) = game.player.rect.center
    F_x = []
    F_y = []
    cursor.set_state(np.array([[x], [y], [0], [0], [0], [0]]))
    for i in np.arange(0,(1/.001)+1):
        '''Dynamic change in goal'''
        # new_goal = 2
        # new_flag = 1

        # if i > 0.6*int(tau/dt):
        #    my_runner.setGoal(new_goal,new_flag)
        '''Dynamic change in goal'''
        print dt_x
        (x_t, xd_t, xdd_t) = my_runner_x.step(tau, dt,error=err_x)
        (y_t, yd_t, ydd_t) = my_runner_y.step(tau, dt,error=err_y)
        # print my_runner.x
        # f = avoid_obstacles(np.array([x_t,y_t]),np.array([xd_t,yd_t]) ,my_runner_y.g)
        # print "obs", np.array([[obstacles[0]],[obstacles[1]]])
        up = 50 * ( np.array([[x_t],  [y_t],  [0]]) - cursor.state[0:3] )
        uv = 50 * ( np.array([[xd_t], [yd_t], [0]]) - cursor.state[3:])

        F = np.array([[xdd_t], [ydd_t], [0]]) - up - uv
        state = cursor.move( F)
        #game.move_player(state[0], state[1])
        game.move_player(state[0], state[1])
        game.update()
        err_x = np.asscalar(1*abs(state[0] - x_t))
        err_y = np.asscalar(1*abs(state[1] - y_t))
        X.append(x_t)
        Y.append(y_t)
        X_r.append(state[0])
        Y_r.append(state[1])
        F_x.append(F[0])
        F_y.append(F[1])
        #f = repluse.get_nabla_U(np.array([[np.asscalar(x_t)], [np.asscalar(y_t)]]),np.array([[obstacles[0]], [obstacles[1]]]))
    print "stop"
    time_step = np.arange(0,(1/.001)+1)
    #plt.plot(X, Y)
    plt.plot(time_step,X)
    #plt.plot(time_step, F_x)
    #plt.plot(time_step,F_y)
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
    game = FinalProject.Game.SpaceWar.SpaceWar((300,100),1,0)
    cursor = Cursor.Cursor(1, 0.01)
    update = True

    t1 = threading.Thread(target=run, args=(game,))
    t1.start()