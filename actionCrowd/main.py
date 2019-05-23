
import json
import uuid
from PIL import Image
import os
import base64
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
import time
import asyncio
try:
    from PIL import Image
except:
    print("Looks like you need to install Pillow")



def program_cozmo_action(robot: cozmo.robot.Robot, nb_vote_init:int):
    
    #params
    robot.camera.image_stream_enabled = True
    robot.camera.color_image_enabled  = True
    cube=None
    numero_cube =0
    nb_vote=nb_vote_init
    answer_json = 0
    url = "http://localhost:3000/V1/image"

    while(cube == None):
        #permet de voir l'environnement qu'entour cozmo
        look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        # scanne l’environnement à la recherche d’un cube.
        cube = robot.world.wait_for_observed_light_cube(timeout=30)
        look_around.stop()      

    # aller jusqu'a la position du cube identifié
    robot.go_to_pose(Pose(cube.pose.position.x, cube.pose.position.y, cube.pose.position.z, angle_z=degrees(0)), relative_to_robot=True).wait_for_completed()

    # take the picture of the cube
    pictureIsTaken = True
    while pictureIsTaken:
        duration_s = 0.1  # time to display each camera frame on Cozmo's face
        latest_image = robot.world.latest_image
        if latest_image is not None:
            image = latest_image.raw_image
            pictureIsTaken =False
            
    #save la photo prise pour pouvoir l'exposer au crowsourcing
    image.save("Cube action" + str(numero_cube) + ".bmp")
    numero = numero + 1

    while (answer_json["nbrVotes"]< nb_vote):
        # send picture to the crowsourcing panel
        id_cube = send_picture(image, url)
        if (id_cube == None):
            robot.say_text("Error cannot ask the crowsourcing")
            return None

        # récupération des infos
        answer_json = recup_picture_info(url, id_cube)
        if (answer_json == None):
            robot.say_text("Error result")
            return None

    # Réaliser les actions demandés
    action = answer_json["answer"]

    red, green, blue, white=cozmo.lights.red_light, cozmo.lights.green_light, cozmo.lights.blue_light, cozmo.lights.white_light
    colors=[red, white, white, white]

    if(action== "red"):
        color_light(cube, red)
    elif(action== "white"):
        color_light(cube, white)
    elif(action== "blue"):
        color_light(cube, blue)
    elif(action== "green"):
        color_light(cube, green)
    elif(action== "crazy_color_1"):
        crazy_color_1(cube)
    elif(action== "crazy_color_2"):
        crazy_color_2(cube)
    elif(action == "off"):
        light_off(cube)
    else:
        print("Action is not possible")
        return None

    return 1


cozmo.run_program(program_cozmo_action)


#################################################
# Fonctions pour intéragir avec les crowsourcing
################################################

def send_picture(image, url):
    new_id = str(uuid.uuid4())
    image.save("./Pendings/pending_" + new_id + ".png")
    image_encode = base64.b64encode(image)
    files = {'id' : new_id,'media': image_encode}
    response = requests.post(url, files=files)
    if response.status_code is 201 :
        return new_id
    else:
        print("Erreur : \n" + "Code reçu : " + response.status_code + "\n" + response.text)
        return None

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

#####################################################
# Fonctions pour allumer les cubes
#####################################################
  
def light_off(cube):
    # on éteint le cube
    if cube is not None:
        cube.set_lights(cozmo.lights.off_light)
    else:
        cozmo.logger.warning("Cozmo is not connected to a LightCube1Id cube - check the battery.")


def crazy_light_1(cube):
    if cube is not None:
        for l in [red, green, blue, white]: 
            cube.set_lights(l)
            time.sleep(1)
    else:
        cozmo.logger.warning("Cozmo is not connected to a LightCube1Id cube - check the battery.")

def color_light(cube, color):
    red, green, blue, white=cozmo.lights.red_light, cozmo.lights.green_light, cozmo.lights.blue_light, cozmo.lights.white_light
    colors=[red, white, white, white]
    if color in colors:
        if color ==red:
            cube.set_lights(cozmo.lights.red_light)
        if color ==blue:
            cube.set_lights(cozmo.lights.blue_light)
        if color ==white:
            cube.set_lights(cozmo.lights.white_light)
        if color ==green:
            cube.set_lights(cozmo.lights.green_light)
        return 
    else:
        print("color not in available colors")
        crazy_light_1(cube)

def crazy_light_2(cube):
    red, green, blue, white=cozmo.lights.red_light, cozmo.lights.green_light, cozmo.lights.blue_light, cozmo.lights.white_light
    colors=[red, white, white, white]
    if cube is not None:
        for i in range(20):
            colors = shift(colors, n=1)
            cube.set_light_corners(colors[0], colors[1], colors[2], colors[3])
            time.sleep(0.4)
    else:
        cozmo.logger.warning("Cozmo is not connected to a LightCube2Id cube - check the battery.")


