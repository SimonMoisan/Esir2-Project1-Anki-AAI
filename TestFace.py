import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
import time
import asyncio
try:
    from PIL import Image
except:
    print("Looks like you need to install Pillow")


def program_cozmo(robot: cozmo.robot.Robot):
    robot.camera.image_stream_enabled = True
    robot.camera.color_image_enabled  = True
    image_inconnu = None
    numero_inconnu = 0
    
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
            if face_to_follow.name is not "" :
                robot.set_all_backpack_lights(cozmo.lights.green_light)
                robot.say_text("Bonjour" + face_to_follow.name,True,use_cozmo_voice=True, in_parallel=True).wait_for_completed()
            else :
                image_inconnu = robot.world.latest_image.raw_image
                image_inconnu.save("inconnu" + str(numero_inconnu) + ".bmp")
                numero_inconnu = numero_inconnu + 1
                inconnu_face_display(robot, "inconnu" + str(numero_inconnu - 1) + ".bmp")
                robot.set_all_backpack_lights(cozmo.lights.white_light)
                robot.say_text("Bonjour inconnu" + str(numero_inconnu),False,use_cozmo_voice=False,voice_pitch=-9, in_parallel=True).wait_for_completed()
            
            face_to_follow = None
            time.sleep(3)
		
def inconnu_face_display(robot: cozmo.robot.Robot, name_inconnu: str):
        
    image = Image.open(name_inconnu)
    image = image.resize(cozmo.oled_face.dimensions(), Image.NEAREST)
    image = cozmo.oled_face.convert_image_to_screen_data(image)

    seconds =3

    for nothing in range(seconds):
        robot.display_oled_face_image(image, 1000.0)

cozmo.run_program(program_cozmo, use_viewer=True, use_3d_viewer=True)