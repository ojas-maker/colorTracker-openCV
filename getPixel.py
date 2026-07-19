import cv2
import numpy as np

# Callback function to handle mouse clicks and extract pixel value
def get_pixel_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Access the pixel value at row 'y' and column 'x'
        # Note: OpenCV images are indexed as image[y, x]
        pixel_value = image[y, x]
        
        # OpenCV reads colors in BGR order by default, not RGB
        blue = pixel_value[0]
        green = pixel_value[1]
        red = pixel_value[2]
        
        print(f"Coordinates: X={x}, Y={y} | BGR Value: [{blue}, {green}, {red}]")

# Create a sample image (color gradient) for demonstration
# Replace this line with image = cv2.imread('your_image.jpg') to use your own image
image = np.zeros((400, 400, 3), dtype=np.uint8)
for i in range(400):
    image[:, i] = [i % 256, (i * 2) % 256, (255 - i) % 256]

# Set up the window and assign the mouse callback function
cv2.setMouseCallback("Pixel Color Detector", get_pixel_color)

print("Click anywhere on the image window to see pixel coordinates and BGR values.")

while True:
    cv2.imshow("Pixel Color Detector", image)
    
    # Press 'q' to exit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
