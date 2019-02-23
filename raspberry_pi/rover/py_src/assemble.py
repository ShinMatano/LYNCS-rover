import rover_module as gps
from time import sleep

cs = lyncs_rover.arduino_control()
if cs.Init() == -1:
    print('error')

while True:
    length, theta = gps.r_theta_to_goal(35.555656, 139.654451)
    for i in range(25):
        judge=cs.Csearch1()
        if length*1000 < 20 and judge == 1:
            cs.Csearch2()
    #if r_theata[0]*1000 < 20:
    #    cs.Csearch2()
    #else:
    if length*1000>=20:
        cs.Transfer(int(theta*1000), 5)
        print(int(theta*1000))
        print('5')
