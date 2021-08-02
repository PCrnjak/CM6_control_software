
import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter import filedialog
from PIL import Image, ImageTk
import multiprocessing
import serial as sr
import time
import random
import numpy as np
import get_send_data as gt
import os,os.path
import axes_robot as rbt
import roboticstoolbox as rp
#from spatialmath import *
import plot_graph_2 as plots

Image_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
print(Image_path)

current_frame = 0 # tells us what frame is active. Move, log, teach...

acc_set = 45 #preset to some value these are % from main to max acc
spd_set = 25 #preset to some value these are % from main to max speed

Enable_disable = False # True is for operating / False is for Stoped

gravity_disable_var = True # True is for gravity comp mode / False is for disabled

Execute_stop_var = True # True is for stop / False is for execute

Now_open = ''

robot_arm = rp.models.DH.CM6()

# p1 = Speed_setpoint
# p2 = acc_setpoint
# p3 = translations
# p4 = left_btns
# p5 = right_btns
# p6 = motor_positions(encoder_ticks)
# p7 = Real RAD angle
# p8 = Current
# p9 = Temperature
# p10 = Robot_pose
# p11 = grav_pos_flag
# p12 = software_control_variables

# p13 = Steer_K1
# p14 = Steer_K2
# p15 = Steer_K3
# p16 = Steer_K4

def Tkinter_GUI(p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16):

    # When button is pressed raise selected frame
    def raise_frame(frame,button1,button2,button3,button4,name):

        global current_frame 
        current_frame = name
        if name == 'move':
            p12[1] = 0
        if name == 'log':
            p12[1] = 1
        if name == 'teach':
            p12[1] = 2
        if name == 'setup':
            p12[1] = 3

        # https://www.tutorialspoint.com/python/tk_relief.htm
        button1.config(relief='sunken',bg = main_color)  #,borderwidth=3
        button2.config(relief='raised',bg = "white")
        button3.config(relief='raised',bg = "white")
        button4.config(relief='raised',bg = "white")

        frame.tkraise()

    def move_frame_stuff():

################ Speed and acceleration setup canvas #########

        # This segment creates speed and acceleration controls
        # They are adjusted by % and shown in RPM and RAD/S² for single joint movement
        # and in m/s and m/s² for translation movements

        speed_canvas = tk.Canvas(move_frame, width=1400, height=80,bg = "white",borderwidth=6, relief='ridge')
        speed_canvas.place(x = 0, y = 0)

        # This is used to show how fast roboto will move when performing translational motion or rotation around its axes
        speed_label = tk.Label(move_frame, text="Speed settings" ,font = (letter_font,18),bg = "white")
        speed_label.place(x = 10, y = 10)

        set_speed_RPM = tk.Label(move_frame, text="####" ,font = (letter_font,14),bg = "white")
        set_speed_RPM .place(x = 500, y = 10)

        set_speed_RAD = tk.Label(move_frame, text="####" ,font = (letter_font,14),bg = "white")
        set_speed_RAD .place(x = 500, y = 35)

        set_ACC_RAD = tk.Label(move_frame, text="####" ,font = (letter_font,14),bg = "white")
        set_ACC_RAD .place(x = 500, y = 60)


        # Set speed and acceleration when pressing buttons
        def speed_acc_setup(var):
            if var == 0:
                p1.value = 25 # p1 is speed
                p2.value = 40

            elif var == 1:
                p1.value = 50
                p2.value = 50

            elif var == 2:
                p1.value = 80
                p2.value = 55

            # Ovo će biti za translacije i rotacije
            #set_speed_RPM.configure(text = str(p1.value) + " RPM")
            #set_speed_RAD.configure(text = str(p1.value) + " RAD/S")
            #set_ACC_RAD.configure(text = str(p2.value) + " RAD/S²")
            
            # This updates values for current desired speed and acceleration in GUI
            for y in range(0,rbt.Joint_num):
                btns_rads[y].configure(text = "Speed: " + str(round(np.interp(p1.value,[1,100],[rbt.Joint_min_speed[y],rbt.Joint_max_speed[y]]),4)) + " RAD/S")
                btns_accel[y].configure(text = "Acceleration: " + str(round(np.interp(p2.value,[1,100],[rbt.Joint_min_acc[y],rbt.Joint_max_acc[y]]),4)) + " RAD/S²")



        # Set Speed and acc with sliders
        def set_speed_acc():
            p1.value = spd_set # speed
            p2.value = acc_set # acceleration

            # This updates values for current desired speed and acceleration in GUI
            for y in range(0,rbt.Joint_num):
                btns_rads[y].configure(text = "Speed: " + str(round(np.interp(p1.value,[1,100],[rbt.Joint_min_speed[y],rbt.Joint_max_speed[y]]),4)) + " RAD/S")
                btns_accel[y].configure(text = "Acceleration: " + str(round(np.interp(p2.value,[1,100],[rbt.Joint_min_acc[y],rbt.Joint_max_acc[y]]),4)) + " RAD/S²")

            # Ovo će biti za translacije i rotacije
            #set_speed_RPM.configure(text = str(round(rbt.RADS2_true_RPM(var_),4)) + " RPM")
            #set_speed_RAD.configure(text = str(round(var_,4)) + " RAD/S")
            #set_ACC_RAD.configure(text = str(round(var2_,4)) + " RAD/S²")

        # Button for slow speed
        spd_b_1 = tk.Button(move_frame, text = "Slow",bg = "white", font = (letter_font,18), width = 10, height = 1,borderwidth=3,command = lambda:speed_acc_setup(0))
        spd_b_1.place(x = 195-180, y = 40)

        # Button for default speed
        spd_b_2 = tk.Button(move_frame, text = "Default",bg = "white", font = (letter_font,18), width = 10, height = 1,borderwidth=3,command = lambda:speed_acc_setup(1))
        spd_b_2.place(x = 345-180, y = 40)

        # Button for fast speed
        spd_b_2 = tk.Button(move_frame, text = "Fast",bg = "white", font = (letter_font,18), width = 10, height = 1,borderwidth=3,command = lambda:speed_acc_setup(2)) 
        spd_b_2.place(x = 495-180, y = 40)

        # Button to set speed from sliders
        set_btn = tk.Button(move_frame, text = "Set",bg = "white", font = (letter_font,18), width = 3, height = 1,borderwidth=3,command = lambda:set_speed_acc()) 
        set_btn.place(x = 1320, y = 25)

