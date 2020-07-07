#!/usr/bin/env python
import rospy
import numpy as np
from Quat import *
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import tf
import math
dest_x=0
dest_y=0
curr_pos_x=0
curr_pos_y=0
eul=None
speed=0.0
angle=0.0
flag=False
index=0
angle_add=0
tic=0
flag1=False
def threadForCall():
    rospy.Subscriber("cmd_pose",Pose,dest);
    rospy.Subscriber("rover/odom",Odometry,curr_pos);
    rospy.Subscriber("rover/scan",LaserScan,scan)
def dest(data):
    global dest_x, dest_y
    dest_x=data.position.x
    dest_y=data.position.y
def curr_pos(data):
    global curr_pos_x, curr_pos_y,eul
    msg=data
    curr_pos_x= msg.pose.pose.position.x
    curr_pos_y= msg.pose.pose.position.y
    q=np.array([msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,msg.pose.pose.orientation.w])
    eul= Q2EA(q, EulerOrder="zyx", ignoreAllChk=True)[0]
def scan(data):
    global flag,angle_add,tic,flag1
    min= data.range_max
    j=0
    c=0
    for i in range(360):
        if(data.ranges[i]<min):
            flag=True
            j=i
            min=data.ranges[i]
            if(flag1==False):
                tic=rospy.get_time()
            flag1=True
    toc=rospy.get_time()
    #print("time",toc-tic)
    max=min
    for i in range(360):
        if(data.ranges[i]>max):
            max=data.ranges[i]
    mindis=360
    for i in range(360):
        if(data.ranges[i]==max):
            if(abs(i-180)<mindis):
                mindis=abs(i-180)
                c=i
    print("nearest",180-c)
    if(180-c>5):
        angle_add=(180-c)*data.angle_increment
def move():
    global dest_x,dest_y,curr_pos_x,curr_pos_y,eul,speed,angle,angle_add,flag
    director=rospy.Publisher('cmd_vel',Twist,queue_size=10)
    if eul is not None:
        yaw=eul[2]
        dist = math.sqrt((dest_x-curr_pos_x)*(dest_x-curr_pos_x)+(dest_y-curr_pos_y)*(dest_y-curr_pos_y))
        angle=(yaw+math.atan((-1*dest_y-curr_pos_y)/(dest_x-curr_pos_x)))*180/math.pi
        angle2=0
        if(curr_pos_x-dest_x<0):
            if(yaw<0):
                angle=angle+180
            else:
                angle=angle-180
        if(dist<0.3):
            speed=0
            angle=0
        else:
            if(flag==True):
                angle=angle_add*36/math.pi#Here the values have been put by trial and error because I was unable to take the distance factor into account.
                speed=4#How to know distance from obstacle :( ?
                flag=False
                angle2=angle
            elif(abs(angle)<4):
                speed=10*dist
                if(abs(angle)<2):
                    angle2=0
                    angle= 0
            else:
                speed=5;
                angle2=angle;
        ans=Twist()
        ans.linear.x=speed;
        ans.angular.z=angle2;
        director.publish(ans)
        #print(angle)
if __name__ == '__main__':
    rospy.init_node('scanner', anonymous=True)
    try:
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
	    move()
            threadForCall()
            rate.sleep()
    except rospy.ROSInterruptException: pass
