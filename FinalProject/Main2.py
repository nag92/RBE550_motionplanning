import FinalProject.Game.SpaceWar
import RRT.RRT as rrt
import A_star.ANA as Astar
import Queue
import time
game = FinalProject.Game.SpaceWar.SpaceWar()
import queue
import matplotlib.pyplot as plt
import math
import numpy as np
import threading
import FinalProject.Motion_Controller.Cursor as Cursor
import FinalProject.Motion_Controller.Potential_Function as PF
import FinalProject.Game.spacewar_helper as sw_helper
import pygame as pg

path = []


def dist(p1,p2):

    return math.sqrt( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2  )

def get_object(player,goals):

    max_d = 100000000000
    next_goal = None

    for goal in goals:
        distance = dist(player.center,goal.rect.center)
        if distance < max_d:
            max_d = distance
            next_goal = goal

    return next_goal

def find_path(game):

    global path
    forces = []
    path = []
    prev_loc = game.get_player()
    path_solver = Astar.ANA(game)
    states = []
    attactor = PF.Velocity_Attractive_Function(.05,.06,2,2)
    replusor = PF.Velocity_Repulsive_Function(900000,10,300)
    alpha = 1
    epsilon = 0.0005
    max_dist = 100

    while len ( game.get_goals() ) > 0 :

       goal =  get_object(game.get_player(),game.get_goals())
       #path =  path_solver.search( game.get_player(), goal, sw_helper.get_obacle_rects(game) )
       #print cursor.state[0:2]
       F =  attactor.get_nabla_U(game.player, goal)

       while dist(game.player.rect.center, goal.rect.center)>29:

           F_a = attactor.get_nabla_U( game.player, goal )
           F_p = move_8way()
           F_r = np.array([0.0, 0.0, 0.0])
           obsticals = game.get_enemies()
           print len(obsticals)
           for obs in obsticals:

               temp = replusor.get_nabla_U(game.player, obs)
               F_r = np.add(F_r,temp)

           print "________________________"
           F_e = np.add(F_a,F_r)
           F =  np.add(F_e, F_p)
           #print "F_r ", F_r
           print F
           #forces.append(F)
           state = cursor.move(alpha * F)
           states.append(state)
           game.move_player(state[3], state[4])


           #if dist( (state[0],state[1]), pt ) > max_dist:pass
               #path = path_solver.search( game.get_player(), goal, sw_helper.get_enemies_rects(game) )
           
       path_solver.reset()
    plot(states,forces)


def plot(states,forces):

    x = []
    y = []
    z = []
    fx = []
    fy = []
    fz = []
    count = len(states)

    for s,f in zip(states,forces):
       fx.append(f[0])
       fy.append(f[1])
       fz.append(f[2])
       x.append(s[0])
       y.append(s[1])
       z.append(s[2])

    plt.subplot(211)
    plt.set_title("position")
    plt.ylabel("pixels")
    plt.plot(range(count), x)
    plt.plot(range(count), y)
    plt.plot(range(count), z)
    #plt.subplot(212)
    plt.set_title("Force")
    plt.xlabel("iteration")
    plt.ylabel("Newtons")
    plt.plot(range(count), fx)
    plt.plot(range(count), fy)
    plt.plot(range(count), fz)
    #ax = plt.gca()
    #ax.set_xticklabels([])

    plt.show()


def run(game,cursor):

    global path
    (x,y) = game.player.rect.center
    cursor.set_state(np.array([[x],[y],[0],[0],[0],[0]]))

    while 1:
        #game.player.update_vel(5,-5)
        game.update()
        (x, y) = game.player.rect.center
        cursor.set_state(np.array([[x], [y], [0], [0], [0], [0]]))

        # for pt in path:
        #     game.add_node(pt)
        if path:
           game.draw_path(path)

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

    return  np.array([F_x, F_y, 0])

if __name__ =="__main__":

    game = FinalProject.Game.SpaceWar.SpaceWar()
    cursor = Cursor.Cursor(1,0.01)
    update = True


    t2 = threading.Thread(target=run, args=(game,cursor))
    t2.start()

    t1 = threading.Thread(target=find_path, args=(game,))
    t1.start()