################ Motor jog canvas ############################

        jog_motors_canvas = tk.Canvas(move_frame, width=700, height=800,bg = "white",borderwidth=6, relief='ridge')
        jog_motors_canvas.place(x = 0, y = 100)

        btns_left = []
        btns_right = []
        btns_label = []
        btns_rads = []
        btns_accel = []

        btn_nr = -1

        global tk_left
        image_left = Image.open(os.path.join(Image_path,'blue_arrow_left.png'))
        tk_left = ImageTk.PhotoImage(image_left)

        global tk_right
        image_right = Image.open(os.path.join(Image_path,'blue_arrow_right.png'))
        tk_right = ImageTk.PhotoImage(image_right)

        robot_names = ['Base', 'Shoulder', 'Elbow', 'Wrist 1', 'Wrist 2', 'Wrist 3']

        def button_press_left(event=None, var = 0):
            p4[var] = 1

        def button_rel_left(event=None, var = 0):
            p4[var] = 0

        def button_press_right(event=None, var = 0):
            p5[var] = 1

        def button_rel_right(event=None, var = 0):
            p5[var] = 0

        # https://stackoverflow.com/questions/14259072/tkinter-bind-function-with-variable-in-a-loop

        for y in range(1,7):

            btn_nr += 1

            def make_lambda1(x):
                return lambda ev:button_press_left(ev,x)

            def make_lambda2(x):
                return lambda ev:button_rel_left(ev,x)

            def make_lambda3(x):
                return lambda ev:button_press_right(ev,x)

            def make_lambda4(x):
                return lambda ev:button_rel_right(ev,x)

            # Create buttons for joging motors and labels for speed and acceleration
            btns_label.append(tk.Label(move_frame, text=robot_names[btn_nr] ,font = (letter_font,16),bg = "white"))
            btns_label[btn_nr].place(x = 17, y = 130+btn_nr*140)

            btns_left.append(tk.Button(move_frame,image = tk_left,bg ="white",highlightthickness = 0,borderwidth=0))
            btns_left[btn_nr].place(x = 150, y = 118+btn_nr*135)
            btns_left[btn_nr].bind('<ButtonPress-1>',make_lambda1(btn_nr))
            btns_left[btn_nr].bind('<ButtonRelease-1>',make_lambda2(btn_nr))

            btns_right.append(tk.Button(move_frame,image = tk_right,bg ="white",highlightthickness = 0,borderwidth=0))
            btns_right[btn_nr].place(x = 610, y = 118+btn_nr*135)
            btns_right[btn_nr].bind('<ButtonPress-1>',make_lambda3(btn_nr))
            btns_right[btn_nr].bind('<ButtonRelease-1>',make_lambda4(btn_nr))

            btns_rads.append(tk.Label(move_frame, text= "Speed: " ,font = (letter_font,8,'bold'),bg = "white"))
            btns_rads[btn_nr].place(x = 17, y = 165+btn_nr*140)

            btns_accel.append(tk.Label(move_frame, text= "Acceleration: " ,font = (letter_font,8,'bold'),bg = "white"))
            btns_accel[btn_nr].place(x = 17, y = 188+btn_nr*140)

        set_speed_acc()

################ Translation canvas ##########################
        jog_pose_canvas = tk.Canvas(move_frame, width=680, height=800,bg = "white",highlightthickness = 0,borderwidth=6, relief='ridge')
        jog_pose_canvas.place(x = 720, y = 100)

        global tk_xu
        global tk_xd
        global tk_yl
        global tk_yr
        global tk_zu
        global tk_zd

        ylevo = Image.open(os.path.join(Image_path,'ylevo.png'))
        tk_yl = ImageTk.PhotoImage(ylevo)

        ydesno = Image.open(os.path.join(Image_path,'ydesno.png'))
        tk_yr = ImageTk.PhotoImage(ydesno)

        xgore = Image.open(os.path.join(Image_path,'xgore.png'))
        tk_xu = ImageTk.PhotoImage(xgore)

        xdole = Image.open(os.path.join(Image_path,'xdole.png'))
        tk_xd = ImageTk.PhotoImage(xdole)

        zgore = Image.open(os.path.join(Image_path,'zgore.png'))
        tk_zu = ImageTk.PhotoImage(zgore)

        zdole = Image.open(os.path.join(Image_path,'zdole.png'))
        tk_zd = ImageTk.PhotoImage(zdole)
      

        translation_position = []
        
        def translation_press(event=None,ax=0):
            p3[ax] = 1

        def translation_release(event=None,ax=0):
            p3[ax] = 0

        def make_lambda_press(x):
                return lambda ev:translation_press(ev,x)        

        def make_lambda_release(x):
                return lambda ev:translation_release(ev,x)   


        zu_button = tk.Button(move_frame, image=tk_zu,borderwidth=0,highlightthickness = 0,bg = 'white') 
        zu_button.place(x = 1160, y = 180-60)
        zu_button.bind('<ButtonPress-1>',make_lambda_press(5))
        zu_button.bind('<ButtonRelease-1>', make_lambda_release(5))

        zd_button = tk.Button(move_frame, image=tk_zd,borderwidth=0,highlightthickness = 0,bg = 'white') 
        zd_button.place(x = 810, y = 180-60)
        zd_button.bind('<ButtonPress-1>',make_lambda_press(4))
        zd_button.bind('<ButtonRelease-1>', make_lambda_release(4))

        yl_button = tk.Button(move_frame, image=tk_yl,borderwidth=0,highlightthickness = 0,bg = 'white') 
        yl_button.place(x = 810, y = 440-140)
        yl_button.bind('<ButtonPress-1>',make_lambda_press(3))
        yl_button.bind('<ButtonRelease-1>', make_lambda_release(3))

        yr_button = tk.Button(move_frame, image=tk_yr,borderwidth=0,highlightthickness = 0,bg = 'white') 
        yr_button.place(x = 1160, y = 440-140)
        yr_button.bind('<ButtonPress-1>',make_lambda_press(2))
        yr_button.bind('<ButtonRelease-1>', make_lambda_release(2))

        xu_button = tk.Button(move_frame, image=tk_xu,borderwidth=0,highlightthickness = 0,bg = 'white') 
        xu_button.place(x = 1090-100, y = 400-140)
        xu_button.bind('<ButtonPress-1>',make_lambda_press(1))
        xu_button.bind('<ButtonRelease-1>', make_lambda_release(1))

        xd_button = tk.Button(move_frame, image=tk_xd,borderwidth=0,highlightthickness = 0,bg = 'white') 
        xd_button.place(x = 1060-100, y = 600-140)
        xd_button.bind('<ButtonPress-1>',make_lambda_press(0))
        xd_button.bind('<ButtonRelease-1>', make_lambda_release(0))

