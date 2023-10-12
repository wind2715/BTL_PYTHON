from tkinter import *
from tkinter import simpledialog
from PIL import ImageTk, Image
import datetime
import os
import tkinter as tk
import webbrowser
import re
from tkinter import messagebox

def logout():
    daily_window.destroy()
    import Login
def open_notion():
    webbrowser.open('https://www.notion.so/')
task_entries = []
description_entries = []
time_entries = []
checkbox_entries = []
def create_table():
    table_frame = Frame(daily_window, bg='white', width=500, height=300)
    table_frame.place(x=300, y=10)

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
    for i in range(2, 17):
        task_entry = Entry(table_frame, width=10 if i != 1 else 20, font=('Open Sans', 10), bd=1)
        task_entry.grid(row=i, column=0, padx=5, pady=5, sticky='e' if i != 1 else 'w')
        task_entries.append(task_entry)

        description_entry = Entry(table_frame, width=20, font=('Open Sans', 10), bd=1)
        description_entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')
        description_entries.append(description_entry)

        time_entry = Entry(table_frame, width=20, font=('Open Sans', 10), bd=1)
        time_entry.grid(row=i, column=2, padx=5, pady=5, sticky='w')
        time_entries.append(time_entry)

        checkbox = Checkbutton(table_frame, bg='white')
        checkbox.grid(row=i, column=3, padx=5, pady=5, sticky='s')
        checkbox_entries.append(checkbox)

        # Add Submit button at the bottom
    submit_button = Button(table_frame, text='Submit', command=submit_table, font=('Open Sans', 12), bg='white',
                           width=10,
                           activebackground='white', bd=1)
    submit_button.grid(row=17, column=0, columnspan=4, pady=10)


def submit_table():
    for i in range(2, 17):
        task_entry_value = task_entries[i - 2].get()
        description_entry_value = description_entries[i - 2].get()
        time_entry_value = time_entries[i - 2].get()
        pattern = re.compile(r'^\d{2}:\d{2} - \d{2}:\d{2}$')
        check = bool(pattern.match(time_entry_value))
        print(f"Row {i}: Task={task_entry_value}, Description={description_entry_value}, Time={time_entry_value}, Check = {check}")
        # Use regular expression to check the format "a:b - c:d"





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


hourly_schedule = HourlySchedule(daily_window, width=350, height=700)
hourly_schedule.place(x=800, y=45)

text_label = Label(daily_window, text="Time Table", font=('Open Sans', 12), bg='white')

# Place the label with specified padding
text_label.place(x=900, y=10)

create_table()
daily_window.mainloop()