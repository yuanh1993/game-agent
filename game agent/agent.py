#####################################################################################################
# For this agent, we creat a map struct to keep all place that we see. and a gamer class to record  #
# what do we have, and how many. In the strategy we make the agent to travel all the map by deep    #
# first. when it's done if we know the treasure we get a road to it, else, we see if we have tree   #
# or stone to go some where else. By the path find we have a start search to get the shorest road   #
# and if we have any block we can solve it, in find_trouble function. and we also have a functuon   #
# to help us choose stones that will give us best choice of where to put, even we have two choice   #
# when the agent get treasure, it will calculate the road to get back and find what it needs.       #
# when the agent on a reft i will find tree and make sure that it can go back then get on the island#
# however we don't know to pervent tcp not recive data, so we just make the thread sleep for a while#
#####################################################################################################

import sys
import socket
from map import *
from game import *
from strategy import *
import time
# declaring visible grid to agent
view = [['' for _ in range(5)] for _ in range(5)]

# function to take get action from AI or user
def get_action(view):

    ## REPLACE THIS WITH AI CODE TO CHOOSE ACTION ##

    # input loop to take input from user (only returns if this is valid)
    while 1:
        inp = input("Enter Action(s): ")
        inp.strip()
        final_string = ''
        for char in inp:
            if char in ['f','l','r','c','u','b','F','L','R','C','U','B']:
                final_string += char
                if final_string:
                     return final_string[0]

# helper function to print the grid
def print_grid(view):
    print('+-----+')
    for ln in view:
        print("|"+str(ln[0])+str(ln[1])+str(ln[2])+str(ln[3])+str(ln[4])+"|")
    print('+-----+')

def regulate_view(view,face):
    if face == "N":
        return view
    else:
        # create a temp view
        turned_map = []
        for i in range(5):
            turned_map.append([-1]*5)
        if face == 'W':
            for i in range(len(view)):
                for j in range(len(view[i])):
                    turned_map[i][j] = view[j][4-i]
        elif face == "S":
            for i in range(len(view)):
                for j in range(len(view[i])):
                    turned_map[i][j] = view[4-i][4-j]
        else:
            for i in range(len(view)):
                for j in range(len(view[i])):
                    turned_map[i][j] = view[4-j][i]
        return turned_map
def updat_pos(face,pos):
    if face =='N':
        return (pos[0]-1,pos[1])
    if face =='E':
        return (pos[0],pos[1]+1)
    if face =='S':
        return (pos[0]+1,pos[1])
    if face == 'W':
        return (pos[0],pos[1]-1)
def turn_face(face,action):
    if face == 'N':
        if action =='R':
            return 'E'
        else:
            return 'W'
    elif face == 'W':
        if action =='R':
            return 'N'
        else:
            return 'S'
    elif face == 'S':
        if action =='R':
            return 'W'
        else:
            return 'E'
    elif face == 'E':
        if action =='R':
            return 'S'
        else:
            return 'N'
if __name__ == "__main__":

    # checks for correct amount of arguments
    if len(sys.argv) != 3:
        print("Usage Python3 "+sys.argv[0]+" -p port \n")
        sys.exit(1)

    port = int(sys.argv[2])

    # checking for valid port number
    if not 1025 <= port <= 65535:
        print('Incorrect port number')
        sys.exit()

    # creates TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
         # tries to connect to host
         # requires host is running before agent
         sock.connect(('localhost',port))
    except (ConnectionRefusedError):
         print('Connection refused, check host is running')
         sys.exit()

    # navigates through grid with input stream of data
    i=0
    j=0
    play_agent = gamer()
    action=None
    graph=map()
    st = Strategy()
    while 1:
        data=sock.recv(100)
        if not data:
            exit()
        for ch in data:
            if (i==2 and j==2):
                view[i][j] = '^'
                view[i][j+1] = chr(ch)
                j+=1
            else:
                view[i][j] = chr(ch)
            j+=1
            if j>4:
                j=0
                i=(i+1)%5
        if j==0 and i==0:
            if action =='F'or action==None:
                temp=regulate_view(view,play_agent.face)
                graph.refrsh_map(temp,play_agent.face,play_agent.position,action)
            graph.map_printer()
            print(action)
            print(st.target)
            print_grid(view) # COMMENT THIS OUT ON SUBMISSION
            # action = get_action(view) # gets new actions
            action = st.play(play_agent,graph)
            if action=='F':
                play_agent.position=updat_pos(play_agent.face,play_agent.position)
            if action == 'L' or action =='R':
                play_agent.face=turn_face(play_agent.face,action)
            print(st.decision)
            sock.send(action.encode('utf-8'))
            time.sleep(0.005)
    sock.close()
