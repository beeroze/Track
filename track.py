from tkinter import *
from picamera import PiCamera
from time import sleep
from os import *
from PIL import Image,ImageTk
import os 
import wave
import time
import threading
import tkinter as tk
import pyaudio
import pygame
import random
import pygame.midi
import pygame.mixer
import pygame.time
import pygame.event
import pygame.display
import pygame.draw
import pygame.font
import pygame.image
import pygame.transform
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import sys

#Defining the main window
global root
root = Tk()
root.title("Timeless Track Project")
root.geometry("800x480")


GPIO.setwarnings(False) # Ignore warning for now
reader = SimpleMFRC522() # Create an object of the class MFRC522

id2 = NONE # id of the card
recorder = None # recorder object


def stepper_motor(): # stepper motor function
    #assign GPIO pins for motor
    motor_channel = (29,31,33,35)  
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) #use BOARD pin numbering
    #for defining more than 1 GPIO channel as input/output use
    GPIO.setup(motor_channel, GPIO.OUT)
    while True:
        GPIO.output(motor_channel, (GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.HIGH)) #set GPIO pins to HIGH
        sleep(0.01) #wait 0.01 seconds
        GPIO.output(motor_channel, (GPIO.HIGH,GPIO.HIGH,GPIO.LOW,GPIO.LOW)) #set GPIO pins to LOW
        sleep(0.01)
        GPIO.output(motor_channel, (GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.LOW)) #set GPIO pins to HIGH
        sleep(0.01)
        GPIO.output(motor_channel, (GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.HIGH)) #set GPIO pins to LOW
        sleep(0.01)

def stepper_thread(): # stepper motor thread
    th= threading.Thread(target=stepper_motor) # create a thread
    th.start() # start the thread
   
def back0(): # back to home page
    label0.destroy() # destroy the label
    button0.destroy() # destroy the button
    button_0.destroy() # destroy the button
    

def back0_0():  
    back0()
    tab0()

def tab0(): # home page
    global label0 # define the label
    label0 = Label(root,text="Choose Record or listening",font=("Times_New_Roman",25)) # create the label
    label0.pack(side=TOP) # pack the label
    global button0 # define the button
    button0 = Button(root,text="Record",font=("Times_New_Roman",30),activebackground="red",height=10,width=15,command=tab1) # create the button
    button0.pack(side=LEFT) # pack the button
    global button_0
    button_0 = Button(root,text="listen",font=("Times_New_Roman",30),activebackground="green",height=10,width=15,command=tab_listen_1)
    button_0.pack(side=RIGHT) 
    read_card_thread() # start the read card thread
   

def back_listening_back_1():# back to listening page
    label9.destroy()
    button_bl.destroy()
    button_play.destroy()
    labell.destroy()
    button_pause.destroy()
    tab0()

def pause_music():# pause the music
    global is_playing # define the is_playing as a flag to switch between pause and play
    if is_playing:
        pygame.mixer.music.pause() 
        is_playing = False # set the flag to false
    else:
        if id2=="584184853470": # if the card id is 584184853470
            pygame.mixer.music.load("George.mp3") # load the voice recording of George
            pygame.mixer.music.play() # play the voice recording of George
            is_playing = True # set the flag to true
        elif id2 =="584185443538": # if the card id is 584185443538
            pygame.mixer.music.load("katy.mp3") # load the voice recording of Katy
            pygame.mixer.music.play() # play the voice recording of Katy
            is_playing = True # set the flag to true

def play_music(): # play the music
    global is_playing
    if is_playing: # if the music is playing
        pygame.mixer.music.unpause()# unpause the music
  
    else:
        if id2=="584184853470": # if the card id is 584184853470
            pygame.mixer.music.load("George.mp3") # load the voice recording of George
            pygame.mixer.music.play() # play the voice recording of George
            is_playing = True
        elif id2 =="584185443538": # if the card id is 584185443538
            pygame.mixer.music.load("katy.mp3") # load the voice recording of Katy
            pygame.mixer.music.play() # play the voice recording of Katy
            is_playing = True

