#importing all the necessary libraries
from tkinter import * #for GUI creation
from tkinter import ttk #for tkinterwidget combobox
from tkinter import messagebox #for displaying message boxes to the user
from PIL import Image, ImageTk #for the images

#list to store all the sutdent data
students = []


def calculate(c1, c2, c3, exam):
    """function to calculate the students marks, percentage
     and grade based on the coursework and exam marks
     Arguments: c1, c2,c3: coursework marks out of 20
                exam: exam mark out of 100
                
    this returns the total coursework, overall mark, percentage, and grade"""
    total = c1 + c2 + c3
    overall = total + exam
    percentage = (overall / 160) * 100

    #this calculates the grade based on the percentage
    if percentage >= 70: grade = "A"
    elif percentage >= 60: grade = "B"
    elif percentage >= 50: grade = "C"
    elif percentage >= 40: grade = "D"
    else: grade = "F"

    return total, overall, round(percentage, 2), grade

def format_students(s):
    """this formats the student data into a string 
    
    Arguments: the student dictionary which contains all the student information
    
    this returns a formatted string with student data"""
    return(
        f"Name: {s['name']}\n"
        f"Student Number: {s['id']}\n"
        f"Total Coursework mark: {s['Course mark']}\n"
        f"Exam Mark: {s['exam']}\n"
        f"Overall Percentage: {s['percentage']:.2f}%\n"
        f"Student Grade: {s['grade']}\n"
    )

def find_student(value, key):
    """this finds a student in the students list by a specific key-value pair
    
    arguments: 
        vale is the value to search for
        key is the dictionary key ro search in"""
    return next((s for s in students if str(s[key]) == str(value)), None)

def show_text(widget, text):
    """this displays text in a text widget with center alignment
    arguments:
        widgets is for the text widget in which the text will be displayed in
        text is the text to display"""
    widget.delete("1.0", END) #this will clear the existing text
    widget.tag_configure("center", justify="center") #center alignment
    widget.insert(END, text, "center") #this adds new text with center alignment

def save():
    """this saves all the student records to a text file"""
    with open("studentMarks.txt", "w") as f:
        for s in students:
            #this seperates the data with commas
            f.write(f"{s['id']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n")

def load():
    """This loads the student records from the text file and populates
    the global student list, it also calculates the fields like totals,
      percentages, and grades"""
    global students
    students = [] #this clears the existing student data

    try:
        with open("studentMarks.txt") as f:
            for line in f:
                sections = line.strip().split(",")#this splits the lines by commas
                sections = [s for s in sections if s != ''] #this removes empty strings

                #this will skip lines that dont have 6 fields as they are invalid
                if len(sections) != 6:
                    continue
                #this will extract the first 2 fields
                sid, name = sections[:2]
                #the rest of the fields will be converted to integers
                c1, c2, c3, exam = map(int, sections[2:])

                #calculating the fields using the calculate function
                total, overall, percentage, grade = calculate(c1, c2, c3, exam)

                #this creates the dictionary with all the fields
                students.append({
                    "id":sid,
                    "name":name,
                    "c1":c1, "c2":c2, "c3":c3,
                    "Course mark":total,
                    "exam":exam,
                    "overall":overall,
                    "percentage":percentage,
                    "grade":grade
                })

    except FileNotFoundError:
        print("FILE NOT FOUND")

load()

def display_all():
    """this will display all the student records"""
    if not students:
        return show_text(all_records_output, "No DATA FOUND")
    
    output_text = ""
    total_percentage = 0

    #this builds the string with all the records
    for s in students:
        output_text += format_students(s) + "-"*40 +"\n"
        total_percentage += s["percentage"]

    #this calculates and displays the average percentage and total students
    avg = total_percentage / len(students)
    output_text += f"\n Total Students: {len(students)}\n"
    output_text += f"Average Percentage Mark Obtained {avg:.2f}%\n"
    #this will display all the text in the text widget
    show_text(all_records_output, output_text)


def individual():
    """this function will display an individual student record 
    based on the selected student number by the user"""
    number = student_num.get().strip()  #this will get the selected number
    student = find_student(number, "id") #this will find the student by the number

    #this checks if selection is valid or not
    if not number:
        return show_text(individual_output, "Select a student number")
    if not student:
        return show_text(individual_output, "Student not found")
    #this displays the found student's record
    show_text(individual_output, format_students(student))

