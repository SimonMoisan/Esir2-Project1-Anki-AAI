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
from io import BytesIO

class ControllerFace(Thread):

    def __init__(self, face, picture, serverUrl, tryMaxNumber, nbVoteMin):
        Thread.__init__(self)
        self.face = face
        self.picture = picture.convert("RGB")
        buffered = BytesIO()
        self.picture.save(buffered, format="JPEG")
        img_base64 = "data:image/jpeg;base64,"
        self.encode64 = img_base64 + base64.b64encode(buffered.getvalue())
        self.serverUrl = serverUrl
        self.Done = False
        self.faceUuid = str(uuid.uuid4())
        no_tiret = self.faceUuid.replace('-',"")
        no_number = ''.join(i for i in no_tiret if not i.isdigit())
        self.face.rename_face("pending" + no_number) # Only alphanumerics
        self.jsonModel = "{id: id_template, image: encoded_template}" # If you want another jsonModel, just verify you have id_template and encode_template
        self.tryMaxNumber = tryMaxNumber
        self.nbVoteMin = nbVoteMin

    def run(self):

        response_send = self.sendPicture()

        if response_send.status_code == 201 :
            tryNumber = 0
            while not self.Done :
                    time.sleep(2)
                    response_check = self.checkPicture()
                    response_text = response_check.json()
                    if response_text.get("nbrVotes") is not None :
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
                    else :
                        tryNumber = tryNumber  + 1
                        
        else:
            print("Error : server status code = " + str(response_send.status_code) + ", could not post face, erasing face " + self.faceUuid)
            self.face.erase_enrolled_face()

    def sendPicture(self) :
        response = requests.post(self.serverUrl, json={"id": self.faceUuid, "image": str(self.encode64)})
        return response

    def checkPicture(self) :
        response = requests.get(self.serverUrl.replace("images","answers") + "/" + self.faceUuid)
        return response

    def checkIfEndOk(self) :
        response = requests.delete(self.serverUrl.replace("images","answers") + "/" + self.faceUuid)
        if response.status_code is 200 : 
            response2 = requests.get(self.serverUrl.replace("images","answers") + "/" + self.faceUuid)
            if response2.status_code is 404 :
                return "Ok"
            else :
                return "Server didnt delete picture, rolling back but you will need to erase manually the picture on the server"
        else :
            return "Status Code from delete : " + response.code() + "\n" + response.body

    def convertToJpeg(self, im):
        with BytesIO() as f:
            im.save(f, format='JPEG')
            return f.getvalue()

        
