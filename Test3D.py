import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
'''
  La fonction 'run_program' prend en paramètre la fonction 'program_cozmo'
  La fonction 'program_cozmo' reçoit en paramètre le pointeur vers l'instance de cozmo obtenue 
'''
def program_cozmo(robot: cozmo.robot.Robot):
	robot.say_text("Hello world").wait_for_completed()
	print("C'est fini")
	# le programme se termine
	while True :
		robot.turn_in_place(degrees(1)).wait_for_completed()

cozmo.run_program(program_cozmo, use_viewer=True, use_3d_viewer=True)