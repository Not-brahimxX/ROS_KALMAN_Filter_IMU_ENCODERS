#!/usr/bin/python3
import rospy
from sensor_msgs.msg import LaserScan
import serial
import Jetson.GPIO as gpio

i=0
# com = serial.Serial(port="/dev/ttyUSB0", baudrate="9600",
#                    timeout = 0.1, write_timeout = 0.1)
def laser_scan_callback(laser):
    global i

    min_range=0.2
    max_range=0.3

    range=laser.ranges[410:990]

    dist_obst=min(range)

    ang_obst=range.index(dist_obst)*0.31

    condition0=dist_obst > max_range
    condition1=dist_obst < max_range and dist_obst > min_range
    condition2=dist_obst < min_range
    if condition0:
        i=0
        print(i)

    if condition1 and i==0:
        # dir l9wada high
        rospy.loginfo("There's an obstacle at a distance of " +
                      str(dist_obst)+"and at a "+str(ang_obst)+"°")
        # com.write(str.encode(str([dist_obst, ang_obst])))
        i=1
        print(i)

    if condition2 and i==1:
        rospy.loginfo("There's an obstacle at a distance of " +
                      str(dist_obst)+"and at a "+str(ang_obst)+"°")
        # com.write(str.encode(str([dist_obst, ang_obst])))
        i=2
        print(i)


if __name__ == '__main__':
    rospy.init_node('hLaserReader')
    range_subscriber=rospy.Subscriber(
        '/scan', LaserScan, laser_scan_callback)

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        #try:
            #data = com.readline()
            #if data:
             #   print(data)

        #except:
            #com.close()
        rate.sleep()

    rospy.spin()
