import os.path
from pathlib import Path
from tkinter import *
from tkcalendar import DateEntry
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, date
from PIL import Image, ImageTk

import screenshot_grabber
import main_analysis

"""
THIS IS THE MAIN GUI WHICH CONTROLS EVERYTHING AND WHICH IS SHOWN TO THE USER.
ALSO IT HAS ALL THE BELOW MENTIONS FEATURES : 
1. Faculty selection dropdown menu.
2. Automatically takes current date.
3. Without selecting any faculty feedback cannot be taken.
4. Directly clicking on submit button will not do anything to the excel file and closes the GUI.
"""

# Global variable to store the emotion value
emotion_result = ""
time_of_start = ""
faculty_selected = ""
screenshot_saved_folder_path = ""


def screenshot_function():
    global screenshot_saved_folder_path
    # Running the function to take ss every 5 min.
    screenshot_saved_folder_path = screenshot_grabber.main(time_of_start)
    analysis_label.config(text="Image saved and started for analysis, please wait...!")
    main_analysis.analysis_main(time_of_start, faculty_selected, screenshot_saved_folder_path)
    analysis_label.config(text="Analyses completed and file saved in downloads.")
    root.after(2000, root.destroy)


def run_main_gui():
    # Function which calls the main feedback program when feedback button is clicked
    global emotion_result, time_of_start, faculty_selected

    # Check if a faculty is Selected.
    if dropdown.get() == "":
        messagebox.showwarning("Warning", "Please select faculty first!")
        return

    # Store the selected faculty name
    faculty_selected = dropdown.get()

    # Capture the time in 12-hour format
    time_of_start = datetime.now().strftime("%I:%M:%S %p")

    # Disable the button
    analysis_button.config(state="disabled")

    # Show Success message
    analysis_label.config(text="Analysis started successfully .... ", fg="green")

    # Function which will take screenshots and save it.
    root.after(100, screenshot_function)


def submitted():
    print("Submitted the form..............")
    # Check if a faculty is Selected.
    if dropdown.get() == "":
        messagebox.showwarning("Warning", "Please select faculty first!")
        return


def on_closing():
    print("Window closed!")
    root.destroy()


def get_selected_faculty(event):
    # Function to handle the dropdown selection event
    selected_faculty = dropdown.get()
    selected_faculty_label.config(text=selected_faculty)


# Create the main Tkinter window
root = tk.Tk()
root.title("Student Engagement Analysis")
root.geometry("925x500+300+200")
root.resizable(False, False)

# Load the image
image = Image.open("./cspit.jpg")
image = image.resize((100, 100))
photo = ImageTk.PhotoImage(image)

# Create a label to display image
image_label = tk.Label(root, image=photo)
image_label.place(x=10, y=10)

# Centered text label
welcome_label = tk.Label(root, text="Welcome to SEA", font=("Times New Roman", 24))
welcome_label.place(relx=0.5, rely=0.2, anchor="center")

# Separator lines
separator = ttk.Separator(root, orient="horizontal")
separator.place(relx=0.5, rely=0.3, anchor="center", relwidth=0.8)

# Dropdown menu
faculty_label = tk.Label(root, text="Please select faculty : ", font=("Arial", 16))
faculty_label.place(relx=0.4, rely=0.35, anchor="e")
faculty_names = ["Dr. Amit Thakkar",
                 "Prof. Hemang Thakar",
                 "Prof. Pinal shah",
                 "Prof. Dharmendrasinh Rathod",
                 "Prof. Brinda Patel",
                 "Prof. Bela Shah",
                 "Prof. Spandan Joshi"]
selected_faculty = tk.StringVar()
dropdown = ttk.Combobox(root, values=faculty_names, textvariable=selected_faculty, state="readonly")
dropdown.place(relx=0.6, rely=0.35, anchor="w")
dropdown.bind("<<ComboboxSelected>>", get_selected_faculty)

# Label to display selected faculty
selected_faculty_label = tk.Label(root, text="", font=("Arial", 16))
selected_faculty_label.place(relx=0.5, rely=0.4, anchor="center")

# Date Label
data_label = tk.Label(root, text="Date : ", font=("Arial", 14))
data_label.place(relx=0.4, rely=0.45, anchor="e")
today = date.today().strftime("%d/%m/%Y")
data_value_label = tk.Label(root, text=today, font=("Arial", 16))
data_value_label.place(relx=0.6, rely=0.45, anchor="w")

# Take feedback button
analysis_button = tk.Button(root, text="Start Analysis", font=("Arial", 16), width=20, height=2,
                            command=run_main_gui)
analysis_button.place(relx=0.5, rely=0.65, anchor="center")

# Label to display analysis status
analysis_label = tk.Label(root, text="", font=("Arial", 14))
analysis_label.place(relx=0.5, rely=0.75, anchor="center")

# # Submit button
# submit_button = tk.Button(root, text="Submit", font=("Arial", 16), width=20, height=2, command=submitted)
# submit_button.place(relx=0.5, rely=0.85, anchor="center")
# submit_button.config(state="disabled")

# Start the tkinter event loop
root.mainloop()
