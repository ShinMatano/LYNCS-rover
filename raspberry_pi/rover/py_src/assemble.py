from bin import lyncs_rover
import rover_module as gps
from rover_module import height
from time import sleep
import sys
import RPi.GPIO as GPIO
import math

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)

goal_lat, goal_log = [30.3744887777778, 130.959956722222]
minimum_dist = 5

cs = lyncs_rover.arduino_control()
if cs.Init() == -1:
    print('error')
cs.Transfer(0, 3)
pre_data_1 = 0


cs.LogOutput('waiting for high state.')
sleep(120)

pre_data_2 = 0
while True:
    sleep(2)
    judge_data = height.readData()
    cs.LogOutput('phase2, height::' + str(judge_data))
    if judge_data < height.low_high  and math.fabs(judge_data - pre_data_2) < 0.8:
        break
    pre_data_2 = judge_data

cs.LogOutput('landed. waiting for 60 seconds.')
sleep(60)
cs.Transfer(0,6)
sleep(5)
cs.Transfer(0,4)
sleep(5)
cs.LogOutput('lift off.')

length, theta = [0,0]

while True:
    list_dis_thet = gps.r_theta_to_goal(goal_lat, goal_log)
    if list_dis_thet is not None:
        length, theta = list_dis_thet
        break

while True:
    list_dis_thet = gps.r_theta_to_goal(goal_lat, goal_log)
    if list_dis_thet is not None:
        length, theta = list_dis_thet
        cs.LogOutput('length::' + str(length) + ', theta::' + str(theta))
    coord = gps.lat_long_measurement()
    if coord is not None:
        cs.LogOutput('lat::' + str(coord[0]) + ', long::' + str(coord[1]))

    if length*1000 > minimum_dist:
        cs.Transfer(int(theta * 1000), 5)
    if length*1000 < minimum_dist:
        print(length)
        ret = cs.Csearch3()
        if ret == 0 :
            pass
        if ret == 1 :
            cs.Transfer(0, 2)
            cs.LogOutput("Searching.")
        if ret == 2 :
            cs.Transfer(0, 4)
            sleep(2)
            cs.LogOutput("Goal.")
            GPIO.output(18, GPIO.HIGH)
            cs.Transfer(0, 3)
            sys.exit(0)
"""
    for i in range(10):
        ret = cs.Csearch3()
        if ret == 0:
            pass
        if ret == 1:
            cs.LogOutput('length::' + str(length) + ', theta::' + str(theta))
            if length > minimum_dist:
                cs.Transfer(int(theta * 1000), 5)
            if length < minimum_dist:
                cs.Transfer(0,2)
        if ret == 2 and length < minimum_dist:
            cs.Transfer(0,4)
            sleep(2)
            cs.LogOutput("Goal.")
            GPIO.output(18, GPIO.HIGH)
            cs.Transfer(0,3)
            sys.exit(0)
    """
