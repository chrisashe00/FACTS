# Welcome to MIP SOFTWARE!

## What is in this Repository? 
This Github Repo contains all the code used to control the Microscopy Imaging Platform (MIP) that was created during this project. This Code can be built upon to control similar microscopy platforms of various imaging modalities.


This Repo contains the three key components involved in controlling the microscope through electronics and Graphical User Interfaces (GUI). This project has constructed MIP based on the design methodology of the open source microscopy 
platform UC2 ('You See Too') (LINK: http://useetoo.org), if you have not constructed a specific microscope setup and just want to see how some of this code works we have outlined some of the requirements just to make the important files run smoothly!

Before proceeding it should be known that the software code was implemented in a Jetson Nano and therefore the GUI and Autofocus algortithms will only run to an extent before requiring a Raspberry Pi dual camera feed. You should also have some version of python installed on a windows OS computer.

This repository is divided into three main folders: GUI, Autofocus and Electronics.

Any Issues please raise an issue in the above 'issues' tab or email: *chris.ashe.2018@uni.strath.ac.uk*

# GUI

This folder contains all the code required to run the Graphical User Interface on the NVIDIA Jetson Nano. if you just want to see how the GUI looks and inspect the code you can also run the code but there will be no camera functionality. Here are the steps to run either of the

## How To Setup and use the GUI

With the Repository cloned locally on your machine you can follow these steps to run the GUI on any machine.

1. Open the terminal in your IDE (we recommend VS code) or on your device

2. Change Directory ('cd') to where the FACTS folder is located from your clone, your file path should end in 

```
...\FACTS
```

3. You will need to make a virtual environment to run the code, create a virtual environment to run the GUI code with this command

```
virtualenv GUI\env  
```

4. Activate the new virtual envrionment 

```
GUI\env\Scripts\activate 
```

5. Now install the required libraries to run the GUIs using:

```
pip install -r GUI\requirements.txt
```


*Now you may run either the camera vision GUI or Image Processing GUI*


7. To run camera vision GUI (will not have any camera vision if not on JETSON NANO) use the command:

```
python GUI\TS_CV.py
```

8 To run the imge processing GUI use: 

```
python GUI\TS_IP.py
```

# Autofocus 

The autofocus code uses serial communication between an NVIDIA Jetson Nano and ESP32 to control a stepper motor based on the autofocus commands, there's not much you can do with this code without a jetson nano and a esp32 and stepper motor, please read our report for more details on our build process and how each sub system interacts to replicate the autofocus routine!

# Electronics Control

The electronics folder includes a number of files however the important one is simply main.cpp. Open the electronics folder in VS code and install the platformIO plugin. You can use platformIO to compile and upload the code to an ESP32. Like autofocus, there is not much you can do with this code without the respective electronics hardware *(build specified in report)* and system but this code could be applied to a number of different microscope setups so please apply it wherever you need in your project!

find out how to add platformIO to your project here: https://platformio.org/install (install PlatformIO for VSCode)


Once PlatformIO is added to this project, you need to install the relevant header .h libraries using the PlatformIO home screen. Then you can compile and upload this code to an ESP32 and control your microscope!
