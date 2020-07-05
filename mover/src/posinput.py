#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Pose
from std_msgs.msg import Float64
def inputVals():
    inputer=rospy.Publisher('cmd_pose',Pose,queue_size=10)
    print("Enter the x")
    inpos=Pose()
    inpos.position.x=int(raw_input())
    print("Enter the y")
    inpos.position.y=int(raw_input())
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        inputer.publish(inpos)
        rate.sleep()
if __name__ == '__main__':
    rospy.init_node('posinput',anonymous=True)
    try:
        #Testing our function
        inputVals()
    except rospy.ROSInterruptException: pass        
