#Import libraries
import cv2
import numpy as np

# Define the callback functions for the trackbars
def set_contrast(value):
    global img, contrast
    contrast = value
    img = cv2.addWeighted(original_img, contrast, np.zeros(original_img.shape, dtype=original_img.dtype), 0, brightness)

def set_brightness(value):
    global img, brightness
    brightness = value
    img = cv2.addWeighted(original_img, contrast, np.zeros(original_img.shape, dtype=original_img.dtype), 0, brightness)

def set_noise_reduction(value):
    global img, original_img
    if value == 1:
        img = cv2.fastNlMeansDenoisingColored(original_img, None, 10, 10, 7, 21)

# Load the image from file
filename = "C:/Users/talha/OneDrive/Documents/FACTS-main/Project Code/Image Processing/RedBloodCell.jpg"
original_img = cv2.imread(filename)

# Create the GUI window and display the image
cv2.namedWindow("Image")
cv2.imshow("Image", original_img)

# Initialize the trackbars and noise reduction button
contrast = 1
brightness = 0
noise_reduction = 0
cv2.createTrackbar("Contrast", "Image", 1, 10, set_contrast)
cv2.createTrackbar("Brightness", "Image", 0, 100, set_brightness)
cv2.createTrackbar("Denoise", "Image", 0, 1, set_noise_reduction)

# Initialize the processed image
img = np.copy(original_img)

# Loop until the user presses 'q' to quit
while True:
    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Clean up the GUI
cv2.destroyAllWindows()
