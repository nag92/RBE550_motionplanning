import sys
import FinalProject.Game.spacewar_helper as sw_helper
import Queue
import math
import time
import matplotlib.pyplot as plt
import pygame as pg

'''
These variables are determined at runtime and should not be changed or mutated by you
'''
import heapq


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        item = heapq.heappop(self.elements)
        return item



class ANA():

    def __init__(self,game):

        self.G = 1000000000000000000
        self.E = 1000000000000000000
        self.e_list = []
        self.goal = ()
        self.start =()
        self.temp = pg.Rect((0, 0), (40, 40))
        self.game = game
        self.flag = False

    def reset(self):
        self.G = 1000000000000000000
        self.E = 1000000000000000000
        self.e_list = []
        self.goal = ()
        self.start = ()

    def a_star_search(self, start_loc, goal_loc,obs_rects):
        frontier = PriorityQueue()

        self.start = start_loc.center
        self.goal = goal_loc.center
        self.obstacles = obs_rects
        frontier.put(self.start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[self.start] = None
        cost_so_far[self.start] = 0
        count = 0

        while not frontier.empty():
            current = frontier.get()

            if current == self.goal:
                break

            for next in self.get_neighbours(current):
                new_cost = cost_so_far[current] + self.distance(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(self.goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current
            #time.sleep(0.1)

        return self.reconstruct_path(came_from)# came_from, cost_so_far

    def search(self,start_loc,goal_loc,obs_rects):



        e_list = []
        self.start = start_loc.center
        self.goal = goal_loc.center
        self.obstacles = obs_rects

        open = PriorityQueue()

        came_from = {}
        cost_so_far = {}

        open.put(self.start, 0)
        came_from[self.start] = None
        cost_so_far[self.start] = 0
        # put your final path into this array (so visualize_search can draw it in purple)
        path = []

        # put your expanded nodes into this dictionary (so visualize_search can draw them in dark gray)
        while not open.empty():

            # came_from, cost_so_far = self.a_star_search(start_loc,goal_loc)
            # path = self.reconstruct_path(came_from)  # came_from, cost_so_far
            # yield path
            # #
            open, came_from, cost_so_far = self.improved_solution(open,came_from,cost_so_far)

            path =  self.reconstruct_path(came_from) #came_from, cost_so_far

            print len(path)
            #print len(self.reduce_path(path))
            yield self.reduce_path(path)
            open = self.prune(open, cost_so_far)


        #return path

    def distance(self,p1,p2):
        """
        caclulate the distance between two points
        :param p1:
        :param p2:
        :return:
        """
        x = (p1[0]-p2[0])**2
        y = (p1[1]-p2[1])**2
        return math.sqrt(  x + y )


    def improved_solution(self,open,came_from,cost_so_far):
        """
        Searchs the map for a path to the goal
        based on: http://theory.stanford.edu/~amitp/GameProgramming/
        :param map: maze to search
        :return:
        """
        count = 0
        while not open.empty():
            #time.sleep(0.1)
            item = open.get() # get the next state from the queue

            e = item[0] # cost
            self.e_list.append(e)
            current = item[1] # state

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
                        open.put(next, key)

                #time.sleep(0.1)

        return open,came_from, cost_so_far

    def prune(self,queue,cost_so_far):
        """
        loop through queue and rebuild with new e(s)
        :param queue:
        :return:
        """

        new_open = PriorityQueue()

        while not queue.empty():
            item = queue.get()

            e = item[0]
            current = item[1]

            if cost_so_far[current] + self.heuristic(self.goal, current) < self.G:
                key = self.make_key(current,cost_so_far)
                new_open.put(current,key)

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
        e = 1/( (self.G - cost_so_far[node])/(self.heuristic(self.goal,node)+.001))
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
        node_size = 1
        neighbors_in = [(loc_x - node_size, loc_y), (loc_x, loc_y + node_size), (loc_x + node_size, loc_y), (loc_x, loc_y - node_size),
                        (loc_x - node_size, loc_y-node_size),(loc_x + node_size, loc_y + node_size),(loc_x + node_size, loc_y - node_size),(loc_x + node_size, loc_y - node_size),]
        neighbors_out = []


        for option in neighbors_in:
            if (option[0] >= 0 and option[0] < width) and (option[1] >= 0 and option[1] < height):

                self.temp.centerx = option[0]
                self.temp.centery = option[1]
                if self.temp.collidelist(self.obstacles) == -1:#
                    neighbors_out.append(option)
                    #print time.time()

        return neighbors_out

    def heuristic(self,p1, p2):
        """
        calculate the heuristic
        :param a:
        :param b:
        :return:
        """
        x = (p1[0] - p2[0]) ** 2
        y = (p1[1] - p2[1]) ** 2
        return math.sqrt(x + y)


    def reduce_path(self,path):

        segments = []
        #segments.append(path[0])
        previous_node = [0,0]

        for index in xrange(len(path)-1):
            dy_p = path[index][1] - previous_node[1]
            dx_p = path[index][0] - previous_node[0]

            dy_n = path[index+1][1] - path[index][1]
            dx_n = path[index+1][0] - path[index][0]

            if dx_n != 0 and dx_p !=0:

                m1 = dy_p/dx_p
                m2 = dy_n/dx_n

                if not m1 == m2:
                    segments.append(path[index])


            elif not dx_p == dx_n or not dy_n == dy_p:
                segments.append(path[index])


            previous_node = path[index]
        segments.append(path[-1])
        return segments



