import picar_4wd as fc
import time
import math
import numpy as np
from pprint import pprint
speed = 10

dim = 15
default_map =  np.zeros((dim, dim))
cur_dir = "north"
target_dir = "north"

def move(direction):
    
    if direction == 'forward':
        fc.forward(speed)
        time.sleep(2)
        
    elif direction == 'left':
        fc.turn_left(speed)
        time.sleep(1.8)
        
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

    if max(scan_list[0:mid]) > min(scan_list[mid:]):
        return "right"
    elif min(scan_list[0:mid]) < max(scan_list[mid:]):
        return "left"
    else:
        return None


def mark_object(dmap,coord):

    dim = len(dmap[0])
    x = coord[0]+int(dim/2)
    y = coord[1]+int(dim/2)

    

    if (x<dim and y<dim and coord[0]!=0 and coord[1]!=0):
        dmap[dim-1-y][x]=1


def check_coord(dmap,coord):
    
    dim = len(dmap[0])
    x = coord[0]+int(dim/2)
    y = coord[1]+int(dim/2)

    

    if (x<dim and y<dim and coord[0]!=0 and coord[1]!=0):
        return dmap[dim-1-y][x]
    else:
        return -1
        


def draw_map(default_map,coords_list):

    # default_row = [0]*25
    # default_map = [default_row*25]

    # dim = 15
    # default_map =  np.zeros((dim, dim))

    # print("coords_list")
    # print(coords_list)

    # mark_object(default_map,coords_list)

    buffer = 0
    coords_list_variant=[]
    for buff in range(0,buffer+1):
        coords_list_variant += [
                [coords_list[0],coords_list[1]+buff],
                [coords_list[0]+buff,coords_list[1]],
                [coords_list[0]-buff,coords_list[1]],
                [coords_list[0],coords_list[1]-buff],
                [coords_list[0]-buff,coords_list[1]-buff],
                [coords_list[0]+buff,coords_list[1]-buff],
                [coords_list[0]-buff,coords_list[1]+buff],
                [coords_list[0]+buff,coords_list[1]+buff],
        ]

    for coord in coords_list_variant:
        try:
            mark_object(default_map,coord)

        except Exception as e:
            print(e)
   

    # print(default_map)
    
def draw_map_2(default_map,coords_list):

    buffer = 1
    # coords_list[7] = [0,0]


    mark_object(default_map,coords_list)
    coords_list_variant=[]
    for buff in range(0,buffer+1):
        coords_list_variant += [
                [coords_list[0],coords_list[1]+buff],
                [coords_list[0]+buff,coords_list[1]],
                [coords_list[0]-buff,coords_list[1]],
                [coords_list[0],coords_list[1]-buff],
                [coords_list[0]-buff,coords_list[1]-buff],
                [coords_list[0]+buff,coords_list[1]-buff],
                [coords_list[0]-buff,coords_list[1]+buff],
                [coords_list[0]+buff,coords_list[1]+buff],
        ]

    flag = False
    for coord in coords_list_variant:
        try:
            val = check_coord(default_map,coord)
            if val == 1:
                flag = True
                break


        except Exception as e:
            print(e)

    # flag = False

    if flag:
        for coord in coords_list_variant:
            try:
                mark_object(default_map,coord)

            except Exception as e:
                print(e)
   


def main():
    while True:
        scan_list = fc.scan_step_dist(25)
        default_map =  np.zeros((dim, dim))
        # scan_list = fc.scan_step(25)


        # scan_list=[2,2,2,2,2,2,2,2,2,2]

        if not scan_list:
            continue

        print(scan_list)
        


        # print(scan_list)
        scan_list_dist=[]
        for angle in range(len(scan_list)):
            # print(angle*18)
            dist = scan_list[angle]
            if(dist<0):
                dist = 0
            x= -int(dist*math.cos(math.pi*0.1*angle))
            y= int(dist*math.sin(math.pi*0.1*angle))

            x_sub=int(x/5)
            y_sub=int(y/5)

           
            scan_list_dist.append([x,y])
            draw_map_2(default_map,[x_sub,y_sub])
        
        print(scan_list_dist)
        print("\n")

        print(default_map)



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
                move('forward')
                print("move forward")
        except:
            pass

        # time.sleep(.5)
        # fc.forward(0)


if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()