#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
def inputVals():
    inputer=rospy.Publisher('cmd_vel',Twist,queue_size=100)
    print("Enter the velocity")
    invel=Twist()
    invel.linear.x=int(raw_input())
    invel.linear.y=0
    invel.linear.z=0
    invel.angular.y=0
    print("Enter the angular velocity")
    invel.angular.z=int(raw_input())
    invel.angular.x=0
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        inputer.publish(invel)
        rate.sleep()
if __name__ == '__main__':
    rospy.init_node('input',anonymous=True)
    try:
        #Testing our function
        inputVals()
    except rospy.ROSInterruptException: pass        
