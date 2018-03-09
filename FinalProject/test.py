import FinalProject.Game.SpaceWar
import RRT.RRT as rrt
import A_star.ANA as Astar
import Queue
import time
game = FinalProject.Game.SpaceWar.SpaceWar()
import queue
import numpy as np
import threading
import FinalProject.Motion_Controller.Cursor as Cursor
import FinalProject.Motion_Controller.Potential_Function as PF
import FinalProject.Game.spacewar_helper as sw_helper


path = []


def find_path(game):

    global path
    path = []
    prev_loc = game.get_player()
    path_solver = Astar.ANA(game)
    attactor = PF.Attractive_Function(1,10)
    replusor = PF.Repulisive_Function(50000000,2*sw_helper.RADIUS+80)
    print 2*sw_helper.RADIUS+15
    alpha = 1

    while(1):

        F_r = np.array([ [0.0],[0.0],[0.0]])
        for point in sw_helper.get_obacle_rects(game):
            pt = point.center
            F_r += replusor.get_nabla_U(cursor.state[0:2], np.asarray([[pt[0]], [pt[1]]]))
        state = cursor.move( alpha*F_r )
        game.move_player( state[3],state[4])


               # print 'Force',F
               # state = cursor.move( alpha*F )
               # game.move_player( state[3],state[4])
               # F = attactor.get_nabla_U(cursor.state[0:2], np.asarray([[pt[0]], [pt[1]]]))




def run(game,cursor):

    global path
    (x,y) = game.player.rect.center
    cursor.set_state(np.array([[x],[y],[0],[0],[0],[0]]))

    while 1:
        #game.player.update_vel(5,-5)
        game.update()
        (x, y) = game.player.rect.center
        cursor.set_state(np.array([[x], [y], [0], [0], [0], [0]]))


if __name__ =="__main__":

    game = FinalProject.Game.SpaceWar.SpaceWar()
    cursor = Cursor.Cursor(0.1,0.01)
    update = True


    t2 = threading.Thread(target=run, args=(game,cursor))
    t2.start()

    t1 = threading.Thread(target=find_path, args=(game,))
    t1.start()