import picar_4wd as fc
import time
speed = 10

cur_dir = "north"
target_dir = "north"

def move(direction):
    
    if direction == 'forward':
        fc.forward(speed)
        time.sleep(1)
        
    elif direction == 'left':
        fc.turn_left(speed)
        time.sleep(1.6)
        
    elif direction == 'right':
        fc.turn_right(speed)
        time.sleep(1.25)
        
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
   


def main():
    while True:
        scan_list = fc.scan_step(25)
        if not scan_list:
            continue

        time.sleep(.1)

        print(len(scan_list))
        tmp = scan_list[2:-2]
        print(tmp)
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

                    move('right')
            else:
                move('forward')
                print("move forward")
        except:
            pass

        time.sleep(.5)
        fc.forward(0)


if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()