##############################################################

    def log_frame_stuff():
        # Here write code for log frame 
        None

    def teach_frame_stuff():

        gravity_hold_canvas_left = tk.Canvas(teach_frame, width=275, height=900,bg = "white",borderwidth=6, relief='ridge')
        gravity_hold_canvas_left.place(x = 0, y = 0)

        gravity_hold_canvas_right = tk.Canvas(teach_frame, width=275, height=900,bg = "white",borderwidth=6, relief='ridge')
        gravity_hold_canvas_right.place(x = 290, y = 0)

        save_canvas = tk.Canvas(teach_frame, width=550, height=280,bg = "white",borderwidth=6, relief='ridge')
        save_canvas.place(x = 855, y = 620)

        control_canvas_teach = tk.Canvas(teach_frame, width=265, height=900,bg = "white",borderwidth=6, relief='ridge')
        control_canvas_teach.place(x = 580, y = 0)

        gravity_l = tk.Label(teach_frame, text="Gravity compensation" ,font = (letter_font,17),bg = "white")
        gravity_l.place(x = 20, y = 10)

        position_l = tk.Label(teach_frame, text="Position hold" ,font = (letter_font,17),bg = "white")
        position_l.place(x = 310, y = 10)

        def open_txt():
            
            global Now_open
            mytext.delete('1.0', tk.END)
            text_file = filedialog.askopenfilename(initialdir = Image_path + "/Programs",title = "open text file", filetypes = (("Text Files","*.txt"),))
            print(text_file)
            Now_open = text_file
            text_file = open(text_file, 'r+')
            stuff = text_file.read()

            mytext.insert(tk.END,stuff)
            text_file.close()

        def save_txt():
            
            global Now_open
            print(Now_open)
            if Now_open != '':
                print("done")
                text_file = open(Now_open,'w+')
                text_file.write(mytext.get(1.0,tk.END))
                text_file.close()
            else:
                Now_open = Image_path + "/Programs/execute_script.txt"
                text_file = open(Now_open,'w+')
                text_file.write(mytext.get(1.0,tk.END))
                text_file.close()

        def save_as_txt():

            var1 = entry_label.get()
            text_file = open(Image_path + "/Programs/" + var1 +".txt",'w+')
            text_file.write(mytext.get(1.0,tk.END))
            text_file.close()

        def record_position(mode_var):

            if entry_label_duration.get() == '':
                move_duration = str(4)
            else:
                move_duration = entry_label_duration.get()
            
            string =  mode_var + ',' #'pos,'
            string = string + move_duration + ','

            for y in range(0,rbt.Joint_num - 1):
                string = string + str(round(p7[y],5)) + ','
            string = string + str(round(p7[rbt.Joint_num-1],5)) #add last joint without "," at the end
            string = string + ',\n'
            mytext.insert(tk.INSERT,string)

        def record_delay():
            if entry_label_delay.get() == '':
                delay_time = 1.5
            else:
                delay_time = entry_label_delay.get()
            mytext.insert(tk.INSERT,'delay,')
            mytext.insert(tk.INSERT,str(delay_time))
            mytext.insert(tk.INSERT,',\n')


        p12[3] = 0
        def execute_stuff():

            global Now_open
            data2save = mytext.get(1.0,tk.END)
            p12[3] = 1
            if Now_open != '':
                text_file = open(Now_open,'w+')
                text_file.write(data2save)
                text_file.close()
                text_file = open(Image_path + "/Programs/execute_script.txt",'w+')
                text_file.write(data2save)
                text_file.close()

            else:

                Now_open = Image_path + "/Programs/execute_script.txt"
                text_file = open(Now_open,'w+')
                text_file.write(data2save)
                text_file.close()

        def stop_execution():
            p12[3] = 0

        def pause_execution():
            p12[3] = 2

        mytext = tk.Text(teach_frame,width = 55, height = 30, font=("Helvetica", 13), bg ='gray')
        mytext.place(x = 860, y = 10)

        execute_button = tk.Button(teach_frame,text = "Execute",font = (letter_font,22), width = 7, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3, command = execute_stuff)
        execute_button.place(x = 1250, y = 630)

        stop_execution_button = tk.Button(teach_frame,text = "Stop",font = (letter_font,22), width = 7, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3, command = stop_execution)
        stop_execution_button.place(x = 1250, y = 685)

        pause_execution_button = tk.Button(teach_frame,text = "Pause",font = (letter_font,22), width = 7, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3, command = pause_execution)
        pause_execution_button.place(x = 1250, y = 740)

        open_button = tk.Button(teach_frame,text = "Open",font = (letter_font,22), width = 7, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3,command = open_txt)
        open_button.place(x = 1085, y = 630)

        save_button = tk.Button(teach_frame,text = "Save",font = (letter_font,14,'bold'), width = 6, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3,command = save_txt)
        save_button.place(x = 865, y = 630)       

        save_as_button = tk.Button(teach_frame,text = "Save as",font = (letter_font,14,'bold'), width = 6, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3,command = save_as_txt)
        save_as_button.place(x = 975, y = 630)  


        p12[4] = 0
        def Start_recording():

            if p12[4] == 0:
                start_recording_button.configure(bg ="green")
            else:
                start_recording_button.configure(bg ="ivory3")
            p12[4] = not(p12[4])


        def Stop_recording():
            p12[4] = 0
            start_recording_button.configure(bg ="ivory3")
        
        p12[5] = 0
        #def Execute_recording():
            #if p12[5] == 0:
                #execute_recording_button.configure(bg ="green")
            #else:
                #execute_recording_button.configure(bg ="ivory3")
            #p12[5] = not(p12[5])
        def Execute_recording():
            p12[5] = 1

        p12[6] = 0
        def Show_recording():
            p12[6] = 1
            

        p12[7] = 0
        def Clear_recording():
            p12[7] = 1

        start_recording_button = tk.Button(teach_frame,text = "Start REC",font = (letter_font,14), width = 9, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3,command = Start_recording)
        start_recording_button.place(x =870, y = 710) 

        stop_recording_button = tk.Button(teach_frame,text = "Stop REC",font = (letter_font,14), width = 9, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3,command = Stop_recording)
        stop_recording_button.place(x =870, y = 750) 
 
        execute_recording_button = tk.Button(teach_frame,text = "Execute REC",font = (letter_font,14), width = 9, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3,command = Execute_recording)
        execute_recording_button.place(x =870, y = 790) 

        show_recording_button = tk.Button(teach_frame,text = "Show REC",font = (letter_font,14), width = 9, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3,command = Show_recording)
        show_recording_button.place(x =870, y = 830) 

        Clear_recording_button = tk.Button(teach_frame,text = "Clear REC",font = (letter_font,14), width = 9, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3,command = Clear_recording)
        Clear_recording_button.place(x =870, y = 870) 

        entry_label = tk.Entry(teach_frame,font = (letter_font,14,'bold'), width = 15, borderwidth = 4,bg ="gray84")
        entry_label.place(x =870, y = 675)

        # Legacy stuff using GOTO position
        # Command is pos 
        record_button_all = tk.Button(teach_frame,text = "Record all",font = (letter_font,19), width = 14, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3,command = lambda: record_position('pos'))
        record_button_all.place(x =20, y = 810)

        record_button_free = tk.Button(teach_frame,text = "Record free",font = (letter_font,19), width = 14, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3,command = lambda: record_position('pos'))
        record_button_free.place(x =20, y = 860)
        ################################################

        CSAAR_button = tk.Button(teach_frame,text = "CSAAR",font = (letter_font,19), width = 14, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3,command = lambda: record_position('CSAAR'))
        CSAAR_button.place(x =590, y = 70+43)

        JTRAJ_button = tk.Button(teach_frame,text = "JTRAJ",font = (letter_font,19), width = 14, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3,command = lambda: record_position('JTRAJ'))
        JTRAJ_button.place(x =590, y = 70+90)

        CTRAJ_button = tk.Button(teach_frame,text = "CTRAJ",font = (letter_font,19), width = 14, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3,command = lambda: record_position('CTRAJ'))
        CTRAJ_button.place(x =590, y = 70+90+47)

        move_duration_l = tk.Label(teach_frame, text="Move duration" ,font = (letter_font,17),bg ="ivory3",highlightthickness = 0,borderwidth=3)
        move_duration_l.place(x =590, y = 112-90)

        entry_label_duration = tk.Entry(teach_frame,font = (letter_font,19,'bold'), width = 4, borderwidth = 4,bg ="gray84")
        entry_label_duration.place(x =767, y = 110-90)

        delay_button = tk.Button(teach_frame,text = "Delay",font = (letter_font,19), width = 9, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3,command = record_delay) 
        delay_button.place(x =590, y = 155-90)

        entry_label_delay = tk.Entry(teach_frame,font = (letter_font,19,'bold'), width = 4, borderwidth = 4,bg ="gray84")
        entry_label_delay.place(x =767, y = 160-90)

        def loop_command():
            mytext.insert(tk.INSERT,'loop,\n')

        def end_command():
            mytext.insert(tk.INSERT,'end,\n')

        end_button = tk.Button(teach_frame,text ="END",font = (letter_font,19), width = 6, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3,command = end_command) 
        end_button.place(x =590, y = 855)

        loop_button = tk.Button(teach_frame,text = "LOOP",font = (letter_font,19), width = 6, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3,command = loop_command) 
        loop_button.place(x =720, y = 855)


        def button_press_grav(event=None, var = 0):
            grav_buttons[var].configure(bg ="green yellow")
            pos_buttons[var].configure(bg ="ivory3")
            p11[var] = 0

        def button_press_pos(event=None, var = 0):
            grav_buttons[var].configure(bg ="ivory3")
            pos_buttons[var].configure(bg ="green yellow")
            p11[var] = 1
            
        def set_all(var):
            if var == 'grav':
                for y in range(0,6):
                    grav_buttons[y].configure(bg ="green yellow")
                    pos_buttons[y].configure(bg ="ivory3")
                    p11[y] = 0

            if var == 'pos':
                for y in range(0,6):
                    grav_buttons[y].configure(bg ="ivory3")
                    pos_buttons[y].configure(bg ="green yellow")
                    p11[y] = 1


        def make_lambda_grav(x):
            return lambda ev:button_press_grav(ev,x)
        
        def make_lambda_pos(x):
            return lambda ev:button_press_pos(ev,x)

        robot_names_text = ['Base', 'Shoulder', 'Elbow', 'Wrist 1', 'Wrist 2', 'Wrist 3']
        grav_buttons = []
        pos_buttons = []

        for cnt in range(0,6):

            grav_buttons.append(tk.Button(teach_frame,text = robot_names_text[cnt],font = (letter_font,22), width = 9, height = 1,bg ="ivory3",highlightthickness = 0,borderwidth=3))
            grav_buttons[cnt].place(x = 7, y = 50+cnt*50)
            grav_buttons[cnt].bind('<ButtonPress-1>',make_lambda_grav(cnt))

            pos_buttons.append(tk.Button(teach_frame,text = robot_names_text[cnt],font = (letter_font,22), width = 9, height = 1,bg ="green yellow",highlightthickness = 0,borderwidth=3))
            pos_buttons[cnt].place(x = 300, y = 50+cnt*50)
            pos_buttons[cnt].bind('<ButtonPress-1>',make_lambda_pos(cnt))

        grav_all=(tk.Button(teach_frame,text = "ALL",font = (letter_font,22), wraplength=1, width = 2, height = 8,bg ="ivory3",highlightthickness = 0,borderwidth=3,command = lambda: set_all('grav')))
        grav_all.place(x = 207, y = 50)

        pos_all=(tk.Button(teach_frame,text = "ALL",font = (letter_font,22), wraplength=1, width = 2, height = 8,bg ="ivory3",highlightthickness = 0,borderwidth=3,command = lambda: set_all('pos')))
        pos_all.place(x = 500, y = 50)        

        gravity_disable_var = 1
        p11[6] = gravity_disable_var
        
        def switch_grav_disable():
            global gravity_disable_var
            if gravity_disable_var  == 0:
                grav_disable.configure(text = "Disable")
            else:
                grav_disable.configure(text =  "Gravity")
            gravity_disable_var = not(gravity_disable_var)
            p11[6] = gravity_disable_var

        grav_disable=(tk.Button(teach_frame,text = "Disable",font = (letter_font,22), width = 9, height = 1,bg ="ivory4",highlightthickness = 0,borderwidth=3,command = lambda: switch_grav_disable()))
        grav_disable.place(x = 7, y = 355)   

        p12[2] = 1
        def set_grav_pos():
                p12[2] = not(p12[2])

        set_motor_mode=(tk.Button(teach_frame,text = "Set",font = (letter_font,22), width = 9, height = 1,bg ="ivory4",highlightthickness = 0,borderwidth=3,command = lambda: set_grav_pos()))
        set_motor_mode.place(x = 300, y = 355)   

        None

    def setup_frame_stuff():

        # Initialize K1,2,3,4 values to default ones
        for y in range(0,rbt.Joint_num):
            p13[y] = rbt.Steer_K1_default[y]
            p14[y] = rbt.Steer_K2_default[y]
            p15[y] = rbt.Steer_K3_default[y]
            p16[y] = rbt.Steer_K4_default[y]

        # When button is pressed change K1,2,3,4 values
        def Change_compliance():
            comp_temp = round(np.interp(Compliance_scale.get(), [0, 100], [18, 0.2]),3)
            for y in range(0,rbt.Joint_num):
                p13[y] = comp_temp
                print(p13[y])
            Current_compliance_label.configure(text="Current compliance K1 value: " + str(p13[0]) )
            

        Compliance_setup_canvas = tk.Canvas(setup_frame, width=900, height=900,bg = "white",borderwidth=6, relief='ridge')
        Compliance_setup_canvas.place(x = 0, y = 0)

        Compliance_settings_l = tk.Label(setup_frame, text="Compliance settings" ,font = (letter_font,17),bg = "white")
        Compliance_settings_l.place(x = 20, y = 10)
        
        Compliance_scale = tk.Scale(setup_frame, label='Compliance in %. (100% being soft, 0 being stiff)', from_=0, to=100, orient = tk.HORIZONTAL,bg = "white",borderwidth=3,length = 400, font = (letter_font,11))
        Compliance_scale.place(x = 23, y = 75)

        Compliance_set_button = tk.Button(setup_frame,text = "Set",font = (letter_font,20),bg = "ivory3",command = lambda:Change_compliance())
        Compliance_set_button.place(x = 350, y = 15)

        Current_compliance_label = tk.Label(setup_frame, text="Current compliance K1 value: " + str(p13[0]), font = (letter_font,13),bg = "white")
        Current_compliance_label.place(x = 20, y = 47)


    letter_font = 'Courier New TUR' # letter font used 
    # http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
    main_color = 'gray63' # Color of background (This is some light blue color)
    root = tk.Tk()
    root.wm_attributes("-topmost", 0)
    root.title('ARM control')
    root.configure(background = main_color)

    # This maintains fixed size of 1920x1080 
    # while enabling to minimise and maximise 

    root.maxsize(1920,1080)
    root.minsize(1920,1080)

    root.geometry("1920x1080") 

    # Create frames for other windows

    move_frame = tk.Frame(root, background = main_color)
    move_frame.place(x=0, y=85, width=1420, height=1010)

    log_frame = tk.Frame(root, background = main_color)
    log_frame.place(x=0, y=85, width=1420, height=1010)

    teach_frame = tk.Frame(root, background = main_color)
    teach_frame.place(x=0, y=85, width=1420, height=1010)

    setup_frame = tk.Frame(root, background = main_color)
    setup_frame.place(x=0, y=85, width=1420, height=1010)

    #Help image and button

    image_help = Image.open(os.path.join(Image_path,'helpimg4.png'))
    tk_image = ImageTk.PhotoImage(image_help)
    
    help_button = tk.Button(root, image=tk_image,borderwidth=0,highlightthickness = 0,bg = main_color) #, command=lambda aurl=url_donate:OpenUrl_donate(aurl) 
    help_button.place(x = 1830, y = 0)

    # Buttons for window select

    control_canvas = tk.Canvas(root, width=470, height=900,bg = "white",borderwidth=6, relief='ridge')
    control_canvas.place(x = 1420, y = 85)

    positons_label = tk.Label(root, text="Tool position:" ,font = (letter_font,18),bg = "white")
    positons_label.place(x = 1450, y = 10+85)

    Enable_disable = 0 # 1 is for enabled, 0 is for disabled
    p12[0] = Enable_disable 

    def Disable_Enable():
        global Enable_disable
        if Enable_disable == 0:
            STOP_button.configure(image=tk_STOP)
        else:
            STOP_button.configure(image=tk_ENABLE)
        Enable_disable = not(Enable_disable)
        p12[0] = Enable_disable

    image_STOP = Image.open(os.path.join(Image_path,'disable_img.png'))
    image_ENABLE = Image.open(os.path.join(Image_path,'enable_img.png'))
    tk_STOP = ImageTk.PhotoImage(image_STOP)
    tk_ENABLE = ImageTk.PhotoImage(image_ENABLE)

    # Button to stop robot
    STOP_button = tk.Button(root, image=tk_ENABLE,borderwidth=0,highlightthickness = 0,bg = "white",command = lambda:Disable_Enable())
    STOP_button.place(x = 1760, y = 30+85)

    # Button to clear error

    def Clear_error_command():
        gt.Clear_Error(1)
        gt.Clear_Error(2)
        gt.Clear_Error(3)
        gt.Clear_Error(4)
        gt.Clear_Error(5)
        gt.Clear_Error(6)

    Clear_error_button = tk.Button(root,text = "Clear error",font = (letter_font,24),bg = "ivory3",command = Clear_error_command)
    Clear_error_button.place(x = 1450, y = 270+85)

    # Button to close gripper
    Gripper_close_button = tk.Button(root,text = "Close gripper",font = (letter_font,20),bg = "ivory3")
    Gripper_close_button.place(x = 1450, y = 370+85)

    # Button to open gripper
    Gripper_open_button = tk.Button(root,text = "Open gripper",font = (letter_font,20),bg = "ivory3")
    Gripper_open_button.place(x = 1670, y = 370+85)


    move_button = tk.Button(root, text = "Move", font = (letter_font,23), width = 15, height = 1,borderwidth=3,command = lambda: raise_frame(move_frame,move_button,log_button,teach_button,setup_button,'move'))
    move_button.place(x = 0, y = 2)

    log_button = tk.Button(root, text = "Log", font = (letter_font,23), width = 15, height = 1,borderwidth=3 ,command = lambda: raise_frame(log_frame,log_button,move_button,teach_button,setup_button,'log'))
    log_button.place(x = 285, y = 2)

    teach_button = tk.Button(root, text = "Teach", font = (letter_font,23), width = 15, height = 1,borderwidth=3 ,command = lambda: raise_frame(teach_frame,teach_button,log_button,move_button,setup_button,'teach'))
    teach_button.place(x = 570, y = 2)

    setup_button = tk.Button(root, text = "Setup", font = (letter_font,23), width = 15, height = 1,borderwidth=3 ,command = lambda: raise_frame(setup_frame,setup_button,log_button,teach_button,move_button,'setup'))
    setup_button.place(x = 855, y = 2)


