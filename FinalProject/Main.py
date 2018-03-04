import FinalProject.Game.SpaceWar
import RRT.RRT as rrt
game = FinalProject.Game.SpaceWar.SpaceWar()



x = 0
y = 0
v = .1
old_pose = None
point = rrt.rrt(game,game.get_player(),game.get_goals()[0].rect)
while 1:

    game.update()

    pt =  next(point)
    game.add_node(pt[0])
    game.draw_line(*pt)

