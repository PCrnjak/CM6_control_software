""" It can send to individual motors by adding joint prefix over commands:
  Modes and commands available:
  #### Commands need to be sent correctly or else it will be ignored. ####
  #### replace words with numbers.Kp and speed can be float values!

    1 - Go to position and hold:
        h(position),speed,Kp,current_threshold
        example: h100,20,3.1,12

    2 - Speed to position and sent flag
        s(position),speed

    3 - Gravitiy compensation mode
        g(current_threshold),compliance_speed

    4 - Position hold mode
        p(Kp),current_threshold

    5 - Speed mode with direction
        o(direction 0 or 1),speed

    6 - Jump to position
        j(position),Kp,current_threshold

    7 - Voltage mode
        v(direction 0 or 1),voltage(0-1000)

    8 - Disable motor
        d

    9 - Enable motor
        e

   10 - Clear error
        c

   11 - Change motor data
        i(Error_temperature),Error_current,Serial_data_outpu_interval

   12 - teleoperation mode
        x(position),speed,K1_t,K2_t,K3_t,K4_t
        // K1_t is most important, K2_t is for speed while 
        // K3_t and K4_t are for current but they tend to make whole system unstable so be carefull
        // TO disable K3_t enter value 0, to disable K4_t enter value !!!!LARGER!!!! then short circuit current!!!

Now if no commands is to be sent to motors, Joint level data sender needs to send dummy code.
If dummy code is not sent controller will report error and probably send motors to gravity compensation. """


import serial as sr
import time
import numpy as np
import axes_robot as rbt

s = sr.Serial(timeout = None)
s.baudrate = 10e6
s.port = '/dev/ttyACM0'
# If there is no serial device available on '/dev/ttyACM0' software will not run
s.open()  #Comment this out if you want to run the software without device connected
print(s.name)        


def send_dummy_data():
    s.write(b'#')
    s.write(b'\n')

def GOTO_position_HOLD(Joint_, Position_, Speed_, Kp_, Current_):

    s.write(b'h')
    s.write(bytes(str(Joint_), encoding="ascii"))
    s.write(bytes(str(int(Position_)), encoding="ascii"))
    s.write(b',')
    s.write(bytes(str(round(Speed_,4)), encoding="ascii"))
    s.write(b',')
    s.write(bytes(str(round(Kp_,2)), encoding="ascii"))
    s.write(b',')
    s.write(bytes(str(int(Current_)), encoding="ascii"))
    s.write(b'\n')

def Speed_Flag(Joint_, Position_, Speed_):

    s.write(b's')
    s.write(bytes(str(Joint_), encoding="ascii"))
    s.write(bytes(str(int(Position_)), encoding="ascii"))
    s.write(b',')
    s.write(bytes(str(round(Speed_,4)), encoding="ascii"))
    s.write(b'\n')

def Gravity_compensation(Joint_, Current_, Comp_):

    s.write(b'g')
    s.write(bytes(str(Joint_), encoding="ascii"))
    s.write(bytes(str(int(Current_)), encoding="ascii"))
    s.write(b',')
    s.write(bytes(str(int(Comp_)), encoding="ascii"))
    s.write(b'\n')

def Disable(Joint_):

    s.write(b'd')
    s.write(bytes(str(Joint_), encoding="ascii"))
    s.write(b'\n')   

def Enable(Joint_):

    s.write(b'e')
    s.write(bytes(str(Joint_), encoding="ascii"))
    s.write(b'\n')   

def Strong_position_hold(Joint_, Kp_, Current_):

    s.write(b'p')
    s.write(bytes(str(Joint_), encoding="ascii"))
    s.write(bytes(str(round(Kp_,3)), encoding="ascii"))
    s.write(b',')
    s.write(bytes(str(int(Current_)), encoding="ascii"))
    s.write(b'\n')

def Speed_Dir(Joint_, Dir_, Speed_):

    s.write(b'o')
    s.write(bytes(str(Joint_), encoding="ascii"))
    s.write(bytes(str(Dir_), encoding="ascii"))
    s.write(b',')
    s.write(bytes(str(round(Speed_,4)), encoding="ascii"))
    s.write(b'\n')

def Voltage_Mode(Joint_, Dir_, Voltage_):

    s.write(b'v')
    s.write(bytes(str(Joint_), encoding="ascii"))
    s.write(bytes(str(Dir_), encoding="ascii"))
    s.write(b',')
    s.write(bytes(str(int(Voltage_)), encoding="ascii"))
    s.write(b'\n')

