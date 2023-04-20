from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QSlider, QLabel
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from qtmodern.styles import dark
from qtmodern.windows import ModernWindow
import cv2
import imutils
import numpy as np
from PyQt5.QtGui import QImage, QPixmap

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi('final_ip_gui.ui', self)
        self.img1.setScaledContents(True)
        self.img2.setScaledContents(True)
        self.original_image1 = None
        self.original_image2 = None
        self.bri_slider.setValue(50)
        self.bri_slider_2.setValue(50)
        self.con_slider.setValue(50)
        self.con_slider_2.setValue(50)
        self.processed_image1 = None
        self.processed_image2 = None

        # Connect the open_1 button to the loadImage function
        self.open_1.clicked.connect(self.loadImage)

        # Connect the open_2 button to the loadImage2 function
        self.open_2.clicked.connect(self.loadImage2)

        # Connect the sliders valueChanged signals to the update_label_value function (Brightness, Contrast, Denoise and Gaussian BLur)
        self.bri_slider.valueChanged.connect(lambda value, slider=self.bri_slider, label=self.bri_value: self.update_label_value(value, slider, label))
        self.con_slider.valueChanged.connect(lambda value, slider=self.con_slider, label=self.con_value: self.update_label_value(value, slider, label))
        self.nr_slider.valueChanged.connect(lambda value, slider=self.nr_slider, label=self.nr_value: self.update_label_value(value, slider, label))
        self.gb_slider.valueChanged.connect(lambda value, slider=self.gb_slider, label=self.gb_value: self.update_label_value(value, slider, label))
        self.bri_slider_2.valueChanged.connect(lambda value, slider=self.bri_slider_2, label=self.bri_value_2: self.update_label_value(value, slider, label))
        self.con_slider_2.valueChanged.connect(lambda value, slider=self.con_slider_2, label=self.con_value_2: self.update_label_value(value, slider, label))
        self.nr_slider_2.valueChanged.connect(lambda value, slider=self.nr_slider_2, label=self.nr_value_2: self.update_label_value(value, slider, label))
        self.gb_slider_2.valueChanged.connect(lambda value, slider=self.gb_slider_2, label=self.gb_value_2: self.update_label_value(value, slider, label))
        
        #Connect the button presses to the noise reduction functions
        self.nr_on.clicked.connect(self.apply_denoising)
        self.nr_on_2.clicked.connect(self.apply_denoising2)

        # Connect the clear_1 button to the clearImage1 function
        self.clear_1.clicked.connect(self.clearImage1)

        # Connect the clear_2 button to the clearImage2 function
        self.clear_2.clicked.connect(self.clearImage2)

        # Connect the revert_1 button to the revertImage1 function
        self.revert_1.clicked.connect(self.revertImage1)

        # Connect the revert_2 button to the revertImage2 function
        self.revert_2.clicked.connect(self.revertImage2)

        # Connect the buttons to apply bilateral filtering
        self.bf_on.clicked.connect(self.apply_bilateral_filter)
        self.bf_on_2.clicked.connect(self.apply_bilateral_filter2)

        # Connect the sliders to update the values of kernel size for Median Blur
        self.mb_slider.valueChanged.connect(lambda value, slider=self.mb_slider, label=self.mb_value: self.update_label_value(value, slider, label))
        self.mb_slider_2.valueChanged.connect(lambda value, slider=self.mb_slider_2, label=self.mb_value_2: self.update_label_value(value, slider, label))

        # Connect the sliders to update the values of d and sigma
        self.d_slider.valueChanged.connect(lambda value, slider=self.d_slider, label=self.d_value: self.update_label_value(value, slider, label))
        self.sigma_slider.valueChanged.connect(lambda value, slider=self.sigma_slider, label=self.sigma_value: self.update_label_value(value, slider, label))
        self.d_slider_2.valueChanged.connect(lambda value, slider=self.d_slider_2, label=self.d_value_2: self.update_label_value(value, slider, label))
        self.sigma_slider_2.valueChanged.connect(lambda value, slider=self.sigma_slider_2, label=self.sigma_value_2: self.update_label_value(value, slider, label))

        # Connect the ib_push button to the blend_and_save function
        self.ib_push.clicked.connect(lambda: self.blend_and_save("img1"))

        # Connect the ib_push_2 button to the blend_and_save function
        self.ib_push_2.clicked.connect(lambda: self.blend_and_save("img2"))

        self.save_1.clicked.connect(lambda: self.save_image("img1"))
        self.save_2.clicked.connect(lambda: self.save_image("img2"))

        self.show()

    def loadImage(self):
        """ This function will load the user selected image
            and set it to label using the setPhoto function
        """
        self.filename = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        
        # Check if the user has not selected an image
        if not self.filename:
            return
        
        self.image = cv2.imread(self.filename)
        self.setPhoto(self.image)
        self.original_image1 = self.image.copy()

    def loadImage2(self):
        """ This function will load the user selected image
            and set it to img2 label using the setPhoto2 function
        """
        self.filename2 = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        
        # Check if the user has not selected an image
        if not self.filename2:
            return
        
        self.image2 = cv2.imread(self.filename2)
        self.setPhoto2(self.image2)
        self.original_image2 = self.image2.copy()

    def setPhoto(self, image):
        self.processed_image1 = image
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        img = img.rgbSwapped()
        self.img1.setPixmap(QPixmap.fromImage(img))

    def setPhoto2(self, image):
        self.processed_image2 = image
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        img = img.rgbSwapped()
        self.img2.setPixmap(QPixmap.fromImage(img))


    def update_label_value(self, value, slider, label):
        """ This function updates the given label with the current
            position of the given slider.
        """
        if isinstance(slider, QSlider) and isinstance(label, QLabel):
            label.setText(str(value))
            if slider is self.bri_slider and self.original_image1 is not None:
                self.apply_brightness(value)
            elif slider is self.bri_slider_2 and self.original_image2 is not None:
                self.apply_brightness2(value)
            elif slider is self.con_slider and self.original_image1 is not None:
                self.apply_contrast(value)
            elif slider is self.con_slider_2 and self.original_image2 is not None:
                self.apply_contrast2(value)
            elif slider is self.gb_slider and self.original_image1 is not None:
                self.apply_gaussian_blur(value, "img1")
            elif slider is self.gb_slider_2 and self.original_image2 is not None:
                self.apply_gaussian_blur(value, "img2")
            elif slider is self.mb_slider and self.original_image1 is not None:
                self.apply_median_blur(value)
            elif slider is self.mb_slider_2 and self.original_image2 is not None:
                self.apply_median_blur2(value)
        else:
            print("Error: Slider or Label not of expected type")
    
    def clearImage1(self):
        """ This function clears the img1 label.
        """
        self.img1.setPixmap(QPixmap())

    def clearImage2(self):
        """ This function clears the img2 label.
        """
        self.img2.setPixmap(QPixmap())

    def revertImage1(self):
            """ This function reverts the img1 label to its original image.
            """
            if self.original_image1 is not None:
                self.setPhoto(self.original_image1)
                self.bri_slider.setValue(50)
                self.bri_slider_2.setValue(50)
                self.con_slider.setValue(50)
                self.con_slider_2.setValue(50)

    def revertImage2(self):
        """ This function reverts the img2 label to its original image.
        """
        if self.original_image2 is not None:
            self.setPhoto2(self.original_image2)
            self.bri_slider.setValue(50)
            self.bri_slider_2.setValue(50)
            self.con_slider.setValue(50)
            self.con_slider_2.setValue(50)

    def apply_brightness(self, value):
        """ This function applies the brightness change to the img1 label.
        """
        brightness_scale = (value - 50) * 2
        bright_image = cv2.convertScaleAbs(self.original_image1, alpha=1, beta=brightness_scale)
        self.processed_image1 = bright_image
        self.setPhoto(bright_image)

    def apply_brightness2(self, value):
        """ This function applies the brightness change to the img2 label.
        """
        brightness_scale = (value - 50) * 2
        bright_image2 = cv2.convertScaleAbs(self.original_image2, alpha=1, beta=brightness_scale)
        self.processed_image2 = bright_image2
        self.setPhoto2(bright_image2)

    def apply_contrast(self, value):
        """ This function applies the contrast change to the img1 label.
        """
        contrast_scale = (value + 50) / 50.0
        contrast_image = cv2.convertScaleAbs(self.original_image1, alpha=contrast_scale, beta=0)
        self.processed_image1 = contrast_image
        self.setPhoto(contrast_image)

    def apply_contrast2(self, value):
        """ This function applies the contrast change to the img2 label.
        """
        contrast_scale = (value + 50) / 50.0
        contrast_image2 = cv2.convertScaleAbs(self.original_image2, alpha=contrast_scale, beta=0)
        self.processed_image2 = contrast_image2
        self.setPhoto2(contrast_image2)
    
    def apply_denoising(self):
        if self.processed_image1 is not None:
            h_value = self.nr_slider.value()
            denoised_image = cv2.fastNlMeansDenoisingColored(self.processed_image1, None, h_value, h_value, 7, 21)
            self.setPhoto(denoised_image)

    def apply_denoising2(self):
        if self.processed_image2 is not None:
            h_value = self.nr_slider_2.value()
            denoised_image2 = cv2.fastNlMeansDenoisingColored(self.processed_image2, None, h_value, h_value, 7, 21)
            self.setPhoto2(denoised_image2)
    
    def apply_gaussian_blur(self, value, img_label):
        """ This function applies the Gaussian Blur to the given image label.
        """
        ksize = value * 2 + 1
        if img_label == "img1" and self.processed_image1 is not None:
            blurred_image = cv2.GaussianBlur(self.processed_image1, (ksize, ksize), 0)
            self.setPhoto(blurred_image)
        elif img_label == "img2" and self.original_image2 is not None:
            blurred_image = cv2.GaussianBlur(self.processed_image2, (ksize, ksize), 0)
            self.setPhoto2(blurred_image)

    def apply_median_blur(self, value):
        """ This function applies the median blur to the img1 label. """
        if value % 2 == 0:
            ksize = value + 1
        else:
            ksize = value
        median_blur_image = cv2.medianBlur(self.processed_image1, ksize)
        self.setPhoto(median_blur_image)

    def apply_median_blur2(self, value):
        """ This function applies the median blur to the img2 label. """
        if value % 2 == 0:
            ksize = value + 1
        else:
            ksize = value
        median_blur_image2 = cv2.medianBlur(self.processed_image2, ksize)
        self.setPhoto2(median_blur_image2)
    
    def apply_bilateral_filter(self):
        if self.processed_image1 is not None:
            d = self.d_slider.value()
            sigma = self.sigma_slider.value()
            filtered_image = cv2.bilateralFilter(self.processed_image1, d, sigma, sigma)
            self.setPhoto(filtered_image)

    def apply_bilateral_filter2(self):
        if self.processed_image2 is not None:
            d = self.d_slider_2.value()
            sigma = self.sigma_slider_2.value()
            filtered_image = cv2.bilateralFilter(self.processed_image2, d, sigma, sigma)
            self.setPhoto2(filtered_image)
    
    def blend_images(self, img1, img2):
        """ This function blends two images with equal weights. """
        # Ensure the images are the same size
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        if h1 != h2 or w1 != w2:
            img2 = cv2.resize(img2, (w1, h1), interpolation=cv2.INTER_AREA)

        # Blend the images using equal weights
        blended_image = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)
        return blended_image

    def save_blended_image(self, blended_image):
        """ This function saves the blended image to the local machine. """
        filename = QFileDialog.getSaveFileName(filter="JPG(*.jpg);;PNG(*.png);;TIFF(*.tiff);;BMP(*.bmp)")[0]
        cv2.imwrite(filename, blended_image)
        print('Blended image saved as:', filename)

    def blend_and_save(self, img_label):
        if self.processed_image1 is not None and self.processed_image2 is not None:
            blended_image = self.blend_images(self.processed_image1, self.processed_image2)
            
            if img_label == "img1":
                self.setPhoto(blended_image)
            elif img_label == "img2":
                self.setPhoto2(blended_image)

            self.save_blended_image(blended_image)
    
    def save_image(self, img_label):
        if img_label == "img1" and self.processed_image1 is not None:
            current_image = self.processed_image1
        elif img_label == "img2" and self.processed_image2 is not None:
            current_image = self.original_image2
        else:
            return

        filename = QFileDialog.getSaveFileName(filter="JPG(*.jpg);;PNG(*.png);;TIFF(*.tiff);;BMP(*.bmp)")[0]
        cv2.imwrite(filename, current_image)
        print(f"Image saved as: {filename}")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dark(app)
    window = MyWindow()
    modern_window = ModernWindow(window)
    modern_window.show()
    sys.exit(app.exec_())