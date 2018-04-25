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
replusor = PF.Repulisive_Function(90000000, 2 * sw_helper.RADIUS + 30)
attactor = PF.Attractive_Function(500, 10)
replusor_vel = PF.Velocity_Repulsive_Function(900000000,20,120 )

DMP_force_static = PF.DMP_Potential_Function(500, 10 / np.pi)
DMP_force_dynamic = PF.DMP_Potential_Function(550000000, 120/math.pi)


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


def get_vel_env_force(game,goal):
    # F_r = np.array([[0.0], [0.0], [0.0]])
    obs = game.get_enemies()
    #player = np.asarray([[np.asscalar(cursor.state[0])], [np.asscalar(cursor.state[1])]])
    goal_pose = np.asarray([[goal.rect.centerx], [goal.rect.centery]])
    F_r = np.array([[0], [0], [0]])
    for point in obs:
        #obstical = np.array([[pt[0]], [pt[1]]])
        print "a"
        temp =  -np.asarray(replusor_vel.get_nabla_U(game.player, point)).reshape((3,1))
        F_r = np.add(F_r, temp)
    #oal_pt = np.asarray([[goal.rect.centerx], [goal.rect.centery]])
    goal_pose = np.asarray([[goal.rect.centerx], [goal.rect.centery]])
    robot = np.array([game.player.rect.centerx, game.player.rect.centery ])
    print robot
    F_a = attactor.get_nabla_U(robot,goal_pose)
    print "Fa", F_a
    print "Fr", F_r
    F_r[[0, 1]] = F_r[[1, 0]]

    F_total = F_r
    print F_total

    #F_total[[0,1]] = F_total[[1, 0]]
    return F_total


def get_static_env_force(cursor,game,goal):

    #F_r = np.array([[0.0], [0.0], [0.0]])
    obs = sw_helper.get_enemies_rects(game)
    player = np.asarray([[np.asscalar(cursor.state[0])], [np.asscalar(cursor.state[1])]])
    goal_pose = np.asarray([[goal.rect.centerx], [goal.rect.centery]])
    F_r = np.array([[0],[0],[0]])
    F_a = attactor.get_nabla_U(player,goal_pose)
    for point in obs:
        pt = point.center

        obstical = np.array([[pt[0]], [pt[1]]])
        F_r = replusor.get_nabla_U( player, obstical )

    return F_r + F_a


def get_goal_force(cursor, goal):

    player = np.asarray([[np.asscalar(cursor.state[0])], [np.asscalar(cursor.state[1])]])
    #oal_pt = np.asarray([[goal.rect.centerx], [goal.rect.centery]])
    goal_pose = np.asarray([[goal.rect.centerx], [goal.rect.centery]])
    F_a = attactor.get_nabla_U(player,goal_pose)

    return F_a


def get_force(cursor, game, goal):

    obs = sw_helper.get_enemies_rects(game)
    F_r = np.array([[0], [0],[0]])
    goal_pt = np.asarray([[goal.rect.centerx], [goal.rect.centery]])
    #temp = [ np.asscalar(x[0]) for x in cursor.state  ]
    for point in obs:
        pt = point.center
        player = np.asarray([np.asscalar(cursor.state[0]), np.asscalar(cursor.state[1])])
        obstical = np.array([[pt[0]], [pt[1]]])
        temp = DMP_force_static.static_force(cursor.state, obstical, goal_pt).reshape((3, 1))

        F_r = np.add( F_r , temp)

    return F_r



def get_force_dynamic(cursor, game, goal):

    obs = game.get_enemies()
    F_r = np.array([[0], [0],[0]])
    goal_pt = np.asarray([[goal.rect.centerx], [goal.rect.centery]])
    #temp = [ np.asscalar(x[0]) for x in cursor.state  ]
    for point in obs:
        player = np.asarray([np.asscalar(cursor.state[0]), np.asscalar(cursor.state[1])])
        #obstical = np.array([[pt[0]], [pt[1]]])
        temp = DMP_force_dynamic.velocity_force(cursor.state, point, goal_pt)
        F_r = np.add( F_r , temp)

    return F_r

def run(game, cursor):

    dt = 0.001

    (x, y) = game.player.rect.center
    cursor.set_state(np.array([[x], [y], [0], [0], [0], [0]]))
    X = []
    Y = []
    F_profile = []
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

            (x_t, xd_t, xdd_t) = runner_x.step(tau, dt,error=err_x, externail_force=F[0])
            (y_t, yd_t, ydd_t) = runner_y.step(tau, dt,error=err_y, externail_force=F[1])

            up = 50 * (np.array([[x_t],   [y_t], [0]]) - cursor.state[0:3])
            uv = 50 * (np.array([[xd_t], [yd_t], [0]]) - cursor.state[3:])

            F = np.array([[xdd_t], [ydd_t], [0]]) - up - uv

            F[0] = np.asscalar(F[0][0])
            F[1] = np.asscalar(F[1][0])

            blocks_hit_list = pg.sprite.spritecollide(game.player, game.all_sprites, False)
            Fx = 0
            Fy = 0
            # for block in blocks_hit_list:
            #     if block != game.player:
            #         if game.player.rect.x > block.rect.x:
            #             Fx = 10000
            #         else:
            #             Fx = -10000
            #
            #         if game.player.rect.y > block.rect.y:
            #             Fy = 10000
            #         else:
            #             Fy = -100000

            F_ext = np.array([[Fx], [Fy],[0]])

            cursor.move(F+F_ext)
            err_x = 0.1 * abs(cursor.state[0] - x_t)[0]
            err_y = 0.1 * abs(cursor.state[1] - y_t)[0]
            #F = get_static_env_force(cursor,game,goal)
            F_vel = get_vel_env_force(game,goal)
            #print "f1", F
            F_dy = get_force_dynamic(cursor, game, goal)
            F_goal = get_goal_force(cursor, goal)
            #print "f2", F
            alpha =0.5

            F  = alpha*(F_vel + F_goal) + (1-alpha)*F_dy
            F_profile.append(F)
            print [cursor.state[0],cursor.state[1]]
            X.append([ np.asscalar(cursor.state[0]), np.asscalar(cursor.state[1])])
            game.move_player(cursor.state[0], cursor.state[1])
            game.update()


    time_step = np.arange(0, (1 / 0.001) + 1)
    plot_force(F_profile,X)


def plot_force(forces,pose):
    """

    :param force_profile:
    :return:
    """

    x = []
    y = []
    z = []
    fx = []
    fy = []
    fz = []
    #print forces
    for f,s in zip(forces,pose):
        x.append(s[0])
        y.append(s[1])
        fx.append(f[0])
        fy.append(f[1])
        fz.append(f[2])
    plt.subplot(211)
    plt.plot(x,y)
    #plt.plot(300,250,'ro',mew=30)
    #plt.plot(300, 100, 'bo',mew=30)
    #plt.ylabel("pixels")
    #plt.xlabel("pixels")
    plt.title("Position")
    plt.subplot(212)
    plt.xlabel("timestep")
    plt.ylabel("Newtons")
    plt.plot(range(len(fx)), fx)
    plt.plot(range(len(fy)), fy)
    plt.title("Force")
    #plt.plot(range(len(fz)), fz)
    plt.legend(["Fx","Fy"])
    # ax = plt.gca()
    # ax.set_xticklabels([])

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
    game = FinalProject.Game.SpaceWar.SpaceWar((600,300),5,5
                                               )
    cursor = Cursor.Cursor(1, 0.01)
    update = True
    raw_input()
    t2 = threading.Thread(target=run, args=(game, cursor))
    t2.start()
