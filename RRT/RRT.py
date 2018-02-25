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
    width = random.random()*maze.WIDTH
    height = random.random()*maze.HEIGHT
    node = ()
    while searching:
        node = (random.random()*width, random.random()*height)
        searching = maze.check_point(node)

    return node

def choose_parent(tree,pt):
    """

    :param tree:
    :param pt:
    :return:
    """
    l = 100000000000000
    parent = ()
    for key, value in tree.iteritems():
        dist = distance(key,pt)
        travel = maze.check_vertex(key,pt)
        if dist > l and travel:
            l = dist
            parent = key

    return parent

maze = Maze()

start = maze.get_start()
nodes = {}
nodes[start] = 0
