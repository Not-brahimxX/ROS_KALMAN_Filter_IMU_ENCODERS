#!/usr/bin/python3
import rospy
from sensor_msgs.msg import LaserScan


# com = serial.Serial(port="/dev/ttyUSB0", baudrate="9600",
#                    timeout = 0.1, write_timeout = 0.1)
def laser_scan_callback(laser):

    min_range = 0.1
    max_range = 0.3
    
    range1 = laser.ranges[0:288]
    range2 = laser.ranges[288:576]
    range3 = laser.ranges[576:864]
    range4 = laser.ranges[864:1152]

    dist_obst_back= min(range1)
    dist_obst_right = min(range2)
    dist_obst_front = min(range3)
    dist_obst_left = min(range4)

    condition1 = dist_obst_back < max_range and dist_obst_back > min_range
    condition2 = dist_obst_right < max_range and dist_obst_right > min_range
    condition3 = dist_obst_front < max_range and dist_obst_front > min_range
    condition4 = dist_obst_left < max_range and dist_obst_left > min_range
    
    s1,s2,s3,s4="","","",""

    if condition1 :
        s1="B"
    
    if condition2 :
        s2="R"
    
    if condition3 :
        s3="F"

    if condition4 :
        s4="L"
    
    print("T_"+s1+s2+s3+s4)
    #if condition1 :

    #    print("T_B")

    #if condition2 :

    #    print("T_R")

    #if condition3 :

    #    print("T_F") 
    
    #if condition4 :

    #    print("T_L") 


if __name__ == '__main__':
    rospy.init_node('hLaserReader')
    range_subscriber = rospy.Subscriber(
        '/scan', LaserScan, laser_scan_callback)

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        # try:
        # data = com.readline()
        # if data:
        #   print(data)

        # except:
        # com.close()
        rate.sleep()

    rospy.spin()
