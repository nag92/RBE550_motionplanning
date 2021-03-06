import Maze
import RRT
import pygame
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
#maze = Maze.Maze()

centers = [(400, 300), (350, 150), (150, 175), (175, 300), (80, 100), (500, 500), (10, 400), (400, 10), (400, 400),
           (700, 500), (500, 300),(650,150)]
sizes = [(100, 100), (80, 100), (100, 20), (100, 170), (95, 95), (100, 80), (80, 100), (75, 135), (80, 80), (100, 100),
         (100, 250),(175,50)]
obs = (centers,sizes)
start = (25,0)
goal = (775,575)

rrt = []
rrt_star = []
brrt_star = []

if __name__ == '__main__':
    #
    for i in xrange(10):

        maze = Maze.Maze("rrt_" + str(i) ,start,goal,obs)
        cost, dist, itt =  RRT.rrt(maze)
        if i == 0:
            maze.take_screenshot()
        rrt.append([dist,itt])
    print rrt

    for i in xrange(10):

        maze = Maze.Maze("rrt_star_" + str(i) ,start,goal,obs)
        cost, dist, itt =  RRT.rrt_star(maze)
        print i
        if i == 0:
            maze.take_screenshot()
        rrt_star.append([dist,itt])


    # print rrt_star
    for i in xrange(10):

        maze = Maze.Maze("brrt_star_" + str(i) ,start,goal,obs)
        cost, dist, itt =  RRT.brrt_star(maze)
        if i == 0:
            maze.take_screenshot()
        brrt_star.append([dist,itt])



    rrt_mean = np.mean(rrt, axis=0)
    rrt_star_mean = np.mean(rrt_star, axis=0)
    brrt_star_mean = np.mean(brrt_star, axis=0)

    rrt_mean[0] = rrt_mean[0] / (np.sqrt((start[0] - goal[0]) ** 2 + (start[1] - goal[1]) ** 2))
    rrt_star_mean[0] = rrt_star_mean[0] / (np.sqrt((start[0] - goal[0]) ** 2 + (start[1] - goal[1]) ** 2))
    brrt_star_mean[0] = brrt_star_mean[0] / (np.sqrt((start[0] - goal[0]) ** 2 + (start[1] - goal[1]) ** 2))

    dist = [rrt_mean[0], rrt_star_mean[0], brrt_star_mean[0]]
    itt = [rrt_mean[1], rrt_star_mean[1], brrt_star_mean[1]]

    N = 3
    # men_means = (20, 35, 30, 35, 27)
    # men_std = (2, 3, 4, 1, 2)

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    plt.ylabel('norm distance')
    fig1, ax1 = plt.subplots()
    rects1 = ax.bar(ind, dist, width, color='r')

    # women_means = (25, 32, 34, 20, 25)
    # women_std = (3, 5, 2, 3, 3)
    rects2 = ax1.bar(ind, itt, width, color='y')

    # # add some text for labels, title and axes ticks

    ax.set_title('RRT comparision')
    ax1.set_title('RRT comparision')

    plt.ylabel('itterations')


    def autolabel(ax, rects):
        """
        Attach a text label above each bar displaying its height
        """
        labels = ['RRT', 'RRT*', 'BRRT*']
        count = 0
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    labels[count], ha='center', va='bottom')
            count += 1


    autolabel(ax, rects1)
    autolabel(ax1, rects2)

    plt.show()

    ################################################################

    # rrt = [[1210.765547571608, 1210.7655475716083, 198], [1269.2376784062596, 1269.2376784062594, 306],
    #        [1113.7017209829414, 1113.701720982941, 563], [1098.133509381353, 1098.1335093813527, 832],
    #        [1067.8977543252613, 1067.8977543252615, 745], [1091.6898048852363, 1091.689804885236, 408],
    #        [1064.2138463224926, 1064.2138463224928, 596], [1124.3036266118468, 1124.303626611847, 521],
    #        [1174.3218182148587, 1174.3218182148587, 567], [1031.5795188069114, 1031.5795188069114, 528]]
    #
    # rrt_star = [[1093.7703531069074, 1093.7703531069074, 0], [1042.39694167927, 1042.39694167927, 0],
    #             [1057.9488806669635, 1057.9488806669635, 0], [1085.991493870085, 1085.9914938700852, 0],
    #             [1099.3026473544835, 1099.3026473544835, 0], [1130.182500115585, 1130.182500115585, 0],
    #             [1122.836734969076, 1122.836734969076, 0], [1067.5086912579006, 1067.5086912579009, 0],
    #             [1077.4796039873454, 1077.4796039873454, 0], [1171.3340417593688, 1171.3340417593686, 0]]
    #
    # brrt_star =[[1458.6574267416977, 1598.882297099114, 151], [1717.3837847310476, 1781.6308937568638, 102],
    #             [1276.6691202373422, 1076.1153073848382, 208], [1668.658032279573, 1170.4811464057927, 177],
    #             [1150.7803244926786, 1086.2063501742623, 100], [1248.2110848931297, 1114.8061908435761, 112],
    #             [1254.1205175962643, 1231.0052702895246, 245], [1298.0874565439512, 1193.014867209797, 189],
    #             [1299.5054432589397, 1144.7828924505807, 214], [1237.9911988953268, 1044.6451075244734, 132]]
    #


    



    print brrt_star
