from tkinter import *
from tkinter import simpledialog
from PIL import ImageTk, Image
import datetime
import os
import tkinter as tk
import webbrowser
import re
from tkinter import Tk, Frame, Label
from tkinter import messagebox
from datetime import datetime
import requests
from tkinter import Text
from pygame import mixer

# Global variables for managing music playlist
music_directory = "music"
music_files = []
current_track_index = 0

# Function to load MP3 files from the "music" directory
def load_music_files():
    global music_files
    music_files = [f for f in os.listdir(music_directory) if f.endswith(".mp3")]

# Function to play the current track
def play_current_track():
    try:
        mixer.init()
        mixer.music.load(os.path.join(music_directory, music_files[current_track_index]))
        mixer.music.play()
    except Exception as e:
        print(f"Error playing music: {e}")

# Function to play the next track
def play_next_track():
    global current_track_index
    current_track_index = (current_track_index + 1) % len(music_files)
    play_current_track()

# Function to play the previous track
def play_previous_track():
    global current_track_index
    current_track_index = (current_track_index - 1) % len(music_files)
    play_current_track()

# Function to stop the music
def stop_music():
    try:
        mixer.music.stop()
    except Exception as e:
        print(f"Error stopping music: {e}")


def fetch_and_display_quote():
    try:
        # Make a request to the ZenQuotes API
        response = requests.get("https://zenquotes.io/api/random")
        data = response.json()

        # Extract the quote and author from the response
        quote = data[0]['q']
        author = data[0]['a']

        # Display the quote in the quotes_frame
        quote_text.config(state="normal")  # Enable editing
        quote_text.delete("1.0", "end")  # Clear previous content
        quote_text.insert("1.0", f'"{quote}"\n\n- {author}')  # Insert new quote
        quote_text.config(state="disabled")  # Disable editing

    except Exception as e:
        print(f"Error fetching quote: {e}")
def save_data_to_file():
    with open("dulieu.txt", "w") as file:
        # Writing header
        file.write("Task,Description,Time,Checkbox\n")
        for i in range(2, 20):
            task_value = task_entries[i - 2].get()
            description_value = description_entries[i - 2].get()
            time_value = time_entries[i - 2].get()
            checkbox_value = "1" if checkbox_entries[i - 2].get() else "0"
            file.write(f"{task_value},{description_value},{time_value},{checkbox_value}\n")