def highest():
    """this function finds and displays the student with 
    the highest overall marks"""
    if not students:
        return show_text(highest_output, "NO STUDENT FOUND")
    #this finds the student with the maximum overall marks using lambda function as key
    top = max(students, key=lambda s: s["overall"])
    show_text(highest_output, format_students(top))

def lowest():
   """this function finds and displays the student with 
    the lowest overall marks"""
   if not students:
        return show_text(lowest_output, "NO STUDENT FOUND")
   #this finds the student with the minimum overall marks using lambda function as key
   low = min(students, key=lambda s: s["overall"])
   show_text(lowest_output, format_students(low))

def sort():
    """this function sorts and displays the student records based on 
    the overall score in a specified order """
    if not students:
        return show_text(sort_output, "No STUDNET FOUND")
    
    #this determines the sort direction based on the dropdown selection 
    descending = sort_order.get() == "Descending"
    #this sorts the students based on overall score
    sorted_list = sorted(students, key=lambda s: s["overall"], reverse=descending)

    output_text = ""
    #this builds the output string with the sorted student records
    for s in sorted_list:
        output_text += format_students(s) + "-"*40 +"\n"
    
    show_text(sort_output, output_text)

def add():
    """this adds a new student record as well as check for input validation"""
    #this gets student id and name
    sid = add_id_entry.get().strip()
    name = add_name_entry.get().strip()
    #this validates if student id and name are in correct format and range
    if not sid.isdigit() or not (1000 <= int(sid) <= 9999):
        return messagebox.showerror("ERROR", "Student number MUST be between 1000 - 9999")
    if name == "":
        return messagebox.showerror("ERROR", "name CANNOT be empty")
    
    #this validates marks input are integers
    try:
        c1 = int(add_c1_entry.get())
        c2 = int(add_c2_entry.get())
        c3 = int(add_c3_entry.get())
        exam = int(add_exam_entry.get())
    except:
        return messagebox.showerror("ERROR", "Marks MUST be integers")
    #this validates that the coursework and exam marks in the correct range 
    if not all (0 <= x <= 20 for x in (c1, c2, c3)):
        return messagebox.showerror("ERROR", "Coursework marks MUST be between 0-20")
    if not (0 <= exam <= 100):
        return messagebox.showerror("ERROR", "Exam mark MUST be between 0-100")
    #this calculates the values using calculate function
    total, overall, percentage, grade = calculate(c1, c2,c3, exam)
    #this adds the new student to the global students list
    students.append({
        "id":sid, "name":name,
        "c1":c1, "c2":c2, "c3":c3,
        "Course mark":total, "exam":exam,
        "overall":overall, "percentage":percentage,
        "grade":grade
    })

    #this adds the student record to the 'studentMarks.txt' text file
    with open("studentMarks.txt","a") as f:
        f.write(f"{sid},{name},{c1},{c2},{c3},{exam}\n")
    #success message box
    messagebox.showinfo("SUCCESS", "Student record added!")
    #this clears all the input fields after the student is added
    for e in (add_id_entry, add_name_entry, add_c1_entry, add_c2_entry, add_c3_entry, add_exam_entry):
        e.delete(0, END)
    #this refreshes the dropdown menus with the updates students list
    refresh_student_dropdown(dropdown_menu, "id")
    refresh_student_dropdown(delete_dropdown, "name")
    refresh_student_dropdown(update_dropdown, "name")

def refresh_student_dropdown(dropdown, value_type="id"):
    """this function is sued to update the dropdown menus 
    with the correct student information
    
    Arguments:
        dropdown is for the combobox widget to update
        value_type is for the type of value to display, 
        'id' for number or 'name' for student names
        """
    if value_type == "id":
        dropdown['values'] = [s["id"] for s in students]
    elif value_type == "name":
        dropdown['values'] = [s["name"] for s in students]
    dropdown.update() 

