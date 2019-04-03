from bin import lyncs_rover
from time import sleep
import math
import sys
import ctypes
import pygame
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)
sleep(120)

pygame.init()
done = False
clock = pygame.time.Clock()
pygame.joystick.init()

cs = lyncs_rover.arduino_control()
if cs.Init() == -1:
    print('error')
cs.Transfer(0, 3)

while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")


    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()





# axis1:center axis2:左右(y軸回転) axis5:上下(x軸回転)
        axis0 = int((-1000)*joystick.get_axis( 0 ))
        buttonm = joystick.get_button( 2 )
        buttonb = joystick.get_button( 1 )
        print(axis0)
        if buttonm == 1:
            cs.Transfer(int(axis0), 4)
        elif buttonb == 1:
            cs.Transfer(int(axis0), 8)
        else:
            cs.Transfer(0, 3)
    clock.tick(300)
