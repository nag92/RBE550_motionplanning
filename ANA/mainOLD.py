import sys
from PIL import Image
import copy
import Queue

'''
These variables are determined at runtime and should not be changed or mutated by you
'''
start = (0, 0)  # a single (x,y) tuple, representing the start position of the search algorithm
end = (0, 0)  # a single (x,y) tuple, representing the end position of the search algorithm
difficulty = ""  # a string reference to the original import file
G = 0
E = 0
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
path = []  # an ordered list of (x,y) tuples, representing the path to traverse from start-->goal
expanded = {}  # a dictionary of (x,y) tuples, representing nodes that have been expanded
frontier = {}  # a dictionary of (x,y) tuples, representing nodes to expand to in the future

open = Queue.PriorityQueue()
came_from = {}
cost_so_far = {}

def search(map):
    """
    This function is meant to use the global variables [start, end, path, expanded, frontier] to search through the
    provided map.
    :param map: A '1-concept' PIL PixelAccess object to be searched. (basically a 2d boolean array)
    """
    # O is unoccupied (white); 1 is occupied (black)



    print "pixel value at start point ", map[start[0], start[1]]
    print "pixel value at end point ", map[end[0], end[1]]

    # put your final path into this array (so visualize_search can draw it in purple)
    path.extend([(8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7)])

    # put your expanded nodes into this dictionary (so visualize_search can draw them in dark gray)
    expanded.update({(7, 2): True, (7, 3): True, (7, 4): True, (7, 5): True, (7, 6): True, (7, 7): True})

    # put your frontier nodes into this dictionary (so visualize_search can draw them in light gray)
    frontier.update({(6, 2): True, (6, 3): True, (6, 4): True, (6, 5): True, (6, 6): True, (6, 7): True})

    '''
    YOUR WORK HERE.

    I believe in you
        -Gunnar (the TA)-
    '''

    while not open.empty():

        came_from = improved_solution(map)
        path.extend(reconstruct_path(came_from))
        visualize_search("out.png")  # see what your search has wrought (and maybe save your results)


def reconstruct_path(came_from):
    """
    reconstructs path
    :param came_from:
    :return:
    """
    current = end
    my_path = []
    # this_step = PoseStamped()
    step_index = 0
    while current != start:
        my_path.append(current)
        current = came_from[current]
        # print my_path.poses[-1]
    my_path.append(start)
    my_path.reverse()  # optional
    return my_path


def improved_solution(map):

    global G
    global E
    while not open.empty():

        current = open.get()
        e = current[1]
        current = current[0]

        if e < E:
            E = e

        if current == end:
            G = cost_so_far[current]
            break

        for next in get_neighbours(map, current):
            new_cost = cost_so_far[current] + 1 # g(s') = g(s) + c(s,s')
            if next not in cost_so_far or new_cost < cost_so_far[next]: # g(s) + c(s,s') < g(s')
                cost_so_far[next] = new_cost # g(s') = g(s) + c(s.s')
                key = make_key(next)
                if key < G:
                    open.put((next, key))
                    came_from[next] = current


    return came_from



def make_key(node):
    """
    make the key
    :param g:
    :param node:
    :return:
    """
    print heuristic(end,node)
    e = (G - cost_so_far[node])/heuristic(end,node)
    return e

def get_neighbours(map, point):
    """
    return a list of neighbours to a point
    :param point: point to find the neighbours off
    :return: list of points
    """

    loc_x = point[0]
    loc_y = point[1]
    width, height = im.size

    neighbors_in = [(loc_x - 1, loc_y), (loc_x, loc_y + 1), (loc_x + 1, loc_y), (loc_x, loc_y - 1)]
    neighbors_out = []

    for option in neighbors_in:
        if (option[0] >= 0 and option[0] < width) and (option[1] >= 0 and option[1] < height):
            if not map[option[0], option[1]]:
                neighbors_out.append(option)

    return neighbors_out


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    print a
    print b
    return abs(x1 - x2) + abs(y1 - y2) + 0.00001


def visualize_search(save_file="do_not_save.png"):
    """
    :param save_file: (optional) filename to save image to (no filename given means no save file)
    """
    im = Image.open(difficulty).convert("RGB")
    pixel_access = im.load()

    # draw start and end pixels
    pixel_access[start[0], start[1]] = NEON_GREEN
    pixel_access[end[0], end[1]] = NEON_GREEN

    # draw path pixels
    for pixel in path:
        pixel_access[pixel[0], pixel[1]] = PURPLE

    # draw frontier pixels
    for pixel in frontier.keys():
        pixel_access[pixel[0], pixel[1]] = LIGHT_GRAY

    # draw expanded pixels
    for pixel in expanded.keys():
        pixel_access[pixel[0], pixel[1]] = DARK_GRAY

    # display and (maybe) save results
    im.show()
    if (save_file != "do_not_save.png"):
        im.save(save_file)

    im.close()


if __name__ == "__main__":
    # Throw Errors && Such
    # global difficulty, start, end
    assert sys.version_info[0] == 2  # require python 2 (instead of python 3)
    assert len(sys.argv) == 2, "Incorrect Number of arguments"  # require difficulty input

    # Parse input arguments
    function_name = str(sys.argv[0])
    difficulty = str(sys.argv[1])
    print "running " + function_name + " with " + difficulty + " difficulty."

    # Hard code start and end positions of search for each difficulty level
    if difficulty == "trivial.gif":
        start = (8, 1)
        end = (20, 1)
    elif difficulty == "medium.gif":
        start = (8, 201)
        end = (110, 1)
    elif difficulty == "hard.gif":
        start = (10, 1)
        end = (401, 220)
    elif difficulty == "very_hard.gif":
        start = (1, 324)
        end = (580, 1)
    else:
        assert False, "Incorrect difficulty level provided"
    G = 10000000
    E = 10000000
    open.put((start, 0))
    came_from[start] = None
    cost_so_far[start] = 0
    # Perform search on given image
    im = Image.open(difficulty)

    search(im.load())