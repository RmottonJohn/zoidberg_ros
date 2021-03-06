#!/usr/bin/env python
"""
Navigation node
===============
Combines avalible sensors to estimate current depth, heading and velocity.
"""

from __future__ import print_function, division
import roslib
roslib.load_manifest('zoidberg_ros')
import rospy
import time
import zoidberg_ros.msg
import std_msgs.msg
import sensor_msgs.msg

class Navigation:
    """Combine all navigation sensors into a single message"""
    def __init__(self):
        """Initialize an empty guidance node"""
        self.target_depth = None
        self.target_heading = None
        self.target_vx = None
        self.target_vy = None

        # channels to listen for instrument updates
        rospy.Subscriber("/depth", sensor_msgs.msg.FluidPressure,
                         self._set_curr_depth)
        rospy.Subscriber("/heading", std_msgs.msg.Float64,
                         self._set_curr_heading)

        # channels where guidance publishes control commands
        self.publisher = rospy.Publisher("/navigation",
                                          zoidberg_ros.msg.State,
                                          queue_size=10)

        # publish comand rate, Hertz
        self.rate = rospy.Rate(10)

        # initilize current state to nonsense values
        self.curr_depth = -9999
        self.curr_heading = -9999.
	self.curr_vx = -9999.
	self.curr_vy = -9999.

    def talker(self):
        """Publish most recent state estimate every 10 Hz"""
        while not rospy.is_shutdown():
            curr_nav = zoidberg_ros.msg.Navigation(depth=self.curr_depth,
                                                   heading=self.curr_heading,
                                                   vx=self.curr_vx,
                                                   vy=self.curr_vy)
            rospy.loginfo(curr_nav)
            self.publisher.publish(curr_nav)
            self.rate.sleep()

    def _set_curr_depth(self, curr_depth):
        """Set the current depth when it is published"""
        self.curr_depth = curr_depth.fluid_pressure

    def _set_curr_heading(self, curr_heading):
        """Set the current depth when it is published"""
        self.curr_heading = curr_heading.data

    def _set_curr_pose(self, dvl_output):
        """Set the current position, velocity and altitude from DVL"""
        pass

if __name__ == '__main__':
    rospy.init_node('navigation_node')
    server = Navigation()
    # this try block taken from rospy tutorials for talker.py
    try:
        server.talker()
    except rospy.ROSInterruptException:
        pass
