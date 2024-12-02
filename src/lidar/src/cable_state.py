#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
import Jetson.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.IN)


def state():
    pub=rospy.Publisher('cablestate',Float32, queue_size=10)
    rospy.init_node('cable_state',anonymous=False)
    rate = rospy.Rate(10) # 10hz
    while True :
        pin=GPIO.input(22)
        if pin==0:
            pub.publish(1)
        else :
            pub.publish(0)


if __name__ == '__main__':
     try:
         state()
     except rospy.ROSInterruptException:
         pass