#creading the window
window = Tk()
window.title("Student Manager") #setting a title to the window
window.geometry("1000x600") #setting the window size
window.resizable(False, False) #disabling the option to resize the window
window.iconphoto(False, ImageTk.PhotoImage(file="images//bsu-logo.png")) #changing the window icon



#defining a function to create buttons easily
def button(parent, text, bg_color, fg_color, hover_bg, hover_fg):
    """arguments:
          parent is the is where the button will be placed for example main frame
          text is the text that will be displayed on the button
          bg_color is the background color of the button
          fg_color is the text color of the button
          hover_bg is the background color when the button is pressed
          hover_fg is the text color when the button is pressed""" 
    
    btn = Button(parent, text=text, font=("LT Comical", 14), bg=bg_color,
                  fg=fg_color, relief="flat",
                    borderwidth=0, activebackground=hover_bg,
                      activeforeground=hover_fg)
    return btn

def nav_buttons(frame):
    """function to create navigation buttons for switching between the frames.
    Arguments:
        frame is the parent frame where buttons will be placed"""
    #this defines the buttons text and command
    buttons = [
        ("Instructions", lambda: [forward_frame(instructions_frame)]),
        ("All student records", lambda: [display_all(), forward_frame(all_records_frame)]),
        ("Individual student record", lambda: forward_frame(individual_records_frame)),
        ("Highest total score", lambda: [highest(), forward_frame(highest_frame)]),
        ("Lowest total score", lambda: [lowest(), forward_frame(lowest_frame)]),
        ("Sort student records", lambda: forward_frame(sort_frame)),
        ("Add student record", lambda: forward_frame(add_frame)),
        ("Delete student record", lambda: [forward_frame(delete_frame)]),
        ("Update student record", lambda: [forward_frame(update_frame)]),
        ("Quit", window.destroy)
    ]

    #this positions the buttons vertically with the consistent spacing
    y = 110
    for text, cmd in buttons:
        btn = button(
            frame, text, "#2d77c7", "#ffffff", "#2d77c7", "#ffffff"
        )
        btn.config(command=cmd) #command for the button
        btn.place(x= 15, y=y, width=200, height=30) #button position and size
        y += 48 #incrementing the y position for each button placed

#defining a frame switcher function
def forward_frame(frame):
    """this functions brings the specified frame 
    in the argument to the front of the window, 
    it is used to switch "pages" of the program
    
    argument: frame is the frame that will be brought
      to the front""" 

    frame.tkraise()
    #refreshing specific dropdowns when their frames are activated
    if frame == delete_frame:
        refresh_student_dropdown(delete_dropdown, "name")
    elif frame == individual_records_frame:
        refresh_student_dropdown(dropdown_menu, "id")

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
main_frame = create_frame("images//student manager 1.png")

#creating the Main header label and placing it
header_lbl = Label(main_frame, text="Student Manager", font=("LT Comical", 32, "bold"),
                   fg="#ffffff", bg="#22263d")
header_lbl.place(x=420, y=30, width=360, height=60)

#adding navigation buttons
nav_buttons(main_frame)

#creating the instructions frame using the create_frame() function 
instructions_frame = create_frame("images//student manager 4.png")

#creating and placing the main header label
header_lbl = Label(instructions_frame, text="Instructions", font=("LT Comical", 32, "bold"),
                   fg="#ffffff", bg="#22263d")
header_lbl.place(x=445, y=10, width=360, height=60)

#creating the instruction label and placing 
instructions_lbl = Label(instructions_frame, text="""Welcome to student manager.\n
When you press the 'All student records' button, the list of all student records will appear.
When you press the 'Individual student record' button, you will get the option to select 
a student based on their student number and display their record alone.
When you press the 'Highest total score' button, the student record with
the highest overall score will appear.
When you press the 'Lowest total score' button, the student record with
the lowest overall score will appear.
When you press the 'Sort student records' button,  you will get the 
option to sort the student records based on ascending or descending 
orders based on the students marks.
When you press the 'Add student record' button, you will have to 
fill the fields then add the student. 
When you press the 'Delete student redcord' button, you will be 
given the option to select a student and delete their record.
When you press the 'Update student record' button, you will be 
given the option to select a student and update their record.
when you press the 'Quit' button, the program window will close.""", font=("LT Comical", 14), 
                          bg="#FFFFFF", fg="#212121", justify="left")
