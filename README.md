# Welcome to MIP!

## What is in this Repository? 
This Github Repo contains all the code used to control the Microscopy Imaging Platform (MIP) that was created during this project. This Code can be built upon to control similar microscopy platforms of various imaging modalities.


This Repo contains the three key components involved in controlling the microscope through electronics and Graphical User Interfaces (GUI). This project has constructed MIP based on the design methodology of the open source microscopy 
platform UC2 ('You See Too') (LINK: http://useetoo.org), if you have not constructed a speicific microscope setup and just want to see how some of this code works we have outlined some of the requirements just to make the important files run smoothly!

Before proceeding it should be known that the software code was implemented in a Jetson Nano and therefore the GUI and Autofocus algortithms will only run to an extent before requiring a Raspberry Pi dual camera feed. 

This repository is divided into three main folders: GUI, Autofocus and Electronics.

# GUI

This folder contains all the code required to run the Graphical User Interface on the NVIDIA Jetson Nano. if you just want to see how the GUI looks and inspect the code you can also run the code but there will be no camera functionality. Here are the steps to run either of the

## How To Setup and use the GUI

With the Repository cloned locally on your machine you can follow these steps to run the GUI on any machine.

1 Open the terminal in your IDE (we recommend VS code) or on your device

2 Change Directory ('cd') to where the FACTS folder is located

3 activate the virtual environment using the terminal

 ```
 GUI\env\Scripts\activate
```

4 Install the python requirements using the terminal

```
pip install -r GUI\requirements.txt
```

5 Run the Camera Vision GUI (no camera vision without Cameras)

```
python GUI\TS_CV.py
```

6 Run the Image Processing GUI (full functionality)

```
python GUI\TS_IP.py
```
