import cv2 as cv
import numpy as np
import json
import os
import subprocess
import sys

cam_HSV = None
calibration_done = False

# 1. An empty list to store your 8 clicks
clicked_points = [] 

def handle_mouse_events(event, x, y, flags, param):
    global cam_HSV, calibration_done, clicked_points
    
    if event == cv.EVENT_LBUTTONDOWN and cam_HSV is not None:
        
        # Add the clicked coordinate to our list
        clicked_points.append((x, y))
        print(f"Point {len(clicked_points)}/8 locked at ({x}, {y})")
        
        # 2. Once we hit 8 points (an octagon), do the math!
        if len(clicked_points) == 8:
            
            # Create a completely black canvas exactly the size of the camera feed
            h_img, w_img = cam_HSV.shape[:2]
            roi_mask = np.zeros((h_img, w_img), dtype=np.uint8)
            
            # Draw a solid white polygon on our black canvas using your 8 points
            pts = np.array(clicked_points, np.int32).reshape((-1, 1, 2))
            cv.fillPoly(roi_mask, [pts], 255)
            
            # Ask OpenCV to calculate the average color, but ONLY where the mask is white
            mean_color = cv.mean(cam_HSV, mask=roi_mask)
            
            # 3. THE FIX: Convert OpenCV's weird data into standard Python integers!
            h = int(mean_color[0])
            s = int(mean_color[1])
            v = int(mean_color[2])
            
            # Now the math will never wrap around backwards!
            h_min, h_max = max(0, h - 15), min(179, h + 15)
            s_min, s_max = max(20, s - 80), min(255, s + 80)
            v_min, v_max = max(20, v - 80), min(255, v + 80)
            
            hsv_data = {
                "lower_limit": [h_min, s_min, v_min],
                "upper_limit": [h_max, s_max, v_max]
            }

            script_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(script_dir, "hsv_config.json")
            
            with open(json_path, "w") as f:
                json.dump(hsv_data, f, indent=4)
            
            print("\n--- Octagon Average Saved! ---")
            print(f"Average HSV inside shape: H:{h} S:{s} V:{v}")
            print("Ready for mask.py!")
            
            calibration_done = True

cap = cv.VideoCapture(0)
# Make sure lighting matches mask.py
cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0)
cap.set(cv.CAP_PROP_EXPOSURE, -4)

cv.namedWindow("Color Picker") 
cv.setMouseCallback("Color Picker", handle_mouse_events)

print("Click 8 times around your object to draw a polygon!")

while True:
    success, camera = cap.read()
    if not success: 
        break
    
    # The Clean Clone (So your UI lines don't get mixed into the math)
    clean_frame = camera.copy()
    blurred = cv.GaussianBlur(clean_frame, (5, 5), 0)
    cam_HSV = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
    
    # 4. THE UI: Draw lines connecting the dots as you click!
    for i, point in enumerate(clicked_points):
        cv.circle(camera, point, 4, (0, 0, 255), -1) # Red dots for clicks
        if i > 0:
            cv.line(camera, clicked_points[i-1], point, (0, 255, 0), 2) # Green connecting lines
            
    # Draw the final closing line if all 8 points are placed
    if len(clicked_points) == 8:
        cv.line(camera, clicked_points[7], clicked_points[0], (0, 255, 0), 2)
    
    # Helpful text counter on screen
    cv.putText(camera, f"Points: {len(clicked_points)}/8", (20, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    cv.imshow("Color Picker", camera)
    
    if calibration_done:
        # Pause for exactly 1 second so you can visually see your finished polygon
        cv.waitKey(1000) 
        print("Transitioning to mask.py...")
        break
        
    if cv.waitKey(1) & 0xFF == ord('q'): 
        break

cap.release()
cv.destroyAllWindows()

if calibration_done:
    subprocess.run([sys.executable, "mask.py"])