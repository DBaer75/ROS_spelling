#!/usr/bin/env python

#goal: 
#   take in a custom message on a service call
#   convert the message into a series of cmd_messages
#   publish to cmd_vel
#   subscribe and watch for collisions


#customServiceMessage
#string stringToDraw
#---
#bool success


import rospy
from geometry_msgs.msg import Twist

tMsg = Twist()
tMsgList = []
def moveUp():

def moveUpRight():
    #turn right

def letter2TwistList(letter):
    #empty the list
    global tMsgList = list.clear()
    tMsgBuff = Twist()
    #all letters will be printed in caps and "BLOCKLETTER" font
    if ((letter=='a') or (letter=='A')):
        #list is format [twista, twistalength, twistb, twistblength]
        #twist length varies from 0 to 1 where 1 is the height of the letter block
        tMsgList = [moveUpRight(), 1, moveDownRight(), 0.5, moveLeft(), 0.4, moveRight(),0.4,moveDownRight(),0.5, moveRight(),0.2]

        


def spellCallback(request):
    for i in range(len(request.stringToDraw)):
        #iterate through string and build a list of vel commands to publish
        tmsg = letter2TwistList(request.stringToDraw[i])

        p


#create service server node
rospy.init_node('robot_spell_server_node')
spell_service = rospy.Service('/spell_service', customServiceMessage, spellCallback)
rospy.spin() #keeps service open

#create publisher
cmdPub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

