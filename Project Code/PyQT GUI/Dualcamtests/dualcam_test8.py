#Import Modules 
import sys
import cv2
import numpy as np
import threading
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from qtmodern.styles import dark
from qtmodern.windows import ModernWindow

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=1920,
    display_height=1080,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id={} ! "
        "video/x-raw(memory:NVMM), width=(int){}, height=(int){}, framerate=(fraction){}/1 ! "
        "nvvidconv flip-method={} ! "
        "video/x-raw, width=(int){}, height=(int){}, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! "
        "appsink".format(
            sensor_id, capture_width, capture_height, framerate, flip_method, display_width, display_height
        )
    )

class CSI_Camera(QThread):
    start_feed = pyqtSignal(int)
    stop_feed = pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)
        # Initialize instance variables
        # OpenCV video capture element
        self.video_capture = None
        # The last captured image from the camera
        self.frame = None
        self.grabbed = False
        self.running = False
        self.read_lock = threading.Lock()

        # Connect the signals to start and stop camera feeds
        self.start_feed.connect(self.start_camera)
        self.stop_feed.connect(self.stop_camera)

    def open(self, gstreamer_pipeline_string):
        try:
            self.video_capture = cv2.VideoCapture(
                gstreamer_pipeline_string, cv2.CAP_GSTREAMER
            )
            # Grab the first frame to start the video capturing
            self.grabbed, self.frame = self.video_capture.read()

        except RuntimeError:
            self.video_capture = None
            print("Unable to open camera")
            print("Pipeline: " + gstreamer_pipeline_string)

    def start_camera(self, sensor_id):
        # Open the camera and start the thread to read frames
        self.open(gstreamer_pipeline(sensor_id=sensor_id))
        self.start()

    def stop_camera(self, sensor_id):
        # Stop the camera feed and release the video capture resources
        self.stop()
        self.release()

    def start(self):
        if self.running:
            print('Video capturing is already running')
            return
        # create a thread to read the camera image
        if self.video_capture is not None:
            self.running = True
            super().start()

    def run(self):
        # This is the thread to read images from the camera
        while self.running:
            try:
                grabbed, frame = self.video_capture.read()
                with self.read_lock:
                    self.grabbed = grabbed
                    self.frame = frame
            except RuntimeError:
                print("Could not read image from camera")
                break
        # Release the video capture resources
        self.release()

    def stop(self):
        self.running = False

    def read(self):
        
        with self.read_lock:
            return self.grabbed, self.frame.copy()


    def release(self):
        if self.video_capture is not None:
            self.video_capture.release()
            self.video_capture = None

class CameraGUI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.camera1 = CSI_Camera() # instantiate CSI_Camera for camera 1
        self.camera2 = CSI_Camera() # instantiate CSI_Camera for camera 2
        loadUi('qt_gui.ui', self)
        self.show()

        # Connect the button presses to the signals
        self.cam1_on.clicked.connect(lambda: self.start_camera(0))
        self.cam1_off.clicked.connect(lambda: self.stop_camera(0))
        self.cam2_on.clicked.connect(lambda: self.start_camera(1))
        self.cam2_off.clicked.connect(lambda: self.stop_camera(1))

        # Create QLabel widgets for displaying camera feeds
        self.camfeed1_label = self.camfeed1
        self.camfeed2_label = self.camfeed2

        # Create a separate thread for updating camfeed1
        self.thread_camfeed1 = None

        # Create a separate thread for updating camfeed2
        self.thread_camfeed2 = None

    @pyqtSlot(int)
    def start_camera(self, sensor_id):
        if sensor_id == 0:
            # Open the camera and start the thread to read frames for camera 1
            self.camera1.open(gstreamer_pipeline(sensor_id=sensor_id))
            self.camera1.start()
            self.thread_camfeed1 = threading.Thread(target=self.update_camfeed1, args=(self.camfeed1_label, self.camera1))
            self.thread_camfeed1.start()
        elif sensor_id == 1:
            # Open the camera and start the thread to read frames for camera 2
            self.camera2.open(gstreamer_pipeline(sensor_id=sensor_id))
            self.camera2.start()
            self.thread_camfeed2 = threading.Thread(target=self.update_camfeed2, args=(self.camfeed2_label, self.camera2))
            self.thread_camfeed2.start()

    @pyqtSlot(int)
    def stop_camera(self, sensor_id):
        if sensor_id == 0:
            # Stop the thread for updating camfeed1 and release camera 1
            self.thread_camfeed1.join()
            self.camera1.stop()
            self.camera1.release()
            # Clear the QLabel widget for camera 1
            self.camfeed1_label.clear()
        elif sensor_id == 1:
            # Stop the thread for updating camfeed2 and release camera 2
            self.thread_camfeed2.join()
            self.camera2.stop()
            self.camera2.release()
            # Clear the QLabel widget for camera 2
            self.camfeed2_label.clear()

    def update_camfeed1(self, label, camera):
        while camera.running:
            grabbed, frame = camera.read()
            if grabbed:
                # Resize the frame to fit in the label
                resized_frame = cv2.resize(frame, (label.width(), label.height()))
                # Convert the frame from BGR to RGB
                rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                # Convert the frame to QImage and display it in the label
                qimage = QImage(rgb_frame.data, rgb_frame.shape[1], rgb_frame.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimage)
                label.setPixmap(pixmap)

    def update_camfeed2(self, label, camera):
        while camera.running:
            grabbed, frame = camera.read()
            if grabbed:
                # Resize the frame to fit in the label
                resized_frame = cv2.resize(frame, (label.width(), label.height()))
                # Convert the frame from BGR to RGB
                rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                # Convert the frame to QImage and display it in the label
                qimage = QImage(rgb_frame.data, rgb_frame.shape[1], rgb_frame.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimage)
                label.setPixmap(pixmap)

    def closeEvent(self, event):
        # Stop the camera feed and release the video capture resources when
        # closing the GUI
        self.camera1.stop()
        self.camera1.release()
        self.camera2.stop()
        self.camera2.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraGUI()
    dark(app)
    modern_window = ModernWindow(window)
    modern_window.show()
    sys.exit(app.exec_())