def load_data_from_file():
    load_goal_from_file()
    clear_all_colors()
    if os.path.exists("dulieu.txt"):
        with open("dulieu.txt", "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines[1:]):
                data = line.strip().split(',')
                task_entries[i].insert(0, data[0])
                description_entries[i].insert(0, data[1])
                time_entries[i].insert(0, data[2])

                # Update this part
                checkbox_entries[i].set(int(data[3].strip()))
                pattern = re.compile(r'^\d{2}:\d{2} - \d{2}:\d{2}$')
                time_entry_value = str(data[2])
                check = bool(pattern.match(time_entry_value))
                if check:
                    print("a")
                    a = int(str(time_entry_value[0]) + str(time_entry_value[1]))
                    b = int(str(time_entry_value[3]) + str(time_entry_value[4])) / 10
                    c = int(str(time_entry_value[8]) + str(time_entry_value[9]))
                    d = int(str(time_entry_value[11]) + str(time_entry_value[12])) / 10
                    for k in range(a, c + 1):
                        for n in range(1, 8):
                            if (k == a and n >= b):
                                highlight_cell(k + 1, n, "red")
                            elif (k > a and k < c):
                                highlight_cell(k + 1, n, "red")
                            elif (k == c and n <= d):
                                highlight_cell(k + 1, n, "red")


class HourlySchedule(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_hourly_table()

    def create_hourly_table(self):
        self.cell_width = 50
        self.cell_height = 28

        for row in range(25):
            for col in range(7):
                x1 = col * self.cell_width
                y1 = row * self.cell_height
                x2 = (col + 1) * self.cell_width
                y2 = (row + 1) * self.cell_height

                # Create a rectangle for each cell with a tag indicating its position
                cell_tag = f"{row * 7 + col}"
                self.create_rectangle(x1, y1, x2, y2, fill="white", outline="black", tags=cell_tag)

                # Add column names for the first row
                if row == 0 and col != 0:
                    col_name = f"{col * 10}"
                    self.create_text((x1 + x2) / 2, y1 + 15, text=col_name, font=("Arial", 8))
                # Add row names for the first column (excluding the first row)
                elif col == 0 and row != 0:
                    row_name = str(row - 1)
                    self.create_text(x1 + 25, (y1 + y2) / 2, text=row_name, font=("Arial", 8))

def clear_all_colors():
    for row in range(25):
        for col in range(7):
            hourly_schedule.delete(f"{row * 7 + col}_highlight")
# def highlight_cell(row, col, color="yellow"):
#     x1 = col * hourly_schedule.cell_width
#     y1 = row * hourly_schedule.cell_height
#     x2 = (col + 1) * hourly_schedule.cell_width
#     y2 = (row + 1) * hourly_schedule.cell_height
#
#     # Delete any existing highlighting in the cell
#     hourly_schedule.delete(f"{row * 7 + col}_highlight")
#
#     # Create a rectangle with the specified color and tag it for future deletion
#     hourly_schedule.create_rectangle(x1, y1, x2, y2, fill=color, outline="", tags=f"{row * 7 + col}_highlight")
# Dictionary to store the count of each cell
highlight_counts = {}

def highlight_cell(row, col, color="yellow"):
    global highlight_counts

    # Update the count for this cell
    cell_key = f"{row * 7 + col}"
    count = highlight_counts.get(cell_key, 0)
    count += 1
    highlight_counts[cell_key] = count

    # Choose color based on the count
    if count == 1:
        cell_color = "red"
    elif count == 2:
        cell_color = "yellow"
    elif count > 2:
        cell_color = "green"

    x1 = col * hourly_schedule.cell_width
    y1 = row * hourly_schedule.cell_height
    x2 = (col + 1) * hourly_schedule.cell_width
    y2 = (row + 1) * hourly_schedule.cell_height

    # Delete any existing highlighting in the cell
    hourly_schedule.delete(f"{cell_key}_highlight")

    # Create a rectangle with the specified color and tag it for future deletion
    hourly_schedule.create_rectangle(x1, y1, x2, y2, fill=cell_color, outline="", tags=f"{cell_key}_highlight")

def logout():
    daily_window.destroy()
    import Login
def open_notion():
    webbrowser.open('https://www.notion.so/')
task_entries = []
description_entries = []
time_entries = []
checkbox_entries = []
checkbox_vars = []
def create_table():
    table_frame = Frame(daily_window, bg='white', width=500, height=300)
    table_frame.place(x=610, y=10)

    # Table title
    table_title = Label(table_frame, text='Task List', font=('Open Sans', 16, 'bold'), bg='white', padx=5)
    table_title.grid(row=0, column=0, columnspan=4, pady=10)

    # Column labels
    task_label = Label(table_frame, text='Task', font=('Open Sans', 12, 'bold'), bg='white', padx=5)
    task_label.grid(row=1, column=0, sticky='e')  # Align to the right

    description_label = Label(table_frame, text='Description', font=('Open Sans', 12, 'bold'), bg='white', padx=5)
    description_label.grid(row=1, column=1)

    time_label = Label(table_frame, text='Time', font=('Open Sans', 12, 'bold'), bg='white', padx=5)
    time_label.grid(row=1, column=2)

    checkbox_label = Label(table_frame, text='Checkbox', font=('Open Sans', 12, 'bold'), bg='white', padx=5)
    checkbox_label.grid(row=1, column=3, sticky='e')  # Align to the right

    # Create 15 rows with checkboxes
    for i in range(2, 20):
        task_entry = Entry(table_frame, width=10 if i != 1 else 20, font=('Open Sans', 10), bd=1)
        task_entry.grid(row=i, column=0, padx=5, pady=5, sticky='e' if i != 1 else 'w')
        task_entries.append(task_entry)

        description_entry = Entry(table_frame, width=20, font=('Open Sans', 10), bd=1)
        description_entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')
        description_entries.append(description_entry)

        time_entry = Entry(table_frame, width=20, font=('Open Sans', 10), bd=1)
        time_entry.grid(row=i, column=2, padx=5, pady=5, sticky='w', ipady = 2)
        time_entries.append(time_entry)

        checkbox_var = tk.IntVar()
        checkbox = Checkbutton(table_frame, variable=checkbox_var, bg='white')
        checkbox.grid(row=i, column=3, padx=5, pady=5, sticky='s')
        checkbox_entries.append(checkbox_var)

        # Add Submit button at the bottom
    submit_button = Button(table_frame, text='Submit', command=submit_table, font=('Open Sans', 12), bg='white',
                           width=9,
                           activebackground='white', bd=1)
    submit_button.grid(row=20, column=0, columnspan=4, pady=10)



def save_goal_to_file():
    with open("goal.txt", "w") as file:
        file.write(goal_text.get("1.0", tk.END))

def load_goal_from_file():
    if os.path.exists("goal.txt"):
        with open("goal.txt", "r") as file:
            goal_text.delete("1.0", tk.END)
            goal_text.insert(tk.END, file.read())

def submit_table():
    global highlight_counts
    highlight_counts = {}
    clear_all_colors()
    for i in range(2, 20):
        task_entry_value = task_entries[i - 2].get()
        description_entry_value = description_entries[i - 2].get()
        time_entry_value = time_entries[i - 2].get()
        check_entry_value = checkbox_entries[i - 2].get()  # Use get() to get the IntVar value

        # print(task_entry_value, description_entry_value, time_entry_value, check_entry_value)

        pattern = re.compile(r'^\d{2}:\d{2} - \d{2}:\d{2}$')
        check = bool(pattern.match(time_entry_value))
        if check:
            a = int(str(time_entry_value[0]) + str(time_entry_value[1]))
            b = int(str(time_entry_value[3]) + str(time_entry_value[4]))/10
            c = int(str(time_entry_value[8]) + str(time_entry_value[9]))
            d = int(str(time_entry_value[11]) + str(time_entry_value[12]))/10
            for k in range (a, c + 1):
                for n in range (1, 8):
                    if (k == a and n >= b):
                        highlight_cell(k + 1, n, "red")
                    elif (k > a and k < c):
                        highlight_cell(k + 1, n, "red")
                    elif(k == c and n <= d):
                        highlight_cell(k + 1, n, "red")
    save_data_to_file()
    save_goal_to_file()



daily_window = Tk()
daily_window.geometry('{}x{}+0+0'.format(daily_window.winfo_screenwidth(), daily_window.winfo_screenheight() - 40))
daily_window.resizable(0, 0)
daily_window.title('10 Min Planner Daily Page')

bgImage = ImageTk.PhotoImage(file='bg_main.png')
bgLabel = Label(daily_window, image=bgImage)
bgLabel.place(x=0, y=0)

student_frame = Frame(daily_window, bg='white', width=200, height=100)
student_frame.place(x=10, y=10)

login_label = Label(student_frame, text='Đăng nhập', font=('Open Sans', 15, 'bold'), bg='white')
login_label.grid(row=0, column=0, columnspan=2, pady=5, sticky='w', padx=70)

id_label = Label(student_frame, text='Tài khoản:', font=('Open Sans', 10), bg='white')
id_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

name_label = Label(student_frame, text='Họ và tên:', font=('Open Sans', 10), bg='white')
name_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

id_entry = Entry(student_frame, width=15, font=('Open Sans', 10), bd=0)
id_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

name_entry = Entry(student_frame, width=15, font=('Open Sans', 10), bd=0)
name_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

id_entry.insert(0, '123456')
name_entry.insert(0, 'John Doe')

id_entry.config(width=20)
name_entry.config(width=20)

logout_button = Button(student_frame, text='Đăng xuất', command=logout, font=('Open Sans', 12), bg='white', width=10,
                      activebackground='white', bd=1)
logout_button.grid(row=3, column=0, columnspan=2, pady=5, padx=70, sticky='w')

func_frame = Frame(daily_window, bg='white', width=250, height=140)
func_frame.place(x=10, y=260)

func_label = Label(func_frame, text='Tính năng', font=('Open Sans', 15, 'bold'), bg='white')
func_label.grid(row=0, column=0, columnspan=2, pady=5, sticky='w', padx=70)

notion_button = Button(func_frame, text='Mở Notion', command=open_notion, font=('Open Sans', 10, 'underline'), bg='white', width=10,
                       activebackground='white', bd=0)
notion_button.grid(row=1, column=0, padx=5, pady=5, sticky='w')

# Load music files when the program starts
load_music_files()
play_button = Button(func_frame, text='Play Music', command=play_current_track, font=('Open Sans', 10), bg='white', width=10,
                     activebackground='white', bd=0)
play_button.grid(row=2, column=0, padx=5, pady=5, sticky='w')

stop_button = Button(func_frame, text='Stop Music', command=stop_music, font=('Open Sans', 10), bg='white', width=10,
                     activebackground='white', bd=0)
stop_button.grid(row=2, column=1, padx=5, pady=5, sticky='w')

next_button = Button(func_frame, text='Next Track', command=play_next_track, font=('Open Sans', 10), bg='white', width=10,
                     activebackground='white', bd=0)
next_button.grid(row=3, column=1, padx=5, pady=5, sticky='w')

prev_button = Button(func_frame, text='Previous Track', command=play_previous_track, font=('Open Sans', 10), bg='white', width=13,
                      activebackground='white', bd=0)
prev_button.grid(row=3, column=0, padx=5, pady=5, sticky='w')

stop_button = Button(func_frame, text='Stop Music', command=stop_music, font=('Open Sans', 10), bg='white', width=10,
                     activebackground='white', bd=0)
stop_button.grid(row=2, column=1, padx=5, pady=5, sticky='w')

hourly_schedule_bg = Frame(daily_window, width=355, height=755, bg = 'white')
hourly_schedule_bg.place(x=1135, y=10)

hourly_schedule = HourlySchedule(daily_window, width=350, height=700)
hourly_schedule.place(x=1137, y=62)

text_label = Label(daily_window, text="Time Table", font=('Open Sans', 16, "bold"), padx=0, bg = "white")

# Place the label with specified padding
text_label.place(x=1135, y=20)
#

# Hiển thị tên frame bên trong frame đó
def update_datetime_label():
    # Lấy ngày giờ hiện tại
    current_datetime = datetime.now()

    # Hiển thị ngày theo định dạng "ngày - tháng - năm"
    date_str = current_datetime.strftime("Date: %d - %m - %Y")
    date_label.config(text=date_str)

    # Hiển thị giờ hiện tại
    time_str = current_datetime.strftime("Time: %H:%M:%S")
    time_label.config(text=time_str)
    # Lặp lại cập nhật sau 1000 miliseconds (1 giây)
    date_label.after(1000, update_datetime_label)


my_frame = Frame(daily_window, width=300, height=200, bg='white')
my_frame.place(x=284, y=10)

# Tạo label để hiển thị ngày
date_label = Label(my_frame, text="", font=('Open Sans', 16, 'bold'), bg='white', fg='black')
date_label.grid(row=0, column=0, pady=0)

# Tạo label để hiển thị giờ
time_label = Label(my_frame, text="", font=('Open Sans', 16, 'bold'), bg='white', fg='black')
time_label.grid(row=1, column=0, pady=0)

goal_frame = Frame(daily_window, width=300, height=350, bg='white')
goal_frame.place(x=284, y=100)
goal_heading = Label(goal_frame, text="Goals", font=('Open Sans', 16, 'bold'), bg='white', fg='black')
goal_heading.place(x = 5, y = 5)
goal_text = Text(goal_frame, font=('Open Sans', 12), bd=1, wrap=tk.WORD)
goal_text.place(x=10, y=40, width=200, height=100)
# Gọi hàm để cập nhật ngày giờ liên tục


# Create the quotes_frame and related widgets
quotes_frame = Frame(daily_window, width=300, height=290, bg='white')
quotes_frame.place(x=284, y=475)

quotes_heading = Label(quotes_frame, text="Quotes", font=('Open Sans', 16, 'bold'), bg='white', fg='black')
quotes_heading.place(x=5, y=5)

quote_text = Text(quotes_frame, font=('Open Sans', 12), bd=1, wrap="word", state="disabled", height=5)
quote_text.place(x=10, y=40, width=280, height=100)

# Add a button to fetch and display a new quote
fetch_quote_button = Button(quotes_frame, text="Fetch Quote", command=fetch_and_display_quote,
                            font=('Open Sans', 12), bg='white', width=12, activebackground='white', bd=1)
fetch_quote_button.place(x=100, y=160)

# Fetch and display a quote when the program starts
fetch_and_display_quote()

update_datetime_label()
create_table()
load_data_from_file()
daily_window.mainloop()