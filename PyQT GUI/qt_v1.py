#V1 - Video Functionality on GUI 
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

    def __init__(self, camera_id):
        super(VideoThread, self).__init__()
        self.camera_id = camera_id

    def run(self):
        cap = cv2.VideoCapture(self.camera_id)
        while True:
            ret, frame = cap.read()
            if ret:
                # Convert the frame to a QImage
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

                # Emit the signal to update the pixmap in the GUI thread
                self.change_pixmap_signal.emit(q_image)

    def stop(self):
        self.quit()
        self.wait()

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi('qt_gui.ui', self)
        self.show()

        self.thread_cam1 = None
        self.thread_cam2 = None

        # Connect the camera 1 button to the start_camera1 function
        self.cam1_on.clicked.connect(self.start_camera1)
        # Connect the camera 2 button to the start_camera2 function
        self.cam2_on.clicked.connect(self.start_camera2)

    @pyqtSlot(QImage)
    def update_image_cam1(self, q_image):
        pixmap = QPixmap.fromImage(q_image)
        self.camfeed1.setPixmap(pixmap)

    @pyqtSlot(QImage)
    def update_image_cam2(self, q_image):
        pixmap = QPixmap.fromImage(q_image)
        self.camfeed2.setPixmap(pixmap)

    def start_camera1(self):
        if self.thread_cam1 is None:
            self.thread_cam1 = VideoThread(0)
            self.thread_cam1.change_pixmap_signal.connect(self.update_image_cam1)
            self.thread_cam1.start()

    def start_camera2(self):
        if self.thread_cam2 is None:
            self.thread_cam2 = VideoThread(1)
            self.thread_cam2.change_pixmap_signal.connect(self.update_image_cam2)
            self.thread_cam2.start()

    def closeEvent(self, event):
        if self.thread_cam1 is not None:
            self.thread_cam1.stop()
        if self.thread_cam2 is not None:
            self.thread_cam2.stop()
        event.accept()       

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    dark(app)
    modern_window = ModernWindow(window)
    modern_window.show()
    sys.exit(app.exec_())