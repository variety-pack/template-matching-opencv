import cv2
import numpy as np
 
# Camera 0 is default
camera_port = 0
 
#Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 30
 
# Set up camera.
camera = cv2.VideoCapture(camera_port)
camera.set(3, 1920)
camera.set(4, 1080)
 
# Captures a single image from the camera and returns it in PIL format
def get_image():
 retval, im = camera.read()
 return im

# Throw away rubbish photos.
for i in xrange(ramp_frames):
 temp = get_image()

# Now take photo.
camera_capture = get_image()

# Release camera.
del(camera)

# Convert image to allow easy processing.
img_grey = cv2.cvtColor(camera_capture, cv2.COLOR_BGR2GRAY)

# Print image.
file = "/home/pi/process_image.jpg"
cv2.imwrite(file, img_grey)

# Load template.
template = cv2.imread("/home/pi/stop.jpg", 0)
w, h = template.shape[::-1]

# Match it.
res = cv2.matchTemplate(img_grey, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.7
loc = np.where(res >= threshold)

# Draw rectangle on original image.
for pt in zip(*loc[::-1]):
    cv2.rectangle(camera_capture, pt, (pt[0]+w, pt[1]+h), (0,255,255), 4)

# Print image.
file = "/home/pi/process_image2.jpg"
cv2.imwrite(file, camera_capture)
