#importing all the necessary libraries
from tkinter import * #tkinter for GUI
from PIL import Image, ImageTk #for importing images
import random # for generating randomised numbers
from tkinter import messagebox #for message boxes
import pygame, sys, time #for sound effects and music

pygame.mixer.init()
#loading in the sound effects/ background music
pygame.mixer.music.load('mathquiz//bg-music.mp3')
correct_ans = pygame.mixer.Sound('mathquiz//yay!.mp3')
wrong_ans = pygame.mixer.Sound('mathquiz//Boo!.mp3')
#song will lopp indefinetly and has a fade volume effect
pygame.mixer.music.play(loops=-1, start=5)
#setting the volume of the background music and sound effects
pygame.mixer.music.set_volume(0.3)
correct_ans.set_volume(1.0)
wrong_ans.set_volume(1.0)


#VARIABLES BEING USED
#tracking the user's score
score = 0  
#tracking current question
question = 1 
#tracking current attempt for scoring 
attempt = 1  
# stores the answer for the current problem
current_ans = None
# stores the difficulty level 
difficulty = None 
#mute toggle
muted = False

#creating the main window
window = Tk()
#giving the window a title
window.title("Math Quiz")
#resizing the window
window.geometry("1100x630")
#disabling resizing so that design stays consistent
window.resizable(False, False)
#changing the window icon
window.iconphoto(False, ImageTk.PhotoImage(file="mathquiz//plus.png"))


#function to play correct answer sound effect:
def correct_sound():
     correct_ans.play()

#function to play wrong answer sound effect:
def wrong_sound():
     wrong_ans.play()

#function to mute/unmute background music
def mute():
     global muted
     muted = not muted
     if muted:
          #mute background music
          pygame.mixer.music.set_volume(0.0)
          #mute sound effects
          correct_ans.set_volume(0.0)
          wrong_ans.set_volume(0.0)
          main_mute_btn.config(text="🔇")
          instructions_mute_btn.config(text="🔇")
          difficulty_mute_btn.config(text="🔇")
          quiz_mute_btn.config(text="🔇")
     else:
          #unmute background music
          pygame.mixer.music.set_volume(0.3)
          #unmute sound effects
          correct_ans.set_volume(1.0)
          wrong_ans.set_volume(1.0)
          main_mute_btn.config(text="🔊")
          instructions_mute_btn.config(text="🔊")
          difficulty_mute_btn.config(text="🔊")
          quiz_mute_btn.config(text="🔊")

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
    frame = Frame(window, width=1100, height=630)
    frame.place(x= 0, y = 0)

    #loading up and setting up the image background
    bg_img = Image.open(bg_image)
    bg_img = bg_img.resize((1100, 630), Image.Resampling.LANCZOS)
    bg_pic = ImageTk.PhotoImage(bg_img)
    #creating a label to display the image
    bg_label = Label(frame, image=bg_pic)
    bg_label.image = bg_pic
    bg_label.place(x = 0, y = 0, relheight= 1, relwidth= 1)

    return frame

def displayMenu():
    #this will display the difficulty frame bt bringing it to the front 
    forward_frame(difficulty_frame)

#This will generate a random number depending on the difficulty chosen
def randomInt(difficulty):
     """Argument:
          difficulty represents the difficulty level 
          ("Easy", "Moderate", and "Advanced")"""
     #if 'Easy' is chosen, random single-digit numbers will be generated
     if difficulty == "Easy":
          num1 = random.randint(0, 9)
          num2 = random.randint(0, 9)
     #if 'Moderate' is chosen, random double-digit numbers will be generated
     elif difficulty == "Moderate":
          num1 = random.randint(10, 99)
          num2 = random.randint(10, 99)
     #if 'Advanced' is chosen, random four-digit numbers will be generated
     elif difficulty == "Advanced":
          num1 = random.randint(1000, 9999)
          num2 = random.randint(1000, 9999)
     return num1, num2

#this function randomly selects whether the operation will be addition or subtraction
def decideOperation():
     return random.choice(["+", "-"])

#This generates and displays a problem based on the difficulty chosen
def displayProblem(diff_level):
     #argument 'diff_level' is used for the difficulty level of the problem
     global current_ans, num1, num2, operation, difficulty, attempt
     #setting up the difficulty level and resetting the attempt counter
     difficulty = diff_level
     attempt = 1

     #This generates random integers and the operation
     num1, num2 = randomInt(difficulty)
     operation = decideOperation()
     
     #calculates the answer based on the operation
     if operation == "+":
          current_ans = num1 + num2
     else:
          current_ans = num1 - num2
     
     #this is used to display the problem and clear any previous answers
     quiz_label3.config(text = f"{num1} {operation} {num2} = ")
     answer_entry.delete(0, END)

