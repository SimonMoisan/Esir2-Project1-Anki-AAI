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

# Imports ci-dessus, ne pas oublier de les installer avec un pip3 install (ou pip install)

# On utilise une class pour pouvoir utiliser les attributs (avec self) de python
class ControllerFace(Thread):
    # fonction lancé automatiquement lorsque le thread est créé (CrowdController.ControllerFace(...) dans le programme principal)
    def __init__(self, face, picture, serverUrl, tryMaxNumber, nbVoteMin):
        try:
            Thread.__init__(self)
            self.face = face
            self.picture = picture.convert("RGB") # On supprime le channel alpha de l'image, qui pourraît poser des problèmes dans certains cas
            buffered = BytesIO()
            self.picture.save(buffered, format="JPEG") # On convertit l'image
            img_base64 = "data:image/jpeg;base64," # Cette chaine de caractères doit être rajouté pour que les navigateur reconnaissance que c'est une image
            self.encode64 = img_base64 + str(base64.b64encode(buffered.getvalue())).replace("b'","").replace("'","") # Les navigateurs arrivent sans problèmes à afficher des images encodé en base64, mais pas quand Python rajoute ses " b' ... '" autour des valeurs brute
            self.serverUrl = serverUrl 
            self.Done = False
            self.faceUuid = str(uuid.uuid4()) # On génère une uuid pour l'image prise, qui servira d'identifiant
            no_tiret = self.faceUuid.replace('-',"")
            no_number = ''.join(i for i in no_tiret if not i.isdigit()) # Les visage ne peuvent avoir QUE des LETTRES dans leur nom, même pas d'espaces
            self.face.rename_face("pending" + no_number) # On renome le visage avec un nom temporaire que COZMO reconnaîtra en attendant le verdict du Crowd
            self.jsonModel = "{id: id_template, image: encoded_template}" # Non-utilisé, avait pour vocation d'être un model remplaçable facilement de JSON pour l'envoi des données mais requests n'est pas SI simple
            self.tryMaxNumber = tryMaxNumber # Nombre de fois maximum que ce thread va essayer de récupérer les informations sur le verdict du Crowd, pour éviter d'avoir des threads immortels
            self.nbVoteMin = nbVoteMin
        except Exception as identifier:
            print("Thread init error " + self.faceUuid)
            self.face.erase_enrolled_face()

    # fonction qui sera automatiquement appelée lors de l'appel ....start() dans le programme principal
    def run(self):

        response_send = self.sendPicture()

        if response_send.status_code == 201 :
            tryNumber = 0
            while not self.Done :
                    time.sleep(2)
                    response_check = self.checkPicture()
                    response_text = response_check.json()
                    if response_text.get("nbrVotes") is not None : # On vérifie que la réponse éxiste
                        if response_text["nbrVotes"] >= self.nbVoteMin : # On vérifie le nombre de vote
                            self.face.rename_face(response_text["answer"]) # On réécrit le nom du visage avec la réponse du Crowd ATTENTION pas de vérification sur la forme de lé réponse, doit être QUE des lettres
                            isOkay = self.checkIfEndOk
                            if "Ok" is "Ok": # A changer si on a un delete sur le serveur API par "if isOkay is 'Ok'", avait vocation de vérifier que l'image avait été supprimée de l'API avant de continuer
                                self.Done = True
                            else :
                                print("Error in cleaning :\n" + str(isOkay) + "\nErasing Face " + self.faceUuid)
                                self.face.erase_enrolled_face()
                        elif tryNumber >= self.tryMaxNumber :
                            print("The number of try reached the max allowed, erasing face " + self.faceUuid)
                            self.face.erase_enrolled_face() # On efface le visage si on arrive pas à contacter la réponse, pour éviter d'avoir un visage avec un nom temporaire pour l'éternité
                        else :
                            tryNumber = tryNumber  + 1
                    else :
                        tryNumber = tryNumber  + 1
                        
        else:
            print("Error : server status code = " + str(response_send.status_code) + ", could not post face, erasing face " + self.faceUuid)
            self.face.erase_enrolled_face() # On efface le visage si on arrive pas à poster l'image sur l'API, pour éviter que le visage ai un nom temporaire pour l'éternité

    # Fonction d'envoi de l'image
    def sendPicture(self) :
        response = requests.post(self.serverUrl, json={"id": self.faceUuid, "image": str(self.encode64)})
        return response

    #Fonction de check de la réponse
    def checkPicture(self) :
        response = requests.get(self.serverUrl.replace("images","answers") + "/" + self.faceUuid) # On change salement l'url, à potentiellement rework si la destination n'est plus l'API de démo
        return response

    # Fonction inutilisée de suppression et vérification de suppression de l'image du serveur API
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

