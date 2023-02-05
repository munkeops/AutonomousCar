
import picar_4wd as fc
import time
from test_server import server
import threading , queue
import atexit
speed = 10

from mapping import *

steps_to_reach = 24
cur_dir = "west"
target_dir = "north"
directions = ['north', 'east', 'south', 'west']
person_detected = False
stop_sign_used = False

def move(direction):        
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

    print("Current Direction: ", cur_dir)
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
        scan_list = fc.scan_step(15)
        if not scan_list:
            continue

        time.sleep(.1)

        if steps_to_reach == 0:
            continue

        print("Steps left: ", steps_to_reach)
        # move('right')
        # time.sleep(1)
        # move('left')
        # time.sleep(1)
        # continue

        print(len(scan_list))
        tmp = scan_list[2:-2]
        print(tmp)
        if not person_detected:

            try:
                if tmp != [2,2,2,2,2,2]:
                    dir_obs = get_obstacle_direction(tmp)
                    print("object is at :", dir_obs)
                    if dir_obs == "left":
                        print("turn right")
                        move('right')                    
                        
                    elif dir_obs == "right" :
                        print("turn left")
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
                        else:                        
                            print("move forward")

                    move('forward')
            except:
                pass    

        last_val = None
        while(not que.empty()):
            last_val = que.get()

        if last_val != None and last_val[0]:
            last_val = last_val[0]
        
        if last_val and last_val.score > 0.5:

            print('Object Detected: ', last_val.category_name, last_val.score)

            if 'person' in last_val.category_name:
                person_detected = True
                fc.stop()
                time.sleep(2)
                
            elif 'stop' in last_val.category_name and stop_sign_used == False:
                fc.stop()
                stop_sign_used = True
                time.sleep(5)

            else:
                person_detected = False
        else:
            person_detected = False

        # print(last_val) 
                        


if __name__ == "__main__":
    try: 
        q = queue.Queue()
        msg =  None
        thread1 = threading.Thread(target=main,args=(q,))
        thread2 = threading.Thread(target=server,args=(q,))
        # main()
        print("setup")
        thread1.start()
        thread2.start()

        atexit.register(lambda: fc.stop())
    
    finally: 
        fc.stop()