# OpenCV Color Tracker (State Machine Architecture)

A dynamic, modular computer vision tracking system built with Python and OpenCV. 

This project solves the common problem of inconsistent HSV color tracking by using a custom **8-point Region of Interest (ROI) calibration tool**. Instead of guessing or clicking a single noisy pixel, the user draws a polygon around the object, and the system calculates the perfect average mathematical color to track. 

This project is built using a **State Machine architecture**, meaning it cycles seamlessly between calibration and tracking modes within a single lightweight engine loop, completely avoiding memory leaks or background subprocesses.

---

## Core Architecture

### 1. `main.py` (The Engine)
The entry point and "traffic cop" of the application. It controls the state machine, loading the calibrator and tracker dynamically without ever opening new background processes. This ensures the tracker uses minimal RAM, no matter how many times you recalibrate.

### 2. `colorPicker.py` (The Calibrator)
An interactive setup module that allows you to sample the exact color of an object under your current lighting conditions.
* **How it works:** Click 8 times around your target object in the live camera feed to draw a custom polygon. 
* **The Math:** The module isolates the area inside your shape, averages out shadows and camera noise, and calculates the optimal minimum and maximum HSV boundaries.
* **The Handoff:** It saves these values to `hsv_config.json` and signals the engine to transition to tracking mode.

### 3. `mask.py` (The Tracker)
The main tracking module that applies your saved color profile to the live video feed.
* **How it works:** It reads the `hsv_config.json` file and filters the camera feed to only see your calibrated color. 
* **Features:** Draws a bounding box and a center-point tracking dot on any object that matches the color profile (ignoring small background noise).
* **The Handoff:** Includes a custom on-screen graphical `"RECALIBRATE"` button built using `cv.pointPolygonTest`. Clicking this safely shuts down the tracker and signals the engine to boot the Calibrator back up.

### 4. `utils.py` (The Helpers)
A centralized module for reusable matrix and image manipulation math (such as the dynamic `imgStack` function) to keep the core codebase perfectly DRY (Don't Repeat Yourself).

---

## Requirements
To run this project, you need Python installed along with the following libraries:
* `opencv-python` (cv2)
* `numpy`

Install them via pip:
```bash
pip install opencv-python numpy