# Stuff that need constant updating and here we define it

    btns_progress = []
    btn_nr_ = -1
    ticks_label = []
    Deg_label = []
    RAD_label = []
    Temperature_label = []
    Current_label = []
    pos_labels = []
    pos_labels2 = []

    pos_text = ['X: ','Y: ','Z: ','phi: ','theta: ','psi: ']
    # Euler angles tell us how to get from out base frame that is static to one our end-effector is now.
    # We do it by rotating for 'phi' around Z then 'theta' around Y and then 'psi' around Z again.

    robot_names = ['Base: ', 'Shoulder: ', 'Elbow: ', 'Wrist 1: ', 'Wrist 2: ', 'Wrist 3: ']

    Data_  = "#####"

    # Raise move frame as default
    raise_frame(move_frame,move_button,setup_button,teach_button,log_button,'move')
    p12[1] = 0
    move_frame_stuff()
    teach_frame_stuff()
    log_frame_stuff()
    setup_frame_stuff()

    # Create scale that allows to set speed of joints 
    # Scales return value from 1-100 
    speed_scale = tk.Scale(move_frame, from_=1, to=100, orient = tk.HORIZONTAL,bg = "white",borderwidth=3,length = 300, font = (letter_font,11))
    speed_scale.place(x = 1008, y = 33)
    speed_scale.set(spd_set)

    # Create scale that allows to set acceleration of joints 
    acc_scale = tk.Scale(move_frame, from_=1, to=100, orient = tk.HORIZONTAL,bg = "white",borderwidth=3,length = 300, font = (letter_font,11))
    acc_scale.place(x = 688, y = 33)
    acc_scale.set(acc_set)

    speed_scale_l = tk.Label(move_frame, text="Speed [%]" ,font = (letter_font,13),bg = "white")
    speed_scale_l.place(x = 1008, y = 8)

    acc_scale_l = tk.Label(move_frame, text="Acceleration [%]" ,font = (letter_font,13),bg = "white")
    acc_scale_l.place(x = 688, y = 8)  

    for y in range(1,7):
            
        # Most of this stuff is labels for jog, these lables will be updating constantly
        btn_nr_ += 1   
        ticks_label.append(tk.Label(move_frame, text="Encoder: " + Data_,font = (letter_font,12),bg = "white"))
        ticks_label[btn_nr_].place(x = 250, y = 152+btn_nr_*135)

        Deg_label.append(tk.Label(move_frame, text="Degree: " + Data_,font = (letter_font,12),bg = "white"))
        Deg_label[btn_nr_].place(x = 250, y = 130+btn_nr_*135)

        RAD_label.append(tk.Label(move_frame, text="Radians: " + Data_,font = (letter_font,12),bg = "white"))
        RAD_label[btn_nr_].place(x = 250, y = 108+btn_nr_*135)

        Temperature_label.append(tk.Label(move_frame, text="Temperature: " + Data_,font = (letter_font,12),bg = "white"))
        Temperature_label[btn_nr_].place(x = 425, y = 130+btn_nr_*135)

        Current_label.append(tk.Label(move_frame, text="Current: " + Data_,font = (letter_font,12),bg = "white"))
        Current_label[btn_nr_].place(x = 425, y = 108+btn_nr_*135)

        btns_progress.append(Progressbar(move_frame, orient = tk.HORIZONTAL, length = 350, mode = 'determinate'))
        btns_progress[btn_nr_].place(x = 250, y = 180+btn_nr_*135)

        pos_labels.append(tk.Label(root, text=pos_text[btn_nr_] + Data_,font = (letter_font,14),bg = "white"))
        pos_labels[btn_nr_].place(x = 1450, y = 45+btn_nr_*35+ 85)

        pos_labels2.append(tk.Label(root, text=robot_names[btn_nr_] + Data_,font = (letter_font,14),bg = "white"))
        pos_labels2[btn_nr_].place(x = 1585, y = 45+btn_nr_*35+ 85)




