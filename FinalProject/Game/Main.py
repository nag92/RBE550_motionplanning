import SpaceWar

game = SpaceWar.SpaceWar()

x = 0
y = 0
v = .1
old_pose = None
while 1:

    game.update()
    points = [game.player.rect.center,(0,0) ]
    game.draw_line(points)
