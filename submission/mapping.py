import picar_4wd as fc
import time
import math
import numpy as np
from pprint import pprint

from test_server import server
import threading , queue


speed = 10
dim = 15 # dimension of the 2d map drawn
default_map =  np.zeros((dim, dim))  # default 2d map with all 0s

def mark_object(dmap,coord):
    """make the location of the object 1 where it is detected (based on coord)

    Args:
        dmap (numpy array): map to draw on
        coord (list): containing x,y
    """

    dim = len(dmap[0])

    # translate data for new origin (ultrasonic data origin is 7,7 in a 15,15 2d map, but arrays have origin at 0,0)
    x = coord[0]+int(dim/2)
    y = coord[1]+int(dim/2)

    if (x<dim and y<dim and coord[0]!=0 and coord[1]!=0 and x>0 and y>0):
        dmap[dim-1-y][x]=1


def check_coord(dmap,coord):
    """check if the location asked for has a 1 or a 0

    Args:
        dmap (numpy array ): mapt to draw on
        coord (list): containing x,y

    Returns:
        int: -1 - invalid input, else the value of the coord
    """
    
    dim = len(dmap[0])

    # translate data for new origin (ultrasonic data origin is 7,7 in a 15,15 2d map, but arrays have origin at 0,0)
    x = coord[0]+int(dim/2)
    y = coord[1]+int(dim/2)
    
    if (x<dim and y<dim and coord[0]!=0 and coord[1]!=0):
        return dmap[dim-1-y][x]
    else:
        return -1
        


def draw_map(default_map,coords_list):
    """draw coordinates on the map by marking them as 1 (and add buffer using logic one)

    Args:
        default_map (numpy array): the map on which to draw on
        coords_list (list): containing the x,y cordinates which need to be marked
    """


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

    # add basic padding to all points
    for coord in coords_list_variant:
        try:
            mark_object(default_map,coord)

        except Exception as e:
            # print(e)
            pass
   

    
def draw_map_2(default_map,coords_list):
    """draw coordinates on the map by marking them as 1 (and add buffer using logic two)

    Args:
        default_map (numpy array): the map on which to draw on
        coords_list (list): containing the x,y cordinates which need to be marked
    """

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

    # similar to DBScan algorithm where we merger coordinates that are close to each other and add a buffer around them
    for coord in coords_list_variant:
        try:
            val = check_coord(default_map,coord)
            if val == 1:
                flag = True
                break


        except Exception as e:
            # print(e)
            pass

    # flag = False

    if flag:
        for coord in coords_list_variant:
            try:
                mark_object(default_map,coord)

            except Exception as e:
                # print(e)
                pass
   
def mapping(scan_list):
    """draw the map based on input data

    Args:
        scan_list (list): list containing all the data sampled from the ultrasonic sensor with the distance data
    """

    # modified the picar code to return scan_list with distance instead of status
    scan_list_dist=[]
    for angle in range(len(scan_list)):
        dist = scan_list[angle]
        if(dist<0):
            dist = 0

        # extract x, y coordinate from the distance and angle information
        x= -int(dist*math.cos(math.pi*0.1*angle))   # flip sign as angle is calculated from 2pi/3
        y= int(dist*math.sin(math.pi*0.1*angle))

        # increase the resolution by shrinking far away data by 2 (eg object at 60, will show 30)
        x_sub=int(x/2)
        y_sub=int(y/2)

        # store the coordinates
        scan_list_dist.append([x,y])

        # draw on map with the coordinates
        draw_map_2(default_map,[x_sub,y_sub])
    
    print("\n")

    # print map generated
    print(default_map)

def main(que):
    while True:
        scan_list = fc.scan_step_dist(25)
        default_map =  np.zeros((dim, dim))

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
        scan_list_status = []

        current_angle = 0
        ref = 15
        for dist in scan_list:
            status = fc.get_status_at(dist,current_angle, ref1=ref)#ref1
            current_angle = current_angle + 18
            scan_list_status.append(status)

        print(scan_list_status)

        print(default_map)

        last_val = None
        while(not que.empty()):
            last_val = que.get()

        print(last_val)


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
    finally: 
        fc.stop()