def play_music_2(): #the relesten function for the recordings of the user
        # Specify the directory where the files are located
        directory = "/home/pi/Track"

        # Get a list of all the .wav files in the directory
        wav_files = [f for f in os.listdir(directory) if f.endswith(".wav")]

        # Sort the list of files in ascending order based on their file name
        sorted_files = sorted(wav_files, key=lambda f: int(f.split("recording")[1].split(".")[0]))

        # Print all the file names
        print("All files in directory:")
        for file in sorted_files:
            print(file)

        # Get the largest file name from the sorted list
        largest_file = sorted_files[-1]

        # Print the largest file name
        print("Largest file name: ", largest_file)
        pygame.mixer.music.load(largest_file)
        pygame.mixer.music.play()
        is_playing = True

GPIO.setwarnings(False) # disable warnings
reader = SimpleMFRC522() # create a reader object

def read_card(): # read card function
    global id2 # define the id2 as a global variable
    id_label = tk.Label(root, text="") 
    id_label.pack()
    try: # try to read the card
        id2 = reader.read_id()  # read the card id
        id2=str(id2) # convert the id to string
        return id2
        
    except: # if the card is not read
        id_label.config(text="Error reading card") # print error message
    # Clean up the GPIO pins when the GUI is closed
    GPIO.cleanup()
    
def read_card_thread(): # read card thread
    t= threading.Thread(target=read_card) # create a thread
    t.start()   # start the thread
    
def update_id_label(): # update the id label
    global id2 #
    root.after(1000, update_id_label) # update the id label every 1000 ms

def tab_listen_1():#listen page
    back0()
    
     #initialize pygame
    pygame.init()
    pygame.midi.init()
    pygame.mixer.init()
    global is_playing
    is_playing = False
    read_card_thread() # start the read card thread
    update_id_label() # start the update id label thread
    stepper_thread() # start the stepper thread
    
    framel = Frame(root, width=600, height=400)
    global label9
    label9 = Label(root,text="Physical Prototyping- 2020 Memories ",font=("Times_New_Roman",25))
    label9.pack(side=TOP)
    global button_bl
    button_bl = Button(root,text="BACK",font=("Times_New_Roman",25),activebackground="yellow",height= 2, width=5,command=back_listening_back_1)
    button_bl.pack(side=TOP) 
    button_bl.place(x=1,y=200)
    global button_play
    button_play = Button(root,text="play",font=("Times_New_Roman",25),activebackground="green",height= 1, width=10, command=play_music)
    button_play.pack(side=BOTTOM) 
    button_play.place(x=1,y=400)
    global button_pause
    button_pause = Button(root,text="stop",font=("Times_New_Roman",25),activebackground="red",height= 2, width=5, command=pause_music)
    button_pause.place(x=1,y=300)
    button_pause.pack(side=RIGHT) 
  
    
    framel = Frame(root, width=600, height=400)
    framel.pack()
    framel.place(anchor='center', relx=0.5, rely=0.5)

# Create a PhotoImage object of the image in the path
    global labell
    if id2 == "584184853470": # if the card id is 584184853470
        imgl = ImageTk.PhotoImage(Image.open("midas.jpg"))
        global labell
        labell = Label(framel, image = imgl)
        labell.image = imgl
        labell.pack()
    elif id2 == "584185443538": # if the card id is 584185443538
        imgl = ImageTk.PhotoImage(Image.open("katy.jpg"))
        labell = Label(framel, image = imgl)
        labell.image = imgl
        labell.pack()
    else: # if the card id is not 584184853470 or 584185443538
        labell = Label(framel, text="Empty disk")
        labell.pack()
        
def back01(): #first page destroy
    label1.destroy()
    button1.destroy()
    button2.destroy()
    labeln.destroy()
    label_step_1.destroy()

def back01_01(): #first page destroy
    back01() 
    tab0()
    
