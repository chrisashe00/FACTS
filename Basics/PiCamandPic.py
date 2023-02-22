import cv2
print(cv2._version_)
dispW=320
dispH=240
flip=2

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam=cv2.VideoCapture(camSet)
while True:
    ret, frame=cam.read()
    cv2.imshow('piCam',frame)
    if cv2.waitKey(1)==ord('q'):
        break
    elif cv2.waitKey(1) == ord('p'):
        cv2.imwrite('picture.jpg', frame)
        print("Picture taken!")
        img = cv2.imread(' Picture.jpg')
        cv2.imshow('Picture Taken', img)
cam.release()
cv2.destroyAllWindows()