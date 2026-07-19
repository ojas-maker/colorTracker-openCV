# OpenCV Color Tracker (Main Branch)

A dynamic, two-part computer vision tracking system built with Python and OpenCV. 

This project solves the common problem of inconsistent HSV color tracking by using a custom **8-point Region of Interest (ROI) calibration tool**. Instead of guessing or clicking a single noisy pixel, the user draws a polygon around the object, and the system calculates the perfect average mathematical color to track.

---

## Core Files

### 1. `colorPicker.py` (The Calibrator)
An interactive setup script that allows you to sample the exact color of an object under your current lighting conditions.
* **How it works:** Click 8 times around your target object in the live camera feed to draw a custom polygon. 
* **The Math:** The script isolates the area inside your shape, averages out shadows and camera noise, and calculates the optimal minimum and maximum HSV boundaries.
* **The Handoff:** It saves these values to `hsv_config.json` and automatically launches `mask.py`.

### 2. `mask.py` (The Tracker)
The main tracking engine that applies your saved color profile to the live video feed.
* **How it works:** It reads the `hsv_config.json` file and filters the camera feed to only see your calibrated color. 
* **Features:** Draws a bounding box and a center-point tracking dot on any object that matches the color profile (ignoring small background noise).
* **The Handoff:** Includes a custom on-screen graphical `"RECALIBRATE"` button. If your lighting changes, clicking this button safely shuts down the tracker and boots `colorPicker.py` back up.

---

## Requirements
To run this project, you need Python installed along with the following libraries:
* `opencv-python` (cv2)
* `numpy`

Install them via pip:
`pip install opencv-python numpy`

---

## How to Use

1. **Start the Calibration:**
   Open your terminal and run the picker script:
   `python colorPicker.py`
   
2. **Draw the 'Octagon':**
   Look at the camera feed and click 8 times around the edge of the object you want to track. The script will draw lines connecting your clicks.
   
3. **Automatic Tracking:**
   Once the 8th point is placed, the script will automatically calculate the average color, save it, and transition straight into tracking mode.
   
4. **Recalibrate on the Fly:**
   If you move to a darker/brighter room and the tracker loses the object, simply click the red **RECALIBRATE** button in the top left corner of the video window to instantly draw a new polygon.