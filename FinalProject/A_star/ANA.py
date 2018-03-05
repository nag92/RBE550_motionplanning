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
'''
These variables determine display coler, and can be changed by you, I guess
'''
NEON_GREEN = (0, 255, 0)
PURPLE = (85, 26, 139)
LIGHT_GRAY = (50, 50, 50)
DARK_GRAY = (100, 100, 100)

'''
These variables are determined and filled algorithmically, and are expected (and required) be mutated by you
'''


def a_star_search(graph, start_loc, goal_loc):
    frontier = Queue.PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    start = start_loc.center
    goal = goal_loc.center
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in get_neighbours(graph, current):
            new_cost = cost_so_far[current] + distance(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

def search(map,start_loc,goal_loc):
    """
    This function is meant to use the global variables [start, end, path, expanded, frontier] to search through the
    provided map.
    :param map: A '1-concept' PIL PixelAccess object to be searched. (basically a 2d boolean array)
    """
    # O is unoccupied (white); 1 is occupied (black)

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
        path = reconstruct_path(came_from)
        open = prune(open,cost_so_far)
    return path

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

def reconstruct_path(came_from):
    """
    reconstructs path
    :param came_from: a dict of nodes
    :return: a list the node from start to finish
    """
    global goal
    global start

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




# if __name__ == "__main__":
#     # Throw Errors && Such
#     # global difficulty, start, end
#     assert sys.version_info[0] == 2  # require python 2 (instead of python 3)
#     assert len(sys.argv) == 2, "Incorrect Number of arguments"  # require difficulty input
#
#     # Parse input arguments
#     function_name = str(sys.argv[0])
#     difficulty = str(sys.argv[1])
#     print "running " + function_name + " with " + difficulty + " difficulty."
#
#     # Hard code start and end positions of search for each difficulty level
#     if difficulty == "trivial.gif":
#         start = (8, 1)
#         end = (20, 1)
#     elif difficulty == "medium.gif":
#         start = (8, 201)
#         end = (110, 1)
#     elif difficulty == "hard.gif":
#         start = (10, 1)
#         end = (401, 220)
#     elif difficulty == "very_hard.gif":
#         start = (1, 324)
#         end = (580, 1)
#     elif difficulty == "my_maze.gif":
#         start = (0, 0)
#         end = (500, 205)
#     elif difficulty == "my_maze2.gif":
#         start = (0, 0)
#         end = (599, 350)
#     else:
#         assert False, "Incorrect difficulty level provided"
#     G = 1000000000000000000
#     E = 1000000000000000000
#     open.put((start, 0))
#     came_from[start] = None
#     cost_so_far[start] = 0
#     # Perform search on given image
#     im = Image.open(difficulty)
#     im = im.convert('1')
#     search(im.load())