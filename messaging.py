from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


import json


import os

# Load the endpoint from file
with open('/home/ec2-user/environment/endpoint.json') as json_file:  
    data = json.load(json_file)


deviceName = os.path.split(os.getcwd())[1]

# Set the destinationDeviceName depending on this deviceName
if deviceName == 'car1':
    destinationDeviceName = 'car2'
else:
    destinationDeviceName = 'car1'


subTopic = 'lab/messaging/' + deviceName
pubTopic = 'lab/messaging/' + destinationDeviceName
keyPath = 'private.pem.key'
certPath = 'certificate.pem.crt'
caPath = '/home/ec2-user/environment/root-CA.crt'
clientId = deviceName
host = data['endpointAddress']
port = 8883



myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(caPath, keyPath, certPath)
myAWSIoTMQTTClient.connect()





def customCallback (client, userdata, message):
    print("Received messsage : " + message.payload.decode() + " from topic " + message.topic) 






myAWSIoTMQTTClient.subscribe(subTopic, 1, customCallback)



def publishToIoTTopic(topic, payload):
    myAWSIoTMQTTClient.publish(topic, payload, 1)
   
    
    


# Infinite loop reading console input and publishing what it finds
while True:
    message = input('Enter a message on the next line to send to ' + pubTopic + ':\r\n')
    
    # Calling function to publish to IoT Topic
    publishToIoTTopic(pubTopic, message)
