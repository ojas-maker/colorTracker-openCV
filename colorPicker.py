import cv2 as cv
import numpy as np
import json
import os
import subprocess
import sys

polygon_points = np.array([
    [54, 3],
    [90, 3],
    [53, 38],
    [90, 40]   
], dtype=np.int32)

polygon_points = polygon_points.reshape((-1, 1, 2))

cam_HSV = None
# 1. Create the boolean tracker
area_clicked = False

def handle_mouse_events(event, x, y, flags, param):
    global cam_HSV, area_clicked # 2. Make it global so the function can modify it
    
    if event == cv.EVENT_LBUTTONDOWN and cam_HSV is not None:
        
        is_inside = cv.pointPolygonTest(polygon_points, (float(x), float(y)), False)
        
        if is_inside >= 0:
            print(f"Success: Click detected INSIDE the target area at ({x}, {y})")
            # 3. Flip the boolean to True!
            area_clicked = True
        else:
            print(f"Click registered outside target at ({x}, {y})")
            
        h_img, w_img = cam_HSV.shape[:2]
        if 0 <= x < w_img and 0 <= y < h_img:
            pixel_hsv = cam_HSV[y, x]
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
            
            print("\n--- Saved to hsv_config.json! ---")
            print(f"lower_limit = {hsv_data['lower_limit']}")
            print(f"upper_limit = {hsv_data['upper_limit']}")
            print("Ready for mask.py!")

cap = cv.VideoCapture(0)
cv.namedWindow("Color Picker") 
cv.setMouseCallback("Color Picker", handle_mouse_events)

while True:
    success, camera = cap.read()
    if not success: 
        break
    
    cv.putText(camera, ".", (40, 40), cv.FONT_HERSHEY_SIMPLEX, 8, (0, 255, 0), 2)
    
    cam_HSV = cv.cvtColor(camera, cv.COLOR_BGR2HSV)
    cv.imshow("Color Picker", camera)
    
    # 4. Check the boolean every single frame
    if area_clicked:
        print("Transitioning to mask.py...")
        break
        
    if cv.waitKey(1) & 0xFF == ord('q'): 
        break

# 5. CRITICAL FIX: Release the camera BEFORE launching the new script!
cap.release()
cv.destroyAllWindows()

# 6. Launch mask.py ONLY if the target was actually clicked (not if you just pressed 'q' to quit)
if area_clicked:
    subprocess.run([sys.executable, "mask.py"])