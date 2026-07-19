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

h_min, s_min, v_min = 0, 0, 0
h_max, s_max, v_max = 179, 255, 255
camera = None
cam_HSV = None

def get_hsv_on_click(event, x, y, flags, param):
    global h_min, s_min, v_min, h_max, s_max, v_max, camera, cam_HSV
    
    if event == cv.EVENT_LBUTTONDOWN and camera is not None:
        scale = 0.4
        height, width, _ = camera.shape
        
        scaled_w = int(width * scale)
        scaled_h = int(height * scale)
        
        if x >= scaled_w and y >= scaled_h:
            
            orig_x = int((x - scaled_w) / scale)
            orig_y = int((y - scaled_h) / scale)
            
            orig_x = min(orig_x, width - 1)
            orig_y = min(orig_y, height - 1)
            
            pixel_hsv = cam_HSV[orig_y, orig_x]
            h, s, v = pixel_hsv[0], pixel_hsv[1], pixel_hsv[2]
            
            h_min, h_max = max(0, h - 10), min(179, h + 10)
            s_min, s_max = max(0, s - 40), min(255, s + 40)
            v_min, v_max = max(0, v - 40), min(255, v + 40)
            
            hsv_data = {
                "lower_limit": [int(h_min), int(s_min), int(v_min)],
                "upper_limit": [int(h_max), int(s_max), int(v_max)]
            }
            
            script_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(script_dir, "hsv_config.json")
            
            with open(json_path, "w") as f:
                json.dump(hsv_data, f, indent=4)
                
            print(f"\n--- LIVE CALIBRATION SUCCESS! ---")
            print(f"Picked: H={h}, S={s}, V={v}")
            print(f"Saved to config and updated instantly!")

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0)
cap.set(cv.CAP_PROP_EXPOSURE, -4)

cv.namedWindow("Vision Dashboard") 
cv.setMouseCallback("Vision Dashboard", get_hsv_on_click)

script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "hsv_config.json")

if os.path.exists(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    h_min, s_min, v_min = data["lower_limit"]
    h_max, s_max, v_max = data["upper_limit"]
    print("Successfully loaded HSV values from JSON!")
else:
    print("No JSON found! Click the bottom-right video feed to calibrate.")

while True:
    success, camera = cap.read()
    if not success:
        break

    picker_view = camera.copy()
    cv.putText(picker_view, "CLICK OBJECT HERE", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cam_HSV = cv.cvtColor(camera, cv.COLOR_BGR2HSV)
    
    lower_limit = np.array([h_min, s_min, v_min])
    upper_limit = np.array([h_max, s_max, v_max])
    mask  = cv.inRange(cam_HSV, lower_limit, upper_limit)
    
    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 500: 
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(camera, (x, y), (x + w, y + h), (0, 255, 0), 3)
            center_x = x + (w // 2)
            center_y = y + (h // 2)
            cv.circle(camera, (center_x, center_y), 5, (0, 0, 255), cv.FILLED)
    
    stacked_images = imgStack(0.5, ([camera, cam_HSV], 
                                    [mask, picker_view]))
    
    cv.imshow("Vision Dashboard", stacked_images)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()