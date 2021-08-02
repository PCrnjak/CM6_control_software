
""" Writen by: Petar Crnjak
Date: 20.10.2020
Tested on: Python 3.8.5
           matplotlib 3.3.2 """

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# All these variables should be multi-process variables 
# Proc_plot_show tells us what plot we are showing i.e. position, speed, current, temperature
# 0 is position, 1 is speed, 2 is current and 3 is temperature!
# If close_event is 1 animation is closed if it is 0 it is open and running
# When plot is closed directly (By pressing X), under runGraph() you should set close_event multi-process variable to 1
# If you dont do that when you close plot with "X" it will re-open itself
# proc_position, speed, current and temperature are lists from 1-7 elements.
# Plot will always open at same position on screen and with same size. 
# Once opened you can resize and move it! 
# runGraph is loop by itself but once we exit it we cant re run it unless we are in another loop 
# since it is written to be used in multi-procces aplications you need to place runGraph in external loop 
# That loop will then control when it is opened and closed

def runGraph(proc_position, proc_speed, proc_current, proc_temperature, proc_plot_show, close_event):

    # This function selects what labels to show
    def showing_plot():

        # if plot is position / joint angles
        if proc_plot_show == 0:

            y_range = [-4, 4] # What range to show on Y axis
            ax.set_ylim(y_range)
            plt.xlabel('Samples [10ms] ', weight='bold')
            plt.ylabel('Joint angle [deg]', weight='bold')
            plt.legend(legend_print,bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=2, borderaxespad=0.)

            plt.grid(True)
            plt.tight_layout()

        # if plot is speed
        elif proc_plot_show == 1:

            y_range = [-10.0, 10.0] # What range to show on Y axis
            ax.set_ylim(y_range)
            plt.xlabel('Samples [10ms] ', weight='bold')
            plt.ylabel('Joint speed [RPM]', weight='bold')
            plt.legend(legend_print,bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=2, borderaxespad=0.)

            plt.grid(True)
            plt.tight_layout()

        #if plot is current
        elif proc_plot_show == 2:

            y_range = [0, 2000] # What range to show on Y axis
            ax.set_ylim(y_range)
            plt.xlabel('Samples [10ms] ', weight='bold')
            plt.ylabel('Joint curent [RPM]', weight='bold')
            plt.legend(legend_print,bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=2, borderaxespad=0.)

            plt.grid(True)
            plt.tight_layout()

        elif proc_plot_show == 3:

            y_range = [-5, 90] # What range to show on Y axis
            ax.set_ylim(y_range)
            plt.xlabel('Samples [10ms] ', weight='bold')
            plt.ylabel('Joint temperature [RPM]', weight='bold')
            plt.legend(legend_print,bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=2, borderaxespad=0.)

            plt.grid(True)
            plt.tight_layout()


    matplotlib.use("TkAgg") # set the backend  
    x_len = 1000         # Number of points to display on X axis
    plt.style.use('bmh')   
    data_len = len(proc_position) # Check length of data touple. 
    line = [None] * 7

    ys1 = [0] * x_len
    ys2 = [0] * x_len
    ys3 = [0] * x_len
    ys4 = [0] * x_len
    ys5 = [0] * x_len
    ys6 = [0] * x_len
    ys7 = [0] * x_len

    color_range = ["r", "g", "b", "y", "m", "k", "c"]

    # https://stackoverflow.com/questions/28575192/how-do-i-set-the-matplotlib-window-size-for-the-macosx-backend
    fig = plt.figure(figsize=(5, 3))
    # https://stackoverflow.com/questions/7449585/how-do-you-set-the-absolute-position-of-figure-windows-with-matplotlib
    fig.canvas.manager.window.wm_geometry("+%d+%d" % (1500, 700))
    #fig.canvas.manager.window.attributes('-topmost', 1)
    #fig.canvas.manager.window.set_keep_above

    #fig.canvas.toolbar.pack_forget()
    ax = fig.add_subplot(1, 1, 1) 
    xs = list(range(0, x_len))

    legend_print = [] # What data we will print in legend

    for x in range(data_len):
        if proc_plot_show == 0:
            legend_print.append("Pos" + str(x+1))
        elif proc_plot_show == 1:
            legend_print.append("Spd" + str(x+1))
        elif proc_plot_show == 2:
            legend_print.append("Cur" + str(x+1))
        elif proc_plot_show == 3:
            legend_print.append("Temp" + str(x+1))


    # Creating blank lines      
    line[0], = ax.plot(xs, ys1, color = color_range[0])
    line[1], = ax.plot(xs, ys2, color = color_range[1])
    line[2], = ax.plot(xs, ys3, color = color_range[2])
    line[3], = ax.plot(xs, ys4, color = color_range[3])
    line[4], = ax.plot(xs, ys5, color = color_range[4])
    line[5], = ax.plot(xs, ys6, color = color_range[5])
    line[6], = ax.plot(xs, ys7, color = color_range[6])

    data_show = []
    showing_plot()

    # This function is called periodically from FuncAnimation
    def on_close(event):
        event.canvas.figure.axes[0].has_been_closed = True
        print ('Closed Figure with X')

    def data_append():

        if proc_plot_show == 0:
            data_show = proc_position
        elif proc_plot_show == 1:
            data_show = proc_speed
        elif proc_plot_show == 2:
            data_show = proc_current
        elif proc_plot_show == 3:
            data_show = proc_temperature
 
        if data_len == 1:
            ys1.append(data_show[0])
        elif data_len == 2:
            ys1.append(data_show[0])
            ys2.append(data_show[1])
        elif data_len == 3:
            ys1.append(data_show[0])
            ys2.append(data_show[1])
            ys3.append(data_show[2])
        elif data_len == 4:
            ys1.append(data_show[0])
            ys2.append(data_show[1])
            ys3.append(data_show[2])
            ys4.append(data_show[3])
        elif data_len == 5:
            ys1.append(data_show[0])
            ys2.append(data_show[1])
            ys3.append(data_show[2])
            ys4.append(data_show[3])
            ys5.append(data_show[4])
        elif data_len == 6:
            ys1.append(data_show[0])
            ys2.append(data_show[1])
            ys3.append(data_show[2])
            ys4.append(data_show[3])
            ys5.append(data_show[4])
            ys6.append(data_show[5])
        elif data_len == 7:
            ys1.append(data_show[0])
            ys2.append(data_show[1])
            ys3.append(data_show[2])
            ys4.append(data_show[3])
            ys5.append(data_show[4])
            ys6.append(data_show[5])
            ys7.append(data_show[6])

    def animate(i, ys1, ys2, ys3, ys4, ys5, ys6, ys7):

        data_append()

        ys1 = ys1[-x_len:]
        ys2 = ys2[-x_len:]
        ys3 = ys3[-x_len:]
        ys4 = ys4[-x_len:]
        ys5 = ys5[-x_len:]
        ys6 = ys6[-x_len:]
        ys7 = ys7[-x_len:]

        fig.canvas.mpl_connect('close_event', on_close)

        if close_event == 1:
            ani.event_source.stop()  

        if data_len == 0:
            line[0].set_ydata(ys1)
        elif data_len == 1:
            line[0].set_ydata(ys1)
            line[1].set_ydata(ys2)
        elif data_len == 2:
            line[0].set_ydata(ys1)
            line[1].set_ydata(ys2)
            line[2].set_ydata(ys3)
        elif data_len == 3:
            line[0].set_ydata(ys1)
            line[1].set_ydata(ys2)
            line[2].set_ydata(ys3)
            line[3].set_ydata(ys4)
        elif data_len == 4:
            line[0].set_ydata(ys1)
            line[1].set_ydata(ys2)
            line[2].set_ydata(ys3)
            line[3].set_ydata(ys4)
            line[4].set_ydata(ys5)
        elif data_len == 5:
            line[0].set_ydata(ys1)
            line[1].set_ydata(ys2)
            line[2].set_ydata(ys3)
            line[3].set_ydata(ys4)
            line[4].set_ydata(ys5)
            line[5].set_ydata(ys6)
        elif data_len == 6:
            line[0].set_ydata(ys1)
            line[1].set_ydata(ys2)
            line[2].set_ydata(ys3)
            line[3].set_ydata(ys4)
            line[4].set_ydata(ys5)
            line[5].set_ydata(ys6)
            line[6].set_ydata(ys7)


        return line[0], line[1], line[2], line[3], line[4], line[5], line[6]

    ani = FuncAnimation(fig,
        animate,
        fargs=(ys1, ys2, ys3, ys4, ys5, ys6, ys7,),
        interval=50,
        blit=True)

    plt.show()

    
if __name__ == "__main__":
    close = True
    while(1):
        #ove variable dobivam od drugog procesa
        var1 = [5.213 ,7.312,9.213,3.12,2.13,1.12]
        var2 = [0.5 ,0.7,0.9,0.3,0.2,0.100]
        var3 = [500 ,700,90,300,200,100]
        var4 = [50 ,70,90,30,20,10]
        #close = True
        if close == True :
            # sve ove variable koje tu prima su multi_proc varijable
            # runGraph(proc_position, proc_speed, proc_current, proc_temperature, proc_plot_show, close_event):
            runGraph(var1,var2,var3,var4,0,0) # event close zatvara kada je 1
            # u proces loopu kada dodem do ove linije kazem da je close_event globalna varijabla = 1 tako da se 
            # graf više ne otvara
            #print(ev)
            print("run")
            #close = False