#### Stuff that will need to be updated after some time e.g. progress bars, x,y,z values... #########
    def Stuff_To_Update():
        global spd_set, acc_set
        spd_set = speed_scale.get() 
        acc_set = acc_scale.get() 

        acc_scale_l.configure(text = "Acceleration " + str(acc_set) + "%")
        speed_scale_l.configure(text = "Speed " + str(spd_set) + "%")

        #T = robot_arm.fkine(p7) # Calculate get homogenous transformation matrix for current joint angles

        # Update motor pos for only joint_num available joints
        for y in range(0,rbt.Joint_num):
            btns_progress[y]["value"] = int(np.interp(p6[y],rbt.Joint_limits_ticks[y],[0,100]))
            btns_progress[y].update()
            ticks_label[y].configure(text="Encoder: " + str(p6[y]))
            Deg_label[y].configure(text="Degree: " + str(round(rbt.RAD2D(p7[y]) ,4)) + " °")
            RAD_label[y].configure(text="Radians: " + str(round(p7[y], 6)))   #raw_var * 0.04394531 * (np.pi / 180, 3)
            Temperature_label[y].configure(text="Temperature: " + str(p9[y]) + " ℃")
            Current_label[y].configure(text="Current: " + str(round(p8[y]/1000, 5)) + " A")
            pos_labels2[y].configure(text= robot_names[y] +str(round(p7[y],4 )))

        for y in range(0,6):
            pos_labels[y].configure(text= pos_text[y] +str(round(p10[y],4 )))

        root.after(95,Stuff_To_Update) # update data every 25 ms

    root.after(1, Stuff_To_Update)
    root.mainloop()




