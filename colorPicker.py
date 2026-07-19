import cv2 as cv
import numpy as np
import json # 1. Import JSON

def get_hsv_on_click(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        pixel_hsv = cam_HSV[y, x]
        h, s, v = pixel_hsv[0], pixel_hsv[1], pixel_hsv[2]
        
        h_min, h_max = max(0, h - 10), min(179, h + 10)
        s_min, s_max = max(0, s - 40), min(255, s + 40)
        v_min, v_max = max(0, v - 40), min(255, v + 40)
        
        # 2. Convert the NumPy integers to standard Python integers so JSON can read them
        hsv_data = {
            "lower_limit": [int(h_min), int(s_min), int(v_min)],
            "upper_limit": [int(h_max), int(s_max), int(v_max)]
        }
        
        # 3. Save to a single readable JSON file
        with open("hsv_config.json", "w") as f:
            json.dump(hsv_data, f, indent=4)
        
        print("\n--- Saved to hsv_config.json! ---")
        print(f"lower_limit = {hsv_data['lower_limit']}")
        print(f"upper_limit = {hsv_data['upper_limit']}")
        print("Ready for mask.py!")

cap = cv.VideoCapture(0)
cv.namedWindow("Color Picker") 
cv.setMouseCallback("Color Picker", get_hsv_on_click)

while True:
    success, camera = cap.read()
    if not success: break
    
    global cam_HSV
    cam_HSV = cv.cvtColor(camera, cv.COLOR_BGR2HSV)
    cv.imshow("Color Picker", camera)
    
    if cv.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv.destroyAllWindows()