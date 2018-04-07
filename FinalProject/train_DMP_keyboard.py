from FinalProject.DMP.Python import train_dmp, DMP_runner
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


left_up_x = pd.read_csv('/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_data_raw/left_up_x.csv', delimiter=',')
left_up_y = pd.read_csv('/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_data_raw/left_up_y.csv', delimiter=',')

right_up_x = pd.read_csv('/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_data_raw/right_up_x.csv', delimiter=',')
right_up_y = pd.read_csv('/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_data_raw/right_up_y.csv', delimiter=',')

right_down_x = pd.read_csv('/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_data_raw/right_down_x.csv', delimiter=',')
right_down_y = pd.read_csv('/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_data_raw/right_down_y.csv', delimiter=',')

left_down_x = pd.read_csv('/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_data_raw/left_down_x.csv', delimiter=',')
left_down_y = pd.read_csv('/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_data_raw/left_down_y.csv', delimiter=',')

down_x = pd.read_csv('/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_data_raw/down_x.csv', delimiter=',')
down_y = pd.read_csv('/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_data_raw/down_y.csv', delimiter=',')

up_x = pd.read_csv('/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_data_raw/up_x.csv', delimiter=',')
up_y = pd.read_csv('/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_data_raw/up_y.csv', delimiter=',')

left_x = pd.read_csv('/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_data_raw/left_x.csv', delimiter=',')
left_y = pd.read_csv('/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_data_raw/left_y.csv', delimiter=',')

right_x = pd.read_csv('/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_data_raw/right_x.csv', delimiter=',')
right_y = pd.read_csv('/home/nathaniel/git/RBE550_motionplanning/FinalProject/keyboard_data_raw/right_y.csv', delimiter=',')


# Or export it in many ways, e.g. a list of tuples
# dmps = [ (left_down_x, left_down_y), (left_up_x,left_up_y), (left_down_x,left_down_y), (right_down_x,right_down_y), (right_up_x,right_up_y),\
#          (right_x,right_y),(up_x,up_y), (down_x,down_y)]


dmps = [  (right_x,right_y),(left_x,left_y) ]
#names = [ "left_down", "left_up","left", "right","right_down","right_up","up","down"]
names = ["right","left" ]
for vals,name in zip(dmps,names):
    T_x = []
    T_y = []
    dfx = vals[0]
    dfy = vals[1]
    for x,y in zip(dfx.values,dfy.values):
        T_x.append(x.tolist())
        T_y.append(y.tolist())
    filex = name + "_x.xml"
    filey = name + "_y.xml"
    Important_values = train_dmp.train_dmp(filex, 200, T_x, 0.001)
    Important_values = train_dmp.train_dmp(filey, 200, T_y, 0.001)

# start = 300
# goal = 145
# my_runnerY = DMP_runner.DMP_runner("tempY.xml",start,goal)
# my_runnerX = DMP_runner.DMP_runner("tempX.xml",start,goal)
#
#
# Y = []
# X = []
# tau = 1
# dt = .001
# for i in np.arange(0,20):
#
#     '''Dynamic change in goal'''
#     #new_goal = 2
#     #new_flag = 1
#     #if i > 0.6*int(tau/dt):
#     #    my_runner.setGoal(new_goal,new_flag)
#     '''Dynamic change in goal'''
#
#     my_runnerY.step(tau,dt)
#     my_runnerX.step(tau, dt)
#     Y.append(my_runnerY.y)
#     X.append(my_runnerX.y)
#
# time = np.arange(0,tau+dt,dt)
#
# plt.title("2-D DMP demonstration")
# plt.xlabel("Time(t)")
# plt.ylabel("Position(y)")
#
# plt.plot(X,Y)
# plt._show()