import sys
import FinalProject.Game.spacewar_helper as sw_helper
import Queue
import math
import matplotlib.pyplot as plt

'''
These variables are determined at runtime and should not be changed or mutated by you
'''

class ANA():

    def __init__(self,game):

        self.G = 1000000000000000000
        self.E = 1000000000000000000
        self.e_list = []
        self.goal = ()
        self.start =()

        self.game = game

    def reset(self):
        self.G = 1000000000000000000
        self.E = 1000000000000000000
        self.e_list = []
        self.goal = ()
        self.start = ()


    def search(self,start_loc,goal_loc):
        # a single (x,y) tuple, representing the end position of the search algorithm


        self.start = start_loc.center
        self.goal = goal_loc.center
        open = Queue.PriorityQueue()

        came_from = {}
        cost_so_far = {}

        open.put((self.start, 0))
        came_from[self.start] = None
        cost_so_far[self.start] = 0
        # put your final path into this array (so visualize_search can draw it in purple)
        path = []

        # put your expanded nodes into this dictionary (so visualize_search can draw them in dark gray)
        while not open.empty():

            open,came_from, cost_so_far = self.improved_solution(open,came_from,cost_so_far)
            path =  self.reconstruct_path(came_from) #came_from, cost_so_far
            yield path
            open = self.prune(open,cost_so_far)
        #return path

    def distance(self,p1,p2):
        """
        caclulate the distance between two points
        :param p1:
        :param p2:
        :return:
        """

        return math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )


    def improved_solution(self,open,came_from,cost_so_far):
        """
        Searchs the map for a path to the goal
        based on: http://theory.stanford.edu/~amitp/GameProgramming/
        :param map: maze to search
        :return:
        """

        while not open.empty():


            current = open.get() # get the next state from the queue

            e = current[1] # cost
            self.e_list.append(e)
            current = current[0] # state

            # update the globals
            if e < self.E:
                self.E = e

            if current == self.goal:
                self.G = cost_so_far[current]

                return open,came_from, cost_so_far

            # loop through the neighbours
            for next in self.get_neighbours(current):

                new_cost = cost_so_far[current] + self.distance(next,current)  # g(s') = g(s) + c(s,s')

                if next not in cost_so_far or new_cost < cost_so_far[next]:  # g(s) + c(s,s') < g(s')
                    cost_so_far[next] = new_cost  # g(s') = g(s) + c(s.s')
                    came_from[next] = current

                    if new_cost + self.heuristic(self.goal, next) < self.G:
                        key = self.make_key(next,cost_so_far)
                        open.put((next, key))

        return open,came_from, cost_so_far

    def prune(self,queue,cost_so_far):
        """
        loop through queue and rebuild with new e(s)
        :param queue:
        :return:
        """

        new_open = Queue.PriorityQueue()

        while not queue.empty():
            current = queue.get()
            e = current[1]
            current = current[0]

            if cost_so_far[current] + self.heuristic(self.goal, current) < self.G:
                key = self.make_key(current,cost_so_far)
                new_open.put((current,key) )

        return new_open

    def reconstruct_path(self,came_from):
        """
        reconstructs path
        :param came_from: a dict of nodes
        :return: a list the node from start to finish
        """

        current = self.goal
        my_path = []

        while current != self.start:
            my_path.append(current)
            current = came_from[current]
        my_path.append(self.start)
        my_path.reverse()  # optional

        return my_path

    def make_key(self,node,cost_so_far):
        """
        make the key
        :param g:
        :param node:
        :return:
        """

        #print "h", heuristic(end,node)
        #print "G'", (G - cost_so_far[node])
        e = (self.G - cost_so_far[node])/self.heuristic(self.goal,node)
        return e

    def get_neighbours(self, point):
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

                if not sw_helper.check_point(self.game,option):
                    neighbors_out.append(option)

        return neighbors_out

    def heuristic(self,a, b):
        """
        calculate the heuristic
        :param a:
        :param b:
        :return:
        """
        (x1, y1) = a
        (x2, y2) = b

        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2) + 0.0001 # need to had a little to avoid division by 0


