#importing all the necessary libraries
from tkinter import * #for GUI 
from PIL import Image, ImageTk #for the images
import random # for selecting random jokes
import pygame, sys, time #for playing sounds and handling their timings
from gtts import gTTS #for text to speech using Google text-to-speech library
import os #for file handling


#Function to speak the text using Google Text-to-speach
def speak(text):
    """This function converts all the text to speech and then plays it.
    'text' is the string that will be read aloud"""
    tts = gTTS(text=text, lang='en') # this converts text to speech using gTTS
    tts.save("temp.mp3") #this saves the generated audio to a temporary MP3 file
    sound = pygame.mixer.Sound("temp.mp3") #this loads in the saved MP3 file as a pygame sound
    sound.play() #this plays the sound

#this is an empty list to store the jokes
jokes_list = []


#loading the jokes from randomJokes.txt
try:
    with open("randomJokes.txt") as f:
        #this reads all the lines and removes the empty lines and wite spaces
        jokes_list = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    #this prints an error message if file isnt found or is missing
    print("file not found")
    jokes_list = []

#creading the window
window = Tk()
window.title("Alexa Jokes") #setting a title to the window
window.geometry("1000x600") #setting the window size
window.resizable(False, False) #disabling the option to resize the window
window.iconphoto(False, ImageTk.PhotoImage(file="cat.png")) #changing the window icon

#initialising the mixer module for background music and sound effects
pygame.mixer.init()
#loading in background music and sound effects
pygame.mixer.music.load("bg-music.mp3")
drumroll_effect = pygame.mixer.Sound("drumroll.mp3")
laugh_effect = pygame.mixer.Sound("laughing.mp3")

#playing the background music infinetly
pygame.mixer.music.play(-1)

#this will track whether the audio is muted or not
muted = False
#this will store the current setup and punchline
current_joke = {"setup": "", "punchline": ""}

#function to mute/unmute background music
def mute():
     global muted
     muted = not muted
     if muted:
          #mute background music
          pygame.mixer.music.set_volume(0.0)
          #mute sound effects
          laugh_effect.set_volume(0.0)
          drumroll_effect.set_volume(0.0)
          main_mute_btn.config(text="🔇")
          instructions_mute_btn.config(text="🔇")
          joke_only_mute_btn.config(text="🔇")
          full_joke_mute_btn.config(text="🔇")
          no_joke_mute_btn.config(text="🔇")
     else:
          #unmute background music
          pygame.mixer.music.set_volume(0.3)
          #unmute sound effects
          laugh_effect.set_volume(1.0)
          drumroll_effect.set_volume(1.0)
          main_mute_btn.config(text="🔊")
          instructions_mute_btn.config(text="🔊")
          joke_only_mute_btn.config(text="🔊")
          full_joke_mute_btn.config(text="🔊")
          no_joke_mute_btn.config(text="🔊")



#this function selects a random joke
def random_jokes():
    """this will select a random joke from the 'jokes_list' and it will
    split it into the setup and punchline based on the '?' in the file"""
    joke = random.choice(jokes_list)
    if "?" in joke:
        setup, punchline = joke.split("?", 1)
    else:
        setup, punchline = joke
    current_joke["setup"] = setup + "?" #this makes sure the setup ends with '?'
    current_joke["punchline"] = punchline


"""this funtion will display the joke setup and play 
the sound effect and lower the background music audio"""
def joke_only():
    #this will show the joke setup
    joke_only_setup_lbl.config(text=current_joke["setup"])
    #this will read the setup  
    speak(current_joke["setup"])
    #plays the drumroll sound effect
    drumroll_effect.play()
    #this will lower the volume of the background music
    pygame.mixer.music.set_volume(0.2)
    #this will switch the frame to the joke setup frame
    forward_frame(joke_only_frame)
    

#this function is to display the full joke and read it
def full_joke():
    #this will show the setup
    full_joke_setup_lbl.config(text=current_joke["setup"])
    #this will show the punchline
    full_punchline_lbl.config(text=current_joke["punchline"])
    #this will lower the background music
    pygame.mixer.music.set_volume(0.2)
    #this will read the pucnhline
    speak(current_joke["punchline"])
    #this switches frames
    forward_frame(full_joke_frame)
    #this will delay the laugh sound effect and then play it
    full_joke_frame.after(1300, lambda: laugh_effect.play())

