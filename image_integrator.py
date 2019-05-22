import requests
import json
import uuid
from PIL import Image
import os
import base64


# Envoi l'image et l'uuid à l'api
# Retourne l'uudi qui est le seul point de contact avec les résultats du crownsourcing de l'image, à ne pas perdre
# Si le serveur n'a pas réussi récupérer l'image, retourne None, pour faciliter les tests et les handling d'erreurs
# TODO à Modifier dès que l'on récupère la vrai API
def send_picture(image, url):
    new_id = str(uuid.uuid4())
    image.save("./Pendings/pending_" + new_id + ".png")
    image_encode = base64.b64encode(image)
    files = {'_id' : new_id,'media': image_encode}
    response = requests.post(url, files=files)
    if response.status_code is 201 :
        return new_id
    else:
        print("Erreur : \n" + "Code reçu : " + response.status_code + "\n" + response.text)
        return None

# Récupère les informations du crownsourcing de l'image
# Retourne un json si get avec succès, None sinon
def recup_picture_info(url, code_uuid):
    response = requests.get(url + "/" + code_uuid)
    if response.status_code is 200 :
        j = response.json
        if None :
            pass #TODO responses not ready
        else :
            response_delete = requests.delete(url + "/" + code_uuid) #TODO Error handling if delete doesn't work on the distant server
            os.remove("./Pendings/pending_" + code_uuid + ".png")
            return j      
    else :
        print("Erreur : \n" + "Code reçu : " + response.status_code + "\n" + response.text)
        return None 


def image_validation(image, code_uuid):
    pass
