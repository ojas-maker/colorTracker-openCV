import cv2 as cv
import numpy as np
import json
import os

def empty(str):
    pass

def imgStack(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    
    rowsAvailable = isinstance(imgArray[0], list)
    
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: 
                    imgArray[x][y] = cv.cvtColor(imgArray[x][y], cv.COLOR_GRAY2BGR)
        
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2: 
                imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
        
    return ver

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0)
cap.set(cv.CAP_PROP_EXPOSURE, -4)

if os.path.exists("openCV/hsv_config.json"):
    with open("openCV/hsv_config.json", "r") as f:
        data = json.load(f)
    
    h_min, s_min, v_min = data["lower_limit"]
    h_max, s_max, v_max = data["upper_limit"]
    print("Successfully loaded HSV values from JSON!")
else:
    print("No JSON found! Run colorPicker.py first. Using defaults.")
    h_min, h_max = 0, 179
    s_min, s_max = 0, 255
    v_min, v_max = 0, 255


while True:
    success, camera = cap.read()
    if not success:
        break

    cam_HSV = cv.cvtColor(camera, cv.COLOR_BGR2HSV)
    

    lower_limit = np.array([h_min, s_min, v_min])
    upper_limit = np.array([h_max, s_max, v_max])
    mask  = cv.inRange(cam_HSV, lower_limit, upper_limit)
    
    print(f"H: {h_min}-{h_max} | S: {s_min}-{s_max} | V: {v_min}-{v_max}")
    
    blankImg = np.zeros_like(camera)
    
    stacked_images = imgStack(0.6, ([camera, cam_HSV], 
                                    [mask, blankImg]))
    
    cv.imshow("Video playbacks", stacked_images)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()