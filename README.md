[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

# Dependancy:

Tested on Ubuntu 18.04.5 LTS running on virtual machine

Running Python 3.6.9 (default, Jan 26 2021, 15:33:00)

Robotic toolbox version - Downloaded 9.3.2021 - Realease 6 v0.9.1  https://github.com/petercorke/robotics-toolbox-python

For additional python packages check /info_folder/versions_info

# Installation steps

After installation of Robotic toolbox you will need to add:

__init__.py and CM6.py from robotic_toolbox_CM6_models folder to installation folder of robotic toolbox library: 

...robotic-toolbox-python/robotictoolbox/models/DH

* After everything is installed when you run Multi_proc_main.py you should get a screen as shown on first image. If you get error for this step: in get_send_data.py file comment s.open() part of code.
* To run this code in tandem with your robot you will need to modify get_send_data.py to your COM port. And you will need to be running mainboard code on your MCU.

# CM6_control_software

CM6_control_software allows "easy" programming of CM6 robot. GUI software was written in python and heavily relies on Peter Corke's robotic toolbox for python! It was tested on Linux virtual machine, laptop running Linux, and raspberry pi 4!

The software offers real-time monitoring of robots:

* Motor position, current, speed, temperature
* End effector position
* Operating modes, errors...
* 
Available modes at this moment are:

* Individual motor jogging 
* freehand teach 
* move from point to point 

Each of these modes of movement can be recorded and replayed!

<img src="https://user-images.githubusercontent.com/30388414/125832896-2a89a1bf-fb66-4173-98a5-139b419b0507.png" width="1200"> 
<img src="https://user-images.githubusercontent.com/30388414/125832902-b11a0970-e8ef-4438-8df5-100ae0ac9608.png" width="1200"> 

Dependancy:


How to install:



# Support the project

This project is completely Open source and free to all and I would like to keep it that way, so any help 
in terms of donations or advice is really appreciated. Thank you!

[![Check the arm in action !](https://user-images.githubusercontent.com/30388414/86798915-a036ba00-c071-11ea-824d-4456f2cdf797.png)](https://paypal.me/PCrnjak?locale.x=en_US)

# Project is under MIT Licence
