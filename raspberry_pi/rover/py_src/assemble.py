from bin import lyncs_rover
import rover_module as gps
from rover_module import height
from time import sleep
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)

goal_lat, goal_log = [30.374528015873, 130.959977142857]
minimum_dist = 10

cs = lyncs_rover.arduino_control()
if cs.Init() == -1:
    print('error')
cs.Transfer(0,3)

count = 0
while True:
    count += 1
    judge_data0 = height.readData()
    if count % 10 == 1:
        cs.LogOutput('phase1, height::' + str(judge_data0))
    if judge_data0 > height.max_high:
        break

while True:
    count += 1
    judge_data = height.readData()
    if count % 10 == 1:
        cs.LogOutput('phase2, height::' + str(judge_data))

    if judge_data < height.low_high and height.math.fabs(height.given_data -
                                                         judge_data) < 0.8:
        break
    height.given_data = judge_data

cs.LogOutput('landed. waiting for 20 seconds.')
sleep(20)
cs.Transfer(0,6)
sleep(5)
cs.Transfer(0,4)
sleep(5)

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

    coord = gps.lat_long_measurement()
    if coord is not None:
        cs.LogOutput('lat::' + str(coord[0]) + ', long::' + str(coord[1]))

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
        if ret == 2:
            cs.Transfer(0,4)
            sleep(2)
            cs.LogOutput("Goal.")
            GPIO.output(18, GPIO.HIGH)
            cs.Transfer(0,3)
            sys.exit(0)