def tab2():#second page
    back01()
    global label2
    label2 = Label(root,text="We took three photos for you.",font=("Times_New_Roman",25))
    label2.pack()
    global label2_01
    label2_01 = Label(root,text="Click next to preview",font=("Times_New_Roman",25))
    label2_01.pack()
    global button_1
    button_1 = Button(root,text="BACK",font=("Times_New_Roman",25),activebackground="yellow",command=back02)
    button_1.pack(side=LEFT) 
    global button_2
    button_2 = Button(root,text="NEXT",font=("Times_New_Roman",25),activebackground="green",command= tab3)
    button_2.pack(side=RIGHT)
    global label_step_2
    label_step_2 = Label(root,text="Step 2 0f 4",font=("Times_New_Roman",15))
    label_step_2.place(x=10,y=400)
    label_step_2.pack() 
    camera01() # call the camera function
    recorder.hide() # hide the camera preview


def camera01(): # camera function
    camera= PiCamera() # create a camera object
    camera.start_preview() # start the camera preview
    for i in range(3): # take 3 photos
        sleep(5) # wait 5 seconds
        camera.capture('/home/pi/Track/image%s.jpg'%i) # save the photos
    camera.stop_preview() # stop the camera preview

def back02(): #second page destroy and rebuild tab1
    back02_1()
    tab1()

def back02_1(): #second page destroy
    label2.destroy()
    label2_01.destroy()
    button_1.destroy()
    button_2.destroy()
    label_step_2.destroy()


def tab1(): # first page
    back0()
    stepper_thread() # start the stepper thread
    global label1
    label1 = Label(root,text="1) please put on a desk",font=("Times_New_Roman",25))
    label1.pack(side=TOP)
    global labeln
    labeln = Label(root,text="2) clicking Next will take 3 photos of you",font=("Times_New_Roman",25))
    labeln.pack(side=TOP)
    global button1
    button1 = Button(root,text="BACK",font=("Times_New_Roman",25),activebackground="yellow",command=back01_01)
    button1.pack(side=LEFT) 
    global button2
    button2 = Button(root,text="NEXT",font=("Times_New_Roman",25),activebackground="green",command= tab2)
    button2.pack(side=RIGHT) 
    global label_step_1
    label_step_1 = Label(root,text="Step 1 0f 4",font=("Times_New_Roman",15))
    label_step_1.place(x=10,y=400)
    label_step_1.pack()
    recorder.hide() # hide the camera preview
    

def tab3():# third page
    
    back02_1()
    radion_var = StringVar()
    global radion_button
    radion_button = Radiobutton(root,text="Option 1",variable=radion_var,value="1") # create a radio button for option 1
    radion_button.pack()
    radion_button.place(x=200,y=100)
    global radion_button2
    radion_button2 = Radiobutton(root,text="Option 2",variable=radion_var,value="2") # create a radio button for option 2
    radion_button2.pack()
    radion_button2.place(x=200,y=250)
    global radion_button3
    radion_button3 = Radiobutton(root,text="Option 3",variable=radion_var,value="3") # create a radio button for option 3
    radion_button3.pack()
    radion_button3.place(x=200,y=400)

    global frame00
    frame00 = Frame(root,width=400,height=400)
    frame00.pack()
    
    frame00.place(anchor="center",relx=0.5,rely=0.5)
    frame00.place(x=0,y=5)
    # Load the image
    image0 = Image.open("image0.jpg")
    image0 = image0.resize((200, 150), Image.ANTIALIAS)
    # Convert the image to a format that tkinter can display
    tk_image0 = ImageTk.PhotoImage(image0)
    # Create a label to display the image
    global image_label0
    image_label0 = Label(frame00, image=tk_image0)
    image_label0.place(x=0,y=0)
    image_label0.image = tk_image0
    image_label0.pack()
    
    global frame01
    frame01 = Frame(root,width=400,height=400)
    frame01.pack()
    frame01.place(anchor="center",relx=0.5,rely=0.5)
    frame01.place(x=0,y=-150)
    # Load the image
    image1 = Image.open("image1.jpg")
    image1 = image1.resize((200, 150), Image.ANTIALIAS)
    # Convert the image to a format that tkinter can display
    tk_image1 = ImageTk.PhotoImage(image1)
    # Create a label to display the image
    global image_label1
    image_label1 = Label(frame01, image=tk_image1)
    image_label1.image = tk_image1
    image_label1.pack()
    
    global frame02
    frame02 = Frame(root,width=400,height=400)
    frame02.pack()
    frame02.place(anchor="center",relx=0.5,rely=0.5)
    frame02.place(x=0,y=160)
    # Load the image
    image2 = Image.open("image2.jpg")
    image2 = image2.resize((200, 150), Image.ANTIALIAS)
    # Convert the image to a format that tkinter can display
    tk_image2 = ImageTk.PhotoImage(image2)
    # Create a label to display the image
    global image_label2
    image_label2 = Label(frame02, image=tk_image2)
    #image_label2.place(x=0,y=50)
    image_label2.image = tk_image2
    image_label2.pack()

    global button3 # create a back button
    button3 = Button(root,text="BACK",font=("Times_New_Roman",25),activebackground="yellow",command=back03)
    button3.pack(side=LEFT) 
    global button4 # create a next button
    button4 = Button(root,text="NEXT",font=("Times_New_Roman",25),activebackground="green",command=tab4)
    button4.pack(side=RIGHT) 
    recorder.hide()

