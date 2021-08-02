import roboticstoolbox as rtb
from spatialmath import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time

# Define the robot
robot = rtb.models.DH.CM6() 
print(robot)

# 2 positions we will be testing 
# These are arrays filled with joint angles in radians
q1 = np.array([0,np.pi/2,0,0.01,0.50,0])
q2 = np.array([0.31,0.5,2.0,0.70,0.3,0.70])

matrix = np.empty(shape=(0,6),order='C',dtype='object')
print(matrix)
print(type(matrix))
print(len(matrix))

def CSAAR(pose1,pose2,exec_time):
    Number_of_Steps = exec_time / 0.01
    Increment_steps = np.empty(shape=6,order='C',dtype='object')
    for n in range(0,6):
        Increment_steps[n] = (pose2[n] - pose1[n]) / Number_of_Steps

    Out_traj = np.empty(shape=(int(Number_of_Steps),6),order='C',dtype='object')

    for n in range(0, int(Number_of_Steps)):
        for m in range(0 ,6):
            Out_traj[n][m] = pose1[m] + Increment_steps[m] * (n + 1)
    
    return Out_traj

bg = time.time()
matrix = CSAAR(q1,q2,3)
print(time.time() - bg)

plt.plot(matrix)
plt.show()

print(matrix)
print(type(matrix))
print(len(matrix))

if __name__ == "__main__":
    None


