import cv2 as cv
import numpy as np

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

cap = cv.VideoCapture(1)
cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0)
cap.set(cv.CAP_PROP_EXPOSURE, -4)

cv.namedWindow("Trackbars")
cv.resizeWindow("Trackbars", 640, 240)
cv.createTrackbar("Hue min", "Trackbars", 0, 179, empty)
cv.createTrackbar("Hue max", "Trackbars", 179, 179, empty)
cv.createTrackbar("Sat min", "Trackbars", 0, 255, empty)
cv.createTrackbar("Sat max", "Trackbars", 255, 255, empty)
cv.createTrackbar("Val min", "Trackbars", 0, 255, empty)
cv.createTrackbar("Val max", "Trackbars", 255, 255, empty)

while True:
    success, camera = cap.read()
    if not success:
        break

    cam_HSV = cv.cvtColor(camera, cv.COLOR_BGR2HSV)
    
    h_min = cv.getTrackbarPos("Hue min", "Trackbars")
    h_max = cv.getTrackbarPos("Hue max", "Trackbars")
    s_min = cv.getTrackbarPos("Sat min", "Trackbars")
    s_max = cv.getTrackbarPos("Sat max", "Trackbars")
    v_min = cv.getTrackbarPos("Val min", "Trackbars")
    v_max = cv.getTrackbarPos("Val max", "Trackbars")
    
    lower_limit = np.array([h_min, s_min, v_min])
    upper_limit = np.array([h_max, s_max, v_max])
    mask  = cv.inRange(cam_HSV, lower_limit, upper_limit)
    
    print(f"H: {h_min}-{h_max} | S: {s_min}-{s_max} | V: {v_min}-{v_max}")
    
    blankImg = np.zeros_like(camera)
    
    stacked_images = imgStack(0.4, ([camera, cam_HSV], 
                                    [mask, blankImg]))
    
    cv.imshow("Vision Dashboard", stacked_images)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()