#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
def move():
    # Starts a new node
    rospy.init_node('mover', anonymous=True)	
    lm=rospy.Publisher('/rover/bogie_left_wheel_lm_controller/command',Float64,queue_size=100)
    lf=rospy.Publisher('/rover/corner_lf_wheel_lf_controller/command',Float64,queue_size=100)
    rm=rospy.Publisher('/rover/bogie_right_wheel_rm_controller/command',Float64,queue_size=100)
    rf=rospy.Publisher('/rover/corner_rf_wheel_rf_controller/command',Float64,queue_size=100)
    lb=rospy.Publisher('/rover/corner_lb_wheel_lb_controller/command',Float64,queue_size=100)
    rb=rospy.Publisher('/rover/corner_rb_wheel_rb_controller/command',Float64,queue_size=100)
    #Receiveing the user's input
    print("Let's move our rover")
    distance = 3
    speed = 50	
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        #Setting the current time for distance calculus
        lm.publish(speed)
    	rf.publish(-1*speed)
    	lf.publish(speed)
    	rm.publish(-1*speed)
    	rb.publish(-1*speed)
    	lb.publish(speed)
   	rate.sleep()
if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass
