import cv2

dispW = 320
dispH = 240
flip = 2

# Camera 1
camSet1 = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam1 = cv2.VideoCapture(camSet1)

# Camera 2
camSet2 = 'nvarguscamerasrc sensor-id=1 ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam2 = cv2.VideoCapture(camSet2)

while True:
    # Read frames from both cameras
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()

    # Show frames
    cv2.imshow('Camera 1', frame1)
    cv2.imshow('Camera 2', frame2)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release cameras and destroy windows
cam1.release()
cam2.release()
cv2.destroyAllWindows()
