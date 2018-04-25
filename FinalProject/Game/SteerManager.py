


class SteerManager():

    def __init__(self,pos,vel,fnc):

        self.pos = pos
        self.vel = vel
        self.move = fnc

    def update(self,*args):
        self.pos = self.fnc(self.pos,self.vel)






