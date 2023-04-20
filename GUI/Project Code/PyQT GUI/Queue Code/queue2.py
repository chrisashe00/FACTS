# Import Modules 
#Qtimer method
import sys
import cv2
import numpy as np
import threading
import queue
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
    frame_ready = pyqtSignal(np.ndarray)

    def __init__(self):
        QThread.__init__(self)
        self.running = False
        self.video_capture = None

    def open(self, gstreamer_pipeline_string):
        try:
            self.video_capture = cv2.VideoCapture(
                gstreamer_pipeline_string, cv2.CAP_GSTREAMER
            )
        except RuntimeError:
            self.video_capture = None
            print("Unable to open camera")
            print("Pipeline: " + gstreamer_pipeline_string)

    def start_camera(self, sensor_id):
        self.open(gstreamer_pipeline(sensor_id=sensor_id))
        self.running = True
        super().start()

    def stop_camera(self):
        self.running = False
        self.wait()

    def run(self):
        while self.running:
            try:
                grabbed, frame = self.video_capture.read()
                if grabbed:
                    self.frame_ready.emit(frame)
            except RuntimeError:
                print("Could not read image from camera")
                break
        self.video_capture.release()

    def release(self):
        if self.video_capture is not None:
            self.video_capture.release()
            self.video_capture = None

class CameraGUI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.camera1 = CSI_Camera()
        self.camera2 = CSI_Camera()
        loadUi('qt_gui.ui', self)
        self.show()

        self.camfeed1_label = self.camfeed1
        self.camfeed2_label = self.camfeed2

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_camfeeds)

        self.cam1_on.clicked.connect(lambda: self.start_camera(0))
        self.cam1_off.clicked.connect(lambda: self.stop_camera(0))
        self.cam2_on.clicked.connect(lambda: self.start_camera(1))
        self.cam2_off.clicked.connect(lambda: self.stop_camera(1))

    @pyqtSlot(int)
    def start_camera(self, sensor_id):
        if sensor_id == 0:
            self.camera1.start_camera(sensor_id)
            self.timer.start()
        elif sensor_id == 1:
            self.camera2.start_camera(sensor_id)
            self.timer.start()

    def stop_camera(self, sensor_id):
        if sensor_id == 0:
            self.camera1.stop_camera()
            self.timer.stop()
            self.camfeed1_label.clear()
        elif sensor_id == 1:
            self.camera2.stop_camera()
            self.timer.stop()
            self.camfeed2_label.clear()

    def update_camfeed(self, label, camera):
        try:
            grabbed, frame = camera.video_capture.read()
            if grabbed:
                resized_frame = cv2.resize(frame, (label.width(), label.height()))
                rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                qimage = QImage(rgb_frame.data, rgb_frame.shape[1], rgb_frame.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimage)
                label.setPixmap(pixmap)
        except RuntimeError:
            pass

    @pyqtSlot(np.ndarray)
    def update_camfeed1(self, frame):
        self.camfeed1_frame = frame

    @pyqtSlot(np.ndarray)
    def update_camfeed2(self, frame):
        self.camfeed2_frame = frame

    def update_camfeeds(self):
        if hasattr(self, 'camfeed1_frame'):
            resized_frame = cv2.resize(self.camfeed1_frame, (self.camfeed1_label.width(), self.camfeed1_label.height()))
            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            qimage = QImage(rgb_frame.data, rgb_frame.shape[1], rgb_frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            self.camfeed1_label.setPixmap(pixmap)
        if hasattr(self, 'camfeed2_frame'):
            resized_frame = cv2.resize(self.camfeed2_frame, (self.camfeed2_label.width(), self.camfeed2_label.height()))
            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            qimage = QImage(rgb_frame.data, rgb_frame.shape[1], rgb_frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            self.camfeed2_label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.camera1.stop_camera()
        self.camera2.stop_camera()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraGUI()
    dark(app)
    modern_window = ModernWindow(window)
    modern_window.show()
    sys.exit(app.exec_())


