import Maze
import math
import random
import time


RADUIS = 100
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
        if new_cost < travel_cost and can_go and dist<RADUIS:
            travel_cost = new_cost
            parent = key
            flag = True

    return parent,travel_cost,flag


def reWire(maze,tree,cost,node):

    for leaf, value in tree.iteritems():
        if leaf != tree[node] and distance(leaf,node) < RADUIS and cost[node]+distance(leaf,node) < cost[leaf]:
            if maze.check_vertex(leaf,node):
                tree[leaf] = node
                cost[leaf] = cost[leaf] + distance(node, leaf)
                #maze.make_vertex(leaf, tree[leaf], (255,140,0))
    return tree, cost


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
    color_b = (0, 0, 255)
    color_g = (0,255,0)
    node = start
    while not maze.check_goal(node):

        connected = False
        flag = False
        cost = 100000000
        while not flag:
            node = get_node(maze)
            maze.make_point(node,color_b)
            parent, cost,flag = choose_parent(maze,tree,cost_so_far,node)

        tree[node] = parent
        cost_so_far[node] = cost
        maze.make_vertex(node,parent,color_g)
        time.sleep(.01)

    make_path(maze,tree,node,start)
    return cost_so_far[node]
#
def rrt_star(maze):
    start = maze.get_start()
    goal = maze.get_goal()
    tree = {}
    cost_so_far = {}
    tree[start] = None
    cost_so_far[start] = 0
    color_b = (0, 0, 255)
    color_g = (0, 255, 0)
    node = start
    while not maze.check_goal(node):

        connected = False
        flag = False
        while not flag:
            node = get_node(maze)
            maze.make_point(node, color_b)
            parent, cost, flag = choose_parent(maze, tree, cost_so_far, node)
        tree[node] = parent
        cost_so_far[node] = cost
        tree, cost_so_far = reWire(maze,tree,cost_so_far,node)
        #maze.make_vertex(node, parent, color_g)
        time.sleep(.01)
    print cost_so_far[node]
    make_path(maze, tree, node, start)
    print cost_so_far[node]
    return cost_so_far[node]
