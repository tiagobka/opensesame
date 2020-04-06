import json
import time
class SetupRecognizer:

    def __init__(self):
        self.configFile = "../setup/config.json"
        self.policyFile = "../setup/policy.json"
        self.configSetup(self.configFile)
        self.policySetup(self.policyFile)

    def configSetup(self, file):
        if file != self.configFile:
            self.configFile = file
        with open(file) as json_file:
            data = json.load(json_file)
            self.cascadeFile = data['cascadeFile']
            self.AccessKeyID = data['AccessKeyID']
            self.SecretKey = data['SecretKey']
            self.faceCollectionID = data['faceCollectionID']
            self.pollingTime = data['pollingTime']
            self.sensitivity = data['sensitivity']


    def policySetup(self, file):
        if file != self.policyFile:
            self.policyFile = file
        with open(file) as json_file:
            data = json.load(json_file)
            self.certaintyThreshold = data["certaintyThreshold"]
            self.piggybackAllow = data["piggybackAllow"]
            self.requestDelay = data["requestDelay"]


    def __str__(self):
        return "cascadeFile: " + self.cascadeFile + "\n" +\
        "AccessKeyID: " + self.AccessKeyID + "\n" +\
        "SecretKey: " + self.SecretKey + "\n" +\
        "faceCollectionID: " + self.faceCollectionID + "\n" +\
        "pollingTime: " + str(self.pollingTime) + "\n"\
        "certaintyThreshold: "  + str(self.certaintyThreshold) + "\n"\
        "piggybackAllow: " + str(self.piggybackAllow) + "\n"\
        "requestDelay: " + str(self.requestDelay) + "\n"\
        "sensitivity: " + str(self.sensitivity) + "\n"

    def showSetup(self):
        print(self.__str__())



class ControlRecognizer:

    def __init__(self):
        self.bestFrame = None # frame datatype containing best image within a poll time
        self.bestRank = 0
        self.startTime = 0 # start of the polltime
        self.frameCounter = 0 #total frames 
        self.faceFrameCounter = 0 # number of frames containing a face
        self.faceDetected = False # Indicates a poll have triggered
        #self.bestArea = 0  new ranking based on 
        self.timeUp = False
        self.lastSent  = 0 #timestamp of last AWS call
        
        
    def trigger(self):
        if not self.faceDetected:
            self.startTime = time.time()
            self.faceDetected = True
            
    def pollImage(self, pollTime, rank) -> bool:
        if self.faceDetected:
            elapsedTime = int(time.time() - self.startTime)
            if (elapsedTime > pollTime):
                self.timeUp = True ## necessary?
            if rank > self.bestRank:
                self.bestRank = rank
                return True
        return False
    
    def timeout(self, delay):
        if self.timeUp:
            self.startTime = 0
            self.faceDetected = False
            self.bestRank = 0
            self.frameCounter = 0
            self.faceFrameCounter = 0
            self.timeUp = False
            if (int(time.time()- self.lastSent) > delay):
                 print("OK To send")
    def cleanup(self):
        self.startTime = 0
        self.faceDetected = False
        self.bestRank = 0
        self.frameCounter = 0
        self.faceFrameCounter = 0
        self.timeUp = False
        
            
                
        
        







