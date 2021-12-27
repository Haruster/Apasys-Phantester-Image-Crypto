import cv2

image_data = cv2.imread('image.jpg')

ROI = cv2.selectROI(image_data)

print('ROI = ', ROI)

cv2.imshow('img', ROI)
cv2.waitKey(0)
cv2.destroyAllWindows()
