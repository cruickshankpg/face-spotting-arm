from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
rawCapture = PiRGBArray(camera)

time.sleep(0.1)

camera.capture(rawCapture, format="bgr")
image = rawCapture.array

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faceDet = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

face = faceDet.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)

if len(face) == 1:
    print("found a face\n")
    for (x, y, w, h) in face:
        gray = gray[y:y + h, x:x + w]
        out = cv2.resize(gray, (350, 350))
        cv2.imwrite("nailedIt.jpg", out)  # Write image
