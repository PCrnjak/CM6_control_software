# This file acts as configuration file for robot you are using
# It works in conjustion with configuration file from robotics toolbox

from numpy import pi 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import roboticstoolbox as rtb


robot = rtb.models.DH.CM6() 
Joint_num = 6 # Number of joints

Joint_limits_ticks =[[-4096,0], [0,7000], [0,7000], [-2048,2048], [-2000,2000], [-2560,2560]] # values you get after homing robot and moving it to its most left and right sides

Joint_reduction_ratio = [8, 8, 9.142857143, 6.5, 6, 5] # Reduction ratio we have on our joints

Encoder_resolution =[1024,1024,1024,1024,1024,1024] # S-Drive is using 10 bit encoders = 1024 ticks per revolution

# These need to be readjusted if you are changing homing position. Zero joint angles WILL ALWAYS NEED TO FOLLOW KINEMATIC DIAGRAM OF THE ROBOT !!!
Joint_offsets = [pi/2, -3.512999 , -1.264317, 0, 0, 0] #[pi/2, -1.264334-pi/2 , 0.3714061]# Here we adjust robot angles to match ones in robotic toolbox. Easiest to adjust when robot is in kinematic zero position

Direction_offsets = [-1,-1,1,-1,-1,1] # If angle change is true to angle change in kinematic model then this is 1 else 0


# Stuff for jogging of single motors
Joint_max_speed = [1.57075, 1.57075, 1.57075, 1.57075, 1.57075, 1.57075] # max speed in RAD/S used, can go to much more than 1.57 but there is bug in S-drive firmware
Joint_min_speed = [0.02617993875, 0.02617993875, 0.02617993875,0.02617993875, 0.02617993875, 0.02617993875] # min speed in RAD/S used 

Joint_max_acc = [5, 5, 5, 5, 5, 5] # max acceleration in RAD/S²
Joint_min_acc = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1] # min speed in RAD/S used 
#############################################

Default_current_limits = [2000,4000,2000,2000,2000,2000] # Current limits for each motor in mA. Once motor reaches this limit it goes to safety mode
Default_security_stop_duration = 3

Data_interval = 0.02 # 0.01 seconds 10 ms

# default stuff for steer mode
Steer_K1_default = [3, 4, 3, 3, 3, 3]
Steer_K2_default = [0, 0, 0, 0, 0, 0]
Steer_K3_default = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
Steer_K4_default= [2500, 5000, 2500, 2500, 2500, 2500]


def RAD2E(True_Radians,index):
    
    '''     Transform True radian value of joints to raw encoder value of joints.
        Note that radian values are usually offset and changed direction from encoder values
        This is done so that radians match kinematic model and right hand positive direction rule '''
    #return_var = (True_Radians * Encoder_resolution[index] * Joint_reduction_ratio[index] - Direction_offsets[index] * Joint_offsets[index]) / (Direction_offsets[index] * 2 * pi)
    return_var = (True_Radians * Encoder_resolution[index] * Joint_reduction_ratio[index] - Direction_offsets[index] * Joint_offsets[index]* Encoder_resolution[index] * Joint_reduction_ratio[index]) / (Direction_offsets[index] * 2 * pi )

    if isinstance(return_var,np.ndarray):
        return return_var.astype(int)
    else:
        return int(return_var)


def E2RAD(Motor_Encoder,index):

    '''     Transform raw encoder value to true radian value of joints.
        Note that radian values are usually offset and changed direction from encoder values
        This is done so that radians match kinematic model and right hand positive direction rule '''

    return_var = ((Motor_Encoder * 2/(Encoder_resolution[index] * Joint_reduction_ratio[index]) * pi + Joint_offsets[index]) * Direction_offsets[index])

    return return_var


def RAD2D(True_Radians):

    '''     Transform true radian values to true degrees value '''
    return_var = np.rad2deg(True_Radians)

    return return_var


def RPM2RADS(Motor_RPM,index):

    '''     Transform raw RPM value we receive from controllers to RAD/S value.
        Note that RPM value we receive is WITHOUT REDUCER. 
        RAD/S value is value WITH reducer.  '''

    return_var = (Motor_RPM / Joint_reduction_ratio[index]) * (pi/30)

    return return_var


def RADS2RPM(True_RADS,index):

    '''     Transform true RAD/S value to raw RPM of motors.
        Note that raw RPM of motors is without gear reduction '''

    return_var = (True_RADS * Joint_reduction_ratio[index] * 30) / pi

    return return_var


def RADS2_true_RPM(True_RADS):
    
    '''     Transform true RADS/S to true RPM.
        Both these values are true values at witch motor joints move '''
    
    return_var = (True_RADS * 30) / pi

    return return_var

def GO_TO_POSE(pose1,pose2,exec_time): 

    speed_true_togo = [0] * Joint_num
    pos_true_togo = [0] * Joint_num
    for i in range(0,Joint_num):
        temp_var = pose2[i] - pose1[i]
        speed_true_togo[i] = temp_var / exec_time
        speed_true_togo[i] = abs(RADS2RPM(speed_true_togo[i],i))
        pos_true_togo[i] = RAD2E(pose2[i],i)

    return pos_true_togo, speed_true_togo


def CSAAR(pose1,pose2,exec_time):

    """     This function creates Continous speed angle to angle rotation for every joint
        It returns numpy array with joint angles that change from 0 to exec_time every 10ms """

    Number_of_Steps = exec_time / Data_interval
    Increment_steps = np.empty(shape=6,order='C',dtype='object')
    for n in range(0,6):
        Increment_steps[n] = (pose2[n] - pose1[n]) / Number_of_Steps

    Out_traj = np.empty(shape=(int(Number_of_Steps),6),order='C',dtype='object')

    for n in range(0, int(Number_of_Steps)):
        for m in range(0 ,6):
            Out_traj[n][m] = pose1[m] + Increment_steps[m] * (n + 1)
    
    return Out_traj


def Clean_CTRAJ(pose1,pose2,exec_time):

    T1 = (robot.fkine(pose1))
    T2 = (robot.fkine(pose2))
    Num_steps = int(exec_time / Data_interval)

    TT2 = rtb.tools.trajectory.ctraj(T1, T2, Num_steps)

    qx1 = robot.ikine_LM(TT2)
    qx1_q =  [0] * Num_steps

    for x in range(0,Num_steps):
        qx1_q[x] = qx1[x].q
    
    return qx1_q
    

if __name__ == "__main__":

    var = Clean_CTRAJ([0,np.pi/2,0,0.01,0.50,0],[0.31,0.5,2.0,0.0,0.3,0.70],2)
    plt.plot(var)
    plt.show()
    #print(var)

