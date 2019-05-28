
import json
import uuid
from PIL import Image
import os
import base64
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
import time
import asyncio
from io import BytesIO
import json
import uuid
import requests
from random import uniform
try:
    from PIL import Image
except:
    print("Looks like you need to install Pillow")

# Imports ci-dessus, ne pas oublier de les installer avec un pip3 install (ou pip install)

#################################################
# Fonctions pour intéragir avec le crowdsourcing
################################################

def sendPicture(encode64, url, id_cube):
    response = requests.post(url, json={"id": id_cube, "image": str(encode64)}) # C'est comme ça que l'on envoie un json avec requests
    return response

def checkPicture(url, id_cube) :
    response = requests.get(url.replace("images","answers") + "/" + id_cube) # On change salement l'url, à potentiellement rework si la destination n'est plus l'API de démo
    return response

#####################################################
# Fonctions pour allumer les cubes
#####################################################
  
def light_off(cube):
    # on éteint le cube
    if cube is not None:
        cube.set_lights(cozmo.lights.off_light)
    else:
        cozmo.logger.warning("Cozmo is not connected to a LightCube1Id cube - check the battery.")

# Cette fonction fait tourner la couleur du cube entre les 4 couleurs suivante : Rouge, Bleu, Vert, Blanc
def crazy_color_1(cube, colors):
    rolls = 40
    while rolls >= 0 :
        cube.set_lights(colors[rolls % len(colors)])
        rolls = rolls - 1
        time.sleep(0.5)

# Cette fonction fait tourner la couleur du cube avec des couleurs aléatoires
def crazy_color_2(cube) :
    r = 0
    g = 0
    b = 0
    rolls = 40
    while rolls >= 0 :
        r = uniform(0, 255)
        g = uniform(0, 255)
        b = uniform(0, 255)
        color_actual = cozmo.lights.Light(cozmo.lights.Color(rgb=(int(r),int(g),int(b))))
        cube.set_lights(color_actual)
        rolls = rolls - 1
        time.sleep(0.5)

# Cette fonction change la couleur du cube. N'accepte que des objets couleurs de la librairie COZMO
def color_light(cube,color):
    cube.set_lights(color)
    time.sleep(20)

# Focntion principale
def program_cozmo_action(robot: cozmo.robot.Robot):
    
    #paramètres et initialisations
    #pour l'url du serveur faire attention à la modifification faite dans le fonction "checkpicture", un rework sera peut-être nécessaire pour viser autre chose que l'API de démo
    robot.camera.image_stream_enabled = True
    robot.camera.color_image_enabled  = True
    cube=None
    numero_cube = 0
    answer_json = 0
    url = "http://localhost:3000/v1/images"
    nbrVotesMin = 3 # Nombre de votes minimaux pour qu'une réponse soit jugée acceptable

    # Tant que COZMO n'a pas vu de cube
    while(cube == None):
        #permet de voir l'environnement qu'entour cozmo
        look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        # scanne l’environnement à la recherche d’un cube.
        cube = robot.world.wait_for_observed_light_cube(timeout=30)
        look_around.stop()      

    # aller jusqu'a la position du cube identifié
    robot.go_to_pose(cozmo.util.Pose(cube.pose.position.x, cube.pose.position.y, cube.pose.position.z, angle_z=degrees(0)), relative_to_robot=True).wait_for_completed()

    # prend en photo le cube (si COZMO a bien réussi à se placer, ce qui n'est pas gagné)
    # c'est une boucle pour être sûr qu'il n'y à pas de problèmes
    pictureIsTaken = True
    while pictureIsTaken:
        time.sleep(0.1)
        latest_image = robot.world.latest_image
        if latest_image is not None:
            image = latest_image.raw_image
            pictureIsTaken = False
            
    # On génère une uuid pour l'image prise, qui servira d'identifiant
    numero_cube = str(uuid.uuid4())

    #save la photo prise pour pouvoir l'exposer au crowsourcing
    image.save("CubeAction" + str(numero_cube) + ".bmp")
    image = image.convert("RGB") # On supprime le channel alpha de l'image, qui pourraît poser des problèmes dans certains cas

    # On utilise un buffer pour capturer les données brutes de l'image
    buffered = BytesIO()
    image.save(buffered, format="JPEG") # On convertit l'image
    img_base64 = "data:image/jpeg;base64," # Cette chaine de caractères doit être rajouté pour que les navigateur reconnaissance que c'est une image
    encode64 = img_base64 + str(base64.b64encode(buffered.getvalue())).replace("b'","").replace("'","") # Les navigateurs arrivent sans problèmes à afficher des images encodé en base64, mais pas quand Python rajoute ses " b' ... '" autour des valeurs brutes

    response_send = sendPicture(encode64, url, numero_cube) #On envoie l'image
    if response_send.status_code is not 201 : # gestion d'erreur
        error_string = "Error, can't POST the picture to the server API : " + response_send.status_code + "\n" + response_send.text
        raise IOError(error_string)
    else : # Si l'image est posté avec succès
        done = False
        while not done : # Boucle de check si le nombre de vote dépasse le minimum requis
            color = cozmo.lights.Light(cozmo.lights.Color(rgb=(178,128,1)))
            robot.set_all_backpack_lights(color)
            time.sleep(3)
            answer_text = checkPicture(url, numero_cube) # On check la réponse sur l'API
            answer_json = answer_text.json()
            if answer_json.get("nbrVotes") is not None : # Si une réponse existe
                if answer_json.get("nbrVotes") > nbrVotesMin: # Vérification du nombre de vote
                    done = True
                    color = cozmo.lights.Light(cozmo.lights.Color(rgb=(1,128,128)))
                    robot.set_all_backpack_lights(color)

    # Réaliser les actions demandés
    action = answer_json.get("answer")

    # Enregistrement de couleurs de base de la librairie COZMO
    red, green, blue, white=cozmo.lights.red_light, cozmo.lights.green_light, cozmo.lights.blue_light, cozmo.lights.white_light
    colors=[red, green, blue, white]

    if(action== "red"):
        color_light(cube, red)
    elif(action== "white"):
        color_light(cube, white)
    elif(action== "blue"):
        color_light(cube, blue)
    elif(action== "green"):
        color_light(cube, green)
    elif(action== "crazy_color_1"):
        crazy_color_1(cube, colors)
    elif(action== "crazy_color_2"):
        crazy_color_2(cube)
    elif(action == "off"):
        light_off(cube)
    elif "say" in action :
        robot.say_text(action.replace("say ", ""),True,use_cozmo_voice=True, in_parallel=True).wait_for_completed()
    else:
        error_string = "This action isn't a valide answer : " + action + "\nThe answer can be : red, blue, green, white, off, crazy_color_1, crazy_color_2"
        raise ValueError(error_string)

    return 1


# Le main du programme, lance la fonction principale
cozmo.run_program(program_cozmo_action, 1)





