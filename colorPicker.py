import cv2 as cv
import numpy as np
import json
import os

cam_HSV = None
calibration_done = False
clicked_points = [] 

def handle_mouse_events(event, x, y, flags, param):
    global cam_HSV, calibration_done, clicked_points
    
    if event == cv.EVENT_LBUTTONDOWN and cam_HSV is not None:
        clicked_points.append((x, y))
        print(f"Point {len(clicked_points)}/8 locked at ({x}, {y})")
        
        if len(clicked_points) == 8:
            h_img, w_img = cam_HSV.shape[:2]
            roi_mask = np.zeros((h_img, w_img), dtype=np.uint8)
            
            pts = np.array(clicked_points, np.int32).reshape((-1, 1, 2))
            cv.fillPoly(roi_mask, [pts], 255)
            
            mean_color = cv.mean(cam_HSV, mask=roi_mask)
            
            h = int(mean_color[0])
            s = int(mean_color[1])
            v = int(mean_color[2])
            
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

def run_picker():
    global cam_HSV, calibration_done, clicked_points
    
    calibration_done = False
    clicked_points = []
    
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0)
    cap.set(cv.CAP_PROP_EXPOSURE, -4.85)

    cv.namedWindow("Color Picker") 
    cv.setMouseCallback("Color Picker", handle_mouse_events)
    print("Click 8 times around your object to draw a polygon!")

    while True:
        success, camera = cap.read()
        if not success: 
            break
        
        clean_frame = camera.copy()
        blurred = cv.GaussianBlur(clean_frame, (5, 5), 0)
        cam_HSV = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)

        for i, point in enumerate(clicked_points):
            cv.circle(camera, point, 4, (0, 0, 255), -1)
            if i > 0:
                cv.line(camera, clicked_points[i-1], point, (0, 255, 0), 2)
                
        if len(clicked_points) == 8:
            cv.line(camera, clicked_points[7], clicked_points[0], (0, 255, 0), 2)
        
        cv.putText(camera, f"Points: {len(clicked_points)}/8", (20, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv.imshow("Color Picker", camera)
        
        if calibration_done:
            cv.waitKey(1000) 
            print("Transitioning to Engine...")
            break
            
        if cv.waitKey(1) & 0xFF == ord('q'): 
            break

    cap.release()
    cv.destroyAllWindows()
    return True