def do_stuff(left_btns,right_btns,raw_ENC,True_rads,spd_set,acc_set,current,temperature,True_pose,RPM_speed,True_rads_speed,grav_pos,software_control,Steer_K1,Steer_K2,Steer_K3,Steer_K4):

    gt.Clear_Error(1)
    gt.Clear_Error(2)
    gt.Clear_Error(3)
    gt.Clear_Error(4)
    gt.Clear_Error(5)
    gt.Clear_Error(6)
    time.sleep(0.01)
    gt.Change_data(1,200,3000,10000)
    gt.Change_data(2,200,5000,10000)
    gt.Change_data(3,200,3000,10000)
    gt.Change_data(4,200,3000,10000)
    gt.Change_data(5,200,3000,10000)
    gt.Change_data(6,200,3000,10000)
    time.sleep(0.01)


    # Array where freeform recorded positions are stored
    freeform_record_array = np.empty(shape=(15000,6),order='C',dtype='object')
    # variable that tells us how many steps we took in our freeform recording
    freeform_record_len = 0
    current_freefrom_step = 0
    current_freefrom_step_execute = 0


    matrix_array = np.empty(shape=(0,6),order='C',dtype='object')

    True_pose_var = [None] * 6 #Variable that stores pose of robot. Index in order: X,Y,Z,R,R,R

    hold_var = [0] * rbt.Joint_num # Hold var is 1 if robot is holding position
    Direction_var = [None] * rbt.Joint_num # None for not moving, True and False for directions


    # Stuff for accelerated jogging of motors
    current_speed = [0] * rbt.Joint_num
    acc_cntr = [0] * rbt.Joint_num

    Speed_jog_setpoint = [0] * rbt.Joint_num
    Acceleration_jog_setpoint = [0] * rbt.Joint_num
    ###################################

    prev_enable_disable = 0
    Sending_stuff = 0 # if it is 0 then send dummy data if it is 1 send nothing since we are sending usefull data
    prev_motor_mode_select = 1

    # code execution control variables
    started_execution = 0 # 0 if we are not executing script, when script is run first time it goes to 1 and stays until script stops executing
    clean_string = [] # whole code of a executing script cleaned up. That means that every '\n' is removed at
    code_step_cntr = 0 # tells us at what line of code we are i.e. what line of code we are executing atm
    time_step_cntr = 0 # Tells us at what time we are at specific line of code
    step_time = 0 # Tells us how long each line of code need to last
    number_of_code_lines = 0 # Number of code lines in script
    Security_flag = 0 # Tells us if security is triggered. 0 if not 1 if triggered
    current_current_limit = rbt.Default_current_limits
    security_stop_duration = rbt.Default_security_stop_duration
    security_counter = 0

    current_pos_command = [None]*rbt.Joint_num # if in pos mode. Save current commanded position here. It will be reexecuted when security is over
    current_speed_command = [None]*rbt.Joint_num # if in pos mode. Save current commanded speed here. It will be reexecuted when security is over
    current_command = '' # command that is being executed atm

    tt = 0
    while(1):
        try:
            bg = time.time()
            
            # Reads all data from serial port. This function also blocks
            ENC,RADS,cur,spd,spd_RAD,temp,vol,err= gt.main_comms_func() 

            # This gets current robot pose and write to multi proc
            Enable_disable_var = software_control[0] # 0 is for disabled / 1 is for enabled
            operating_mode = software_control[1]
             
            T = robot_arm.fkine(RADS)
            T2 = T*1
            True_pose_var[0] = T2[0][3]
            True_pose_var[1] = T2[1][3]
            True_pose_var[2] = T2[2][3]
            True_pose_var[3:] = T.eul('deg')
            
            # This reads all multi process variables and writes to all multi process variables (With len of joint_num)
            for y in range(0,rbt.Joint_num):
                
                # Read multi proc
                # No need for this just read the index you want

                # Write multi proc
                raw_ENC[y] = ENC[y]
                True_rads[y] = RADS[y]
                current[y] = cur[y]
                temperature[y] = temp[y]
                RPM_speed[y] = spd[y]
                True_rads_speed[y] = spd_RAD[y]

            # This reads all multi process variables and writes to all multi process variables (With len of 6)
            for y in range(0,6):

                # Write multi proc
                True_pose[y] = True_pose_var[y]


            if np.any(cur > np.array(current_current_limit)) or Security_flag == 1:

                if security_counter == 0:
                    Security_flag = 1

                    gt.Strong_position_hold(1,7.5,1)
                    gt.Strong_position_hold(2,7.5,1)
                    gt.Strong_position_hold(3,7.5,1)

                if security_counter >= 0 and security_counter < ((security_stop_duration / rbt.Data_interval)):

                    #print(security_counter)
                    security_counter = security_counter + 1
  

                if security_counter == ((security_stop_duration / rbt.Data_interval)):

                    security_counter = 0
                    Security_flag = 0

                    if current_command == 'pos':
                        for y in range(0,rbt.Joint_num):
                            gt.GOTO_position_HOLD(y+1,current_pos_command[y],current_speed_command[y],7.5,1)


### Send dummy data when nobody else is sending data
            if Sending_stuff == 0:
                gt.send_dummy_data()
                #print("dummy_data")
            else:
                #print("not_dummy_data")
                None
########################

