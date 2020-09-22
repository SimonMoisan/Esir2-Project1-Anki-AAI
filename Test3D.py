import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
import time
import asyncio
'''
  La fonction 'run_program' prend en paramètre la fonction 'program_cozmo'
  La fonction 'program_cozmo' reçoit en paramètre le pointeur vers l'instance de cozmo obtenue 
'''

def program_cozmo(robot: cozmo.robot.Robot):
	while True :
		robot.turn_in_place(degrees(20)).wait_for_completed()
		robot.move_head(1)
		time.sleep(3)
		robot.move_head(-1)
		time.sleep(3)

cozmo.run_program(program_cozmo, use_viewer=True, use_3d_viewer=True)