instructions_lbl.place(x=275, y= 95, width=655, height=480)

#adding navigation buttons
nav_buttons(instructions_frame)


#All records frame
all_records_frame = create_frame("images//student manager 2.png")

#header label
header_lbl = Label(all_records_frame, text="Student Manager", font=("LT Comical", 32, "bold"),
                   fg="#ffffff", bg="#22263d")
header_lbl.place(x=420, y=10, width=400, height=60)

#sub heading label
header2_lbl = Label(all_records_frame, text="All Student Records", 
                    font=("LT Comical", 18, "bold"), bg="#ffffff", fg="#000000")
header2_lbl.place(x=470, y=100, width=280, height=20)

#output text widget
all_records_output = Text(all_records_frame, font=("Arial", 14), 
                          bg="#FFFFFF", fg="#212121", borderwidth=0, relief="flat")
all_records_output.place(x=320, y= 135, width=600, height=450)

#navigation buttons
nav_buttons(all_records_frame)



#individual records frame
individual_records_frame = create_frame("images//student manager 2.png")

#main label
header_lbl = Label(individual_records_frame, text="Student Manager", font=("LT Comical", 32, "bold"),
                   fg="#ffffff", bg="#22263d")
header_lbl.place(x=420, y=10, width=400, height=60)

#subheading label
header2_lbl = Label(individual_records_frame, text="Select a student number to view", 
                    font=("LT Comical", 18, "bold"), bg="#ffffff", fg="#000000")
header2_lbl.place(x=440, y=100, width=340, height=20)

#creating dropdown to select sutdents by their number
student_num = StringVar() #this stores the selected student number
dropdown_menu = ttk.Combobox(
    individual_records_frame, textvariable=student_num,
    font=("Comical LT", 14)
)
dropdown_menu.place(x=570, y= 125, width=80, height=30)
#refreshing the dropdown menu with the student numbers
refresh_student_dropdown(dropdown_menu, "id")

#button to display the selected student's record
show_btn = button(individual_records_frame, "Show Record",
                   "#ffffff", "#000000", "#ffffff", "#000000")
show_btn.config(command= individual)
show_btn.place(x= 510, y = 160, width=200, height=40)

#text widget to display the individual record
individual_output = Text(individual_records_frame, font=("LT Comical", 14), 
                         bg="#ffffff",fg="#000000", borderwidth=0)
individual_output.place(x= 460, y=250, width=300, height=300)

#navigation buttons
nav_buttons(individual_records_frame)


#Highest Score Frame
highest_frame = create_frame("images//student manager 2.png")

#main header label
header_lbl = Label(highest_frame, text="Student Manager", font=("LT Comical", 32, "bold"),
                   fg="#ffffff", bg="#22263d")
header_lbl.place(x=420, y=10, width=400, height=60)

#subheading label
highest_lbl = Label(highest_frame, text="Student With Highest Score:", font=("LT Comical", 18, "bold"),
                bg="#ffffff", fg="#000000")
highest_lbl.place(x= 470, y=120, width=300, height=40)

#text widget to display the highest score record 
highest_output = Text(highest_frame, font=("LT Comical", 14), 
                         bg="#ffffff",fg="#000000", borderwidth=0)
highest_output.place(x= 460, y=200, width=300, height=300)

#navigation buttons
nav_buttons(highest_frame)


#lowest Score Frame
lowest_frame = create_frame("images//student manager 2.png")

#main header label
header_lbl = Label(lowest_frame, text="Student Manager", font=("LT Comical", 32, "bold"),
                   fg="#ffffff", bg="#22263d")
header_lbl.place(x=420, y=10, width=400, height=60)

#subheading label
lowest_lbl = Label(lowest_frame, text="Student With Lowest Score:", font=("LT Comical", 18, "bold"),
                bg="#ffffff", fg="#000000")
lowest_lbl.place(x= 470, y=120, width=300, height=40)

#text widget to display the lowest score record
lowest_output = Text(lowest_frame, font=("LT Comical", 14), 
                         bg="#ffffff",fg="#000000", borderwidth=0)
