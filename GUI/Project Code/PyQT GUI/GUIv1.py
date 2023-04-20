import sys
import cv2
import threading
import numpy as np
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.uic import loadUi
from qtmodern.styles import dark
from qtmodern.windows import ModernWindow

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi('qt_gui.ui', self)
        self.show()

        # Connect buttons to their respective functions
        self.cam1_on.clicked.connect(self.start_left_camera)
        self.cam1_off.clicked.connect(self.stop_left_camera)
        self.cam2_on.clicked.connect(self.start_right_camera)
        self.cam2_off.clicked.connect(self.stop_right_camera)
        self.img1_takeimg.clicked.connect(self.capture_left_camera_image)
        self.img2_takeimg.clicked.connect(self.capture_right_camera_image)

        # Initialize camera instances
        self.left_camera = CSI_Camera()
        self.right_camera = CSI_Camera()

    def start_left_camera(self):
        self.left_camera.open(gstreamer_pipeline(sensor_id=0, capture_width=1280, capture_height=720, flip_method=2, display_width=960, display_height=540))
        self.left_camera.start()
        self.left_camera_update_thread = QThread()
        self.left_camera_update_thread.run = self.update_left_camera_feed
        self.left_camera_update_thread.start()

    def stop_left_camera(self):
        self.left_camera.stop()
        self.left_camera.release()
        self.left_camera_update_thread.quit()
        self.camfeed1.setPixmap(QPixmap())

    def start_right_camera(self):
        self.right_camera.open(gstreamer_pipeline(sensor_id=1, capture_width=1280, capture_height=720, flip_method=2, display_width=960, display_height=540))
        self.right_camera.start()
        self.right_camera_update_thread = QThread()
        self.right_camera_update_thread.run = self.update_right_camera_feed
        self.right_camera_update_thread.start()

    def stop_right_camera(self):
        self.right_camera.stop()
        self.right_camera.release()
        self.right_camera_update_thread.quit()
        self.camfeed1.setPixmap(QPixmap())

    def update_left_camera_feed(self):
        while self.left_camera.running:
            grabbed, frame = self.left_camera.read()
            if grabbed:
                qimage = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
                pixmap = QPixmap.fromImage(qimage)
                self.camfeed1.setPixmap(pixmap)

    def update_right_camera_feed(self):
        while self.right_camera.running:
            grabbed, frame = self.right_camera.read()
            if grabbed:
                qimage = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
                pixmap = QPixmap.fromImage(qimage)
                self.camfeed2.setPixmap(pixmap)

#Setup the CSI Camera Class
class CSI_Camera:
    def __init__(self):
        # Initialize instance variables
        # OpenCV video capture element
        self.video_capture = None
        # The last captured image from the camera
        self.frame = None
        self.grabbed = False
        # The thread where the video capture runs
        self.read_thread = None
        self.read_lock = threading.Lock()
        self.running = False

    def open(self, gstreamer_pipeline_string):
        try:
            self.video_capture = cv2.VideoCapture(gstreamer_pipeline_string, cv2.CAP_GSTREAMER)
            # Grab the first frame to start the video capturing
            self.grabbed, self.frame = self.video_capture.read()
        except RuntimeError:
            self.video_capture = None
            print("Unable to open camera")
            print("Pipeline: " + gstreamer_pipeline_string)

    def start(self):
        if self.running:
            print('Video capturing is already running')
            return None
        # create a thread to read the camera image
        if self.video_capture != None:
            self.running = True
            self.read_thread = threading.Thread(target=self.updateCamera)
            self.read_thread.start()
        return self

    def stop(self):
        self.running = False
        # Kill the thread
        self.read_thread.join()
        self.read_thread = None

    def updateCamera(self):
        # This is the thread to read images from the camera
        while self.running:
            try:
                grabbed, frame = self.video_capture.read()
                with self.read_lock:
                    self.grabbed = grabbed
                    self.frame = frame
            except RuntimeError:
                print("Could not read image from camera")
        # FIX ME - stop and cleanup thread
        # Something bad happened

    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
            grabbed = self.grabbed
        return grabbed, frame

    def release(self):
        if self.video_capture != None:
            self.video_capture.release()
            self.video_capture = None
        # Now kill the thread
        if self.read_thread != None:
            self.read_thread.join()

#Gstreamer pipeline function 
def gstreamer_pipeline(sensor_id=0,capture_width=1920,capture_height=1080,display_width=1920,display_height=1080,framerate=30,flip_method=0,):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (sensor_id,capture_width,capture_height,framerate,flip_method,display_width,display_height,)
    )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    dark(app)
    modern_window = ModernWindow(window)
    modern_window.show()
    sys.exit(app.exec_())
