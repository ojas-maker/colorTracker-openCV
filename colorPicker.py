import cv2 as cv
import numpy as np

# 1. The Mouse Click Listener
def get_hsv_on_click(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        # Get the exact HSV pixel values at the Y, X coordinate
        pixel_hsv = cam_HSV[y, x]
        print(f"Clicked Pixel HSV: Hue={pixel_hsv[0]} | Sat={pixel_hsv[1]} | Val={pixel_hsv[2]}")

cap = cv.VideoCapture(1)
cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0)
cap.set(cv.CAP_PROP_EXPOSURE, -4)

cv.namedWindow("Color Picker")
# Attach the listener to the window
cv.setMouseCallback("Color Picker", get_hsv_on_click)

while True:
    success, camera = cap.read()
    if not success:
        break

    # We make this global so the mouse function can see it
    global cam_HSV
    cam_HSV = cv.cvtColor(camera, cv.COLOR_BGR2HSV)

    cv.imshow("Color Picker", camera)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()