#this checks if the user's answer is correct and updates the game 
def isCorrect(answer):
     #The argument 'answer' is used for the user's input
     global score, question, attempt, current_ans, difficulty

     #this makes sure a number is inputted
     try:
          answer = int(answer)
     except ValueError:
          messagebox.showwarning("Invalid", "Not a valid number")
          answer_entry.delete(0, END)
          return
     
     #this checks if answer is correct and how many attemps it took
     if answer == current_ans:
          #play correct sound effect
          correct_sound()
          #if it took only 1 attempt full points are given
          if attempt == 1:
               score += 10
          #if it took more than 1 attempt half points are given
          else:
               score += 5

          #This updates the score display accordingly
          quiz_label1.config(text=f"Score = {score}/100")
          #moves on to the next question
          question += 1
          quiz_label2.config(text=f"Question {question}/10")
          #reseting the attempt counter
          attempt = 1

          #this decides whether to continue with the questions or end it and display results
          #if the question number is below 10 it will continue displaying problems
          if question < 10:
               displayProblem(difficulty)
          #if the question number is above 10 it will end the quiz and display the results 
          else:
               displayResults()
     #if the answer is wrong          
     else:
          #play wrong sound effect
          wrong_sound()
          #display that the answer is wrong and allow a 2nd attempt
          if attempt == 1:
               attempt += 1
               messagebox.showinfo("Incorrect", "Incorrect. \n try again")
               answer_entry.delete(0, END)
          #if 2nd attempt is also incorrect, it will show the correct answer and move on
          else:
               messagebox.showinfo("Incorrect", f"Incorrect \nthe correct answer was {current_ans}.")
               question += 1
               quiz_label2.config(text=f"Question {question}/10")
               attempt=1


               #this will check if it conties with the next question or end the quiz
               if question < 10:
                    displayProblem(difficulty)
               else:
                    displayResults()


def displayResults():
     global score, question, attempt
     """This function will display the results after
          all 10 questions are completed. It will display 
          the score, grade, as well as, ask the user if they
          would like to play again"""

     #this will deduce the grade based on the score earned
     if score >= 90:
          grade = "A+"
     elif score >= 80:
          grade = "A"
     elif score >= 70:
          grade = "B"
     elif score >=60:
          grade = "C"
     elif score >=50:
          grade = "D"
     else:
          grade = "F"
     
     #This will show the results and ask the user if they would like to play again
     replay = messagebox.askyesno("Quiz Completed", f"Your score is {score}/100 \n Grade: {grade} \n \nDo you want to play again?")
     #this resets the game's counters
     score = 0
     question = 1
     attempt = 1
     quiz_label1.config(text=f"Score = {score}/100")
     quiz_label2.config(text=f"Question {question}/10")
     quiz_label3.config(text="")

     #if the user wants to replay the quiz, the difficulty menu will be shown
     if replay:
          displayMenu()
     #if the user doesnt want to replay the quiz, it will bring them back to the main menu
     else:
          forward_frame(main_frame)

#Using the 'create_frame()' function to create the main menu frame 
main_frame = create_frame("mathquiz//2.png")

#creating a header and placing it appropriately
header_lbl = Label(main_frame, text="Welcome To \n My Math Quiz!!!", font=("LT Comical", 32, "bold"), 
                   fg="#212121", bg="#64b5f6")
header_lbl.place(x=390, y=131, width=320, height=110)

#creating the buttons using the "button()" function and placing them appropriately
main_mute_btn = button(main_frame, "🔊", "#00ff57", "#212121", "#00ff57", "#212121")
main_mute_btn.config(command=mute)
main_mute_btn.place(x=1032, y=33, width=35, height=35)

difficulty_btn = button(main_frame, "Difficulty", "#1976d2", "#212121", "#1976d2", "#212121" )
difficulty_btn.config(command=lambda: displayMenu())
difficulty_btn.place(x=422, y=276, width=230, height=45)

instructions_btn = button(main_frame, "Instructions", "#1976d2", "#212121", "#1976d2", "#212121" )
instructions_btn.config(command=lambda: forward_frame(instructions_frame))
instructions_btn.place(x=422, y=355, width=230, height=45)

quit_btn = button(main_frame, "Quit", "#1976d2", "#212121", "#1976d2", "#212121" )
quit_btn.config(command=window.destroy)
quit_btn.place(x=442, y=433, width=200, height=45)

#creating the instructions frame using the "create_frame()" function 
instructions_frame = create_frame("mathquiz//9.png")
#creating a header and placing it appropriately
header_lbl = Label(instructions_frame, text="Instructions", font=("LT Comical", 32, "bold"), 
                   fg="#212121", bg="#e3f2fd")
header_lbl.place(x=400, y=20, width=320, height=50)

