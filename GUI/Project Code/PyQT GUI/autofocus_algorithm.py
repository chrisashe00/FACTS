"""
Preliminary autofocus for microscope using the energy in the LaPlace of 
camera as a measure of image contrast 

FS
"""

import cv2 
import numpy as np
import matplotlib.pyplot as plt 

ddepth = cv2.CV_16S
kernel_size = 3
window_name = "Autofocus Testing"
 
#Camera Preamble 
dispW=320
dispH=240
flip=2

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam=cv2.VideoCapture(camSet)
 
#function deciding how to move the objective lens in the z-plane 
def z_move(): 
    distance = distance/2 

    if e_diff > 0:
        direction = 1
        #move by distance 
    elif e_diff < 0:  
        direction = 0
        #move by distance

def reset(): 
    #move objective to initial position
    distance = 100              #total range of movement of the z-stage 
                                #or more likely range over which focussing is possible

def autofocus():
    # Set the threshold for difference in contrast between image[n] and image[n-1]
    e_diff_threshold = 1 

    #Absolute threshold for energy in the LaPlace before the image is deemed in focus 
    e_threshold = 50

    #Take snapshot from camera 
    snapshot = cam.read() 

    #Convert image to greyscale
    grey = cv2.cvtColor(snapshot, cv2.COLOR_BGR2GRAY)  

    #Apply LaPlacian transform to image  
    laplacian = cv2.Laplacian(grey, cv2.CV_64F)   

    # Compute the sum of the absolute values of the Laplacian image
    sum_abs_laplacian = cv2.sumElems(cv2.absdiff(laplacian, 0))[0] 

    # Compute the total number of pixels in the image
    num_pixels = grey.shape[0] * grey.shape[1] 

    # Compute the energy in the Laplacian transform of the image (Contrast)
    energy = sum_abs_laplacian / num_pixels 

    e_diff = energy 

    #counter keeping track of number of iterations of autofocus algorithm
    watchdog_count = 0

    #direction variable on which way z-stage is moved
    direction = 1               # 1 = upwards, 0 = downwards 

    while (e_diff < e_diff_threshold) & (energy < e_threshold): 
        
        #If number of cycles exceeds 25 then finish autofocus algorithm
        if (watchdog_count >25):  
            print("!!! Autofocus Algorithm halted due to too many cycles")
            print("Finished with contrast rating of:", energy)
            break 

        #Move objective lens to new position
        #z_move() 

        #Save save energy value for previous snapshot 
        energy_last = energy

        #Take snapshot from camera 
        snapshot = cam.read() 

        #Convert image to greyscale
        grey = cv2.cvtColor(snapshot, cv2.COLOR_BGR2GRAY)  

        #Apply LaPlacian transform to image  
        laplacian = cv2.Laplacian(grey, cv2.CV_64F)   

        # Compute the sum of the absolute values of the Laplacian image
        sum_abs_laplacian = cv2.sumElems(cv2.absdiff(laplacian, 0))[0] 

        # Compute the total number of pixels in the image
        num_pixels = grey.shape[0] * grey.shape[1] 

        # Compute the energy in the Laplacian transform of the image (Contrast)
        energy = sum_abs_laplacian / num_pixels 

        e_diff = energy - energy_last       

        watchdog_count += 1




