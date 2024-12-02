#!/usr/bin/python3

import rospy
import tf
from nav_msgs.msg import Odometry

def odom_callback(msg):
    # Extract the position and orientation from the Odometry message
    position = msg.pose.pose.position
    orientation = msg.pose.pose.orientation
    
    # Create a tuple for the translation
    translation = (position.x, position.y, position.z)
    
    # Create a tuple for the orientation as a quaternion
    orientation_quat = (orientation.x, orientation.y, orientation.z, orientation.w)
    
    # Create a transform with the translation and orientation
    transform = tf.TransformerROS().fromTranslationRotation(translation, orientation_quat)
    
    # Broadcast the transform
    br = tf.TransformBroadcaster()
    br.sendTransform((position.x, position.y, position.z),
                     (orientation.x, orientation.y, orientation.z, orientation.w),
                     rospy.Time.now(),
                     "base_link",
                     "odom")

if __name__ == '__main__':
    rospy.init_node('odom_transformer')
    rospy.Subscriber("odom", Odometry, odom_callback)
    rospy.spin()