#this function will reset the joke frames and return to the no-joke-frame
def to_joke_only():
    """this function clears the labels in the frames
    and brings the user back to the first joke frame"""
    joke_only_setup_lbl.config(text="")
    full_joke_setup_lbl.config(text="")
    full_punchline_lbl.config(text="")
    pygame.mixer.music.set_volume(0.2)
    forward_frame(no_joke_frame)

#defining a function to create buttons easily
def button(parent, text, bg_color, fg_color, hover_bg, hover_fg):
    """arguments:
          parent is the is where the button will be placed for example main frame
          text is the text that will be displayed on the button
          bg_color is the background color of the button
          fg_color is the text color of the button
          hover_bg is the background color when the button is pressed
          hover_fg is the text color when the button is pressed""" 
    
    btn = Button(parent, text=text, font=("LT Comical", 20), bg=bg_color,
                  fg=fg_color, relief="flat",
                    borderwidth=0, activebackground=hover_bg,
                      activeforeground=hover_fg)
    return btn

#defining a frame switcher function
def forward_frame(frame):
    """this functions brings the specified frame 
    in the argument to the front of the window, 
    it is used to switch "pages" of the program
    
    argument: frame is the frame that will be brought
      to the front""" 

    frame.tkraise()

#definding a reusable frame creator function
def create_frame(bg_image, body_text=None):
    """this function creates a frame with a background image.
          Arguments:
          bg_image is the path of the background image file
          body_text is the optional text for the frame (this was used
            in the instructions frame to save codes of line)"""
    #creating a frame that covers the entire window
    frame = Frame(window, width=1000, height=600)
    frame.place(x= 0, y = 0)

    #loading up and setting up the image background
    bg_img = Image.open(bg_image)
    bg_img = bg_img.resize((1000, 600), Image.Resampling.LANCZOS)
    bg_pic = ImageTk.PhotoImage(bg_img)
    #creating a label to display the image
    bg_label = Label(frame, image=bg_pic)
    bg_label.image = bg_pic
    bg_label.place(x = 0, y = 0, relheight= 1, relwidth= 1)

    return frame

#creating the main frame using the creae_frame() function
main_frame = create_frame("main.png")

#label holding main title
header_lbl = Label(main_frame, text="Welcome To \nAlexa Tell Me A Joke",
                   font=("LT Comical", 32, "bold"), fg="#212121", 
                   bg="#2d77c7")
#placing the header label 
header_lbl.place(x=320, y=70, width=360, height=120)

#setting a mute button with the button() function and giving it a command of mute()
main_mute_btn = button(main_frame, "🔊", "#00ff57", "#212121", "#00ff57", "#212121")
main_mute_btn.config(command=mute)
main_mute_btn.place(x=938, y=33, width=33, height=30)

#button to move to the joke frame
start_btn = button(main_frame, "Start", "#1976d2", "#212121", "#1976d2", "#212121" )
start_btn.config(command=lambda: forward_frame(no_joke_frame))
start_btn.place(x=445, y=270, width=100, height=45)

#button to move to the instructions frame
instructions_btn = button(main_frame, "Instructions", "#1976d2", "#212121", "#1976d2", "#212121" )
instructions_btn.config(command=lambda: forward_frame(instructions_frame))
instructions_btn.place(x=428, y=375, width=150, height=45)

#button to quit the program
quit_btn = button(main_frame, "Quit", "#1976d2", "#212121", "#1976d2", "#212121" )
quit_btn.config(command=window.destroy)
quit_btn.place(x=448, y=483, width=100, height=45)

#creating the instructions frame
instructions_frame = create_frame("instructions1.png")

#Mute button
instructions_mute_btn = button(instructions_frame, "🔊", "#00ff57", "#212121", "#00ff57", "#212121")
instructions_mute_btn.config(command=mute)
instructions_mute_btn.place(x=938, y=33, width=33, height=30)

#creating a back button so that the user can go back to the previous frame
back_btn = button(instructions_frame, "back", "#053f8c", "#212121", "#053f8c", "#212121")
back_btn.config(command=lambda: forward_frame(main_frame))
back_btn.place(x= 40, y=17, height=40, width=80)

