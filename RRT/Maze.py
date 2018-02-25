import pygame
import time
class Maze(object):

    def __init__(self):


        self.WIDTH = 800
        self.HEIGHT = 600
        pygame.init()
        self.screen = pygame.display.set_mode([self.WIDTH,self.HEIGHT])
        pygame.display.set_caption('RRTstar')
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.RED = (255,0,0)
        self.screen.fill(self.WHITE)
        self.obsticals = []
        self.start = (25,0)
        self.zone = 50
        self.goal = (775,575)
        self.make_obsticals()
        pygame.draw.rect(self.screen, (125,125,0), (self.start[0]-0.5*self.zone,self.start[1]-0.5*self.zone,self.zone,self.zone ), 0)
        pygame.draw.rect(self.screen, (125,125,0), (self.goal[0]-0.5*self.zone,self.goal[1]-0.5*self.zone,self.zone,self.zone ), 0)

        pygame.display.update()



    def make_obsticals(self):
        centers = [(400,300), (350,150), (150,175),(175,300),(80,100),(500,500),(10,400), (400,10),(400,400),(700,500),(500,300)]
        sizes = [ (100,100),(80,100), (100,20), (100,170),(95,95),(100,80),(80,100), (75,135),(80,80),(100,100),(100,250)]

        for center, size in zip(centers,sizes):
            px = center[0] - 0.5 * size[0]
            py = center[1] - 0.5 * size[1]
            obs = pygame.Rect((px,py),size)
            self.obsticals.append(pygame.Rect((px,py),size) )
            pygame.draw.rect(self.screen, self.BLACK,obs,0)

    def make_vertex(self, point1, point2,color,width=1):
        """

        :param point1: first point vertex
        :param point2: secound point vertex
        :return:
        """
        pygame.draw.line(self.screen, color, point1, point2, width)
        pygame.display.update()

    def make_point(self,point1,color):
        """
        draws a point
        :param point1: the point to draw
        :return:
        """
        pygame.draw.circle(self.screen, color, point1,1)
        pygame.display.update()

    def check_point(self,point):
        """
        see if the point
        :param point:
        :return:
        """
        rect = pygame.Rect((point[0],point[1]),(1,1))
        collision =  rect.collidelist(self.obsticals)
        return not (collision == -1)

    def check_vertex(self,point1,point2):
        """

        :param point1: check if the vertex is in collision
        :param point2:
        :return:
        """
        a = point2[0] - point1[0] + 0.001
        b = point2[1] - point1[1] + 0.001
        m = b/a + 0.001

        for obs in self.obsticals:

            p1 = obs.topleft
            p2 = obs.topright
            p3 = obs.bottomleft
            p4 = obs.bottomright


            # check y value at p1[0]
            y_at_x1 = m * (p1[0] - point1[0]) + point1[1]
            t_y_at_x1 = (p1[0] - point1[0]) / a
            
            # checksegments y value at p2[0
            y_at_x2 = m * (p2[0] - point1[0]) + point1[1]
            t_y_at_x2 = (p2[0] - point1[0]) / a
            
            # check segments x value at p1[1]
            x_at_y1 = (p1[1] - point1[1]) / m + point1[0]
            t_x_at_y1 = (p1[1] - point1[1]) / b
            
            # check segments x value at p3[1]
            x_at_y3 = (p3[1] - point1[1]) / m + point1[0]
            t_x_at_y3 = (p3[1] - point1[1]) / b

            if ((y_at_x1 >= p1[1]) and (y_at_x1 <= p3[1]) and (t_y_at_x1 >= 0) and (t_y_at_x1 <= 1)):
                return 0
            
            elif((y_at_x2 >= p1[1]) and (y_at_x2 <= p3[1]) and (t_y_at_x2 >= 0) and (t_y_at_x2 <= 1)):
                return 0
            
            elif((x_at_y1 >= p1[0]) and (x_at_y1 <= p2[0]) and (t_x_at_y1 >= 0) and (t_x_at_y1 <= 1)):
                return 0
                
            elif((x_at_y3 >= p1[0]) and (x_at_y3 <= p2[0]) and (t_x_at_y3 >= 0) and (t_x_at_y3 <= 1)):
                return 0
                

        return 1

    def get_start(self):

        return self.start

    def get_goal(self):

        return self.goal

    def check_goal(self,node):

        x_zone = node[0] <= self.goal[0] + 0.5*self.zone and node[0] >= self.goal[0] - 0.5*self.zone
        y_zone = node[1] <= self.goal[1] + 0.5*self.zone and node[1] >= self.goal[1] - 0.5*self.zone
        return x_zone and y_zone
