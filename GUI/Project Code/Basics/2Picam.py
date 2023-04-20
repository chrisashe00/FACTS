import cv2

# initialize camera 1
cam1 = cv2.VideoCapture(0)

# initialize camera 2
cam2 = cv2.VideoCapture(1)

while True:
    # read frame from camera 1
    ret1, frame1 = cam1.read()
    
    # read frame from camera 2
    ret2, frame2 = cam2.read()
    
    # display frames in separate windows
    cv2.imshow('Camera 1', frame1)
    cv2.imshow('Camera 2', frame2)
    
    # wait for key press
    key = cv2.waitKey(1)
    if key == 27:   # press ESC to exit
        break

# release camera resources
cam1.release()
cam2.release()

# close all windows
cv2.destroyAllWindows()
