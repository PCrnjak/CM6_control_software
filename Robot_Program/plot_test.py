#!/usr/bin/env python
"""
@author Jesse Haviland
"""

import roboticstoolbox as rp
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time
import axes_robot as rb

fig, ax = plt.subplots(1, 3)

# Make a panda robot
link3 = rp.models.DH.three_link()

q0 = [0.1, 0.5, 0.3]
qf = [1.2, 1.1, 1]

s1 = time.time()
t2 = (np.arange(0,3.5,0.01))
#print(len(t2))
s_speed = np.array([0.3,0.5,0.6])
qt = rp.tools.trajectory.jtraj(q0, qf, t2,s_speed,s_speed)
test = (rb.RAD2E((qt.q[:,0]),0))
#print(test)
#q_test = rb.RAD2E(qt.q
s2 = time.time()

print(s2-s1)
#fig.suptitle('Position, speed and acceleration plots')

ax[0].set_ylabel('Position [DEG]')
ax[1].set_ylabel('Speed in [RPM]')
ax[2].set_ylabel('Acceleration [RAD/S**2')

#print(rb.RAD2E((qt.q[:,0]),0))
print(type(qt.q))
print(len(qt.q))
print((qt.q).shape)
#ax1.plot(qt.q[:,2])
#ax1.plot(qt.q[:,1])
ax[0].plot(qt.q * (180/np.pi),linewidth=1.5) #DEG = RAD * (180 / np.pi)
ax[1].plot(qt.qd * (60/(2*np.pi)),linewidth=1.5) # RPM = rad/s * (60/(2*np.pi))
ax[2].plot(qt.qdd,linewidth=1.5)

#plt.legend(["joint","joint2","joint3"],bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=1, borderaxespad=0.)
#plt.show()

link3.plot(qt.q.T, dt=10 )

#link3.q = link3.qs
# Init joint to the 'ready' joint angles
#panda.q = panda.qz

# Open a plot with the teach panel
#e = link3.teach()