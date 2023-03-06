#Video Functionality in GUI

import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from qtmodern.styles import dark
from qtmodern.windows import ModernWindow

 

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self, camera_id, width, height, fps):
        super().__init__()
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.fps = fps
        self.stopped = False

    def run(self):
        cap = cv2.VideoCapture(self.camera_id, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        cap.set(cv2.CAP_PROP_FPS, self.fps)

        while not self.stopped:
            ret, frame = cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.change_pixmap_signal.emit(q_image)
        cap.release()

               

    def stop(self):
        self.stopped = True
        self.quit()
        self.wait()

 
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('qt_gui_v2.ui', self)
        self.show()

       
        self.thread_cam1 = None
        self.thread_cam2 = None

        self.cam1_on.clicked.connect(self.start_camera1)
        self.cam2_on.clicked.connect(self.start_camera2)

       

    @pyqtSlot(QImage)
    def update_image_cam1(self, q_image):
        pixmap = QPixmap.fromImage(q_image)
        pixmap = pixmap.scaled(self.camfeed1.size(), Qt.KeepAspectRatio)
        self.camfeed1.setPixmap(pixmap)

       

    @pyqtSlot(QImage)
    def update_image_cam2(self, q_image):
        pixmap = QPixmap.fromImage(q_image)
        pixmap = pixmap.scaled(self.camfeed2.size(), Qt.KeepAspectRatio)
        self.camfeed2.setPixmap(pixmap)

       

    def start_camera1(self):
        if self.thread_cam1 is None:
            self.thread_cam1 = VideoThread(0, 320, 240, 30)
            self.thread_cam1.change_pixmap_signal.connect(self.update_image_cam1)
            self.thread_cam1.start()
           

    def start_camera2(self):
        if self.thread_cam2 is None:
            self.thread_cam2 = VideoThread(1, 320, 240, 30)
            self.thread_cam2.change_pixmap_signal.connect(self.update_image_cam2)
            self.thread_cam2.start()

           

    def closeEvent(self, event):
        if self.thread_cam1 is not None:
            self.thread_cam1.stop()
        if self.thread_cam2 is not None:
            self.thread_cam2.stop()