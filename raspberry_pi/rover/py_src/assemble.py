from bin import lyncs_rover
import rover_module as gps
from time import sleep

cs = lyncs_rover.arduino_control()
cs.Init()
while True:
    for i in range(25):
        cs.Csearch1()

    length, theta = gps.r_theta_to_goal(35.555225, 139.654664)
    #if r_theata[0]*1000 < 20:
    #    cs.Csearch2()
    #else:
    cs.Transfer(int(theta*1000), 5)
    #print("s")
    #sleep(1)