def back03(): # back button for tab3
    back03_1()
    tab2()

def back03_1():
    button3.destroy()
    button4.destroy()
    radion_button.destroy()
    radion_button2.destroy()
    radion_button3.destroy()
    image_label0.destroy()
    image_label1.destroy()
    image_label2.destroy()
    frame00.destroy()
    frame01.destroy()
    frame02.destroy()

def tab4(): # fourth page
    back03_1()
    global label4
    label4 = Label(root,text="Next you will be recording voice memo",font=("Times_New_Roman",25))
    label4.pack(side=TOP)
    global button4
    button4 = Button(root,text="BACK",font=("Times_New_Roman",25),activebackground="yellow",command=back04)
    button4.pack(side=LEFT) 
    global button5
    button5 = Button(root,text="NEXT",font=("Times_New_Roman",25),activebackground="green",command=tab5)
    button5.pack(side=RIGHT) 
    global label_step_3
    label_step_3 = Label(root,text="Step 3 0f 4",font=("Times_New_Roman",15))
    label_step_3.place(x=10,y=400)
    label_step_3.pack() 
    recorder.hide() # hide the recorder
    
def back04(): 
    back04_1()
    tab3()

def back04_1():
    label4.destroy()
    button4.destroy()
    button5.destroy()
    label_step_3.destroy()

def tab5(): # Recording page
    back04_1()
    global label5
    label5 = Label(root,text="Click to start, reclick to stop",font=("Times_New_Roman",25))
    label5.pack(side=TOP)
    global button6
    button6 = Button(root,text="BACK",font=("Times_New_Roman",25),activebackground="yellow",command=back05)
    button6.pack(side=LEFT) 
    global button7
    button7 = Button(root,text="NEXT",font=("Times_New_Roman",25),activebackground="green",command= tab6)
    button7.pack(side=RIGHT) 
    global recorder
    recorder = record() # call the recorder

