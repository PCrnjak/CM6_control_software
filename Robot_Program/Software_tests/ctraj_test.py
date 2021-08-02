import roboticstoolbox as rtb
#from spatialmath import *
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

# Time to execute movement
# 50 time steps and we are using time_step of 10ms
execution_time = 50
print(execution_time)

# Transform joint angles to homogenous transformation matrix
T1 = (robot.fkine(q1))
T2 = (robot.fkine(q2))
print(T2)

# Create Cartesian trajectory between two poses
# Output of this function are Homogenous transformation matrices x execution time
bg = time.time()
TT2 = rtb.tools.trajectory.ctraj(T1, T2, execution_time)
print(time.time() - bg)


# Here we transform those Homogenous transformation matrices to joint angles
# ikine_LM function returns bunch of stuff 
bg = time.time()
qx1 = robot.ikine_LM(TT2)
print(time.time() - bg)

# Extract Joint angles from qx1 
qx1_q =  [0] * execution_time
for x in range(0,execution_time):
    qx1_q[x] = qx1[x].q
    #print(qx1_q[x])

# Prove that Commanded pose and true pose we got are the same!
print(robot.fkine(qx1_q[execution_time-1]))

# Plot our trajectory
plt.plot(qx1_q)
plt.show()

