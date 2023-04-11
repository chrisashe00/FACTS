#Imports
import sys
import cv2
import os 
import time 
import threading
import numpy as np
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.uic import loadUi
from qtmodern.styles import dark
from qtmodern.windows import ModernWindow

#Image Conversion Functions
def qimage_to_np(img: QImage):
    # Properly handling the data type of the numpy array
    return np.array(img.bits().asarray(img.width() * img.height() * img.depth() // 8)).reshape(img.height(), img.width(), img.depth() // 8).astype(np.uint8)

def np_to_qimage(arr: np.ndarray) -> QImage:
    # Properly handling the data type of the numpy array
    return QImage(arr.astype(np.uint8).data, arr.shape[1], arr.shape[0], arr.strides[0], QImage.Format_RGB888)

def draw_scale_bar(image, pixels_per_unit, bar_length_units, bar_thickness, position, color=(255, 255, 255), label=True, font_scale=1):
    bar_length_pixels = int(bar_length_units * pixels_per_unit)
    x, y = position
    cv2.rectangle(image, (x, y), (x + bar_length_pixels, y - bar_thickness), color, -1)
    if label:
        micrometers = int(bar_length_units * 10)  # Convert units to micrometers
        text = f"{micrometers} um"
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 1)
        cv2.putText(image, text, (x + (bar_length_pixels - text_width) // 2, y - bar_thickness - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 1, cv2.LINE_AA)

#GUI Window Class
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi('nuiv4.ui', self)
        self.show()

        # Connect buttons to their respective functions
        self.cam1_on.clicked.connect(self.start_left_camera)
        self.cam1_off.clicked.connect(self.stop_left_camera)
        self.cam2_on.clicked.connect(self.start_right_camera)
        self.cam2_off.clicked.connect(self.stop_right_camera)
        self.img1_on.clicked.connect(self.capture_left_camera_image)
        self.img2_on.clicked.connect(self.capture_right_camera_image)
        self.img1_off.clicked.connect(self.clear_left_image)
        self.img2_off.clicked.connect(self.clear_right_image)
        self.colour_on.clicked.connect(self.update_camera_feed_colour)
        self.grey_on.clicked.connect(self.update_camera_feed_greyscale)

        # Set the stretch factors for the bottom horizontal layout
        self.horizontalLayout_2.setStretch(0, 2)  # First image label
        self.horizontalLayout_2.setStretch(1, 1)  # Group Box
        self.horizontalLayout_2.setStretch(2, 2)  # Second Image label
        
        # Initialize camera variables
        self.left_camera = CSI_Camera()
        self.right_camera = CSI_Camera()
        self.left_camera_running = False
        self.right_camera_running = False
        self.left_camera_greyscale = False
        self.right_camera_greyscale = False

    def stop_left_camera(self):
        if self.left_camera_running:
            self.left_camera.stop()
            self.left_camera.release()
            self.camfeed1.setPixmap(QPixmap())
            self.left_camera.frame_received.disconnect()
            self.left_camera_running = False

    def start_left_camera(self):
        if not self.left_camera_running:
            self.left_camera.open(gstreamer_pipeline(sensor_id=0, capture_width=1280, capture_height=720, flip_method=2, display_width=960, display_height=540))
            self.left_camera.start()
            self.left_camera.frame_received.connect(self.update_left_camera_feed)
            self.left_camera_running = True

    def start_right_camera(self):
        if not self.right_camera_running:
            self.right_camera.open(gstreamer_pipeline(sensor_id=1, capture_width=1280, capture_height=720, flip_method=2, display_width=960, display_height=540))
            self.right_camera.start()
            self.right_camera.frame_received.connect(self.update_right_camera_feed)
            self.right_camera_running = True

    def stop_right_camera(self):
        if self.right_camera_running:
            self.right_camera.stop()
            self.right_camera.release()
            self.camfeed2.setPixmap(QPixmap())
            self.right_camera.frame_received.disconnect()
            self.right_camera_running = False

    @pyqtSlot(QImage)
    def update_left_camera_feed(self, qimage):
        np_image = qimage_to_np(qimage)
        np_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
        np_image = cv2.cvtColor(np_image, cv2.COLOR_GRAY2BGR)
        
        pixels_per_unit = 165  # This is now in pixels per 1 mm
        draw_scale_bar(np_image, pixels_per_unit, 2 , 5, (50, 500))


        qimage = np_to_qimage(np_image)
        pixmap = QPixmap.fromImage(qimage)
        self.camfeed1.setPixmap(pixmap)

    @pyqtSlot(QImage)
    def update_right_camera_feed(self, qimage):
        np_image = qimage_to_np(qimage)
        np_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
        np_image = cv2.cvtColor(np_image, cv2.COLOR_GRAY2BGR)
        
        pixels_per_unit = 165  # This is now in pixels per 1 mm
        draw_scale_bar(np_image, pixels_per_unit, 2 , 5, (50, 500))


        qimage = np_to_qimage(np_image)
        pixmap = QPixmap.fromImage(qimage)
        self.camfeed2.setPixmap(pixmap)

    @pyqtSlot()
    def capture_left_camera_image(self):
        grabbed, frame = self.left_camera.read()
        if grabbed:
            if self.left_camera_greyscale:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            pixels_per_unit = 165  # This is now in pixels per 1 mm
            draw_scale_bar(frame, pixels_per_unit, 2 , 5, (50, 500))
            qimage = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(qimage)
            self.imgcam1.setPixmap(pixmap)

            # Save the image to the computer
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            save_path = os.path.join(os.path.expanduser("~"), "Pictures", "CapturedImages", f"left_image_{timestamp}.png")
            directory = os.path.join(os.path.expanduser("~"), "Pictures", "CapturedImages")
            if not os.path.exists(directory):
                os.makedirs(directory)
            cv2.imwrite(save_path, frame)

    @pyqtSlot()
    def capture_right_camera_image(self):
        grabbed, frame = self.right_camera.read()
        if grabbed:
            if self.right_camera_greyscale:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            pixels_per_unit = 165  # This is now in pixels per 1 mm
            draw_scale_bar(frame, pixels_per_unit, 2 , 5, (50, 500))
            qimage = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(qimage)
            self.imgcam2.setPixmap(pixmap)

            # Save the image to the computer
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            save_path = os.path.join(os.path.expanduser("~"), "Pictures", "CapturedImages", f"right_image_{timestamp}.png")
            directory = os.path.join(os.path.expanduser("~"), "Pictures", "CapturedImages")
            if not os.path.exists(directory):
                os.makedirs(directory)
            cv2.imwrite(save_path, frame)

    @pyqtSlot()
    def clear_left_image(self):
        self.imgcam1.clear()

    @pyqtSlot()
    def clear_right_image(self):
        self.imgcam2.clear()

    @pyqtSlot(QImage)
    def update_left_camera_feed_colour(self, qimage):
        np_image = qimage_to_np(qimage)
        pixels_per_unit = 165  # This is now in pixels per 1 mm
        draw_scale_bar(np_image, pixels_per_unit, 2 , 5, (50, 500))
        qimage = np_to_qimage(np_image)
        pixmap = QPixmap.fromImage(qimage)
        self.camfeed1.setPixmap(pixmap)

    @pyqtSlot(QImage)
    def update_right_camera_feed_colour(self, qimage):
        np_image = qimage_to_np(qimage)
        pixels_per_unit = 165  # This is now in pixels per 1 mm
        draw_scale_bar(np_image, pixels_per_unit, 2 , 5, (50, 500))
        qimage = np_to_qimage(np_image)
        pixmap = QPixmap.fromImage(qimage)
        self.camfeed2.setPixmap(pixmap)
    
    @pyqtSlot()
    def update_camera_feed_colour(self):
        if not self.left_camera_greyscale and not self.right_camera_greyscale:
            return

        if self.left_camera_running:
            self.left_camera.frame_received.disconnect()
            self.left_camera.frame_received.connect(self.update_left_camera_feed_colour)

        if self.right_camera_running:
            self.right_camera.frame_received.disconnect()
            self.right_camera.frame_received.connect(self.update_right_camera_feed_colour)

        self.left_camera_greyscale = False
        self.right_camera_greyscale = False

    @pyqtSlot()
    def update_camera_feed_greyscale(self):
        if self.left_camera_greyscale and self.right_camera_greyscale:
            return

        if self.left_camera_running:
            self.left_camera.frame_received.disconnect()
            self.left_camera.frame_received.connect(self.update_left_camera_feed)

        if self.right_camera_running:
            self.right_camera.frame_received.disconnect()
            self.right_camera.frame_received.connect(self.update_right_camera_feed)

        self.left_camera_greyscale = True
        self.right_camera_greyscale = True
    
#CSI Camera Class
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

    def reinitialize(self, gstreamer_pipeline_string):
        if self.video_capture is not None and self.video_capture.isOpened():
            self.video_capture.release()

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
            if self.read_thread is None or not self.read_thread.isRunning():
                self.read_thread = QThread()
                self.moveToThread(self.read_thread)
                self.read_thread.started.connect(self.updateCamera)
            self.read_thread.start()
        elif self.video_capture is None:
            print("Camera not initialized. Call 'reinitialize()' with the appropriate pipeline string before starting.")

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