lowest_output.place(x= 460, y=200, width=300, height=300)

#navigation buttons
nav_buttons(lowest_frame)

#sort Frame
sort_frame = create_frame("images//student manager 2.png")

#main header label
header_lbl = Label(sort_frame, text="Student Manager", font=("LT Comical", 32, "bold"),
                   fg="#ffffff", bg="#22263d")
header_lbl.place(x=420, y=10, width=400, height=60)

#subheading label
header2_lbl = Label(sort_frame, text="Sort Student Records", font=("LT Comical", 18, "bold"),
                   fg="#000000", bg="#ffffff")
header2_lbl.place(x= 610, y=230, width=300, height=40)

#dropdown for selecting the sort order
sort_order = StringVar() #this stores the sort order selection
sort_order.set("Ascending")  #default is set to ascending
sort_dropdown = ttk.Combobox(sort_frame, textvariable=sort_order,
                             font=("LT Comical", 14)) 
sort_dropdown['values'] = ["Ascending", "Descending"]  #available options for selection
sort_dropdown.place(x=700, y= 275, width= 120, height=40) 

#button to trigger and display sorting
sort_btn = button(sort_frame, "Sort", "#ffffff", "#000000",
                   "#ffffff", "#000000") 
sort_btn.config(command=sort) 
sort_btn.place(x= 650, y= 320, width= 200, height=40) 

#text widget to display sorted student records
sort_output = Text(sort_frame, font=("LT Comical", 14), bg="#ffffff",
                   fg="#000000", borderwidth=0) 
sort_output.place(x= 320, y=80, width=300, height=505)

#navigation buttons
nav_buttons(sort_frame)


#ADD FRAME
add_frame = create_frame("images//student manager 2.png")

#main header label
header_lbl = Label(add_frame, text="Student Manager", font=("", 32, "bold"),
                   fg="#ffffff", bg="#22263d")
header_lbl.place(x=420, y=10, width=400, height=60)

#subheading label
add_lbl = Label(add_frame, text="Add a New Student Record", font=("LT Comical", 18, "bold"),
                bg="#ffffff", fg="#000000")
add_lbl.place(x= 470, y=120, width=280, height=40)

#input fields for student number, name, coursework and exam marks
number_Lbl= Label(add_frame, text="Student Number:", font=("LT Comical", 14),
                  bg="#ffffff").place(x=445, y=190)
add_id_entry = Entry(add_frame, font=("LT Comical", 14),  relief="solid", borderwidth=2)
add_id_entry.place(x=585, y=190, width=200)

name_Lbl= Label(add_frame, text="Student Name:", font=("LT Comical", 14),
                  bg="#ffffff").place(x=462, y=240)
add_name_entry = Entry(add_frame, font=("LT Comical", 14),  relief="solid", borderwidth=2)
add_name_entry.place(x=585, y=240, width=200)

c1_Lbl= Label(add_frame, text="Coursework Mark 1:", font=("LT Comical", 14),
                  bg="#ffffff").place(x=425, y=290)
add_c1_entry = Entry(add_frame, font=("LT Comical", 14), relief="solid", borderwidth=2)
add_c1_entry.place(x=585, y=290, width=200)

c2_Lbl= Label(add_frame, text="Coursework Mark 2:", font=("LT Comical", 14),
                  bg="#ffffff").place(x=422, y=340)
add_c2_entry = Entry(add_frame, font=("LT Comical", 14), relief="solid", borderwidth=2)
add_c2_entry.place(x=585, y=340, width=200)

c3_Lbl= Label(add_frame, text="Coursework Mark 3:", font=("LT Comical", 14),
                  bg="#ffffff").place(x=423, y=390)
add_c3_entry = Entry(add_frame, font=("LT Comical", 14),  relief="solid", borderwidth=2)
add_c3_entry.place(x=585, y=390, width=200)

exam_Lbl= Label(add_frame, text="Exam Mark:", font=("LT Comical", 14),
                  bg="#ffffff").place(x=485, y=440)
add_exam_entry = Entry(add_frame, font=("LT Comical", 14), relief="solid", borderwidth=2)
add_exam_entry.place(x=585, y=440, width=200)

