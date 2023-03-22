#Greyscale
import sys
import cv2
import os 
import time 
import threading
import numpy as np
from time import sleep
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.uic import loadUi
from qtmodern.styles import dark
from qtmodern.windows import ModernWindow

#Helper Functions
def qimage_to_np(qimage):
        buffer = qimage.bits().asstring(qimage.byteCount())
        np_image = np.frombuffer(buffer, np.uint8).reshape((qimage.height(), qimage.width(), -1))
        return np_image

def np_to_qimage(np_image):
        height, width, channel = np_image.shape
        bytes_per_line = 3 * width
        return QImage(np_image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

def apply_noise_reduction_to_pixmap(pixmap):
    if pixmap is None:
        return None

    img = pixmap.toImage()
    np_image = qimage_to_np(img)
    np_image = cv2.fastNlMeansDenoising(np_image, None, 10, 7, 21)
    img = np_to_qimage(np_image)

    return QPixmap.fromImage(img)

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
        self.cam2_img.clicked.connect(self.capture_right_camera_image)
        self.cam1_bri_slider.valueChanged.connect(self.adjust_left_camera_brightness)
        self.cam2_bri_slider.valueChanged.connect(self.adjust_right_camera_brightness)
        self.img1_bri_slider.valueChanged.connect(self.adjust_left_image_brightness)
        self.img2_bri_slider.valueChanged.connect(self.adjust_right_image_brightness)
        self.cam1_con_slider.valueChanged.connect(self.adjust_left_camera_contrast)
        self.cam2_con_slider.valueChanged.connect(self.adjust_right_camera_contrast)
        self.img1_con_slider.valueChanged.connect(self.adjust_imgcam1_contrast)
        self.img2_con_slider.valueChanged.connect(self.adjust_imgcam2_contrast)
        self.cam1_denoise.clicked.connect(self.toggle_left_camera_noise_reduction)
        self.cam2_denoise.clicked.connect(self.toggle_right_camera_noise_reduction)
        self.img1_denoise.clicked.connect(self.apply_left_image_noise_reduction)
        self.img2_denoise.clicked.connect(self.apply_right_image_noise_reduction)

        #Noise Reduction initialise 
        self.left_camera_noise_reduction = False
        self.right_camera_noise_reduction = False

        # Initialize camera instances
        self.left_camera = CSI_Camera()
        self.right_camera = CSI_Camera()

    def start_left_camera(self):
        self.left_camera.open(gstreamer_pipeline(sensor_id=0, capture_width=1280, capture_height=720, flip_method=2, display_width=960, display_height=540))
        self.left_camera.start()
        self.left_camera.frame_received.connect(self.update_left_camera_feed)

    def stop_left_camera(self):
        self.left_camera.stop()
        self.left_camera.release()
        self.camfeed1.setPixmap(QPixmap())

    def start_right_camera(self):
        self.right_camera.open(gstreamer_pipeline(sensor_id=1, capture_width=1280, capture_height=720, flip_method=2, display_width=960, display_height=540))
        self.right_camera.start()
        self.right_camera.frame_received.connect(self.update_right_camera_feed)

    def stop_right_camera(self):
        self.right_camera.stop()
        self.right_camera.release()
        self.camfeed2.setPixmap(QPixmap())
    
    @pyqtSlot(QImage)
    def update_left_camera_feed(self, qimage):
        np_image = qimage_to_np(qimage)
        np_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
        np_image = cv2.cvtColor(np_image, cv2.COLOR_GRAY2BGR)
        if self.left_camera_noise_reduction:
            np_image = cv2.fastNlMeansDenoisingColored(np_image, None, 10, 10, 7, 21)
        qimage = np_to_qimage(np_image)
        pixmap = QPixmap.fromImage(qimage)
        self.camfeed1.setPixmap(pixmap)

    @pyqtSlot(QImage)
    def update_right_camera_feed(self, qimage):
        np_image = qimage_to_np(qimage)
        np_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
        np_image = cv2.cvtColor(np_image, cv2.COLOR_GRAY2BGR)
        if self.right_camera_noise_reduction:
            np_image = cv2.fastNlMeansDenoisingColored(np_image, None, 10, 10, 7, 21)
        qimage = np_to_qimage(np_image)
        pixmap = QPixmap.fromImage(qimage)
        self.camfeed2.setPixmap(pixmap)

    @pyqtSlot()
    def capture_left_camera_image(self):
        grabbed, frame = self.left_camera.read()
        if grabbed:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            qimage = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(qimage)
            self.imgcam1.setPixmap(pixmap)

            # Save the image to the computer
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            save_path = os.path.join(os.path.expanduser("~"), "Pictures", "CapturedImages", f"left_image_{timestamp}.png")
            cv2.imwrite(save_path, frame)

    @pyqtSlot()
    def capture_right_camera_image(self):
        grabbed, frame = self.right_camera.read()
        if grabbed:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            qimage = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(qimage)
            self.imgcam2.setPixmap(pixmap)

            # Save the image to the computer
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            save_path = os.path.join(os.path.expanduser("~"), "Pictures", "CapturedImages", f"right_image_{timestamp}.png")
            cv2.imwrite(save_path, frame)

    @pyqtSlot(int)
    def adjust_left_camera_brightness(self, value):
        self.left_camera.set_brightness(value)

    @pyqtSlot(int)
    def adjust_right_camera_brightness(self, value):
        self.right_camera.set_brightness(value)

    @pyqtSlot(int)
    def adjust_left_image_brightness(self, value):
        self._adjust_image_brightness(self.imgcam1, value)

    @pyqtSlot(int)
    def adjust_right_image_brightness(self, value):
        self._adjust_image_brightness(self.imgcam2, value)
    
    @pyqtSlot(int)
    def adjust_left_camera_contrast(self, value):
        self.left_camera.set_contrast(value)

    @pyqtSlot(int)
    def adjust_right_camera_contrast(self, value):
        self.right_camera.set_contrast(value)
    
    @pyqtSlot(int)
    def adjust_imgcam1_contrast(self, value):
        self.imgcam1.setPixmap(self.apply_contrast_to_pixmap(self.imgcam1.pixmap(), value))

    @pyqtSlot(int)
    def adjust_imgcam2_contrast(self, value):
        self.imgcam2.setPixmap(self.apply_contrast_to_pixmap(self.imgcam2.pixmap(), value))
    
    @pyqtSlot()
    def toggle_left_camera_noise_reduction(self):
        self.left_camera_noise_reduction = not self.left_camera_noise_reduction

    @pyqtSlot()
    def toggle_right_camera_noise_reduction(self):
        self.right_camera_noise_reduction = not self.right_camera_noise_reduction
    
    @pyqtSlot()
    def apply_left_image_noise_reduction(self):
        self.imgcam1.setPixmap(apply_noise_reduction_to_pixmap(self.imgcam1.pixmap()))

    @pyqtSlot()
    def apply_right_image_noise_reduction(self):
        self.imgcam2.setPixmap(apply_noise_reduction_to_pixmap(self.imgcam2.pixmap()))

    def _adjust_image_brightness(self, label, value):
        pixmap = label.pixmap()
        if pixmap is not None:
            img = pixmap.toImage()
            np_image = qimage_to_np(img)
            np_image = cv2.add(np_image, np.array([value, value, value]))
            img = np_to_qimage(np_image)
            pixmap = QPixmap.fromImage(img)
            label.setPixmap(pixmap)
    
    def apply_contrast_to_pixmap(self, pixmap, value):
        if pixmap is None:
            return None

        contrast = value / 50.0
        img = pixmap.toImage()
        np_image = qimage_to_np(img)
        np_image = cv2.addWeighted(np_image, contrast, np_image, 0, 128 * (1 - contrast))
        img = np_to_qimage(np_image)
        return QPixmap.fromImage(img)

class CSI_Camera(QObject):
    frame_received = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.video_capture = None
        self.frame = None
        self.grabbed = False
        self.read_lock = threading.Lock()
        self.running = False
        self.read_thread = None

    def open(self, gstreamer_pipeline_string):
        try:
            self.video_capture = cv2.VideoCapture(gstreamer_pipeline_string, cv2.CAP_GSTREAMER)
            self.grabbed, self.frame = self.video_capture.read()
        except RuntimeError:
            self.video_capture = None
            print("Unable to open camera")
            print("Pipeline: " + gstreamer_pipeline_string)

    @pyqtSlot()
    def start(self):
        if self.running:
            print('Video capturing is already running')
            return None
        if self.video_capture is not None:
            self.running = True
            self.read_thread = QThread()
            self.moveToThread(self.read_thread)
            self.read_thread.started.connect(self.updateCamera)
            self.read_thread.start()

    @pyqtSlot()
    def stop(self):
        self.running = False
        if self.read_thread is not None:
            self.read_thread.quit()
            self.read_thread.wait()

    def updateCamera(self):
        while self.running:
            try:
                grabbed, frame = self.video_capture.read()
                with self.read_lock:
                    self.grabbed = grabbed
                    self.frame = frame.copy() if frame is not None else None
                if frame is not None:  
                    qimage = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
                    self.frame_received.emit(qimage)
                QThread.msleep(30)
            except RuntimeError:
                print("Could not read image from camera")

    def set_brightness(self, value):
        if self.video_capture is not None:
            self.video_capture.set(cv2.CAP_PROP_BRIGHTNESS, value / 100)
    
    def set_contrast(self, value):
        contrast = value / 100.0  # Assuming the slider has a range of 0 to 100
        if self.video_capture is not None:
            self.video_capture.set(cv2.CAP_PROP_CONTRAST, contrast)

    def read(self):
        with self.read_lock:
            return self.grabbed, self.frame if self.frame is not None else None
            
    def release(self):
        if self.video_capture is not None:
            self.video_capture.release()
            self.video_capture = None

#Gstreamer Pipeline for camera feeds
def gstreamer_pipeline(sensor_id=0, capture_width=1280, capture_height=720, display_width=960, display_height=540, framerate=30, flip_method=0,):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (sensor_id, capture_width, capture_height, framerate, flip_method, display_width, display_height,)
    )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    dark(app)
    modern_window = ModernWindow(window)
    modern_window.show()
    sys.exit(app.exec_())
