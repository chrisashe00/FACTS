#Import libraries 
import cv2
import numpy as np
import jetson.inference
import jetson.utils

# Define the callback functions for the trackbars
def set_contrast(value):
    global img, contrast
    contrast = value
    img = cv2.addWeighted(original_img, contrast, np.zeros(original_img.shape, dtype=original_img.dtype), 0, brightness)

def set_brightness(value):
    global img, brightness
    brightness = value
    img = cv2.addWeighted(original_img, contrast, np.zeros(original_img.shape, dtype=original_img.dtype), brightness, 0)

def set_noise_reduction(value):
    global img, original_img
    if value == 1:
        img = cv2.fastNlMeansDenoisingColored(original_img, None, 10, 10, 7, 21)

# Initialize the camera
camera = jetson.utils.gstCamera(1280, 720, "0")

# Create the GUI window and display the camera feed
cv2.namedWindow("Camera")
cv2.moveWindow("Camera", 0, 0)

# Initialize the trackbars and noise reduction button
contrast = 1
brightness = 0
noise_reduction = 0
cv2.createTrackbar("Contrast", "Camera", 1, 10, set_contrast)
cv2.createTrackbar("Brightness", "Camera", 0, 100, set_brightness)
cv2.createTrackbar("Denoise", "Camera", 0, 1, set_noise_reduction)

# Loop until the user presses 'q' to quit
while True:
    # Capture a frame from the camera
    img, width, height = camera.CaptureRGBA(zeroCopy=1)

    # Convert the image to BGR format for OpenCV
    img_bgr = jetson.utils.cudaToNumpy(img, width, height, 4).astype(np.uint8)[:,:,:3]

    # Store a copy of the original image
    original_img = np.copy(img_bgr)

    # Apply the current brightness, contrast, and noise reduction settings to the image
    img = cv2.addWeighted(original_img, contrast, np.zeros(original_img.shape, dtype=original_img.dtype), brightness, 0)
    if noise_reduction == 1:
        img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

    # Display the image in the GUI window
    cv2.imshow("Camera", img)

    # Check for key presses
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Clean up the GUI
cv2.destroyAllWindows()