#header label for the instructions frame
header_lbl = Label(instructions_frame, text="INSTRUCTIONS",
                   font=("LT Comical", 32, "bold"), fg="#212121", 
                   bg="#e3f2fd")
header_lbl.place(x=360, y=15, width=300, height=50)

#creating a label to hold the instructions text content and placing it appropriately 
instructions_label = Label(
    instructions_frame, text="""
Welcome to alexa tell me a joke \n when you press the button,
 a joke setup will be displayed, then when you press the 
 'reveal punchline' button, the whole joke will be displayed.
   You can also skip the joke by pressing the 'next joke' button\n Enjoy!!""",
font=("LT Comical", 19),bg="#1f2036", fg="#ffffff", justify="left")
instructions_label.place(x= 68, y= 83, height=290)


#creating the first joke frame
no_joke_frame = create_frame("4.png")

#tell me a joke button
joke_btn = button(no_joke_frame, "Alexa tell me a joke", "#0b54a5", 
                  "#212121", "#0b54a5", "#212121")
joke_btn.config(command=lambda: [random_jokes(), joke_only()])
joke_btn.place(x=165, y= 260, width= 200, height=40)

#mute button
no_joke_mute_btn = button(no_joke_frame, "🔊", "#00ff57", "#212121", "#00ff57", "#212121")
no_joke_mute_btn.config(command=mute)
no_joke_mute_btn.place(x=938, y=33, width=33, height=30)

#quit button
quit_btn = button(no_joke_frame, "Quit", "#e56b6f", 
                  "#212121", "#e56b6f", "#212121")
quit_btn.config(command=window.destroy)
quit_btn.place(x=445, y= 522, width= 110, height=46)




#second joke frame
joke_only_frame = create_frame("5.png")

#label to hold the joke
joke_only_setup_lbl = Label(joke_only_frame, text="",
                  font=("LT Comical", 20, "bold"),
                  fg="#212121", bg="#f7c948", 
                  wraplength=300, justify="center")
joke_only_setup_lbl.place(x= 115, y= 85, width=300, height=130)

#button to show punchline
punchline_btn = button(joke_only_frame, "Show Punchline", "#0b54a5", 
                  "#212121", "#0b54a5", "#212121")
punchline_btn.config(command= full_joke)
punchline_btn.place(x=630, y= 345, width= 200, height=40)

#mute button
joke_only_mute_btn = button(joke_only_frame, "🔊", "#00ff57", "#212121", "#00ff57", "#212121")
joke_only_mute_btn.config(command=mute)
joke_only_mute_btn.place(x=938, y=33, width=33, height=30)

#quit button
quit_btn = button(joke_only_frame, "Quit", "#e56b6f", 
                  "#212121", "#e56b6f", "#212121")
quit_btn.config(command=window.destroy)
quit_btn.place(x=445, y= 522, width= 110, height=46)



#last joke button
full_joke_frame = create_frame("6.png")

#joke label
full_joke_setup_lbl = Label(full_joke_frame, text="",
                  font=("LT Comical", 20, "bold"),
                  fg="#212121", bg="#f7c948", 
                  wraplength=300, justify="center")
full_joke_setup_lbl.place(x= 115, y= 85, width=300, height=130)

#punchline label
full_punchline_lbl = Label(full_joke_frame, text="",
                  font=("LT Comical", 20, "bold"),
                  fg="#212121", bg="#f7c948",
                  wraplength=300, justify="center")
full_punchline_lbl.place(x= 580, y= 170, width=300, height=130)


#next joke button
next_joke_btn = button(full_joke_frame, "Next Joke", "#00ff57", 
                  "#212121", "#00ff57", "#212121")
next_joke_btn.config(command=to_joke_only)
next_joke_btn.place(x=400, y= 438, width= 200, height=56)

#mute button
full_joke_mute_btn = button(full_joke_frame, "🔊", "#00ff57", "#212121", "#00ff57", "#212121")
full_joke_mute_btn.config(command=mute)
full_joke_mute_btn.place(x=938, y=33, width=33, height=30)

#quit button
quit_btn = button(full_joke_frame, "Quit", "#e56b6f", 
                  "#212121", "#e56b6f", "#212121")
quit_btn.config(command=window.destroy)
quit_btn.place(x=445, y= 522, width= 110, height=46)

#starts on the main frame
forward_frame(main_frame)
#run the tkinter event loop
window.mainloop()