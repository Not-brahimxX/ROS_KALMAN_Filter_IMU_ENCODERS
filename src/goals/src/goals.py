#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped, Quaternion

class NavigationNode:
    def __init__(self):
        rospy.init_node('navigation_node')

        # Define goal points (replace these with your actual goal points)
        self.goal_points = [
            (0.8, -0.5 ,0, 1),    # Goal point 1 (pose_x, pose_y, orientation_z, orientation_w)
            (1.5, 0, -0.7, 0.72), 
            (0.8, 0.5, -1, 0), 
            (0.2, 0.0, -0.7, 0.7), 

   # Goal point 2 (pose_x, pose_y, orientation_z, orientation_w)
            # Add more goal points as needed
        ]
        self.current_goal_index = 0

        # Create action client for move_base
        self.move_base_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.move_base_client.wait_for_server()

    def send_goal(self, pose_x, pose_y, orientation_z, orientation_w):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()

        # Set position
        goal.target_pose.pose.position.x = pose_x
        goal.target_pose.pose.position.y = pose_y
        goal.target_pose.pose.position.z = 0.0  # Assuming z is 0 in pose

        # Set orientation
        quaternion = Quaternion()
        quaternion.z = orientation_z
        quaternion.w = orientation_w
        goal.target_pose.pose.orientation = quaternion

        # Send goal
        self.move_base_client.send_goal(goal)
        self.move_base_client.wait_for_result()

    def navigate(self):
        rospy.loginfo("Navigation started")

        while not rospy.is_shutdown() and self.current_goal_index < len(self.goal_points):
            pose_x, pose_y, orientation_z, orientation_w = self.goal_points[self.current_goal_index]
            rospy.loginfo(f"Sending goal: pose_x={pose_x}, pose_y={pose_y}, orientation_z={orientation_z}, orientation_w={orientation_w}")

            # Send goal point to move_base
            self.send_goal(pose_x, pose_y, orientation_z, orientation_w)

            # Move to next goal point
            self.current_goal_index += 1


        rospy.loginfo("Navigation completed")

if __name__ == '__main__':
    try:
        nav_node = NavigationNode()
        nav_node.navigate()
    except rospy.ROSInterruptException:
        rospy.logerr("ROS node interrupted.")

