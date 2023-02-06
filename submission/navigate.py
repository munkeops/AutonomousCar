
import picar_4wd as fc
import time
from test_server import server
import threading , queue
import atexit
speed = 10

from mapping import *

steps_to_reach = 16
cur_dir = "west"
target_dir = "north"
directions = ['north', 'east', 'south', 'west']
person_detected = False
stop_sign_used = False
speed = 10
dim = 15
default_map =  np.zeros((dim, dim))

def move(direction):  
    """wrapper method for moving front, left and right based on precalibrated time values for a perfect rotation

    Args:
        direction (string): direction to move in
    """


    global cur_dir, steps_to_reach

    if direction == 'forward':
        fc.forward(speed)
        time.sleep(.35)

        if cur_dir == target_dir:
            steps_to_reach -= 1
        
    elif direction == 'left':
        fc.turn_left(speed)
        time.sleep(1.4)

        i = directions.index(cur_dir)
        cur_dir = directions[3 if i == 0 else i - 1]        
        
    elif direction == 'right':
        fc.turn_right(speed)
        time.sleep(1.05)

        i = directions.index(cur_dir)
        cur_dir = directions[0 if i == 3 else i + 1]

    fc.forward(0)

def get_obstacle_direction(scan_list):
    """
    get the direction of the obstacle

    Args:
        scan_list (list) : list containing the information about obstructing objects

    Return:
        string: string giving the direction 
    """

    mid = int(len(scan_list)/2)

    if scan_list[mid] < 2:
        return "forward"
    elif max(scan_list[0:mid]) > min(scan_list[mid:]):
        return "right"
    elif min(scan_list[0:mid]) < max(scan_list[mid:]):
        return "left"
    else:
        return "forward"
   

def main(que):
    global cur_dir, target_dir, steps_to_reach, person_detected, stop_sign_used

    while True:
        ref = 15

        scan_list_d = fc.scan_step_dist(ref)

        if not scan_list_d:
            continue

        mapping(scan_list_d)
        scan_list = []

        current_angle = 0
        for dist in scan_list_d:
            status = fc.get_status_at(dist,current_angle, ref1=ref)#ref1
            current_angle = current_angle + 18
            scan_list.append(status)

        time.sleep(.1)

        if steps_to_reach == 0:
            continue

        tmp = scan_list[2:-2]
        if not person_detected:

            try:
                if tmp != [2,2,2,2,2,2]:
                    dir_obs = get_obstacle_direction(tmp)
                    # print("object is at :", dir_obs)
                    if dir_obs == "left":
                        # print("turn right")
                        move('right')                    
                        
                    elif dir_obs == "right" :
                        # print("turn left")
                        move('left')                    

                    else:
                        if target_dir == 'north':
                            if cur_dir == 'east':
                                move('left')
                            elif cur_dir == 'west':
                                move('right')
                            else:
                                move('right')
                    
                    move('forward')
                    move('forward')
                    move('forward')
                else:

                    if target_dir == 'north':
                        if cur_dir == 'east':
                            move('left')
                            move('forward')
                        elif cur_dir == 'west':
                            move('right')
                            move('forward')                      
                        # else:                        
                            # print("move forward")

                    move('forward')
            except:
                pass    

        ######################## sampling video data ##############################


        last_val = None
        # read the queue until the last recorded value in order to make sure we are processing in real time
        while(not que.empty()):
            last_val = que.get()

        if last_val != None and last_val[0]:
            last_val = last_val[0]
        
        if last_val and last_val.score > 0.5:

            # stop indefinitely until the person moves and we are sure we can proceeed
            if 'person' in last_val.category_name:
                person_detected = True
                fc.stop()
                time.sleep(2)

            
            # stop for 5 seconds and then proceed cautiously without colliding                
            elif 'stop' in last_val.category_name and stop_sign_used == False:
                fc.stop()
                stop_sign_used = True
                time.sleep(5)

            else:
                person_detected = False
        else:
            person_detected = False

                        


if __name__ == "__main__":
    try: 
        q = queue.Queue()
        msg =  None
        thread1 = threading.Thread(target=main,args=(q,))
        thread2 = threading.Thread(target=server,args=(q,))
        print("setup")
        thread1.start()
        thread2.start()

        atexit.register(lambda: fc.stop())
    
    finally: 
        fc.stop()