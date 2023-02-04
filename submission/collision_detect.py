import picar_4wd as fc
import time
speed = 10

def get_obstacle_direction(scan_list):
    """
    get the direction of the obstacle

    Args:
        scan_list (list) : list containing the information about obstructing objects

    Return:
        string: string giving the direction 
    """_

    mid = int(len(scan_list)/2)

    if max(scan_list[0:mid]) > min(scan_list[mid:]):
        return "right"
    elif min(scan_list[0:mid]) < max(scan_list[mid:]):
        return "left"
    else:
        return None
   


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
                    fc.turn_right(speed)

                elif dir_obs == "right" :
                    print("turn left")
                    fc.turn_left(speed)

            else:
                fc.forward(speed)
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