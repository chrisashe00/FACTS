import cv2
import numpy as np

# Load grayscale image with noise
img = cv2.imread('RULERpic.png', cv2.IMREAD_GRAYSCALE)

# Apply median filtering
img_median = cv2.medianBlur(img, 5)

# Apply bilateral filtering
img_bilateral = cv2.bilateralFilter(img, 9, 75, 75)

# Apply non-local means filtering
img_nlm = cv2.fastNlMeansDenoising(img, None, 40, 7, 21)

# Display results
cv2.imshow('Original Image', img)
cv2.imshow('Median Filtering', img_median)
cv2.imshow('Bilateral Filtering', img_bilateral)
cv2.imshow('Non-Local Means Filtering', img_nlm)
cv2.waitKey(0)
cv2.destroyAllWindows()
