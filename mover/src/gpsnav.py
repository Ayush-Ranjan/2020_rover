#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
from sensor_msgs import NavSatFix
from pyproj import Proj
import math
import utm
dest_x,dest_y,curr_x,curr_y,curr_pos_x,curr_pos_y
#myProj = Proj("+proj=utm +zone=23K, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
def threadForCall():    
    rospy.Subscriber("desired_point_gps",NavSatFix,dp);
    rospy.Subscriber("fix",NavSatFix,cp);
    rospy.Subscriber("odom",Odometry,curr_pos);
def dp(data):
    global dest_x, dest_y
    dest_lat=data.latitude
    dest_lon=data.longitude
    #dest_x, dest_y=myProj(dest_lon,dest_lat)
    dest_x, dest_y=utm.from_latlon(dest_lat,dest_lon)
def cp(data):
    global curr_x, curr_y
    curr_lat_x=data.latitude
    curr_lon=data.longitude
    #curr_x, curr_y=myProj(curr_lon,curr_lat)
    dest_x, dest_y=myProj(dest_lon,dest_lat)
def curr_pos(data):
    global curr_pos_x, curr_pos_y
    msg=data
    curr_pos_x= msg.pose.pose.position.x
    curr_pos_y= msg.pose.pose.position.y
def give():
    global dest_x,dest_y,curr_x,curr_y,curr_pos_x,curr_pos_y
    director=rospy.Publisher('cmd_pose',Pose,queue_size=10)
    reach_x=dest_x-curr_x+curr_pos_x
    reach_y=dest_y-curr_y+curr_pos_y 
    final=Pose()
    final.position.x= reach_x
    final.position.y= reach_y
    diector.publish(final)
if __name__ == '__main__':
    rospy.init_node('pos_move', anonymous=True)
    try:
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
	    threadForCall()
            give()
            rate.sleep()
    except rospy.ROSInterruptException: pass
