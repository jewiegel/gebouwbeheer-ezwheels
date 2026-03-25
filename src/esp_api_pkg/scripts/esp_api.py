#!/usr/bin/env python3
import rospy
import requests
from std_msgs import String

def get_api_data():
    url = "http:///api/data"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            rospy.logerr(f"API fout: {response.status_code}")
            return None
    except Exception as e:
        rospy.logerr(f"Verbindingsfout: {e}")
        return None
    
def talker():
    pub = rospy.Publisher('api_data', String, queue_size=10)
    rospy.init_node('api_client_node', anonymous=True)
    rate = rospy.Rate(0.1) # Haal elke 10 seconden data op

    while not rospy.is_shutdown():
        data = get_api_data()
        if data:
            # We sturen de ruwe JSON als string door (voor het gemak)
            rospy.loginfo("Data opgehaald van API")
            pub.publish(str(data))
        
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass