import FinalProject.Game.SpaceWar
import math
import numpy as np
import threading
import FinalProject.Motion_Controller.Cursor as Cursor
import pygame as pg
import FinalProject.Motion_Controller.Potential_Function as PF
from FinalProject.DMP.Python.Mod_DMP_runner import  Mod_DMP_runner
import matplotlib.pyplot as plt
import FinalProject.Game.spacewar_helper as sw_helper


full_path = "/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_DMP/"
replusor = PF.Repulisive_Function(900000000000, 2 * sw_helper.RADIUS + 30)
attactor = PF.Attractive_Function(0, 10)
DMP_force = PF.DMP_Potential_Function(500,10/np.pi)


def get_DMP(player,goal):

    dx = player[0] - goal[0]
    dy = player[1] - goal[1]

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

def get_obs_force(cursor,game):

    #F_r = np.array([[0.0], [0.0], [0.0]])
    obs = sw_helper.get_enemies_rects(game)
    F_r = np.array([[0],[0],[0]])

    for point in obs:
        pt = point.center
        player = np.asarray([ np.asscalar(cursor.state[0]), np.asscalar(cursor.state[1])])
        obstical = np.array([[pt[0]], [pt[1]]])
        F_r = replusor.get_nabla_U( player, obstical )
        print "yo"

    return F_r

def get_goal_force(cursor, goal):
    player = np.asarray([np.asscalar(cursor.state[0]), np.asscalar(cursor.state[1])])
    goal_pt = np.asarray([[goal.rect.centerx], [goal.rect.centery]])
    return attactor.get_nabla_U( player, goal_pt )


def get_force(cursor, game, goal):

    obs = sw_helper.get_enemies_rects(game)
    F_r = np.array([[0], [0],[0]])
    goal_pt = np.asarray([[goal.rect.centerx], [goal.rect.centery]])
    #temp = [ np.asscalar(x[0]) for x in cursor.state  ]
    for point in obs:
        pt = point.center
        player = np.asarray([np.asscalar(cursor.state[0]), np.asscalar(cursor.state[1])])
        obstical = np.array([[pt[0]], [pt[1]]])
        temp = DMP_force.static_force(cursor.state,obstical,goal_pt).reshape((3,1))
        print "temp", temp
        print "F_r", F_r
        F_r = np.add( F_r , temp)
        print "sum",F_r

    #F_r = np.array([[0], [0],[0]])

    return F_r


def run(game, cursor):

    dt = 0.001

    (x, y) = game.player.rect.center
    cursor.set_state(np.array([[x], [y], [0], [0], [0], [0]]))
    X = []
    Y = []
    total_force = np.array([[0], [0]])
    while len(game.get_goals()) > 0:

        goal = get_goal(game.get_player(), game.get_goals() )

        dmp_file = get_DMP(cursor.state,goal.rect.center)
        runner_y = Mod_DMP_runner(dmp_file + "_y.xml", np.asscalar(cursor.state[1]) , goal.rect.centery  )
        runner_x = Mod_DMP_runner(dmp_file + "_x.xml", np.asscalar(cursor.state[0]) , goal.rect.centerx  )
        err_x = 0
        err_y = 0
        tau = dist(cursor.state,goal.rect.center)/math.sqrt( 200**2 + 200**2)
        F = np.array([[0],[0],[0]])
        print "-----------------------------"
        for _ in np.arange(0, (tau / dt) + 1):

            (x_t, xd_t, xdd_t) = runner_x.step(tau, dt,error=err_x, externail_force=-F[0])
            (y_t, yd_t, ydd_t) = runner_y.step(tau, dt,error=err_y, externail_force=-F[1])

            up = 20 * (np.array([[x_t],   [y_t], [0]]) - cursor.state[0:3])
            uv = 20 * (np.array([[xd_t], [yd_t], [0]]) - cursor.state[3:])

            F = np.array([[xdd_t], [ydd_t], [0]]) - up - uv

            F[0] = np.asscalar(F[0][0])
            F[1] = np.asscalar(F[1][0])
            cursor.move(F)
            err_x = 0.1 * abs(cursor.state[0] - x_t)[0]
            err_y = 0.1 * abs(cursor.state[1] - y_t)[0]
            # F_r = get_obs_force(cursor,game)
            # F_a = get_goal_force(cursor,goal)

            F = get_force(cursor,game,goal)

            X.append(cursor.state[0])
            Y.append(cursor.state[1])
            game.move_player(cursor.state[0], cursor.state[1])
            game.update()


    time_step = np.arange(0, (1 / 0.001) + 1)
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
    game = FinalProject.Game.SpaceWar.SpaceWar((600,300),5,5)
    cursor = Cursor.Cursor(1, 0.01)
    update = True

    t2 = threading.Thread(target=run, args=(game, cursor))
    t2.start()
