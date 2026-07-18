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

#Please use a stable-colored and good camera for best results 

camera_index = 1 #change this to your prefferd camera index

cap = cv.VideoCapture(camera_index)
cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0)
cap.set(cv.CAP_PROP_EXPOSURE, -4)


while True:
    success, camera = cap.read()
    if not success:
        break

    cam_HSV = cv.cvtColor(camera, cv.COLOR_BGR2HSV)
    
    #put the HSV values for the desired color using the "trackColors.py" script
    h_min = None
    h_max = None
    s_min = None
    s_max = None
    v_min = None
    v_max = None
    
    lower_limit = np.array([h_min, s_min, v_min])
    upper_limit = np.array([h_max, s_max, v_max])
    mask  = cv.inRange(cam_HSV, lower_limit, upper_limit)
    
    print(f"H: {h_min}-{h_max} | S: {s_min}-{s_max} | V: {v_min}-{v_max}")
    
    blankImg = np.zeros_like(camera)
    
    stacked_images = imgStack(0.7, ([camera, cam_HSV], 
                                    [mask, blankImg]))
    
    cv.imshow("Find your color values", stacked_images)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()