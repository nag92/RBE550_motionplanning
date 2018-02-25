import Maze
import math
import random





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
    width  = random.random()*maze.WIDTH
    height = random.random()*maze.HEIGHT
    node = ()
    while searching:
        node = (random.random()*width, random.random()*height)
        searching = maze.check_point(node)

    return node




def choose_parent(maze,tree,cost,pt):
    """
    find the parent node and travel cost
    :param tree:
    :param pt:
    :return:
    """
    travel_cost = 100000000000000
    parent = ()
    for key, value in tree.iteritems():
        dist = distance(key,pt)
        new_cost = dist + cost[key]
        can_go = maze.check_vertex(key,pt)
        if new_cost < travel_cost and can_go:
            travel_cost = new_cost
            parent = key


    return parent,travel_cost


def rewire(came_from,cost_so_far):

     
    pass




def make_path(tree,leaf,root):
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
        parent = tree[parent]
        path.append(parent)




def rrt(maze):

    start = maze.get_start()
    goal = maze.get_goal()
    Ta = {}
    Tb = {}
    Ta[start] = 0
    Tb[goal] = 0





