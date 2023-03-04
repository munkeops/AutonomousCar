
import picar_4wd as fc
from flask import Flask, request, jsonify
import threading

from flask_cors import CORS
import time

# , cv2


# from flaskapp.views import *
# from flaskapp import app

app = Flask(__name__)
CORS(app)

action =  None
old_action = None
power_val = 50

@app.route("/actions", methods = ["POST", "GET"])
def actions_on():
    global action
    global old_action

    print(request.form)

    action = request.form["action"]
    time.sleep(0.5)
    old_action = action
    data = {"status":action}
    return jsonify(data)

    
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


def run_flask():
    app.run(port=6001,host = "0.0.0.0", debug=False)


if __name__ == '__main__':
    th = threading.Thread(target=run_flask)
    th.daemon = True
    th.start()    

    # render_video()
    Keyborad_control()