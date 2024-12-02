#!/usr/bin/python3

import rospy
from std_msgs.msg import Float32
from nav_msgs.msg import Odometry
from math import cos, sin, pi

# Define the callback functions for the subscribers
wheel_radius =  0.028
wheel_distance = 0.33

right_wheel_rpm = 0
left_wheel_rpm = 0


def right_wheel_rpm_callback(msg):
    global right_wheel_rpm
    right_wheel_rpm = msg.data


def left_wheel_rpm_callback(msg):
    global left_wheel_rpm
    left_wheel_rpm = msg.data


# Initialize the node
rospy.init_node('odometry_listener')

# Set up the subscribers
rospy.Subscriber('/right_wheel_rpm', Float32, right_wheel_rpm_callback)
rospy.Subscriber('/left_wheel_rpm', Float32, left_wheel_rpm_callback)

# Set up the publisher
odom_pub = rospy.Publisher('/odom', Odometry, queue_size=5)

# Set the publishing rate
rate = rospy.Rate(120)  # 10Hz

# Initialize the odometry message
odom = Odometry()

# Set the frame IDs for the message
odom.header.frame_id = 'odom'
odom.child_frame_id = 'base_link'

# Initialize the position and velocity variables
x = 0.0
y = 0.0
theta = 0.0
vx = 0.0
vy = 0.0
vtheta = 0.0

# Set the initial time for the message
odom.header.stamp = rospy.Time.now()

# Start the main loop
while not rospy.is_shutdown():
    # Update the time for the message
    current_time = rospy.Time.now()
    dt = (current_time - odom.header.stamp).to_sec()
    odom.header.stamp = current_time

    # Compute the linear and angular velocities
    vr = (right_wheel_rpm * 2 * pi) / 60
    vl = (left_wheel_rpm * 2 * pi) / 60

    vx = ((vr + vl) * wheel_radius) / 2.0
    vtheta = ((vr - vl) * wheel_radius) / wheel_distance

    # Update the position and orientation
    x += vx * dt * cos(theta)
    y += vx * dt * sin(theta)
    theta += vtheta * dt

    # Populate the odometry message
    odom.pose.pose.position.x = x
    odom.pose.pose.position.y = y
    odom.pose.pose.position.z = 0.0
    odom.pose.pose.orientation.w = cos(theta / 2.0)
    odom.pose.pose.orientation.x = 0.0
    odom.pose.pose.orientation.y = 0.0
    odom.pose.pose.orientation.z = sin(theta / 2.0)
    odom.twist.twist.linear.x = vx
    odom.twist.twist.linear.y = vy
    odom.twist.twist.angular.z = vtheta

    # Publish the odometry message
    odom_pub.publish(odom)

    # Sleep to maintain the publishing rate
    rate.sleep()
