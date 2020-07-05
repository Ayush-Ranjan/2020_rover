#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from std_msgs.msg import Float64
import math
speed=0
angvel=0
def threadforCall():
    rospy.Subscriber("cmd_vel", Twist, callback)
    #rospy.spin()
def callback(data):
    global speed, angvel
    vel_msg=data
    speed = vel_msg.linear.x
    angvel = vel_msg.angular.z*(math.pi)/90.0
    #print(speed)
def moveForward():
    #Starts a new node
    #Receiveing the user's input
    global speed,angvel
    lm=rospy.Publisher('/rover/bogie_left_wheel_lm_controller/command',Float64,queue_size=10)
    lf=rospy.Publisher('/rover/corner_lf_wheel_lf_controller/command',Float64,queue_size=10)
    rm=rospy.Publisher('/rover/bogie_right_wheel_rm_controller/command',Float64,queue_size=10)
    rf=rospy.Publisher('/rover/corner_rf_wheel_rf_controller/command',Float64,queue_size=10)
    lb=rospy.Publisher('/rover/corner_lb_wheel_lb_controller/command',Float64,queue_size=10)
    rb=rospy.Publisher('/rover/corner_rb_wheel_rb_controller/command',Float64,queue_size=10)
    sep=0.3;
    omega = 50*angvel;	
    a=speed+ omega*sep/2;
    lf.publish(a);
    lm.publish(a);
    lb.publish(a);
    a=-(speed- omega*sep/2);
    rb.publish(a);
    rm.publish(a);
    rf.publish(a);
    #@staticmethod
def turn():
    global angvel
    angrb=rospy.Publisher('/rover/rocker_right_corner_rb_controller/command',Float64,queue_size=10)
    anglb=rospy.Publisher('/rover/rocker_left_corner_lb_controller/command',Float64,queue_size=10)
    anglf=rospy.Publisher('/rover/bogie_left_corner_lf_controller/command',Float64,queue_size=10)
    angrf=rospy.Publisher('/rover/bogie_right_corner_rf_controller/command',Float64,queue_size=10)
    angrb.publish(angvel)
    anglb.publish(angvel)
    angrf.publish(angvel)
    anglf.publish(angvel)
if __name__ == '__main__':
    rospy.init_node('mover', anonymous=True)
    try:
        print("Let's move our rover")
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            #Testing our function
            threadforCall()
            moveForward()
            #turn()
            rate.sleep()
    except rospy.ROSInterruptException: pass
