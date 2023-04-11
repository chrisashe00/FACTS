import cv2
import numpy as np

# Image processing functions
def adjust_brightness_contrast(img, brightness, contrast):
    return cv2.addWeighted(img, 1 + float(contrast) / 100, img, 0, float(brightness) - 50)

def sharpen_image(img):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    return cv2.filter2D(img, -1, kernel)

def reduce_noise(img, h_value):
    return cv2.fastNlMeansDenoising(img, None, h_value, 7, 21)

def apply_median_blur(img, ksize):
    return cv2.medianBlur(img, ksize)

median_blur = 1
h_value = 10

def on_brightness_trackbar(val):
    global brightness
    brightness = val
    update_display()

def on_contrast_trackbar(val):
    global contrast
    contrast = val
    update_display()

def on_sharpen_trackbar(val):
    global sharpen
    sharpen = val
    update_display()

def on_noise_trackbar(val):
    global noise_reduction
    noise_reduction = val
    update_display()

def on_median_blur_trackbar(val):
    global median_blur
    median_blur = 2 * val + 1  # Ensure that the value is always an odd number
    update_display()

def on_h_value_trackbar(val):
    global h_value
    h_value = val
    update_display()

def update_display():
    global image, brightness, contrast, sharpen, noise_reduction, h_value, median_blur

    img_processed = adjust_brightness_contrast(image, brightness, contrast)

    if sharpen:
        img_processed = sharpen_image(img_processed)

    if noise_reduction:
        img_processed = reduce_noise(img_processed, h_value)

    img_processed = apply_median_blur(img_processed, median_blur)

    cv2.imshow('Image Processing', img_processed)

# Load image
image = cv2.imread('RULERpic.png')

def display_image(img):
    cv2.imshow('Image Processing', img)

# Initialize global variables
brightness = 50
contrast = 0
sharpen = 0
noise_reduction = 0

# Create window and trackbars
cv2.namedWindow('Image Processing', cv2.WINDOW_NORMAL)
cv2.namedWindow('Controls', cv2.WINDOW_NORMAL)  # New window for trackbars
cv2.createTrackbar('Brightness', 'Controls', 50, 100, on_brightness_trackbar)
cv2.createTrackbar('Contrast', 'Controls', 0, 100, on_contrast_trackbar)
cv2.createTrackbar('Sharpen', 'Controls', 0, 1, on_sharpen_trackbar)
cv2.createTrackbar('Denoise', 'Controls', 0, 1, on_noise_trackbar)
cv2.createTrackbar('Median Blur', 'Controls', 0, 10, on_median_blur_trackbar)
cv2.createTrackbar('H', 'Controls', 10, 50, on_h_value_trackbar)

update_display()

cv2.waitKey(0)
cv2.destroyAllWindows()