# If in teach mode
            if (operating_mode == 2 or operating_mode == 0) and Enable_disable_var == 1 and Security_flag == 0:
                
                if software_control[3] == 1: # stared exectuting script

                    if started_execution == 0:
                        text_file = open(Image_path + "/Programs/execute_script.txt",'r')
                        code_string = text_file.readlines()
                        text_file.close()
 
                        for i in range(0,len(code_string)):
                            if code_string[i] == '\n':
                                continue
                            else:
                                clean_string.append(code_string[i])
                            
                        if clean_string[len(clean_string)-1] == 'end\n' or clean_string[len(clean_string)-1] == 'loop\n':
                            valid_data = 1
                        else:
                            valid_data = 0 

                        started_execution = 1
                        code_step_cntr = 0
                        time_step_cntr = 0
                        number_of_code_lines = len(clean_string)
                        step_time = 0


                    if code_step_cntr < number_of_code_lines:
                        Sending_stuff = 1
                        if time_step_cntr == 0:
                            code2execute = clean_string[code_step_cntr].split(',')
                            code2execute = code2execute[:-1]
                            #print(clean_string)
                            print(code2execute)

                            if(code2execute[0] == 'pos'):

                                step_time = float(code2execute[1]) # data after index 1 is position data and index 1 is time data
                                start_pos = [None]*rbt.Joint_num
                                stop_pos = [None]*rbt.Joint_num

                                current_command = 'pos'

                                for y in range(0,rbt.Joint_num):

                                    start_pos[y] = True_rads[y]
                                    stop_pos[y] = float(code2execute[y+2])

                                pos_var,spd_var = rbt.GO_TO_POSE(start_pos, stop_pos,step_time)

                                current_pos_command = pos_var
                                current_speed_command = spd_var

                                for y in range(0,rbt.Joint_num):
                                    gt.GOTO_position_HOLD(y+1,pos_var[y],spd_var[y],7.5,1)
                                
                                # send movement shit

                            elif(code2execute[0] == 'CSAAR'):
                                
                                step_time = float(code2execute[1]) # data after index 1 is position data and index 1 is time data
                                start_pos = [None]*rbt.Joint_num
                                stop_pos = [None]*rbt.Joint_num

                                current_command = 'CSAAR'

                                for y in range(0,rbt.Joint_num):

                                    start_pos[y] = True_rads[y]
                                    stop_pos[y] = float(code2execute[y+2])

                                
                                matrix_array = np.empty(shape=( int( step_time / rbt.Data_interval ),6),order='C',dtype='object')
                                matrix_array = rbt.CSAAR(start_pos,stop_pos,step_time)
                                for m in range(0,rbt.Joint_num):
                                    gt.teleop_mode(m+1,rbt.RAD2E(matrix_array[time_step_cntr][m],m),0,Steer_K1[m],Steer_K2[m],Steer_K3[m],Steer_K4[m])


                            elif(code2execute[0] == 'JTRAJ'):
                                
                                step_time = float(code2execute[1]) # data after index 1 is position data and index 1 is time data
                                start_pos = [None]*rbt.Joint_num
                                stop_pos = [None]*rbt.Joint_num

                                current_command = 'JTRAJ'

                                for y in range(0,rbt.Joint_num):

                                    start_pos[y] = True_rads[y]
                                    stop_pos[y] = float(code2execute[y+2])

                                
                                matrix_array = np.empty(shape=( int( step_time / rbt.Data_interval ),6),order='C',dtype='object')
                                temp_var = rp.tools.trajectory.jtraj(start_pos,stop_pos,int( step_time / rbt.Data_interval ))    
                                matrix_array = temp_var.q
                                for m in range(0,rbt.Joint_num):
                                    gt.teleop_mode(m+1,rbt.RAD2E(matrix_array[time_step_cntr][m],m),0,Steer_K1[m],Steer_K2[m],Steer_K3[m],Steer_K4[m])


                            elif(code2execute[0] == 'CTRAJ'):
                                
                                step_time = float(code2execute[1]) # data after index 1 is position data and index 1 is time data
                                start_pos = [None]*rbt.Joint_num
                                stop_pos = [None]*rbt.Joint_num

                                current_command = 'CTRAJ'

                                for y in range(0,rbt.Joint_num):

                                    start_pos[y] = True_rads[y]
                                    stop_pos[y] = float(code2execute[y+2])

                                
                                matrix_array = np.empty(shape=( int( step_time / rbt.Data_interval ),6),order='C',dtype='object')
                                temp_var = rp.tools.trajectory.jtraj(start_pos,stop_pos,int( step_time / rbt.Data_interval ))    
                                matrix_array = temp_var.q
                                for m in range(0,rbt.Joint_num):
                                    gt.teleop_mode(m+1,rbt.RAD2E(matrix_array[time_step_cntr][m],m),0,Steer_K1[m],Steer_K2[m],Steer_K3[m],Steer_K4[m])

                            elif(code2execute[0] == 'delay'):
                                
                                current_command = 'delay'
                                step_time = float(code2execute[1])
                                gt.send_dummy_data()

                            elif(code2execute[0] == 'end'):

                                current_command = 'end'
                                code_step_cntr = 0
                                step_time = 0
                                time_step_cntr = 0
                                started_execution = 0
                                software_control[3] = 0
                                clean_string = []

                            elif(code2execute[0] == 'loop'):

                                current_command = 'loop'
                                code_step_cntr = 0
                                step_time = 0
                                time_step_cntr = 0
                                software_control[3] = 1
                                started_execution = 1


                        elif time_step_cntr > 0 and time_step_cntr < ((step_time / rbt.Data_interval)):
                            if(current_command == 'CSAAR'):
                                #print(rbt.RAD2E((matrix_array[time_step_cntr][5]),5))
                                #gt.teleop_mode(6,rbt.RAD2E(matrix_array[time_step_cntr][5],5),0,Steer_K1[5],Steer_K2[5],Steer_K3[5],Steer_K4[5])
                                #print(matrix_array)
                                for m in range(0,rbt.Joint_num):
                                    gt.teleop_mode(m+1,rbt.RAD2E(matrix_array[time_step_cntr][m],m),0,Steer_K1[m],Steer_K2[m],Steer_K3[m],Steer_K4[m])

                            elif(current_command == 'JTRAJ'):
                                for m in range(0,rbt.Joint_num):
                                    gt.teleop_mode(m+1,rbt.RAD2E(matrix_array[time_step_cntr][m],m),0,Steer_K1[m],Steer_K2[m],Steer_K3[m],Steer_K4[m])

                            else:
                                gt.send_dummy_data()
                                #print("dummy data" + str(time_step_cntr))
                            
                        if time_step_cntr < ((step_time / rbt.Data_interval) ):

                            time_step_cntr = time_step_cntr + 1

                        #print(time_step_cntr)

                        if time_step_cntr == ((step_time / rbt.Data_interval)) and current_command != 'loop':
                            time_step_cntr = 0 
                            step_time = 0
                            code_step_cntr = code_step_cntr + 1
                        
                        
                elif software_control[3] == 0: # stop executing. Stops script completely, execute will rerun the script

                    Sending_stuff = 0
                    code_step_cntr = 0
                    step_time = 0
                    time_step_cntr = 0
                    started_execution = 0
                    clean_string = []

                elif software_control[3] == 2: # pause executing, meaning that after you press pause press execute it will continue where it left off
                    Sending_stuff = 0
                    None

                # This stuff is for enabling and disabling(gravity comp or disable) specific motors on left side panel
                if prev_motor_mode_select != software_control[2]:
                    prev_motor_mode_select = software_control[2]
                    for y in range(0, rbt.Joint_num):
                        if grav_pos[y] == 1:
                            gt.Strong_position_hold(y+1,7.5,1)
                        if grav_pos[y] == 0 and grav_pos[6] == 1:
                            gt.Gravity_compensation(y+1,20,5)
                        if grav_pos[y] == 0 and grav_pos[6] == 0:
                            gt.Disable(y+1)

# Jog motors WITH acceleration



            if operating_mode == 0 and Enable_disable_var == 1 and Security_flag == 0:

                for y in range(0,rbt.Joint_num):

                    # Reads positions from sliders or slow,default,fast setting and scales for each joint
                    Speed_jog_setpoint[y] = np.interp(spd_set.value,[1,100],[rbt.Joint_min_speed[y],rbt.Joint_max_speed[y]])
                    Acceleration_jog_setpoint[y] = np.interp(acc_set.value,[1,100],[rbt.Joint_min_acc[y],rbt.Joint_max_acc[y]])

                    # Acceleration in negative direction of robots joint
                    # NOTE: directions follow right hand rule:
                    # * your tumb on right hand is positive direction of z axes, and fingers represent positive rotation.
                    # * Axes are defined by DH params
                    if left_btns[y] == 1 and right_btns[y] == 0: 
                        Sending_stuff = 1
                        #print("jog")
                        current_speed[y] = rbt.Joint_min_speed[y] + acc_cntr[y] * rbt.Data_interval * Acceleration_jog_setpoint[y]
                        if(current_speed[y] >= Speed_jog_setpoint[y]):
                            current_speed[y] = Speed_jog_setpoint[y]

                        gt.Speed_Dir(y+1, 0 if rbt.Direction_offsets[y] == 1 else 1,rbt.RADS2RPM(current_speed[y],y))
                        acc_cntr[y] = acc_cntr[y] + 1
                        Direction_var[y] = True
                        hold_var[y] = 0

    
                    # Acceleration in positive direction of robots joint
                    if right_btns[y] == 1 and left_btns[y] == 0:
                        Sending_stuff = 1
                        #print("jog")
                        current_speed[y] = rbt.Joint_min_speed[y] + acc_cntr[y] * rbt.Data_interval * Acceleration_jog_setpoint[y]
                        if(current_speed[y] >= Speed_jog_setpoint[y]):
                            current_speed[y] = Speed_jog_setpoint[y]

                        gt.Speed_Dir(y+1, 1 if rbt.Direction_offsets[y] == 1 else 0,rbt.RADS2RPM(current_speed[y],y))
                        acc_cntr[y] = acc_cntr[y] + 1
                        Direction_var[y] = False
                        hold_var[y] = 0

                    # Deacceleration 
                    if current_speed[y] >= rbt.Joint_min_speed[y] and left_btns[y] == 0 and right_btns[y] == 0 and hold_var[y] == 0 and Direction_var[y] != None:
                        Sending_stuff = 1
                        #print("jog")
                        current_speed[y] = current_speed[y] - rbt.Data_interval * Acceleration_jog_setpoint[y]

                        if(current_speed[y] <= rbt.Joint_min_speed[y]):
                            current_speed[y] = rbt.Joint_min_speed[y]
                            Direction_var[y] = None

                        if Direction_var[y] == False:
                            gt.Speed_Dir(y+1, 1 if rbt.Direction_offsets[y] == 1 else 0,rbt.RADS2RPM(current_speed[y],y))
                        elif Direction_var[y] == True:
                            gt.Speed_Dir(y+1, 0 if rbt.Direction_offsets[y] == 1 else 1,rbt.RADS2RPM(current_speed[y],y))

                        acc_cntr[y] = 0

                    # If no button is pressed and we stopped deaccelerating, hold position
                    if left_btns[y] == 0 and right_btns[y] == 0 and hold_var[y] == 0 and Direction_var[y] == None:
                        gt.Strong_position_hold(y+1, 7.5, 1)   # OVO SU JAKO DOBRE VRIJEDNOSTI (y+1, 7.5, 1) SA 17000 UPDATE RATE samo kp 10 je ok bez struje
                        Sending_stuff = 0
                        #print("jog")
                        #gt.Gravity_compensation(y+1,50,5)
                        acc_cntr[y] = 0
                        hold_var[y] = 1
            
            # When we disable robot
            if Enable_disable_var == 0 and prev_enable_disable == 1:
                prev_enable_disable = Enable_disable_var

                gt.Gravity_compensation(1,50,3)
                gt.Gravity_compensation(2,50,3)
                gt.Gravity_compensation(3,50,3)
                gt.Gravity_compensation(4,50,3)
                gt.Gravity_compensation(5,50,3)
                gt.Gravity_compensation(6,50,3)

                #elif grav_pos[6] == 0:
                    #gt.Disable(1)
                    #gt.Disable(2)
                    #gt.Disable(3)
                
            # When we enable robot 
            elif Enable_disable_var == 1 and prev_enable_disable == 0:
                prev_enable_disable = Enable_disable_var
                for y in range(0, rbt.Joint_num):
                    gt.Enable(y+1)  
                    gt.teleop_mode(y+1,raw_ENC[y],0,Steer_K1[y],Steer_K2[y],Steer_K3[y],Steer_K4[y])


            #print(time.time() - bg)

