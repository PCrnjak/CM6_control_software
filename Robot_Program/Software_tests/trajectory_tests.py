import roboticstoolbox as rtb
from spatialmath import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time

# Inicijalizacija plotova
fig, ax = plt.subplots(1, 3)

# ovak se radi execution time array
# Vrijeme trajanja putanje može biti ovako ili preko integerea
execution_time = (np.arange(0,4,0.01))

# Definiraj robot 
robot = rtb.models.DH.CM6() 
#print(robot)

# Fkine of motor angles i dobijem jednu HG matricu T1 
T1 = robot.fkine(robot.qz)

# Definiraj početni i zadnji joint pos i naporavi HG matrice od toga
q1 = np.array([0,np.pi/2,0,0.01,0.50,0])
q2 = np.array([0.31,0.5,2.0,0.70,0.3,0.70])

T1 = (robot.fkine(q1))
print(T1)
T2 = (robot.fkine(q2))
print(T2)

len_time = 500
# Ctraj radi, može se vrijeme pomoću array ili int
TT2 = rtb.tools.trajectory.ctraj(T1, T2, len_time)
#print(TT2)

#Metode za izvršavanje inverzne kinematike
qx1 = robot.ikine_LM(TT2) # radi dobro
#print(qx1)
#qx1 = robot.ikine_LMS(TT2) # radi
#qx1 = robot.ikine_min(TT2) # radi dobro
# qx1 je array sa dosta podataka a u qx1.q se nalaze joint pozicije


print(type(qx1[0].q))
print(qx1[0].q) #

# ovdje se moraju izvrtiti te joint pozicije i spremiti u novu var jer ga
# zeza ovaj oblik koji dobijem ok ikine_LMS i drugih inverze kinematic metoda
qx1_q =  [0] * len_time
for x in range(len_time):
    qx1_q[x] = qx1[x].q

print(qx1_q[99])
print(robot.fkine(qx1_q[99]))


# Jtraj radi 
qx2 = rtb.tools.trajectory.jtraj(q1,q2,200)
#print(qx2)
#print(qx2.q) # Pozicije 
#print(qx2.qd) # Trebale bi biti brzine ali nisu ???
print(qx2.q[199])
print(robot.fkine(qx2.q[199]))


# ovo radi i isto je ko jtraj ako stavim tpoly
qx3 = rtb.tools.trajectory.mtraj(rtb.tools.trajectory.tpoly,q1,q2,20) # TPOLY OR LSPB
#print(qx3.q)

ax[0].set_ylabel('ctraj')
ax[1].set_ylabel('jtraj')
ax[2].set_ylabel('mtraj')

ax[0].plot(qx1_q ,linewidth=1.5) 
ax[1].plot(qx2.q ,linewidth=1.5) 
ax[2].plot(qx3.q ,linewidth=1.5) 

plt.legend(["joint1","joint2","joint3","joint4","joint5","joint6"],bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=2, borderaxespad=0.)
plt.show()


#robot.plot(qx1_q[99]) #plot poziciju konačnu

robot.plot(robot.qs)
# Mstraj test!!
#qx2 = rtb.tools.trajectory.mstraj()



