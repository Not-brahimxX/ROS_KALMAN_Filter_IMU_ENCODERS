#!/usr/bin/env python3

from math import cos, sin, tan
import time
from std_msgs.msg import Empty
from std_msgs.msg import Float32
from std_msgs.msg import Int16
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped, Twist
import Jetson.GPIO as GPIO
from rosnode import rosnode_ping_all, kill_nodes
import roslaunch

GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.IN)


if __name__ == '__main__':
    try:
        GPIO.setwarnings(False)
        i = 0
        while True:
            if GPIO.input(22) == 0 and i == 0:
                uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
                roslaunch.configure_logging(uuid)
                launch = roslaunch.parent.ROSLaunchParent(
                    uuid, ['/home/jetson/eurobot_ws/src/launcher/launch/robot.launch'])
                launch.start()
                i = 1
            elif GPIO.input(22) == 1 and i == 1:
                node_list = rosnode_ping_all()
                print(node_list)
                for node in node_list:
                    kill_nodes(node)
                i = 0
        # time.sleep(25)
    except rospy.ROSInterruptException:
        pass
