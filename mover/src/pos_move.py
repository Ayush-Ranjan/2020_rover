#!/usr/bin/env python
import rospy
from squaternion import Quaternion
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
import tf
import math
dest_x,dest_y,curr_pos_x,curr_pos_y,eul,speed,angle
def threadForCall(data):    
    rospy.Subscriber("cmd_pose",Pose,dest);
    rospy.Subscriber("odom",Odometry,curr_pos);
def des(data):
    global dest_x, dest_y
    dest_x=data.position.x
    dest_y=data.position.y
def curr_pos(data):
    global curr_pos_x, curr_pos_y
    msg=data
    curr_pos_x= msg.pose.pose.position.x
    curr_pos_y= msg.pose.pose.position.y
    q=Quaternion(msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,msg.pose.pose.orientation.w)
    eul = q.to_euler(degrees=True)
def move():
    global dest_x,dest_y,curr_pos_x,curr_pos_y,eul,speed,angle
    director=rospy.Publisher('cmd_vel',Twist,queue_size=10)
    yaw=eul[2]
    dist = math.sqrt((dest_x-curr_pos_x)*(dest_x-curr_pos_x)+(dest_y-curr_pos_y)*(dest_y-curr_pos_y))
    angle=(yaw+math.atan((-1*dest_y-curr_pos_y)/(dest_x-curr_pos_x)))*180/math.pi
    angle2=0
    if(curr_pos_x-dest_x<0):
        if(yaw<0):
            angle=angle+180
        else
            angle=angle-180
    if(dist<0.3):
        speed=0
        angle=0
    else: 
        if(abs(angle)<4):
            speed=10*dist
            if(abs(angle)<2):
                angle2=0
                angle.data= 0
        else:
            speed=0;
            angle2=angle;
    ans=Twist()	
    ans.linear.x=speed;
    ans.angular.z=angle2;
    director.publish(ans) 	  
if __name__ == '__main__':
    rospy.init_node('pos_move', anonymous=True)
    try:
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
	    
            #Testing our function
            #turn()
            rate.sleep()
    except rospy.ROSInterruptException: pass
