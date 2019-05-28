import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
import time
import asyncio
import CrowdController
try:
    from PIL import Image
except:
    print("Looks like you need to install Pillow")

# Imports ci-dessus, ne pas oublier de les installer avec un pip3 install (ou pip install)

# La fonction principale
def program_cozmo(robot: cozmo.robot.Robot):

    #paramètres et initialisations
    #pour l'url du serveur faire attention à la modifification faite dans le fonction "checkpicture", un rework sera peut-être nécessaire pour viser autre chose que l'API de démo
    url = "http://localhost:3000/v1/images"
    robot.camera.image_stream_enabled = True
    robot.camera.color_image_enabled  = True
    image_inconnu = None
    
    #Boucle infinie
    while True :
        face_to_follow = None # Réinitilisation du visage enregistré
        robot.move_lift(-3) # On llibère la vision de la caméra
        while face_to_follow is None :
            robot.set_all_backpack_lights(cozmo.lights.red_light)
            robot.move_head(1)
            try:
                face_to_follow = robot.world.wait_for_observed_face(timeout=60) # COZMO attend un visage
                robot.set_all_backpack_lights(cozmo.lights.blue_light)
            except asyncio.TimeoutError:
                print("Didn't find a face - exiting!")

            # COZMO ne reconnais pas directement la personne, on essaye alors de scanner plusieurs fois la personne
            i = 0
            if face_to_follow.name is "" : # On check si le visage à un nom ou pas (si il est connu ou non)
                robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabSquint2,ignore_body_track=True, ignore_lift_track=True,in_parallel=True) # Juste une animation visuelle des yeux de COZMO
            
            # Workaround étrange, entre le bloc if ci-dessus et celui, COZMO peut perdre le visage et ainsi créer une erreur, alors on vérifie
            if face_to_follow is not None :
                while face_to_follow.name is "" and i < 50 : # Lancement du scan long, avec un nombre de passage i et une vérification si le visage est toujours inconnu
                    try:
                        face_to_follow = robot.world.wait_for_observed_face(timeout=5)
                        robot.turn_towards_face(face_to_follow,in_parallel=True).wait_for_completed # Permet un suivit du visage, mais bouger va ralentir le scan. Si on enlève le "wait_for_completed", on s'expose à des crashs
                    except asyncio.TimeoutError:
                        print("Perte du visage pendant le scan")
                        face_to_follow = None
                        break
                    i = i + 1
                    time.sleep(0.2)
                    


        while face_to_follow is not None : # Une fois qu'on a bien scanner, pour être juste un peu plus sûr que COZMO ne connaît effectivement pas déjà le visage, ou qu'il le connaît
            robot.turn_towards_face(face_to_follow, in_parallel=True).wait_for_completed()
            #Cas si COZMO connaît déjà le visage
            if face_to_follow.name is not "" and "pending" not in face_to_follow.name :
                robot.set_all_backpack_lights(cozmo.lights.green_light)
                robot.say_text("Bonjour" + face_to_follow.name,True,use_cozmo_voice=True, in_parallel=True).wait_for_completed()
            #Cas si COZMO voit une face qu'il reconnaît mais qui a un "pending" dans son nom (veut dire que le Crowd n'a pas encore rendu son verdict)
            elif "pending" in face_to_follow.name:
                color = cozmo.lights.Light(cozmo.lights.Color(rgb=(128,128,1)))
                robot.set_all_backpack_lights(color)
                robot.say_text("Bonjour humain numéro" + face_to_follow.name.replace("pending for crowd", "") + ", merci d'attendre votre reconnaissance",True,use_cozmo_voice=True, in_parallel=True).wait_for_completed()
            #Cas si COZMO ne connaît pas le visage
            else :
                image_inconnu = robot.world.latest_image.raw_image #On prend la photo

                robot.set_all_backpack_lights(cozmo.lights.white_light)
                try:
                    treadController = CrowdController.ControllerFace(face_to_follow, image_inconnu, url ,100 , 5) # Création du thread
                    treadController.start() # Lancement du thread de reconnaissance et le thread principal ne s'en occupe plus du tout.
                except Exception as identifier:
                    print("Erreur\n" + str(identifier))
                robot.say_text("Bonjour inconnu, votre visage va être traité, merci de votre patience" ,False,use_cozmo_voice=False,voice_pitch=-9, in_parallel=True).wait_for_completed()

            
            face_to_follow = None
            time.sleep(3)

# Le main du programme, lance la fonction principale
cozmo.run_program(program_cozmo, use_viewer=True)