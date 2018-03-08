import math
import numpy as np


class Attractive_Function():

    def __init__(self, zeta, d_threash):

        self.zeta = zeta
        self.d_threash = d_threash

    def get_U(self,robot_pos,goal_pos):
        """

        :param robot_pos: position of the robot
        :param goal_pos: position of the goal
        :return: engery
        """
        dist = math.sqrt( ( robot_pos[0] - goal_pos[0] ) ** 2 + ( robot_pos[1] - goal_pos[1] ) ** 2 )
        U = 0

        if dist <= self.d_threash:
            U = 0.5 * self.zeta * (dist ** 2)
        else:
            U = self.d_threash*self.zeta*dist - 0.5*self.zeta*(self.d_threash ** 2)

        return U

    def get_nabla_U(self, robot_pos, goal_pos):
        """

        :param robot_pos: position of the robot
        :param goal_pos: position of the goal
        :return: engery
        """

        dist = math.sqrt((robot_pos[0] - goal_pos[0]) ** 2 + (robot_pos[1] - goal_pos[1]) ** 2)
        U = 0

        if dist <= self.d_threash:
            U = self.zeta * ( np.asarray(robot_pos) - np.asarray(goal_pos) )
        else:
            U =  (self.d_threash*self.zeta * ( np.asarray(robot_pos) - np.asarray(goal_pos) ))/(dist)

        return U



class Repulisive_Function():

    def __init__(self, eta, Q_star):

        self.eta = eta
        self.Q_star = Q_star

    def get_U(self,robot_pos,obs_pos):
        """

        :param robot_pos: position of the robot
        :param goal_pos: position of the goal
        :return: engery
        """
        dist = math.sqrt( ( robot_pos[0] - obs_pos[0] ) ** 2 + ( robot_pos[1] - obs_pos[1] ) ** 2 )
        U = 0

        if dist <= self.Q_star:
            U = 0.5 * self.eta * (  (1.0/dist) - (1/self.Q_star)  ) ** 2
        else:
            U = 0
        return U


    def get_nabla_U(self, robot_pos, obs_pos):
        """

        :param robot_pos: position of the robot
        :param goal_pos: position of the goal
        :return: engery
        """

        dist = math.sqrt((robot_pos[0] - obs_pos[0]) ** 2 + (robot_pos[1] - obs_pos[1]) ** 2)
        nabla_dist = ( np.asarray(robot_pos) - np.asarray(obs_pos) )/( dist )
        U = 0

        if dist <= self.Q_star:
            U = self.eta * ((1.0 / self.Q_star) - (1 / dist)) * (nabla_dist/(dist*dist))
        else:
            U = 0

        return U
