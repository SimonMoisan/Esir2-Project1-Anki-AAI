
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


#################################################
# Fonctions pour intéragir avec le crowdsourcing
################################################

def sendPicture(encode64, url, id_cube):
    response = requests.post(url, json={"id": id_cube, "image": str(encode64)})
    return response

def checkPicture(url, id_cube) :
    response = requests.get(url.replace("images","answers") + "/" + id_cube)
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


def crazy_color_1(cube, colors):
    rolls = 40
    while rolls >= 0 :
        cube.set_lights(colors[rolls % len(colors)])
        rolls = rolls - 1
        time.sleep(0.5)

def crazy_color_2(cube) :
    r = 0
    g = 0
    b = 0
    rolls = 40
    while rolls >= 0 :
        r = uniform(0, 255)
        g = uniform(0, 255)
        b = uniform(0, 255)
        #print(str(r) + " " + str(g) + " " + str(b))
        color_actual = cozmo.lights.Light(cozmo.lights.Color(rgb=(int(r),int(g),int(b))))
        cube.set_lights(color_actual)
        rolls = rolls - 1
        time.sleep(0.5)





def color_light(cube,color):
    cube.set_lights(color)
    time.sleep(20)


def program_cozmo_action(robot: cozmo.robot.Robot):
    
    #params
    robot.camera.image_stream_enabled = True
    robot.camera.color_image_enabled  = True
    cube=None
    numero_cube =0
    answer_json = 0
    url = "http://localhost:3000/v1/images"
    nbrVotesMin = 3

    while(cube == None):
        #permet de voir l'environnement qu'entour cozmo
        look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        # scanne l’environnement à la recherche d’un cube.
        cube = robot.world.wait_for_observed_light_cube(timeout=30)
        look_around.stop()      

    # aller jusqu'a la position du cube identifié
    robot.go_to_pose(cozmo.util.Pose(cube.pose.position.x, cube.pose.position.y, cube.pose.position.z, angle_z=degrees(0)), relative_to_robot=True).wait_for_completed()

    # take the picture of the cube
    pictureIsTaken = True
    while pictureIsTaken:
        time.sleep(0.1)
        latest_image = robot.world.latest_image
        if latest_image is not None:
            image = latest_image.raw_image
            pictureIsTaken = False
            
    #save la photo prise pour pouvoir l'exposer au crowsourcing
    numero_cube = str(uuid.uuid4())
    image.save("CubeAction" + str(numero_cube) + ".bmp")
    image = image.convert("RGB")
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = "data:image/jpeg;base64,"
    encode64 = img_base64 + str(base64.b64encode(buffered.getvalue())).replace("b'","").replace("'","")

    response_send = sendPicture(encode64, url, numero_cube)
    if response_send.status_code is not 201 :
        error_string = "Error, can't POST the picture to the server API : " + response_send.status_code + "\n" + response_send.text
        raise IOError(error_string)
    else :
        done = False
        while not done :
            color = cozmo.lights.Light(cozmo.lights.Color(rgb=(178,128,1)))
            robot.set_all_backpack_lights(color)
            time.sleep(3)
            answer_text = checkPicture(url, numero_cube)
            answer_json = answer_text.json()
            if answer_json.get("nbrVotes") is not None :
                if answer_json.get("nbrVotes") > nbrVotesMin:
                    done = True
                    color = cozmo.lights.Light(cozmo.lights.Color(rgb=(1,128,128)))
                    robot.set_all_backpack_lights(color)

    # Réaliser les actions demandés
    action = answer_json.get("answer")

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


cozmo.run_program(program_cozmo_action, 1)





