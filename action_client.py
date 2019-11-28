#!/usr/bin/env python
# license removed for brevity

import rospy

# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

import requests as reqs
import json
import sys  


def talker():
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1) # 10hz
    while not rospy.is_shutdown():
        url = 'http://nxcom.000webhostapp.com/data2robot.php?id=0' 
        response = reqs.get(url)        # To execute get request 
        #print(response.status_code)      To print http response code  
        text_received = response.text
        if (sys.getsizeof(text_received)<500):
           print(response.text)            # To print formatted JSON response
        

        if (response.text!="0" and sys.getsizeof(text_received)<500):
	    bad_chars = ['[', ']']
            for i in bad_chars : 
               text_received = text_received.replace(i, '')  
            # parse x:
	    y = json.loads(text_received)

	    # the result is a Python dictionary:
	    #print(y["x"])
            global x_val
            global y_val
            global w_val
            global z_val
            x_val = float(y["x"])
            y_val = float(y["y"])
            w_val = float(y["w"])
            z_val = float(y["z"])
            result = movebase_client()
            if result:
              rospy.loginfo("Goal execution done!")
        
        #hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(hello_str)
        rate.sleep()
        
        


def movebase_client():

   # Create an action client called "move_base" with action definition file "MoveBaseAction"
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
 
   # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()

   # Creates a new goal with the MoveBaseGoal constructor
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
   # Move 0.5 meters forward along the x axis of the "map" coordinate frame 
    goal.target_pose.pose.position.x = x_val
    # Move 0.5 meters forward along the x axis of the "map" coordinate frame 
    goal.target_pose.pose.position.y = y_val
   # No rotation of the mobile base frame w.r.t. map frame
    goal.target_pose.pose.orientation.w = w_val
    # No rotation of the mobile base frame w.r.t. map frame
    goal.target_pose.pose.orientation.z = z_val

   # Sends the goal to the action server.
    client.send_goal(goal)
   # Waits for the server to finish performing the action.
    wait = client.wait_for_result()
   # If the result doesn't arrive, assume the Server is not available
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
    # Result of executing the action
        return client.get_result()   

# If the python node is executed as main process (sourced directly)
if __name__ == '__main__':
    try:
       # Initializes a rospy node to let the SimpleActionClient publish and subscribe
        talker()
        
    except rospy.ROSInterruptException:
        pass

