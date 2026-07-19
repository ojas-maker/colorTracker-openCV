# OpenCV Utility Sub-Modules

This branch contains a collection of standalone utility scripts designed to help setup, test, and calibrate OpenCV computer vision projects. These modules act as helper tools for debugging cameras and extracting precise color data for masking.

## 📁 Included Modules

### 1. `ExternalCamTest.py`
A simple diagnostic script to verify camera functionality. 
* **Use Case:** Run this to ensure your webcam or external USB camera is correctly detected by OpenCV, properly initialized, and streaming video without errors before running more complex tracking scripts.

### 2. `getPixel.py`
A mouse-click event tracker for real-time coordinate and color extraction.
* **Use Case:** Click anywhere on the live video feed to instantly grab the exact `(X, Y)` screen coordinates and the specific color values of that exact pixel. Perfect for mapping out custom boundary zones or checking specific lighting spots.

### 3. `trackColors.py`
A manual HSV (Hue, Saturation, Value) calibration dashboard.
* **Use Case:** Opens your video feed alongside a set of GUI trackbars. This allows you to manually slide and tweak the minimum and maximum HSV values in real-time until your object is perfectly masked out from the background. 

---

## ⚙️ Requirements
To run these scripts, you need Python installed along with the following libraries:
* `opencv-python` (cv2 as cv)
* `numpy`

You can install them via pip if you haven't already:
`pip install opencv-python numpy`

## 🚀 How to Run
Navigate to this folder in your terminal and run any of the scripts directly using Python:
`python trackColors.py`