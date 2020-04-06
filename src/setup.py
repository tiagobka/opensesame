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



class controlRecognizer:

    def __init__(self):
        self.nFaces = 0
        self.bestFrame = None
        self.startTime = 0
        self.frameCounter = 0
        self.faceFramecounter = 0
        self.faceDetected = False
        self.bestArea = 0







