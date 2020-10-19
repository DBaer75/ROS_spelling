#!/usr/bin/env python

#goal: 
#   take in a custom message on a service call
#   convert the message into a series of cmd_messages
#   publish to cmd_vel
#   subscribe and watch for collisions


#CustomServiceMessage information
    #string stringToDraw
    #---
    #bool success

#debugging print switches on 
debugOnSub = 0
debugOnTurn = 1

#throttle of how fast the program writes 0:1
speed = 0.5

import rospy
import time as t
import numpy as np
from custom_service_message_pkg.srv import CustomServiceMessage, CustomServiceMessageResponse
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import Empty

#variables to handle twist
tMsg = Twist()
tMsgList = []
currOdom = Odometry()

#create publisher
cmdPub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)


#variables to hold the position and orientatioin of the robot read from /odom
pos_x = 0.0
pos_y = 0.0
ang_z = 0.0
odom_cur = [pos_x, pos_y, ang_z]


def subCallback(data):
    global odom_cur
    global currOdom
    currOdom = data
    odom_cur[0] = data.pose.pose.position.x
    odom_cur[1] = data.pose.pose.position.y
    quat_x = data.pose.pose.orientation.x
    quat_y = data.pose.pose.orientation.y
    quat_z = data.pose.pose.orientation.z
    quat_w = data.pose.pose.orientation.w

    #convert quarterion orientation to radians. This math is heavily based on example C code given on the wiki article for quaterions.
    anglerad = np.arctan2(2 * (quat_w * quat_z + quat_x * quat_y),1 - 2 * (quat_y * quat_y + quat_z * quat_z))
    odom_cur[2] = anglerad #follows right hand rule. ie x+ is 0, y+ is pi/2

    if (debugOnSub):
        print("pos_x = " + str(odom_cur[0]))
        print("pos_y = " + str(odom_cur[1]))
        print("ang_z = " + str(odom_cur[2]))
        #t.sleep(0.5)
    


def stopRobot():
    global tMsg
    tMsg = Twist()
    cmdPub.publish(tMsg)
    return

def turnRobot(degreeRequest):
    #turns robot to a specific degree orientation
    #degrees from 180 to -180 with 
    #   x+ = 0
    #   y+ = 90
    global tMsg
    global odom_cur
    global currOdom
    radR = degreeRequest*(np.pi/180) #convert to rad
    radC = odom_cur[2]
    if (debugOnTurn):
        print("radR = " + str(radR) + "radC = " + str(radC))

    while ((radR-radC)>(np.pi/90)): 
        tMsg.angular.z = speed
        print("radR = " + str(radR) + "radC = " + str(radC))
        cmdPub.publish(tMsg)
        subCallback(currOdom)
    while ((radR-radC)<(np.pi/90)): 
        tMsg.angular.z = -speed
        print("radR = " + str(radR) + "radC = " + str(radC))
        cmdPub.publish(tMsg)
        subCallback(currOdom)
    #cmdPub.publish(tMsg)
    return 

def moveUpRight(distance):
    #turn right
    global speed
    global odom_cur
    global tMsg

    stopRobot()
    turnRobot(45)
    #stopRobot()
    t.sleep(5)
    start_location = [odom_cur[0],odom_cur[1]]

    #tMsg.linear.x = speed
    #cmdPub.publish(tMsg)
    #while 

def letterPrint(letter):
    print("letterPrint called")
    #all letters will be printed in caps and "BLOCKLETTER" font
    if ((letter=='a') or (letter=='A')):
        moveUpRight(0.5)
    #    moveDownRight()
    #    moveLeft()
    #    moveRight()
    #    moveDownRight()
    #    moveRight()
    return 1
    

        

successFail = 0
def serviceCallback(request):
    response = CustomServiceMessageResponse()
    for i in range(len(request.stringToDraw)):
        #iterate through string and build a list of vel commands to publish
        successFail = letterPrint(request.stringToDraw[i])
    response.success = successFail 
    return response           


#create service server node
rospy.init_node('robot_spell_server_node')
spell_service = rospy.Service('/spell_service', CustomServiceMessage, serviceCallback)

#create subscriber
poseSub = rospy.Subscriber('/odom', Odometry, subCallback)
rospy.spin() #keeps service open

