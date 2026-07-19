import cv2 as cv
import numpy as np

def get_hsv_on_click(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        pixel_hsv = cam_HSV[y, x]
        print(f"Clicked Pixel HSV: Hue={pixel_hsv[0]} | Sat={pixel_hsv[1]} | Val={pixel_hsv[2]}")


cap = cv.VideoCapture(1)


cv.namedWindow("Color Picker")
cv.setMouseCallback("Color Picker", get_hsv_on_click)

while True:
    success, camera = cap.read()
    
    if not success:
        print("========================================")
        print("CRASH: Could not connect to the camera!")
        print("1. Check if the DroidCam app is open and awake on your phone.")
        print("2. Verify the IP address matches perfectly.")
        print("3. Ensure PC and Phone are on the same Wi-Fi.")
        print("========================================")
        break

    global cam_HSV
    cam_HSV = cv.cvtColor(camera, cv.COLOR_BGR2HSV)

    cv.imshow("Color Picker", camera)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()