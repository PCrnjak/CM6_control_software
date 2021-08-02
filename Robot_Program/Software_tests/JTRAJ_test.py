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

qx2 = rtb.tools.trajectory.jtraj(q1,q2,200)
#print(qx2)
#print(qx2.q) # Pozicije 
#print(qx2.qd) # Trebale bi biti brzine ali nisu ???
print(qx2.q)
print(robot.fkine(qx2.q[199]))

plt.plot(qx2.q)
plt.show()