def record(): # recorder
    class VoiceRecorder: # create a class for the recorder
        def __init__(self): # create a constructor
            self.root=root
            self.button= tk.Button(text="Rec", font=("Arial", 120, "bold"), command=self.click_handler)
            self.button.pack()
            self.label= tk.Label(text="00:00:00")
            self.button.pack()
            self.recording=False
        

        def click_handler(self): # create a click handler
            if self.recording: # if the recorder is recording
                self.recording=False # stop recording
                self.button.config(fg= "black") # change the color of the button
            else:
                self.recording= True # start recording
                self.button.config(fg="red") # change the color of the button
                threading.Thread(target=self.record).start() # start a thread to record the voice
        
        def record(self): # create a function to record the voice
            audio= pyaudio.PyAudio() # create an object of pyaudio
            stream= audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024) # open the stream
            frames=[] # create a list to store the frames
            start= time.time() # get the current time
            print("start   ", start) # print the current time

            while self.recording: # while the recorder is recording
                data= stream.read(1024) # read the data
                frames.append(data) # append the data to the list
                passed= time.time()- start # get the time passed
                print("passe  ",passed) # print the time passed
                secs= passed%60 # get the seconds
                mins= passed //60 # get the minutes
                hours= mins// 60 # get the hours
                print("second", secs, "mins" , mins, "hours", hours) # print the seconds, minutes and hours

                self.label.config(text=f"{int(hours):02d}: {int(mins):02d}: {int(secs):02d}") #putting a leading zero so it will look like 09:07:03 and casting the numbers to integiers
                self.label.pack()
            #writing the collected frames into a file
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            #we are going to hava adefault file name followed by a number and this number is gonna indicate the recording
            #check if theses files exist and as long as the file exist we r going to increase the value of the number after the recording 
            exists= True 
            i=1
            while exists: 
                if os.path.exists(f"recording{i}.wav"): # check if the file exists
                    i+=1 # increase the value of i
                else: # if the file does not exist
                    exists= False # set the value of exists to false
            sound_file= wave.open(f"recording{i}.wav", "wb") # open the file
            sound_file.setnchannels(1) # set the number of channels
            sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16)) # set the sample width
            sound_file.setframerate(44100) # set the frame rate
            sound_file.writeframes(b"".join(frames)) # write the frames
            sound_file.close() # close the file

        def hide(self): # create a function to hide the recorder
            self.button.destroy()
            self.label.destroy()
            

    return VoiceRecorder() # return the recorder


def back05():
    back05_1()
    tab4()

def back05_1(): 
    label5.destroy()
    button6.destroy()
    button7.destroy()

def tab6(): # Relisten page
    back05_1()
    #initialize pygame
    pygame.init()
    pygame.midi.init()
    pygame.mixer.init()
    global label6
    label6 = Label(root,text="Step 4 0f 4",font=("Times_New_Roman",15))
    label6.pack(side=TOP)
    global button8
    button8 = Button(root,text="BACK",font=("Times_New_Roman",25),activebackground="yellow",command=back06)
    button8.pack(side=LEFT) 
    global button9
    button9 = Button(root,text="NEXT",font=("Times_New_Roman",25),activebackground="green",command=tab7)
    button9.pack(side=RIGHT)
    global button_relisten
    button_relisten = Button(root,text="Relisten",font=("Times_New_Roman",35),activebackground="red",command=play_music_2,height= 10, width=20) # play the recorded voice
    button_relisten.pack(side=BOTTOM)
    global recorder
    recorder.hide() # hide the recorder
   
def back06():
    back06_1()
    tab5()

def back06_1():
    label6.destroy()
    button8.destroy()
    button9.destroy()
    button_relisten.destroy()
    
def tab7():# Complete page
    back06_1()
    global label7
    label7 = Label(root,text="You completed all steps",font=("Times_New_Roman",25))
    label7.pack(side=TOP)
    global button10
    button10 = Button(root,text="BACK",font=("Times_New_Roman",25),activebackground="red",command=back07)
    button10.pack(side=LEFT) 
    global button11
    button11 = Button(root,text="NEXT",font=("Times_New_Roman",25),activebackground="green",command=tab8)
    button11.pack(side=RIGHT)

def back07():
    label7.destroy()
    button10.destroy()
    button11.destroy()
    tab6()

def back07_1():
    label7.destroy()
    button10.destroy()
    button11.destroy()

def tab8(): # Thank you page
    back07_1()
    global label8
    label8 = Label(root,text="Thank you for sharing your memory",font=("Times_New_Roman",25))
    label8.pack(side=TOP)
    global button12
    button12 = Button(root,text="Home",font=("Times_New_Roman",25),activebackground="blue",command=back08)
    button12.pack(side=BOTTOM) 

def back08():
    label8.destroy()
    button12.destroy()
    tab0()
    restart_program()
 
def restart_program(): # restart the program
    python = sys.executable # get the path of the python interpreter
    os.execl(python,python,*sys.argv) # restart the program
    print("Restart program....")

tab0() # start the program
root.mainloop() # start the mainloop
