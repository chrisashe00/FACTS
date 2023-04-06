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

def blend_images(img1, img2, alpha):
    return cv2.addWeighted(img1, alpha, img2, 1 - alpha, 0)

# Callback functions for trackbars
def on_brightness1_trackbar(val):
    global brightness1
    brightness1 = val
    update_display()

def on_contrast1_trackbar(val):
    global contrast1
    contrast1 = val
    update_display()

def on_brightness2_trackbar(val):
    global brightness2
    brightness2 = val
    update_display()

def on_contrast2_trackbar(val):
    global contrast2
    contrast2 = val
    update_display()

def on_sharpen1_trackbar(val):
    global sharpen1
    sharpen1 = val
    update_display()

def on_sharpen2_trackbar(val):
    global sharpen2
    sharpen2 = val
    update_display()

def on_noise1_trackbar(val):
    global h_value
    h_value = val
    update_display()

def on_noise2_trackbar(val):
    global h_value
    h_value = val
    update_display()

def on_noise_reduction1_trackbar(val):
    global noise_reduction1
    noise_reduction1 = val
    update_display()

def on_noise_reduction2_trackbar(val):
    global noise_reduction2
    noise_reduction2 = val
    update_display()

def on_h_value_trackbar(val):
    global h_value
    h_value = val

def on_blend_trackbar(val):
    global alpha, blend_enabled
    alpha = val / 100
    blend_enabled = True
    update_display()

def apply_median_blur(img, ksize):
    return cv2.medianBlur(img, ksize)

median_blur1 = 1
median_blur2 = 1

def on_median_blur1_trackbar(val):
    global median_blur1
    median_blur1 = 2 * val + 1  # Ensure that the value is always an odd number
    update_display()

def on_median_blur2_trackbar(val):
    global median_blur2
    median_blur2 = 2 * val + 1  # Ensure that the value is always an odd number
    update_display()

def update_display():
    global image1, image2, brightness1, contrast1, brightness2, contrast2, sharpen1, sharpen2, noise_reduction1, noise_reduction2, h_value, alpha, blend_enabled, median_blur1, median_blur2

    img1_processed = adjust_brightness_contrast(image1, brightness1, contrast1)
    img2_processed = adjust_brightness_contrast(image2, brightness2, contrast2)

    if sharpen1:
        img1_processed = sharpen_image(img1_processed)

    if sharpen2:
        img2_processed = sharpen_image(img2_processed)

    if noise_reduction1:
        img1_processed = reduce_noise(img1_processed, h_value)

    if noise_reduction2:
        img2_processed = reduce_noise(img2_processed, h_value)

    img1_processed = apply_median_blur(img1_processed, median_blur1)
    img2_processed = apply_median_blur(img2_processed, median_blur2)

    display_images(img1_processed, img2_processed)

    if blend_enabled:
        blended_image = blend_images(img1_processed, img2_processed, alpha)
        cv2.imshow('Blended Image', blended_image)
        blend_enabled = False

# Load images
image1 = cv2.imread('img1.png')
image2 = cv2.imread('img2.png')

def display_images(img1, img2):
    combined = np.hstack((img1, img2))
    cv2.imshow('Image Processing', combined)

# Initialize global variables
blend_enabled = False
brightness1 = 50
contrast1 = 0
brightness2 = 50
contrast2 = 0
sharpen1 = 0
sharpen2 = 0
noise_reduction1 = 0
noise_reduction2 = 0
h_value = 10
alpha = 0.5

# Create window and trackbars
cv2.namedWindow('Image Processing', cv2.WINDOW_NORMAL)
cv2.namedWindow('Controls', cv2.WINDOW_NORMAL)  # New window for trackbars
cv2.namedWindow('Blended Image', cv2.WINDOW_NORMAL)
cv2.createTrackbar('Bri-1', 'Controls', 50, 100, on_brightness1_trackbar)
cv2.createTrackbar('Con-1', 'Controls', 0, 100, on_contrast1_trackbar)
cv2.createTrackbar('Bri-2', 'Controls', 50, 100, on_brightness2_trackbar)
cv2.createTrackbar('Con-2', 'Controls', 0, 100, on_contrast2_trackbar)
cv2.createTrackbar('Sharp-1', 'Controls', 0, 1, on_sharpen1_trackbar)
cv2.createTrackbar('Sharp-2', 'Controls', 0, 1, on_sharpen2_trackbar)
cv2.createTrackbar('Denoise-1', 'Controls', 0, 1, on_noise_reduction1_trackbar)
cv2.createTrackbar('Denoise-2', 'Controls', 0, 1, on_noise_reduction2_trackbar)
cv2.createTrackbar('MedBlur-1', 'Controls', 0, 10, on_median_blur1_trackbar)
cv2.createTrackbar('MedBlur-2', 'Controls', 0, 10, on_median_blur2_trackbar)
cv2.createTrackbar('H', 'Controls', 10, 50, on_h_value_trackbar)
cv2.createTrackbar('Blend', 'Controls', 50, 100, on_blend_trackbar)

update_display()

cv2.waitKey(0)
cv2.destroyAllWindows()
