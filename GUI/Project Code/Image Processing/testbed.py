import cv2
import numpy as np

def adjust_brightness(img, brightness):
    return cv2.convertScaleAbs(img, alpha=1, beta=brightness)

def adjust_contrast(img, contrast):
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_image)
    v = v.astype('float32')
    v = v * contrast
    v = np.clip(v, 0, 255)
    v = v.astype('uint8')
    hsv_image = cv2.merge([h, s, v])
    return cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

def denoise_gray(img, h, templateWindowSize, searchWindowSize):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.fastNlMeansDenoising(gray, None, h, templateWindowSize, searchWindowSize)

filename = "C:/Users/talha/OneDrive/Documents/FACTS-1/Project Code/Image Processing/timage.png"
original_img = cv2.imread(filename)
window_name = "Image Adjuster"

cv2.namedWindow(window_name)
cv2.createTrackbar("Contrast", window_name, 100, 300, lambda x: None)
cv2.createTrackbar("Brightness", window_name, 50, 100, lambda x: None)
cv2.createTrackbar("Denoise", window_name, 0, 1, lambda x: None)
cv2.createTrackbar("h", window_name, 10, 50, lambda x: None)
cv2.createTrackbar("TemplateWindowSize", window_name, 7, 21, lambda x: None)
cv2.createTrackbar("SearchWindowSize", window_name, 21, 31, lambda x: None)

img = original_img.copy()

while True:
    contrast = cv2.getTrackbarPos("Contrast", window_name) / 100.0
    brightness = cv2.getTrackbarPos("Brightness", window_name) - 50
    denoise = cv2.getTrackbarPos("Denoise", window_name)
    h = cv2.getTrackbarPos("h", window_name)
    templateWindowSize = cv2.getTrackbarPos("TemplateWindowSize", window_name)
    searchWindowSize = cv2.getTrackbarPos("SearchWindowSize", window_name)

    img_adjusted = adjust_contrast(img, contrast)
    img_adjusted = adjust_brightness(img_adjusted, brightness)

    if denoise:
        gray_denoised = denoise_gray(img_adjusted, h, templateWindowSize, searchWindowSize)
        img_adjusted = cv2.cvtColor(gray_denoised, cv2.COLOR_GRAY2BGR)
        print("Noise reduction complete.")

    cv2.imshow(window_name, img_adjusted)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

cv2.destroyAllWindows()

