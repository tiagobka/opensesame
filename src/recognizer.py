
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from setup import SetupRecognizer

setup = SetupRecognizer()
print(setup.cascadeFile)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

face_cascade  = cv2.CascadeClassifier(setup.cascadeFile)
print(face_cascade)
for frame in camera.capture_continuous(rawCapture, format= "bgr", use_video_port=True):
	image = frame.array
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.1, 5)
	for (x,y,w,h) in faces:
		cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
		#roi_gray = gray[y:y+h, x:x+w]
		#roi_color = image[y:y+h, x:x+w]
	
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1)
	rawCapture.truncate(0)
	if key == ord("q"):
		break
cv2.destroyAllWindows()
