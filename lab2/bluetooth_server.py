"""
A simple Python script to receive messages from a client over
Bluetooth using Python sockets (with Python 3.3 or above).
"""
import picar_4wd as fc
# from flask import Flask, request, jsonify
import threading

# from flask_cors import CORS
import time
import socket

action =  None
old_action = None
power_val = 50

hostMACAddress =  "E4:5F:01:F5:A0:4B" # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 1 # 3 is an arbitrary choice. However, it must match the port used by the client.
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)

def bluetooth_server():
    global power_val
    global action
    global old_action
    try:
        client, address = s.accept()
        while 1:
            action = client.recv(size).decode()
            time.sleep(.5)
            if action:
                print(action)
                old_action = action
                client.send(str(action).encode())
    except Exception as e:	
        print("Closing socket")	
        print(e)
        client.close()
        s.close()


def Keyborad_control():
    while True:
        global power_val
        global action
        global old_action
        # key=readkey()
        key = action

        if key=='PH':
            if power_val <=90:
                power_val += 10
                print("power_val:",power_val)
                action=power_val
        elif key=='PL':
            if power_val >=10:
                power_val -= 10
                print("power_val:",power_val)
                action=power_val
        if key=='forward':
            fc.forward(power_val)
        elif key=='left':
            fc.turn_left(power_val)
            time.sleep(0.2)
            # action = "forward"
            if(old_action == "forward"):
                fc.forward(power_val)
                action = "forward"

            if(old_action=="backward"):
                fc.backward(power_val)
                action = "backward"

        elif key=='backward':
            fc.backward(power_val)
        elif key=='right':
            fc.turn_right(power_val)
            time.sleep(0.2)
            # action = "forward"
            if(old_action == "forward"):
                fc.forward(power_val)
                action = "forward"

            if(old_action=="backward"):
                fc.backward(power_val)
                action = "backward"
        else:
            fc.stop()
        if key=='q':
            print("quit")  
            break  

if __name__ == '__main__':
    th = threading.Thread(target=bluetooth_server)
    th.daemon = True
    th.start()    

    # render_video()
    Keyborad_control()