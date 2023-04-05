# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd
import numpy as np


#TODO 1: modify the following parameters
#Starting and end index, modify this
device_st = 1
device_end = 2

#Path to the dataset, modify this
data_path = "vehicle{}.csv"

#Path to your certificates, modify this
certificate_formatter = "./certificates/device_{}/cert.pem"
key_formatter = "./certificates/device_{}/private.key"


class MQTTClient:
    def __init__(self, device_id, cert, key):
        # For certificate based connection
        self.device_id = str(device_id)
        self.state = 0
        self.client = AWSIoTMQTTClient(self.device_id)
        #TODO 2: modify your broker address
        self.client.configureEndpoint("a15ur3upsc9do2-ats.iot.us-east-1.amazonaws.com", 8883)
        self.client.configureCredentials("root_ca.pem", key, cert)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec
        self.client.onMessage = self.customOnMessage
        

    def customOnMessage(self,message):
        #TODO3: fill in the function to show your received message
        print("client {} received payload {} from topic {}".format(self.device_id, message.payload, message.topic))


    # Suback callback
    def customSubackCallback(self,mid, data):
        #You don't need to write anything here
        pass


    # Puback callback
    def customPubackCallback(self,mid):
        #You don't need to write anything here
        pass


    def publish(self, payload="payload"):
        #TODO4: fill in this function for your publish
        self.client.subscribeAsync("vehicle/emission", 0, ackCallback=self.customSubackCallback)
        
        self.client.publishAsync("vehicle/emission", json.dumps(payload), 0, ackCallback=self.customPubackCallback)



print("Loading vehicle data...")
data = []
for i in range(1):
    a = pd.read_csv(data_path.format(i))    
    data.append(a)

print("Initializing MQTTClients...")
clients = []
for device_id in range(device_st, device_end):
    client = MQTTClient(device_id,certificate_formatter.format(device_id,device_id) ,key_formatter.format(device_id,device_id))
    client.client.connect()
    clients.append(client)
 

while True:
    print("send now?")
    x = input()
    if x == "s":
        for i,c in enumerate(clients):
            c.publish({
                "id": i,
                "message": "payload"
            })

    elif x == "d":
        for c in clients:
            c.client.disconnect()
        print("All devices disconnected")
        exit()
    else:
        print("wrong key pressed")

    time.sleep(3)