#add button to add student 
add_btn = button(add_frame, "Add Student Record", "#ffffff", "#000000", "#ffffff", "#000000")
add_btn.config(command= add)
add_btn.place(x=450, y= 510, width=300, height=40)

#navigation buttons
nav_buttons(add_frame)

#DELETE FRAME
delete_frame = create_frame("images//student manager 2.png")

#main header label
header_lbl = Label(delete_frame, text="Student Manager", font=("", 32, "bold"),
                   fg="#ffffff", bg="#22263d")
header_lbl.place(x=420, y=10, width=400, height=60)

#subheading label
del_lbl = Label(delete_frame, text="Delete A Student Record", font=("LT Comical", 18, "bold"),
                bg="#ffffff", fg="#000000")
del_lbl.place(x= 470, y=120, width=280, height=40)

#dropdown for selecting a student to delete by their name
delete_student = StringVar() #stores the selected name
delete_dropdown = ttk.Combobox(delete_frame, textvariable=delete_student,
                               font=("LT Comical", 14))
delete_dropdown.place(x=525, y=170 , width=150 , height=30 )
refresh_student_dropdown(delete_dropdown, "name")



def delete():
    """function to delete selected student record"""
    #getting the student name
    name = delete_student.get().strip()
    if not name:
        return messagebox.showerror("ERROR", "You MUST select a student to delete")
    
    global students
    #finding the student by their name
    student = next((s for s in students if s["name"] == name), None)
    if not student:
        return messagebox.showerror("ERRPR", "UNKNOWN STUDENT")
    
    #confirming deletion with user 
    if messagebox.askyesno("CONFIRMATION", f"Are You Sure You Want To Delete {student['name']}?"):
        #removing the selected student from the list
        students = [s for s in students if s["name"] != name]
        #this rewrites the file without the deleted student
        with open("studentMarks.txt", "w") as f:
            f.writelines(f"{s['id']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n" 
                         for s in students)

        #success message box    
        messagebox.showinfo("SUCCESS", f"Student record for {student['name']} has been deleleted")
        #refreshing all drop down menus
        for dropdown in (delete_dropdown, dropdown_menu, update_dropdown):
            refresh_student_dropdown(dropdown, "name" if dropdown != dropdown_menu else "id")
            #clearing selections
            delete_student.set("")
            update_student.set("")

#delete button
delete_btn = button(delete_frame, "Delete Student Record", "#ffffff", "#000000",
                     "#ffffff", "#000000")
delete_btn.config(command=delete)
delete_btn.place(x=450, y= 210, width=300, height=40)

#navigation buttons
nav_buttons(delete_frame)



def load_update(event=None):
    """this functions loads the slected student's data 
    into the update form field"""
    #find the selected student by their name
    student = next((s for s in students if s["name"] == update_student.get().strip()), None)
    if not student:
        return
    #get all entry widgets and corresponding student values
    entries = [    update_id_entry, update_name_entry, update_c1_entry, update_c2_entry,
                update_c3_entry, update_exam_entry]
    values = [student["id"],student["name"],student["c1"],student["c2"],student["c3"],
              student["exam"]]
    #clear exisiting content and insert current value
    for e, v in zip(entries, values):
        e.delete(0, END)
        e.insert(0, v)

def update():
    """this function updates the selected student record 
    with the new data from the fields"""
    #finding the selected student by name
    student = next((s for s in students if s["name"] == update_student.get().strip()), None)
    if not student:
        return messagebox.showerror("ERROR", "You MUST Select A Student To Update")
    
    #getting and validating the vales from the input fields
    try:
        sid, c1, c2, c3, exam = [int(e.get().strip()) for e in 
                                 (update_id_entry, update_c1_entry, update_c2_entry,
                                   update_c3_entry, update_exam_entry)]
        new_name = update_name_entry.get().strip()
    except ValueError:
        return messagebox.showerror("ERROR", "ID and Marks Must be whole numbers")
    
    #this validates the coursework and exam marks with ranges
    if not (1000<= sid <= 9999) or not all(0 <= x <= 20 for x in (c1, c2, c3)) or not (0 <= exam <= 100) or new_name == "":
        return messagebox.showerror("ERROR", "Check ID, Marks, and name")
    
    #calculating the updates values using calculate function
    total, overall, percentage, grade = calculate(c1, c2,c3, exam)

    #updating the student records with new values
    student.update({"id":sid, "name":new_name, "c1":c1, "c2":c2, "c3":c3,
                     "exam":exam, "Course mark":total, "overall":overall,
                       "percentage":percentage, "grade":grade,})
    
    #saving all records to 'studentMarks.txt' file with updated data
    with open("studentMarks.txt", "w") as f:
        f.writelines(f"{s['id']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n"
                     for s in students)

    #success message    
    messagebox.showinfo("SUCCESS", "Student Record Updated Successfully")
    #refreshing all dropdown menus with updated data
    refresh_student_dropdown(update_dropdown, "name")
    refresh_student_dropdown(delete_dropdown, "name")
    refresh_student_dropdown(dropdown_menu, "id")

