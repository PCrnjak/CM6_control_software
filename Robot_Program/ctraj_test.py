#!/usr/bin/env python
"""
@author Jesse Haviland
"""

import roboticstoolbox as rtb
from spatialmath import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time

fig, ax = plt.subplots(1, 2)
robot = rtb.models.DH.Puma560()

print(robot.isspherical())


q1 = np.array([0,0,0,0,0,0])

q2 = np.array([0.1,0,0,0,0,0])

T1 = (robot.fkine(q1))
print(T1)
T2 = (robot.fkine(q2))
print(T2)
var = robot.ikine(T1)
print(var)
var = robot.ikine(T2)

print(var)



#ls = rtb.tools.trajectory.lspb(q1, q2, 100, V=None)
qt2 = rtb.tools.trajectory.ctraj(T1, T2, 20)

v = np.array(q1)
print( v)
#v = np.atleast_2d(v).T
print( qt2)

t1 = time.time()
var = robot.ikine(qt2)
#var = robot.ikinem(qt2[49])
var = robot.ikine(qt2)
print(var)



ax[0].set_ylabel('Position [RAD]')
#ax[1].set_ylabel('Speed in [RAD/S]')
#ax[2].set_ylabel('Acceleration [RAD/S**2')

ax[0].plot(var ,linewidth=1.5) #DEG = RAD * (180 / np.pi)
#ax[1].plot(qt2 ,linewidth=1.5) # RPM = rad/s * (60/(2*np.pi))
#ax[2].plot(qt.qdd,linewidth=1.5)

plt.legend(["joint1","joint2","joint3","joint4","joint5","joint6"],bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=1, borderaxespad=0.)
plt.show()


#robot.plot(qt.q.T, dt=10, block=True) #movie='puma_sitting.gif')
#robot.plot(qt2, dt=10, block=False,movie='puma_sitting_2.gif')
