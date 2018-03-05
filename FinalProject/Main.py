import FinalProject.Game.SpaceWar
import RRT.RRT as rrt
import A_star.ANA as Astar
game = FinalProject.Game.SpaceWar.SpaceWar()



x = 0
y = 0
v = .1
old_pose = None
#point = rrt.rrt_star(game,game.get_player(),game.get_goals()[0].rect)
while 1:

    game.update()
    #rrt.rrt(game, game.get_player(), game.get_goals()[0].rect)
    path = Astar.search(game, game.get_player(), game.get_goals()[0].rect)
    game.draw_path(path)