#creating a label to hold the instructions text content and placing it appropriately 
instructions_label = Label(
    instructions_frame, text="""
Difficulty Levels:
1.Easy - single-digit problems
2.Moderate- double-digit problems
3.Advanced - four-digit problems
 
How To Play:
After selecting the desired difficulty level, the quiz will start with
one problem at a time
Enter your answer and submit it.
if your answer is correct, you’ll get 10 points and move on to the next problem.
if your answer is incorrect, you’ll get a chance to try again and 
if you do get it correct, you will only get 5 points instead.
Try your best to get the highest score possible!!!""",
font=("LT Comical", 19),bg="#64b5f6", fg="#212121", justify="left")
instructions_label.place(x= 68, y= 83, height=490)

#creating a back button so that the user can go back to the previous frame
back_btn = button(instructions_frame, "back", "#1976d2", "#212121", "#1976d2", "#212121")
back_btn.config(command=lambda: forward_frame(main_frame))
back_btn.place(x= 47, y=20, height=40, width=80)

instructions_mute_btn = button(instructions_frame, "🔊", "#00ff57", "#212121", "#00ff57", "#212121")
instructions_mute_btn.config(command=mute)
instructions_mute_btn.place(x=1032, y=33, width=35, height=35)

#Creating the difficulty frame
difficulty_frame = create_frame("mathquiz//3.png")
#creating a header and palcing it appropriately
difficulty_lbl = Label(difficulty_frame, text="Difficulty", font=("LT Comical", 32, "bold"), 
                   fg="#212121", bg="#64b5f6")
difficulty_lbl.place(x=450, y=131, width=200, height=70)

#creating a back button so that the user can go back to the previous frame
back_btn = button(difficulty_frame, "back", "#1976d2", "#212121", "#1976d2", "#212121")
back_btn.config(command=lambda: forward_frame(main_frame))
back_btn.place(x= 47, y=20, height=40, width=80)

#creating the difficulty frames buttons using the "button()" function
difficulty_mute_btn = button(difficulty_frame, "🔊", "#00ff57", "#212121", "#00ff57", "#212121")
difficulty_mute_btn.config(command=mute)
difficulty_mute_btn.place(x=1032, y=33, width=35, height=35)

easy_btn = button(difficulty_frame, "Easy", "#1976d2", "#212121", "#1976d2", "#212121")
easy_btn.config(command=lambda:[forward_frame(quiz_frame), displayProblem("Easy")])
easy_btn.place(x=116, y=334, width=200, height=45)

moderate_btn = button(difficulty_frame, "Moderate", "#1976d2", "#212121", "#1976d2", "#212121" )
moderate_btn.config(command=lambda:[forward_frame(quiz_frame), displayProblem("Moderate")])
moderate_btn.place(x=460, y=334, width=180, height=45)

advanced_btn = button(difficulty_frame, "Advanced", "#1976d2", "#212121", "#1976d2", "#212121" )
advanced_btn.config(command=lambda:[forward_frame(quiz_frame), displayProblem("Advanced")])
advanced_btn.place(x=796, y=334, width=180, height=45)

#Creating the quiz frame where the quiz will take place
quiz_frame = create_frame("mathquiz//11.png")

#creating a label for the score
quiz_label1 = Label(quiz_frame, text="Score = 00/100", font=("LT Comical", 20, "bold"), 
                    fg="#212121", bg="#1565c0")
quiz_label1.place( x = 40, y= 34, width=225, height=40)

#creating a label for the question number
quiz_label2 = Label(quiz_frame, text="Question 01/10", font=("LT Comical", 30, "bold"), 
                    fg="#212121", bg="#e3f2fd")
quiz_label2.place( x = 410, y= 180, width=290, height=40)

#creating a label for the quiz problem
quiz_label3 = Label(quiz_frame, text="", font=("LT Comical", 30, "bold"), 
                    fg="#212121", bg="#e3f2fd") #64b5f6
quiz_label3.place( x = 300, y= 285, width=300, height=40)

#creating a entry widget for the user input for the answer
answer_entry = Entry(quiz_frame, font=("LT Comical", 30), bg="#e3f2fd", fg="#212121" )
answer_entry.place(x= 570, y = 285, width= 175, height=40)

#creating a quit button so that the user can quit the program whenever they want to
quit_btn2 = button(quiz_frame, "Quit", "#ff0000", "#212121", "#ff0000", "#212121" )
quit_btn2.config(command=window.destroy)
quit_btn2.place(x=234, y=488, width=200, height=45)

#creating a submit button to submit the answer in the entry widget
submit_btn2 = button(quiz_frame, "Submit", "#00ff57", "#212121", "#00ff57", "#212121" )
submit_btn2.config(command=lambda: isCorrect(answer_entry.get()))
submit_btn2.place(x=658, y=488, width=200, height=45)

#mute button
quiz_mute_btn = button(quiz_frame, "🔊", "#00ff57", "#212121", "#00ff57", "#212121")
quiz_mute_btn.config(command=mute)
quiz_mute_btn.place(x=1032, y=33, width=35, height=35)

#This will bring the main menu frame forward
forward_frame(main_frame)

#starting the tkinter event loop to run the program
window.mainloop()