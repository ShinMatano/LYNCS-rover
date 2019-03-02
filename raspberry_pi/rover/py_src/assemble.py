from bin import lyncs_rover
import rover_module as gps
#from rover_module import height
from time import sleep


#height.judgeHight1()
#print("phase1")
#height.judgeHight2()
#print("phase2")

cs = lyncs_rover.arduino_control()
if cs.Init() == -1:
    print('error')
cs.Transfer(0, 6)
sleep(1)

length, theta = [0,0]
while True:
    list_dis_thet = gps.r_theta_to_goal(35.555744, 139.654071)
    if list_dis_thet != None:
        length, theta = list_dis_thet
        break

while True:
    list_dis_thet = gps.r_theta_to_goal(35.555744, 139.654071)
    if list_dis_thet != None:
        length, theta = list_dis_thet
    #print(length)
    #print(theta)
    #cs.Transfer(int(theta*1000), 5)
    #sleep(3)
    for i in range(100):
        judge=cs.Csearch1()
        if length*1000 < 20 and judge == 1:
            cs.Csearch2()
    #if r_theata[0]*1000 < 20:
       #cs.Csearch2()
    #else:
    if length*1000>=20:
        cs.Transfer(int(theta*1000), 5)
        #print(int(theta*1000))
        #print('5')