# If freeform recordiong is on
            if(software_control[4] == 1 and software_control[5] == 0):
                freeform_record_array[current_freefrom_step][:] = True_rads
                #print(freeform_record_array[current_freefrom_step][:])
                current_freefrom_step = current_freefrom_step + 1
                freeform_record_len = current_freefrom_step
# If executing freeform movement

            if(software_control[4] == 0 and software_control[5] == 1):

                if(current_freefrom_step_execute == 0):
                    for y in range(0,rbt.Joint_num):
                        gt.GOTO_position_HOLD(y+1,rbt.RAD2E(freeform_record_array[0][y],y),30,5.5,1)
                        #print("firstGOTO i sleep 3s")
                    time.sleep(3)

                for m in range(0,rbt.Joint_num):
                    gt.teleop_mode(m+1,rbt.RAD2E(freeform_record_array[current_freefrom_step_execute][m],m),0,Steer_K1[m],Steer_K2[m],Steer_K3[m],Steer_K4[m])

                #print(current_freefrom_step_execute)
                if(current_freefrom_step_execute == freeform_record_len - 1):
                    current_freefrom_step_execute = 0
                    software_control[5] = 0 
                    #print("done")

                if(software_control[5] == 1):
                    current_freefrom_step_execute = current_freefrom_step_execute + 1

                # Ako je current_freefrom_step_execute == freeform_record_len 
                # software_control[5] = 0 
                # current_freefrom_step_execute = 0




# If we want to show plot
            if(software_control[6] == 1):
                #print(freeform_record_len)
                software_control[6] = 0
                plt.plot(freeform_record_array)
                plt.show()

# Clear all recorded
            if(software_control[7] == 1):
                software_control[7] = 0
                freeform_record_array = np.empty(shape=(15000,6),order='C',dtype='object')
                # variable that tells us how many steps we took in our freeform recording
                freeform_record_len = 0
                current_freefrom_step = 0
            tt = tt + 1
            if(tt == 10):
                print((time.time() - bg))
                tt = 0
####################################
        except:
            gt.try_reconnect()
            

def show_graph(p1, p2, p3, p4, p5, p6):
    
    
    while(1):
        #print(p5.value)
        #print(p6.value)
        if p6.value == 0:
            plots.runGraph(p1,p2,p3,p4,p5.value,p6.value)
            p6.value = 1


if __name__ == "__main__":

    Setpoint_Speed_Proc =  multiprocessing.Value('d',0) # return value of speed setpoint
    Setpoint_Acc_Proc =  multiprocessing.Value('d',0) # return value  of acceleration setpoint

    # return value of what translation button is pressed
    # Variables go like this X+,X-,Y+,Y-,Z+,Z-
    Translations_Proc = multiprocessing.Array("i",6, lock=False) 
    
    # Variables go from top top bottom and 1 represents pressed and 0 released
    Left_btns_Proc = multiprocessing.Array("i",6, lock=False) # return value of what left button is pressed
    Right_btns_Proc = multiprocessing.Array("i",6, lock=False) # return value of what right button is pressed

    software_control_variables = multiprocessing.Array("i",8, lock=False) # variables are index values:
        #Index 0: Enable/Disable robot. Disable places it in position hold mode, Enable allows to use other functions(jog, teach...)
                  # 0 is for disabled / 1 is for enabled
        #Index 1: What window is open: 0 - Move, 1 - log, 2 - Teach, 3 - setup
        #Index 2: variable to set motor modes in teach mode/position hold
        #Index 3: Execute flag. If 1 we are executing script if 0 we are not
        #Index 4: Recording freeform movement 1 is for recording 0 for not recordning
        #Index 5: 1 is for executing freeform movement 0 is for not executing freeform
        #Index 6: Show plot 1 is to trigger show
        #Index 7: Clear all recorded


    grav_pos_flag = multiprocessing.Array("i",[1,1,1,1,1,1,1], lock=False) # Used to log what joints should be in gravity compensation and what should be in position hold.
                                                                           # Index 6 (7nth variable) is used to tell us if we are in gravity comp(1) or disable motor(0)

    # These are variables we get packed in one string from master serial port
    # Len is the number of joints available
    p_position = multiprocessing.Array("i", rbt.Joint_num, lock=False) # Raw encoder ticks
    p_position_RADS = multiprocessing.Array("d", rbt.Joint_num, lock=False) # True radians position for kinematic model
    # this includes all offsets and conversions so the robot matches his kinematic model
    p_speed = multiprocessing.Array("i", rbt.Joint_num, lock=False) # Raw Speed in RPM
    p_speed_RADS = multiprocessing.Array("d", rbt.Joint_num, lock=False) # True speed in RAD/S
    p_current = multiprocessing.Array("i", rbt.Joint_num, lock=False)
    p_temperature = multiprocessing.Array("i", rbt.Joint_num, lock=False)
    p_voltage = multiprocessing.Value('i',0)
    p_error =  multiprocessing.Value('i',0)

    proc_value_show_plot =  multiprocessing.Value('i',2)
    proc_value_close_plot =  multiprocessing.Value('i',0)

    p_robot_pose = multiprocessing.Array("d", 6, lock=False) # Current pose of the robot 

    # Variables for Steer mode
    Steer_K1 = multiprocessing.Array("d", rbt.Joint_num, lock=False)
    Steer_K2 = multiprocessing.Array("d", rbt.Joint_num, lock=False)
    Steer_K3 = multiprocessing.Array("d", rbt.Joint_num, lock=False)
    Steer_K4 = multiprocessing.Array("d", rbt.Joint_num, lock=False)


    process1 = multiprocessing.Process(target=Tkinter_GUI,args=[Setpoint_Speed_Proc,Setpoint_Acc_Proc,Translations_Proc,Left_btns_Proc,
                                                                Right_btns_Proc,p_position,p_position_RADS,p_current,p_temperature,
                                                                p_robot_pose,grav_pos_flag,software_control_variables,
                                                                Steer_K1,Steer_K2,Steer_K3,Steer_K4])

    process2 = multiprocessing.Process(target=do_stuff,args=[Left_btns_Proc,Right_btns_Proc,p_position,p_position_RADS,Setpoint_Speed_Proc,
                                                            Setpoint_Acc_Proc,p_current,p_temperature,p_robot_pose,p_speed,p_speed_RADS,
                                                            grav_pos_flag,software_control_variables,Steer_K1,Steer_K2,Steer_K3,Steer_K4])
                                                            

    #proc_position, proc_speed, proc_current, proc_temperature, proc_plot_show, close_event
    process3 = multiprocessing.Process(target=show_graph,args=[p_position_RADS,p_speed_RADS,p_current,p_temperature,proc_value_show_plot,proc_value_close_plot])

    process1.start()
    process2.start()
    process3.start()
    process1.join()
    process2.join()
    process3.join()
    process1.terminate()
    process2.terminate()
    process3.terminate()