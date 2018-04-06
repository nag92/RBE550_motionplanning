import numpy as np
import time
class Cursor():


    def __init__(self,Kp,Kd):
        self.Kd = Kp
        self.Kd = Kd
        self.state = np.array([[0],[0],[0],[0],[0],[0]])
        self.time0 = time.clock()
        self.mass = 1

    def set_state(self,state):

        self.state = state

    def move(self,F):

        dt = time.clock() - self.time0
        xdd = -np.array(F).reshape(3, 1)  #- 50*self.state[3:]
        B = np.zeros(shape=(6, 3))
        A = np.identity(6)
        v_max = 15
        B[3, 0] = dt
        B[4, 1] = dt
        B[5, 2] = dt

        A[0, 3] = dt
        A[1, 4] = dt
        A[2, 5] = dt


        self.state = np.dot(A, self.state) + np.dot(B, xdd)
        self.state[3] = max(-v_max, min(self.state[3], v_max))
        self.state[4] = max(-v_max, min(self.state[4], v_max))
        self.state[5] = max(-v_max, min(self.state[5], v_max))
        self.time0 = time.clock()

        return self.state