def Clear_Error(Joint_):

    s.write(b'c')
    s.write(bytes(str(Joint_), encoding="ascii"))
    s.write(b'\n')  

def Jump_position(Joint_, Position_, Kp_, Current_):

    s.write(b'j')
    s.write(bytes(str(Joint_), encoding="ascii"))
    s.write(bytes(str(int(Position_)), encoding="ascii"))
    s.write(b',')
    s.write(bytes(str(round(Kp_,3)), encoding="ascii"))
    s.write(b',')
    s.write(bytes(str(int(Current_)), encoding="ascii"))
    s.write(b'\n')

def Change_data(Joint_, E_temp, E_Current, Serial_data_output_interval):

    s.write(b'i')
    s.write(bytes(str(Joint_), encoding="ascii"))
    s.write(bytes(str(int(E_temp)), encoding="ascii"))
    s.write(b',')
    s.write(bytes(str(int(E_Current)), encoding="ascii"))
    s.write(b',')
    s.write(bytes(str(int(Serial_data_output_interval)), encoding="ascii"))
    s.write(b'\n')

def teleop_mode(Joint_,Position_,Speed_,K1_t,K2_t,K3_t,K4_t):
    s.write(b'x')
    s.write(bytes(str(Joint_), encoding="ascii"))
    s.write(bytes(str(int(Position_)), encoding="ascii"))
    s.write(b',')
    s.write(bytes(str(round(Speed_,2)), encoding="ascii"))
    s.write(b',')
    s.write(bytes(str(round(K1_t,3)), encoding="ascii"))
    s.write(b',')
    s.write(bytes(str(round(K2_t,3)), encoding="ascii"))
    s.write(b',')
    s.write(bytes(str(round(K3_t,3)), encoding="ascii"))
    s.write(b',')
    s.write(bytes(str(round(K4_t,3)), encoding="ascii"))
    s.write(b'\n')



#initiate arrays
position_var = [None] * rbt.Joint_num
position_var_RADS = [None] * rbt.Joint_num
speed_var = [None] * rbt.Joint_num
current_var = [None] * rbt.Joint_num
temperature_var = [None] * rbt.Joint_num
speed_var_RADS = [None] * rbt.Joint_num


def get_data(data_rec_):

    ''' data gets received in this order: position,current,speed,temperature,voltage,error '''

    data_split = data_rec_.split(b',') # Data split splits all data on "," and places it in array

    # Fill arrays with data points received
    for x in range(rbt.Joint_num):

        position_var[x] = int(data_split[x].decode("utf-8"))
        position_var_RADS[x] = rbt.E2RAD(position_var[x],x) 
        current_var[x] = int(data_split[x + rbt.Joint_num].decode("utf-8"))
        speed_var[x] = int(data_split[x + rbt.Joint_num * 2].decode("utf-8"))
        speed_var_RADS[x] = rbt.RPM2RADS(speed_var[x],x)
        temperature_var[x] = int(data_split[x + rbt.Joint_num * 3].decode("utf-8"))

    voltage_var = int(data_split[4 * rbt.Joint_num].decode("utf-8"))
    error_var = int(data_split[4 * rbt.Joint_num + 1].decode("utf-8"))

    return position_var, position_var_RADS, current_var, speed_var, speed_var_RADS, temperature_var, voltage_var, error_var



def main_comms_func():
    data_rec = s.readline()
    #print(data_rec)
    d1,d2,d3,d4,d5,d6,d7,d8 = get_data(data_rec)

    return d1,d2,d3,d4,d5,d6,d7,d8



def try_reconnect():
    try:
        s.close()
        time.sleep(0.01)
        s.open()
        time.sleep(0.01)
    except:
        print("no serial available")


if __name__ == "__main__":
    #Enable(2)
    #Clear_Error(2)
    while(1):
        try:
            #bg = time.time()
            a1,a2,a3,a4,a5,a6,a7,a8 = main_comms_func()
            #print(time.time() - bg)
            #print(a1)
            #print(a2)
            #print(a3)
            #time.sleep(0.01)
            #teleop_mode(2,2000,0,18,0,0.7,1000) # 0.7, 1000
            #Disable(2)
        except:
            try_reconnect()
            
    
