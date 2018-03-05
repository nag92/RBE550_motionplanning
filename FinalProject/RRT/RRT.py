import FinalProject.Game.spacewar_helper as sw_helper
import math
import random
import time


RADUIS = 150
def distance(p1,p2):
    """
    caclulate the distance between two points
    :param p1:
    :param p2:
    :return:
    """

    return math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )


def check_goal(goal,node):
    zone = 40

    x_zone = node[0] <= goal[0] + 0.5*zone and node[0] >= goal[0] - 0.5*zone
    y_zone = node[1] <= goal[1] + 0.5*zone and node[1] >= goal[1] - 0.5*zone
    return x_zone and y_zone


def get_node(maze):
    """
    finds a legal node
    :param maze:
    :return:
    """
    searching = True
    width  = sw_helper.WIDTH
    height = sw_helper.HEIGHT
    node = ()
    while searching:
        node = (int(random.random()*width), int(random.random()*height))
        searching = sw_helper.check_point(maze,node)
    print "found"
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
        can_go = sw_helper.check_vertex(maze,key,pt)
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
                maze.make_vertex(leaf, tree[leaf], (255,140,0))
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

    total_dist = 0
    while parent != root:
        next = tree[parent]
        dist = distance(next,parent)
        total_dist+=dist
        #sw_helper.make_vertex(next, parent, (75,0,130),3)
        parent = next
        path.append(parent)
    return path,total_dist

def rrt(maze,start_loc,goal_loc):


    start = start_loc.center
    goal = goal_loc.center
    tree = {}
    cost_so_far = {}
    tree[start] = None
    cost_so_far[start] = 0
    node = start
    itterations = 0
    while not check_goal(goal,node):

        connected = False
        flag = False
        cost = 100000000
        while not flag:
            node = get_node(maze)
            parent, cost,flag = choose_parent(maze,tree,cost_so_far,node)
        itterations += 1
        tree[node] = parent
        cost_so_far[node] = cost
        #dist = sw_helper.make_vertex(maze,node,parent)
        #time.sleep(.01)

        #yield (node,parent)
    print "sldajflakdjfldfjasldf"
    path,dist = make_path(maze,tree,node,start)
    #return path
    return cost_so_far[node],dist,itterations
#


def rrt_star(maze,start_loc,goal_loc):
    start = start_loc.center
    goal = goal_loc.center
    tree = {}
    cost_so_far = {}
    tree[start] = None
    cost_so_far[start] = 0
    node = start
    itterations = 0

    while not check_goal(goal, node):

        flag = False
        cost = 0
        parent = (0,0)
        while not flag:
            node = get_node(maze)
            parent, cost, flag = choose_parent(maze, tree, cost_so_far, node)

        itterations += 1
        tree[node] = parent
        cost_so_far[node] = cost

        if not flag:
            tree, cost_so_far = reWire(maze,tree,cost_so_far,node)
            itterations += 1

        #yield (node,parent)

        #maze.make_vertex(node, parent, color_g)
        #time.sleep(0.01)

    dist = make_path(maze, tree, node, start)

    #return cost_so_far[node],dist,itterations




def brrt_star(maze):
    start = maze.get_start()
    goal = maze.get_goal()
    tree_a = {}
    tree_b = {}
    cost_so_far = {}
    tree_a[start] = None
    tree_b[goal] = None
    cost_so_far[start] = 0
    cost_so_far[goal] = 0
    point_a = (0, 0, 255)
    point_b = (255, 0, 0)
    vertex_a = (0, 255, 0)
    vertex_b = (125, 0, 125)
    node = start

    shared_node = start
    unconnected = False
    in_tree_a = True

    itterations = 0

    while not unconnected:


        flag = False
        cost = 100000
        while not flag:
            node = get_node(maze)
            maze.make_point(node, point_a)
            parent, cost, flag = choose_parent(maze, tree_a, cost_so_far, node)

        tree_a[node] = parent
        cost_so_far[node] = cost
        tree, cost_so_far = reWire(maze,tree_a,cost_so_far,node)
        maze.make_vertex(node, parent, vertex_a)

        parent, cost, unconnected = choose_parent(maze, tree_b, cost_so_far, node)
        itterations+=1
        if unconnected:

            shared_node = parent
        else:
            tree_a,tree_b=tree_b,tree_a
            vertex_a,vertex_b = vertex_b,vertex_a
            point_a,point_b = point_b,point_a
            in_tree_a = not in_tree_a

        time.sleep(0.01)
    dist = 0
    if in_tree_a:
        dist1 = make_path(maze, tree_a, node, start)
        dist2 = make_path(maze, tree_b, shared_node, goal)
        dist = dist1 + dist2
    else:
        dist1 = make_path(maze, tree_a, node, goal)
        dist2 = make_path(maze, tree_b, shared_node, start)
        dist = dist1 + dist2

    maze.make_vertex(node, shared_node, (75,0,130), 3)
    total_cost = cost_so_far[node] + cost_so_far[shared_node]
    return total_cost,dist,itterations
