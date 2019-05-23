import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
import time
import asyncio
import CrowdController
try:
    from PIL import Image
except:
    print("Looks like you need to install Pillow")


def program_cozmo(robot: cozmo.robot.Robot):
    url = "http://localhost:3000/v1/images"
    robot.camera.image_stream_enabled = True
    robot.camera.color_image_enabled  = True
    image_inconnu = None
    
    while True :
        face_to_follow = None
        robot.move_lift(-3)
        while face_to_follow is None :
            robot.set_all_backpack_lights(cozmo.lights.red_light)
            robot.move_head(1)
            try:
                face_to_follow = robot.world.wait_for_observed_face(timeout=60)
                robot.set_all_backpack_lights(cozmo.lights.blue_light)
            except asyncio.TimeoutError:
                print("Didn't find a face - exiting!")

            # COZMO ne reconnais pas directement la personne, on essaye alors de scanner plusieurs fois la personne
            i = 0
            if face_to_follow.name is "" :
                robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabSquint2,ignore_body_track=True, ignore_lift_track=True,in_parallel=True)
            
            if face_to_follow is not None :
                while face_to_follow.name is "" and i < 50 :
                    try:
                        face_to_follow = robot.world.wait_for_observed_face(timeout=5)
                        robot.turn_towards_face(face_to_follow,in_parallel=True).wait_for_completed
                    except asyncio.TimeoutError:
                        print("Perte du visage pendant le scan")
                        face_to_follow = None
                        break
                    i = i + 1
                    time.sleep(0.2)
                    


        while face_to_follow is not None :
            robot.turn_towards_face(face_to_follow, in_parallel=True).wait_for_completed()
            #Case if COZMO already know the face
            if face_to_follow.name is not "" and "pending" not in face_to_follow.name :
                robot.set_all_backpack_lights(cozmo.lights.green_light)
                robot.say_text("Bonjour" + face_to_follow.name,True,use_cozmo_voice=True, in_parallel=True).wait_for_completed()
            #Case if COZMO see a face which treatment is pending
            elif "pending" in face_to_follow.name:
                color = cozmo.lights.Light(cozmo.lights.Color(rgb=(128,128,1)))
                robot.set_all_backpack_lights(color)
                robot.say_text("Bonjour humain numéro" + face_to_follow.name.replace("pending for crowd", "") + ", merci d'attendre votre reconnaissance",True,use_cozmo_voice=True, in_parallel=True).wait_for_completed()
            #Case if COZMO don't know the face
            else :
                image_inconnu = robot.world.latest_image.raw_image

                robot.set_all_backpack_lights(cozmo.lights.white_light)
                try:
                    treadController = CrowdController.ControllerFace(face_to_follow, image_inconnu, url ,100 , 5)
                    treadController.start()
                except Exception as identifier:
                    print("Erreur\n" + str(identifier))
                robot.say_text("Bonjour inconnu, votre visage va être traité, merci de votre patience" ,False,use_cozmo_voice=False,voice_pitch=-9, in_parallel=True).wait_for_completed()

            
            face_to_follow = None
            time.sleep(3)

cozmo.run_program(program_cozmo, use_viewer=True)