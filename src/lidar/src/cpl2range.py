#!/usr/bin/env python3

import rospy
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Header

def convert_pointcloud_to_laserscan(pointcloud_msg):
    # Create a LaserScan message
    laserscan_msg = LaserScan()

    # Set the header information
    laserscan_msg.header = Header()
    laserscan_msg.header.stamp = rospy.Time.now()
    laserscan_msg.header.frame_id = pointcloud_msg.header.frame_id

    # Set the LaserScan parameters
    laserscan_msg.angle_min = -1.57  # Minimum angle in radians
    laserscan_msg.angle_max = 1.57  # Maximum angle in radians
    laserscan_msg.angle_increment = 3.14 / pointcloud_msg.width  # Angular resolution in radians
    laserscan_msg.range_min = 0.0  # Minimum range value
    laserscan_msg.range_max = 100.0  # Maximum range value

    # Convert the point cloud to a list of tuples
    pointcloud_list = list(pc2.read_points(pointcloud_msg))

    # Convert the list of tuples to a list of ranges
    laserscan_msg.ranges = []
    for point in pointcloud_list:
        range_val = (point[0] ** 2 + point[1] ** 2 + point[2] ** 2) ** 0.5
        laserscan_msg.ranges.append(range_val)

    # Publish the LaserScan message
    laserscan_pub.publish(laserscan_msg)

if __name__=='__main__':
    rospy.init_node('pointcloud2range')
    laserscan_pub=rospy.Publisher('/laser_scan',LaserScan,queue_size=1)
    rospy.Subscriber('/point_cloud',pc2,convert_pointcloud_to_laserscan)
    rospy.spin()
