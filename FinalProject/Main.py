import FinalProject.Game.SpaceWar
import RRT.RRT as rrt
import A_star.ANA as Astar
import Queue
import time
game = FinalProject.Game.SpaceWar.SpaceWar()
import queue
import threading
import FinalProject.Game.spacewar_helper as sw_helper

x = 0
y = 0
v = .1
old_pose = None


def find_path(game):

    global path
    path = []
    prev_loc = game.get_player()
    path_solver = Astar.ANA(game)
    while(1):

       solver =  path_solver.search( game.get_player(), game.get_goals()[0].rect,sw_helper.get_obacle_rects(game) )
       #
       for pt in solver:
          #time0 = time.time()
          path =  pt
          print len(path)
          for pt in path:
              game.add_node(pt)
          #print time.time() - time0
          while(1):pass

       path_solver.reset()




def run(game):
    global path
    while 1:
        #game.player.update_vel(5,-5)
        game.update()

        #if path and update:
           #game.draw_path(path)


if __name__ =="__main__":

    game = FinalProject.Game.SpaceWar.SpaceWar()
    update = True


    t2 = threading.Thread(target=run, args=(game,))
    t2.start()

    t1 = threading.Thread(target=find_path, args=(game,))
    t1.start()
