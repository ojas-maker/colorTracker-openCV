import cv2 as cv
import numpy as np
import json
import os


polygon_points = np.array([
    [10, 10],   # top-left
    [150, 10],  # top-right
    [150, 50],  # bottom-right
    [10, 50]    # bottom-left
], dtype=np.int32).reshape((-1, 1, 2))

recalibrate_clicked = False

def empty(str):
    pass

# ==========================================
# 2. MOUSE CALLBACK
# ==========================================
def handle_mouse_events(event, x, y, flags, param):
    global recalibrate_clicked
    
    if event == cv.EVENT_LBUTTONDOWN:
        # Check if the click happened inside our defined polygon
        is_inside = cv.pointPolygonTest(polygon_points, (float(x), float(y)), False)
        
        if is_inside >= 0:
            print("Recalibrate button clicked! Transitioning...")
            recalibrate_clicked = True


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


def run_mask():
    global recalibrate_clicked
    recalibrate_clicked = False
    
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0)
    cap.set(cv.CAP_PROP_EXPOSURE, -4.85)
    # cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "hsv_config.json")

    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
        
        h_min, s_min, v_min = data["lower_limit"]
        h_max, s_max, v_max = data["upper_limit"]
        print("Successfully loaded HSV values from JSON!")
    else:
        print("No JSON found! Run colorPicker.py first. Using defaults.")
        h_min, h_max = 35, 55
        s_min, s_max = 0, 80
        v_min, v_max = 61, 141

    cv.namedWindow("Video playbacks")
    cv.setMouseCallback("Video playbacks", handle_mouse_events)

    while True:
        success, camera = cap.read()
        if not success:
            break

        blurred = cv.GaussianBlur(camera, (5, 5), 0)
        cam_HSV = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
        
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

        blankImg = np.zeros_like(camera)
        stacked_images = imgStack(0.6, ([camera, mask]))
        
        cv.rectangle(stacked_images, (10, 10), (150, 50), (0, 0, 255), cv.FILLED)
        cv.putText(stacked_images, "RECALIBRATE", (18, 35), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv.imshow("Video playbacks", stacked_images)

        if recalibrate_clicked:
            break

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

    return recalibrate_clicked