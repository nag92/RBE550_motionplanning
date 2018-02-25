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
        self.start = (1,1)
        self.goal = (799,599)
        self.make_obsticals()
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

    def make_vertex(self, point1, point2,color):
        """

        :param point1: first point vertex
        :param point2: secound point vertex
        :return:
        """
        pygame.draw.line(self.screen, color, point1, point2, 1)
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
        temp = pygame.draw.line(self.screen, self.RED, point1, point2, 1)
        collision =  temp.collidelist(self.obsticals)
        return (collision == -1)

    def get_start(self):

        return self.start

    def get_goal(self):

        return self.goal
