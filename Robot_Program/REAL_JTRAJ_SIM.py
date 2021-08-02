#!/usr/bin/env python
"""
@author Jesse Haviland
"""

import roboticstoolbox as rp
from spatialmath import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time
import axes_robot as rbt

fig, ax = plt.subplots(1, 4)

# 3link robot 
link3 = rp.models.DH.three_link()


# Joint start angles in radians
q0 = [0,np.pi/2,0]

# Joint stop angles in radians
qf = [1.30235,0.129621,1.433505]

s1 = time.time()

# how long movement will take and what are time steps. In example:
# (np.arange(0,10.5,0.01)) from 0 sec to 10.5s with 0.01 time step
t2 = (np.arange(0,4,0.01))
print(len(t2))

start_speed = np.array([0.09,0.09,0.09])
stop_speed = np.array([0.09,0.09,0.09])

# Create trajectory
qt = rp.tools.trajectory.jtraj(q0, qf, t2,start_speed,stop_speed)
#tg = rp.tools.trajectory.ctraj(SE3.Rand(), SE3.Rand(), 20)

s2 = time.time()

print(s2-s1)
#fig.suptitle('Position, speed and acceleration plots')

ax[0].set_ylabel('Position [DEG]')
ax[1].set_ylabel('Speed in [RPM]')
ax[2].set_ylabel('Acceleration [RAD/S**2')

#print(qt.q[:,0])
#print(rbt.RAD2E(qt.q[:,0],0))

print(abs(qt.qd[:,1]))
print("penis")
print(rbt.RADS2RPM(qt.qd[:,0],0))
#print(type(qt.q))
#print(len(qt.q))
#ax1.plot(qt.q[:,2])
#ax1.plot(qt.q[:,1])
#ax[0].plot(qt.q * (180/np.pi),linewidth=1.5) #DEG = RAD * (180 / np.pi)
#ax[1].plot(qt.qd * (60/(2*np.pi)),linewidth=1.5) # RPM = rad/s * (60/(2*np.pi))
ax[0].plot(qt.q ,linewidth=1.5) #DEG = RAD * (180 / np.pi)
ax[1].plot(qt.qd ,linewidth=1.5) # RPM = rad/s * (60/(2*np.pi))
ax[2].plot(qt.qdd,linewidth=1.5)

plt.legend(["joint1","joint2","joint3"],bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=1, borderaxespad=0.)
plt.show()

link3.plot(qt.q.T, dt=10 )

link3.q = link3.qs

print(link3.qs)
T = link3.fkine(link3.qs)
print(T)
T2 = T*1
print(T2[2,3] + 100)
#R2 = SO3.Rz(30, 'deg')
print(T.rpy('deg','zyx'))
#print(T.angvec())
#print(R2)
#print((T[0,1]))
# Init joint to the 'ready' joint angles
#panda.q = panda.qz

# Open a plot with the teach panel
# e = link3.teach()