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

#GUI Window Class
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi('New_GUI', self)
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
        self.ip_on.clicked.connect(self.open_image_processing_window)
        self.ip_off.clicked.connect(self.close_image_processing_window)

        # Set the stretch factors for the bottom horizontal layout
        self.horizontalLayout_2.setStretch(0, 2)  # First image label
        self.horizontalLayout_2.setStretch(1, 1)  # Group Box
        self.horizontalLayout_2.setStretch(2, 2)  # Second Image label
        
        # Initialize camera instances
        self.left_camera = CSI_Camera()
        self.right_camera = CSI_Camera()

    def stop_left_camera(self):
        self.left_camera.stop()
        self.left_camera.release()
        self.camfeed1.setPixmap(QPixmap())

    def start_left_camera(self):
        self.left_camera.reinitialize(gstreamer_pipeline(sensor_id=0, capture_width=1280, capture_height=720, flip_method=2, display_width=960, display_height=540))
        self.left_camera.start()
        self.left_camera.frame_received.connect(self.update_left_camera_feed)

    def start_right_camera(self):
        self.right_camera.reinitialize(gstreamer_pipeline(sensor_id=1, capture_width=1280, capture_height=720, flip_method=2, display_width=960, display_height=540))
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
        qimage = np_to_qimage(np_image)
        pixmap = QPixmap.fromImage(qimage)
        self.camfeed1.setPixmap(pixmap)

    @pyqtSlot(QImage)
    def update_right_camera_feed(self, qimage):
        np_image = qimage_to_np(qimage)
        np_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
        np_image = cv2.cvtColor(np_image, cv2.COLOR_GRAY2BGR)
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
            directory = os.path.join(os.path.expanduser("~"), "Pictures", "CapturedImages")
            if not os.path.exists(directory):
                os.makedirs(directory)
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

    def open_image_processing_window(self):
        # Retrieve images from imgcam1 and imgcam2 labels
        pixmap1 = self.imgcam1.pixmap()
        pixmap2 = self.imgcam2.pixmap()

        if pixmap1 is None or pixmap2 is None:
            print("Both images must be captured before opening the image processing window.")
            return

        # Convert QPixmap objects to OpenCV-compatible numpy arrays
        img1 = qimage_to_np(pixmap1.toImage())
        img2 = qimage_to_np(pixmap2.toImage())

        # Create an OpenCV window
        if cv2.getWindowProperty("Image Processing", cv2.WND_PROP_VISIBLE) < 1:
            cv2.namedWindow("Image Processing", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Image Processing", 960, 540)

        # Create trackbars for brightness, contrast, and noise reduction adjustments
        cv2.createTrackbar("Brightness-Cam-1", "Image Processing", 0, 100, lambda x: None)
        cv2.createTrackbar("Contrast-Cam-1", "Image Processing", 0, 100, lambda x: None)
        cv2.createTrackbar("Denoise-Cam-1", "Image Processing", 0, 100, lambda x: None)
        cv2.createTrackbar("Brightness-Cam-2", "Image Processing", 0, 100, lambda x: None)
        cv2.createTrackbar("Contrast-Cam-2", "Image Processing", 0, 100, lambda x: None)
        cv2.createTrackbar("Denoise-Cam-2", "Image Processing", 0, 100, lambda x: None)

        def apply_clahe(img, clip_limit=2.0, tile_grid_size=(8, 8)):
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
            if len(img.shape) == 3:
                lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
                l, a, b = cv2.split(lab)
                cl = clahe.apply(l)
                limg = cv2.merge((cl, a, b))
                return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
            else:
                return clahe.apply(img)

        def adjust_gamma(img, gamma=1.0):
            inv_gamma = 1.0 / gamma
            table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
            return cv2.LUT(img, table)

        while True:
            # Retrieve the trackbar values
            gamma1 = cv2.getTrackbarPos("Brightness-Cam-1", "Image Processing") / 100
            clahe1 = cv2.getTrackbarPos("Contrast-Cam-1", "Image Processing") / 100
            denoise1 = cv2.getTrackbarPos("Denoise-Cam-1", "Image Processing")
            gamma2 = cv2.getTrackbarPos("Brightness-Cam-2", "Image Processing") / 100
            clahe2 = cv2.getTrackbarPos("Contrast-Cam-2", "Image Processing") / 100
            denoise2 = cv2.getTrackbarPos("Denoise-Cam-2", "Image Processing")

            # Apply brightness, contrast, and noise reduction adjustments
            adjusted_img1 = apply_clahe(img1, clip_limit=clahe1)
            adjusted_img1 = adjust_gamma(adjusted_img1, gamma=gamma1)
            adjusted_img1 = cv2.fastNlMeansDenoisingColored(adjusted_img1, None, denoise1, denoise1, 7, 21)

            adjusted_img2 = apply_clahe(img2, clip_limit=clahe2)
            adjusted_img2 = adjust_gamma(adjusted_img2, gamma=gamma2)
            adjusted_img2 = cv2.fastNlMeansDenoisingColored(adjusted_img2, None, denoise2, denoise2, 7, 21)

            # Display the adjusted images side by side
            adjusted_side_by_side_image = np.hstack((adjusted_img1, adjusted_img2))
            cv2.imshow("Image Processing", adjusted_side_by_side_image)

            # Wait for user interactions
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                # User pressed "q" to quit the loop
                break
            elif key == ord("b"):
                # User pressed "b" to blend the images
                blend_ratio = 0.5  # Adjust this value to change the blending ratio
                blended_image = cv2.addWeighted(adjusted_img1, blend_ratio, adjusted_img2, 1 - blend_ratio, 0)
                cv2.imshow("Blended Image", blended_image)

        # Close the OpenCV window
        cv2.destroyWindow("Image Processing")
        cv2.waitKey(1)
    
    def close_image_processing_window(self):
        cv2.destroyAllWindows()
        cv2.waitKey(1)

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