#Update frame
update_frame= create_frame("images//student manager 2.png")

#main header label
header_lbl = Label(update_frame, text="Student Manager", font=("", 32, "bold"),
                   fg="#ffffff", bg="#22263d")
header_lbl.place(x=420, y=10, width=400, height=60)

#subheading label
update_lbl = Label(update_frame, text="Update Student Record", font=("LT Comical", 18, "bold"),
                bg="#ffffff", fg="#000000")
update_lbl.place(x= 470, y=90, width=280, height=40)

#creating dropdown for student update selection
update_student = StringVar() #this stores the selected students name
update_dropdown = ttk.Combobox(update_frame, textvariable=update_student,
                               font=("LT Comical", 14))
update_dropdown.place(x= 520, y = 135, width=200, height=30 )
refresh_student_dropdown(update_dropdown, "name")
#this loads data when the selection changes
update_dropdown.bind("<<ComboboxSelected>>", load_update)

#labels and input fields for student number, name, coursework and exam marks
number_Lbl= Label(update_frame, text="Student Number:", font=("LT Comical", 14),
                  bg="#ffffff").place(x=445, y=190)
update_id_entry = Entry(update_frame, font=("LT Comical", 14),  relief="solid", borderwidth=2)
update_id_entry.place(x=585, y=190, width=200)

name_Lbl= Label(update_frame, text="Student Name:", font=("LT Comical", 14),
                  bg="#ffffff").place(x=462, y=240)
update_name_entry = Entry(update_frame, font=("LT Comical", 14),  relief="solid", borderwidth=2)
update_name_entry.place(x=585, y=240, width=200)

c1_Lbl= Label(update_frame, text="Coursework Mark 1:", font=("LT Comical", 14),
                  bg="#ffffff").place(x=425, y=290)
update_c1_entry = Entry(update_frame, font=("LT Comical", 14), relief="solid", borderwidth=2)
update_c1_entry.place(x=585, y=290, width=200)

c2_Lbl= Label(update_frame, text="Coursework Mark 2:", font=("LT Comical", 14),
                  bg="#ffffff").place(x=422, y=340)
update_c2_entry = Entry(update_frame, font=("LT Comical", 14), relief="solid", borderwidth=2)
update_c2_entry.place(x=585, y=340, width=200)

c3_Lbl= Label(update_frame, text="Coursework Mark 3:", font=("LT Comical", 14),
                  bg="#ffffff").place(x=423, y=390)
update_c3_entry = Entry(update_frame, font=("LT Comical", 14),  relief="solid", borderwidth=2)
update_c3_entry.place(x=585, y=390, width=200)

exam_Lbl= Label(update_frame, text="Exam Mark:", font=("LT Comical", 14),
                  bg="#ffffff").place(x=485, y=440)
update_exam_entry = Entry(update_frame, font=("LT Comical", 14), relief="solid", borderwidth=2)
update_exam_entry.place(x=585, y=440, width=200)

#update button with command
update_btn = button(update_frame, "Update Student Record", "#ffffff", "#000000", "#ffffff", "#000000")
update_btn.config(command= update)
update_btn.place(x=450, y= 510, width=300, height=40)

#navigation buttons
nav_buttons(update_frame)

#starts on the main frame
forward_frame(main_frame)
#run the tkinter event loop
window.mainloop()