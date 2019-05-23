from threading import Thread
import time
import cozmo
import requests
import json
import uuid
from PIL import Image
import os
import base64
import json

class ControllerFace(Thread):

    def __init__(self, face, picture, serverUrl, tryMaxNumber, nbVoteMin):
        Thread.__init__(self)
        self.face = face
        self.picture = picture
        self.encode64 = base64.b64encode(self.picture)
        self.serverUrl = serverUrl
        self.Done = False
        self.faceUuid = str(uuid.uuid4())
        self.face.rename_face("pending for crowd" + self.faceUuid) # Only alphanumerics
        self.jsonModel = "{id: id_template, image: encoded_template}" # If you want another jsonModel, just verify you have id_template and encode_template
        self.tryMaxNumber = tryMaxNumber
        self.nbVoteMin = nbVoteMin

    def run(self):

        response_send = self.sendPicture()

        if response_send is 201 :
            tryNumber = 0
            while not self.Done :
                    time.sleep(2)
                    response_check = self.checkPicture()
                    response_text = response_check.json()

                    if response_text["nbrVotes"] >= self.nbVoteMin :
                        self.face.rename_face(response_text["answer"])
                        isOkay = self.checkIfEndOk
                        if isOkay is "Ok":
                            self.Done = True
                        else :
                            print("Error in cleaning :\n" + isOkay + "\nErasing Face " + self.faceUuid)
                            self.face.erase_enrolled_face()
                    elif tryNumber >= self.tryMaxNumber :
                        print("The number of try reached the max allowed, erasing face " + self.faceUuid)
                        self.face.erase_enrolled_face()
                    else :
                        tryNumber = tryNumber  + 1
        else:
            print("Error : server status code = " + response_send + ", could not post face, erasing face " + self.faceUuid)
            self.face.erase_enrolled_face()

    def sendPicture(self) :
        files = self.jsonModel.replace("id_template",self.faceUuid).replace("encoded_template", self.encode64)
        response = requests.post(self.serverUrl, files=files)
        return response

    def checkPicture(self) :
        response = requests.get(self.serverUrl + "/" + self.faceUuid)
        return response

    def checkIfEndOk(self) :
        response = requests.delete(self.serverUrl + "/" + self.faceUuid)
        if response.status_code is 200 : 
            response2 = requests.get(self.serverUrl + "/" + self.faceUuid)
            if response2.status_code is 404 :
                return "Ok"
            else :
                return "Server didnt delete picture, rolling back but you will need to erase manually the picture on the server"
        else :
            return "Status Code from delete : " + response.code() + "\n" + response.body


        
