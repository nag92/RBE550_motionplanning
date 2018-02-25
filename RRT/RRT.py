import Maze
import math
import random
import time


def distance(p1,p2):
    """
    caclulate the distance between two points
    :param p1:
    :param p2:
    :return:
    """
    return math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )


def get_node(maze):
    """
    finds a legal node
    :param maze:
    :return:
    """
    searching = True
    width  = maze.WIDTH
    height = maze.HEIGHT
    node = ()
    while searching:
        node = (int(random.random()*width), int(random.random()*height))
        searching = maze.check_point(node)

    return node


def choose_parent(maze,tree,cost,pt):
    """
    find the parent node and travel cost
    :param tree:
    :param pt:
    :return:
    """
    travel_cost = float('inf')
    parent = (None,None)
    flag = False
    for key, value in tree.iteritems():
        dist = distance(key,pt)
        new_cost = dist + cost[key]
        can_go = maze.check_vertex(key,pt)
        if new_cost < travel_cost and can_go:
            travel_cost = new_cost
            parent = key
            flag = True


    return parent,travel_cost,flag


def rewire(came_from,cost_so_far):

     
    pass


def make_path(maze,tree,leaf,root):
    """
    recreated the path
    :param Ta:
    :param Tb:
    :param goal:
    :return:
    """

    path = [leaf]
    parent = leaf
    while parent != root:
        next = tree[parent]
        maze.make_vertex(next, parent, (75,0,130))
        parent = next
        path.append(parent)



def rrt(maze):

    start = maze.get_start()
    goal = maze.get_goal()
    tree = {}
    cost_so_far = {}
    tree[start] = None
    cost_so_far[start] = 0
    color_a = (255,0,0)
    color_a = (0, 0, 255)
    color_g = (0,255,0)
    path_found = False
    node = start
    while node[0] <= goal[0] or node[1] <= goal[1]:

        connected = False
        flag = False
        while not flag:
            node = get_node(maze)
            maze.make_point(node,color_a)
            parent, cost,flag = choose_parent(maze,tree,cost_so_far,node)

        tree[node] = parent
        cost_so_far[node] = cost
        maze.make_vertex(node,parent,color_g)
        time.sleep(.01)

    make_path(maze,tree,node,start)
    print "done"

