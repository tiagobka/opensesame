
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from setup import SetupRecognizer, ControlRecognizer
import boto3
import botocore
from gpiozero import LED #GPIO functions (Migrated From RPI.GPIO)
from collections import defaultdict
from statistics import mean

setup = SetupRecognizer() #Read Configuration Files
control = ControlRecognizer() #Initiate backend logic controller
client = setup.connectClient()#Connects to AWS system

relay = LED(4) #Set pin 7 (GPIO4) as an output digital pin

#Setup the Raspberry Pi Camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

face_cascade  = cv2.CascadeClassifier(setup.cascadeFile)
#start video capture and process frame by frame
for frame in camera.capture_continuous(rawCapture, format= "bgr", use_video_port=True):
	image = frame.array
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.1, 5)
	
	rank = cv2.Laplacian(image, cv2.CV_64F).var()
	
	for (x,y,w,h) in faces:
		cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
		#roi_gray = gray[y:y+h, x:x+w]
		#roi_color = image[y:y+h, x:x+w]
	control.frameCounter = control.frameCounter + 1
	if (len(faces) > 0 ):
		control.faceFrameCounter  = control.faceFrameCounter + 1
		control.trigger()
	
	if control.pollImage(setup.pollingTime, rank):
		control.bestFrame = image
	
	#control.timeout(setup.requestDelay)

	if control.timeUp:
		delay  = int(time.time()- control.lastSent) > setup.requestDelay
		stats = control.faceFrameCounter/control.frameCounter*100
		#print(delay, stats)
		if (delay & (stats > setup.sensitivity)):
			print("sending")
			img_encode = cv2.imencode('.jpg', control.bestFrame)[1].tostring()
			try:
				response=client.search_faces_by_image(CollectionId=setup.faceCollectionID,
								Image={"Bytes":img_encode},
								FaceMatchThreshold=70,
								MaxFaces=3)
			except botocore.exceptions.ParamValidationError as error: 
				print(error)
			faceMatches=response['FaceMatches']
			tab = defaultdict(list)

			
			for match in faceMatches:
				tab[match['Face']['ExternalImageId']].append(match['Similarity'])
				#print ('FaceId:' + match['Face']['ExternalImageId'])
				#print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
			if len(tab) == 1:
				name = list(tab.keys())[0]
				val = mean(tab[name])
				print(val)
				if val > setup.certaintyThreshold:
					print("Unlocking door for " +  name + " with an average certainty of " + str (val) + "%")
					relay.on()#open the door
					time.sleep(5)
					relay.off()#lock the door
			
			control.lastSent = time.time()
			
		control.cleanup()
		  
	
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1)
	rawCapture.truncate(0)
	if key == ord("q"):
		break
cv2.destroyAllWindows()
