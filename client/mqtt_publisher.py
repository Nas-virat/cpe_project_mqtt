import paho.mqtt.client as mqtt
import os
import socket
import random
from sensor import *
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv('HOST_MQTT')

class mqtt_publisher:
    
    def __init__(self,nodeID,host,port=1883):
        self.nodeID = nodeID
        self.host = host
        self.port = port

        self.client = mqtt.Client()
        self.client.connect(self.host,self.port)
        self.client.publish("BROKER/LOGGING", f"Publisher {socket.gethostname()} with IP {socket.gethostbyname(socket.gethostname())} connected to broker")
        self.client.loop_start()
        
    def publish(self,topic,message):
        result, _ = self.client.publish(topic,message)
        if result == mqtt.MQTT_ERR_SUCCESS:
            print(f"Topic:'{topic}' Message:'{message}'")
        else:
            print(f"Failed to publish message to topic '{topic}': {mqtt.error_string(result)}")
        
    def read_sensor_data(self):
        # Client simultaneously reads all the sensors every 3 minutes
        for data in ReadSensor():
            Time = data[0]
            Humidity = data[1]
            Temp = data[2]
            Thermal = data[3]
            
            self.publish("SENSOR/HUMIDITY", self.nodeID+";"+str(Time)+";"+str(Humidity))
            self.publish("SENSOR/TEMP", self.nodeID+";"+str(Time)+";"+str(Temp))
            self.publish("SENSOR/THERMAL", self.nodeID+";"+str(Time)+";"+str(Thermal))   
            
    def disconnect(self):
        self.client.loop_stop()
        self.client.publish("BROKER/LOGGING", f"Publisher {socket.gethostname()} with IP {socket.gethostbyname(socket.gethostname())} disconnected from broker")
        self.client.disconnect()


if __name__ == "__main__":
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print("Your Computer Name is: " + hostname)
    print("Your Computer IP Address is: " + IPAddr)
    iot_id = input("Enter IoT Node ID (Blank to random): ")
    if iot_id == "" or not iot_id.isdigit() or len(iot_id) != 4:
        iot_id = str(random.randint(1000,9999))

    #eclipse mosquitto mqtt broker
    iot_node_1 = mqtt_publisher(iot_id, HOST, 1883)
    iot_node_1.read_sensor_data()
    iot_node_1.disconnect()
    
    

    
    
    
    







