import FinalProject.Game.SpaceWar
import RRT.RRT as rrt
import A_star.ANA as Astar
import Queue
import time
game = FinalProject.Game.SpaceWar.SpaceWar()
import queue
import threading

x = 0
y = 0
v = .1
old_pose = None
#point = rrt.rrt(game,game.get_player(),game.get_goals()[0].rect)
#rrt.rrt(game, game.get_player(), game.get_goals()[0].rect)
#pt = next(point)
#path = Astar.a_star_search(game, game.get_player(), game.get_goals()[0].rect)
#game.draw_path(path)
#game.draw_line(*pt)
# print "go"

path = []
def find_path(game):

    global path
    prev_loc = game.get_player()
    path_solver = Astar.ANA(game)
    while(1):

       solver =  path_solver.search( game.get_player(), game.get_goals()[0].rect)

       for pt in solver:
           path =  pt


       path_solver.reset()



if __name__ =="__main__":
    global path
    game = FinalProject.Game.SpaceWar.SpaceWar()
    update = True

    t = threading.Thread(target=find_path,args=(game,))
    t.start()

    while 1:
        game.update()

        if path and update:
           game.draw_path(path)

