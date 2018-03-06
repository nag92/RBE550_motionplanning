import sys
import FinalProject.Game.spacewar_helper as sw_helper
import Queue
import math
import matplotlib.pyplot as plt

'''
These variables are determined at runtime and should not be changed or mutated by you
'''
start = ()
goal = ()
 # a single (x,y) tuple, representing the end position of the search algorithm
difficulty = ""  # a string reference to the original import file
G = 1000000000000000000
E = 1000000000000000000
e_list = []

# class ANA():
#
#     def __init__(self,game):
#
#         self.G = 1000000000000000000
#         self.E = 1000000000000000000
#         self.e_list = []
#         self.goal = ()
#         self.start =()
#         self.came_form = []
#         self.cost_so_far = []
#
#     def reset(self):
#         self.G = 1000000000000000000
#         self.E = 1000000000000000000
#         self.e_list = []
#         self.goal = ()
#         self.start = ()


def search(map,start_loc,goal_loc):


    global open
    global start
    global goal
    global G
    global E
    global e_list
    start = ()
    goal = ()
    # a single (x,y) tuple, representing the end position of the search algorithm
    difficulty = ""  # a string reference to the original import file
    G = 1000000000000000000
    E = 1000000000000000000
    e_list = []
    start = start_loc.center
    goal = goal_loc.center
    open = Queue.PriorityQueue()

    came_from = {}
    cost_so_far = {}
    open.put((start, 0))
    came_from[start] = None
    cost_so_far[start] = 0
    # put your final path into this array (so visualize_search can draw it in purple)
    path = []

    # put your expanded nodes into this dictionary (so visualize_search can draw them in dark gray)
    while not open.empty():

        came_from, cost_so_far = improved_solution(map,came_from,cost_so_far)
        path =  reconstruct_path(start,goal,came_from) #came_from, cost_so_far
        yield path
        open = prune(open,cost_so_far)
    #return path

def distance(p1,p2):
    """
    caclulate the distance between two points
    :param p1:
    :param p2:
    :return:
    """

    return math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )

def improved_solution(map,came_from,cost_so_far):
    """
    Searchs the map for a path to the goal
    based on: http://theory.stanford.edu/~amitp/GameProgramming/
    :param map: maze to search
    :return:
    """

    global G
    global E
    global start
    global goal
    global e_list
    count = 0
    while not open.empty():
        count+=1
        current = open.get() # get the next state from the queue

        e = current[1] # cost
        e_list.append(e)
        current = current[0] # state

        # update the globals
        if e < E:

            E = e

        if current == goal:
            G = cost_so_far[current]

            return came_from, cost_so_far

        # loop through the neighbours
        for next in get_neighbours(map, current):
            new_cost = cost_so_far[current] + distance(next,current)  # g(s') = g(s) + c(s,s')
            if next not in cost_so_far or new_cost < cost_so_far[next]:  # g(s) + c(s,s') < g(s')
                cost_so_far[next] = new_cost  # g(s') = g(s) + c(s.s')
                came_from[next] = current

                if new_cost + heuristic(goal, next) < G:
                    key = make_key(next,cost_so_far)
                    open.put((next, key))
    return came_from, cost_so_far

def prune(queue,cost_so_far):
    """
    loop through queue and rebuild with new e(s)
    :param queue:
    :return:
    """
    global goal
    new_open = Queue.PriorityQueue()

    while not queue.empty():
        current = queue.get()
        e = current[1]
        current = current[0]

        if cost_so_far[current] + heuristic(goal, current) < G:

            key = make_key(current,cost_so_far)

            new_open.put((current,key) )

    return new_open

def reconstruct_path(start,goal,came_from):
    """
    reconstructs path
    :param came_from: a dict of nodes
    :return: a list the node from start to finish
    """


    current = goal
    my_path = []

    while current != start:
        my_path.append(current)
        current = came_from[current]
    my_path.append(start)
    my_path.reverse()  # optional

    return my_path

def make_key(node,cost_so_far):
    """
    make the key
    :param g:
    :param node:
    :return:
    """
    global G
    global goal
    #print "h", heuristic(end,node)
    #print "G'", (G - cost_so_far[node])
    e = (G - cost_so_far[node])/heuristic(goal,node)
    return e

def get_neighbours(map, point):
    """
    return a list of neighbours to a point
    :param point: point to find the neighbours off
    :return: list of points
    """

    loc_x = point[0]
    loc_y = point[1]
    width, height = sw_helper.WIDTH,sw_helper.HEIGHT
    node_size = 5
    neighbors_in = [(loc_x - node_size, loc_y), (loc_x, loc_y + node_size), (loc_x + node_size, loc_y), (loc_x, loc_y - node_size),
                    (loc_x - node_size, loc_y - node_size),(loc_x + node_size, loc_y + node_size),(loc_x - node_size, loc_y+node_size),(loc_x + node_size, loc_y-5)]
    neighbors_out = []

    for option in neighbors_in:
        if (option[0] >= 0 and option[0] < width) and (option[1] >= 0 and option[1] < height):

            if not sw_helper.check_point(map,option):
                neighbors_out.append(option)

    return neighbors_out

def heuristic(a, b):
    """
    calculate the heuristic
    :param a:
    :param b:
    :return:
    """
    (x1, y1) = a
    (x2, y2) = b

    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2) + 0.0001 # need to had a little to avoid division by 0


