import SpaceWar

game = SpaceWar.SpaceWar()

x = 0
y = 0
v = .1
while 1:
    print "yo"
    x+=v
    y+=v
    game.player.update_vel(x,y)
    game.update()
