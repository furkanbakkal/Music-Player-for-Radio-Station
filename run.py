#python3
from datetime import datetime
from pygame import mixer #pip3 install pygame
import pygame
import csv #pip3 install csv
import os
import time

# Starting the mixer
mixer.init()

MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)

screen = pygame.display.set_mode((1, 1))

mixer.music.set_volume(1)

start_time=["","","","",""]
playlist=["","","","",""]

comparator=[000000,999999,999999,999999,999999,999999]
path=None

def find_time():
    now = datetime.now()
    timer= (now.strftime("%H:%M:%S"))
    return timer
    

def first_start_time_comparator():
    global path

    curr_date=datetime.today().strftime("%A") #current date
   
    with open("time.csv","r") as f:
        csv_read=csv.reader(f)

        for line in csv_read:
            if line[0]==curr_date: #find starting time this day
                try:
                    data=line[1].split("-")
                    start_time[0]=data[0]
                    playlist[0]=data[1]

                    data=line[2].split("-")
                    start_time[1]=data[0]
                    playlist[1]=data[1]
        
                    data=line[3].split("-")
                    start_time[2]=data[0]
                    playlist[2]=data[1]

                    data=line[4].split("-")
                    start_time[3]=data[0]
                    playlist[3]=data[1]

                    data=line[5].split("-")
                    start_time[4]=data[0]
                    playlist[4]=data[1]

                except IndexError:
                    continue

        for i in range(5):

            try:
                data=start_time[i].split(":")
                comparator[i+1]=int(data[0]+data[1]+ data[2] )

            except IndexError:
                continue
        now = datetime.now()
        value= int(now.strftime("%H%M%S"))
        #print(comparator) 

        for i in range(5):
            try:
                if (comparator[i]<value) and (comparator[i+1]>value):
                    path=(playlist[i-1])

                    
                if path=="":
 
                    path=None
                    break

            except IndexError:
                continue        
        

#------------------------------------------------------------------------

def csv_read():
    global start_time, playlist

    curr_date=datetime.today().strftime("%A") #current date
    with open("time.csv","r") as f:
        csv_read=csv.reader(f)

        for line in csv_read:
            if line[0]==curr_date: #find starting time this day
                try:
                    data=line[1].split("-")
                    start_time[0]=data[0]
                    playlist[0]=data[1]

                    data=line[2].split("-")
                    start_time[1]=data[0]
                    playlist[1]=data[1]

                    data=line[3].split("-")
                    start_time[2]=data[0]
                    playlist[2]=data[1]

                    data=line[4].split("-")
                    start_time[3]=data[0]
                    playlist[3]=data[1]

                    data=line[5].split("-")
                    start_time[4]=data[0]
                    playlist[4]=data[1]

                except IndexError:
                    continue
#//////////////////////////////////////////////////////////

def music_play(music_path):
    global path, start_time, playlist, broker

    mixer.music.load(music_path) # Loading the song

    # Start playing the song
    mixer.music.play() 

    # infinite loop
    while True:
        csv_read() 
        now = datetime.now()
        curr_time = now.strftime("%H:%M:%S")

        for i in range(5):
            if (curr_time==start_time[i]): #start playing music at this time again 
                mixer.music.pause() 
                path=playlist[i]
                print("Folder changing to " + path +"-" + find_time())
                time.sleep(1)
                broker=True
                return 0

        for event in pygame.event.get():

            if event.type == MUSIC_END:
                print('Music ended - playing next one')
                return 0

############################################################################
    
settings = open("settings.log")
setting=settings.readline()

if setting=="repeat=on\n":
    repeat=True
    

if setting=="repeat=off\n":
    repeat=False

setting=settings.readline()

settings.close()

if setting=="resume=on":
    resume=True

if setting=="resume=off":
    resume=False
    queue=1

def wait_for_switch():
    global turn_back
    global path

    first_play=True
    print("Waiting for switch time...")
    while first_play:
        csv_read()      
        now = datetime.now()
        curr_time = now.strftime("%H:%M:%S")

        for i in range(5):
            if (curr_time==start_time[i]): #start playing music at this time again 
                path=playlist[i]
                print("Folder changing to " + path +"-" + find_time() )
                time.sleep(1)        
                first_play=False
                turn_back=False
                return 0


broker=False
turn_back=False
queue_counter=0
c=1

if resume:
    try:
        log1 = open("main.log")
        log=log1.readline()
        log=log.split("-")
        log1.close()

        path=log[0]
        queue=int(log[1])
        #print(queue)
        

        print("Log data accepted")
        #print("log date: "+ log[0])
        #print("log song: "+ log[1])

    except IndexError:
        print("Log is empty")
        queue=1

    except FileNotFoundError:
        print("Log file not found - Creating new one ")
        log = open("main.log", "w")
        queue=1

    c=queue

first_start_time_comparator()

if path==None:
    wait_for_switch()

while True:


    
    if ((turn_back and repeat==False) or (broker)):
  
        wait_for_switch()
                 
    now = datetime.now()
    curr_time = now.strftime("%H:%M:%S")

    for i in range(5):
        if (curr_time==start_time[i]): #start playing music at this time again 
            mixer.music.pause() 
            path=playlist[i]
            print("Folder changing to " + path +"-" + find_time() )
            time.sleep(1)
            break

    files=sorted(filter(lambda x: os.path.isfile(os.path.join(path, x)),os.listdir(path)))
 
    for file in files:  
        queue_counter=queue_counter+1  

        if queue_counter==c:
            log = open("main.log", "w")
            log.write(path+"-"+str(c))
            log.close()

            print("Now playing: " + path+"/"+file +"--" + find_time())
            music_play(path+"/"+file)

            c=c+1
            

            turn_back=True
            
            if broker:
                broker=False
                turn_back=False
                break
    c=1
    queue_counter=0



          