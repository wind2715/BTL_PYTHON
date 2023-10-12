from tkinter import *
from tkinter import simpledialog
from PIL import ImageTk, Image
import datetime
import os
import webbrowser
from tkinter import messagebox

events_dict = {}
days_frame = None  # Define days_frame outside the function


def logout():
    weekly_window.destroy()


def add_event(day):
    popup = Toplevel(weekly_window)
    popup.title('Thêm sự kiện')

    event_info = {}

    def submit_event():
        event_info['name'] = name_entry.get()
        event_info['time'] = time_entry.get()
        event_info['room'] = room_entry.get()
        event_info['instructor'] = instructor_entry.get()

        if event_info['name']:
            if day not in events_dict:
                events_dict[day] = []

            events_dict[day].append(event_info)
            update_gui()
            popup.destroy()

    name_label = Label(popup, text='Tên sự kiện:', font=('Open Sans', 12))
    name_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    name_entry = Entry(popup, font=('Open Sans', 12), bd=1)
    name_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    time_label = Label(popup, text='Thời gian (từ đến):', font=('Open Sans', 12))
    time_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
    time_entry = Entry(popup, font=('Open Sans', 12), bd=1)
    time_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    room_label = Label(popup, text='Phòng học:', font=('Open Sans', 12))
    room_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')
    room_entry = Entry(popup, font=('Open Sans', 12), bd=1)
    room_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    instructor_label = Label(popup, text='Tên giảng viên:', font=('Open Sans', 12))
    instructor_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')
    instructor_entry = Entry(popup, font=('Open Sans', 12), bd=1)
    instructor_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')

    submit_button = Button(popup, text='Submit', command=submit_event, font=('Open Sans', 12), bg='white', width=10,
                           activebackground='white', bd=1)
    submit_button.grid(row=4, column=1, pady=10, sticky='e')


def open_notion():
    webbrowser.open('https://www.notion.so/')


def show_event_details(day, event_index):
    popup = Toplevel(weekly_window)
    popup.title('Chi tiết sự kiện')

    event_info = events_dict[day][event_index]

    details_label = Label(popup, text=f"Tên việc làm: {event_info['name']}\n"
                                     f"Thời gian: {event_info['time']}\n"
                                     f"Phòng học: {event_info['room']}\n"
                                     f"Tên giảng viên: {event_info['instructor']}",
                          font=('Open Sans', 12), padx=20, pady=20)
    details_label.pack()


def update_gui():
    for widget in days_frame.winfo_children():
        widget.destroy()

    current_date = datetime.datetime.now()
    start_of_week = current_date - datetime.timedelta(days=current_date.weekday())
    month_label = Label(days_frame, text=start_of_week.strftime('%B %Y'), font=('Open Sans', 20), bg='white',
                        relief='solid', bd=0)
    month_label.grid(row=0, columnspan=8, pady=5)

    event_width = 170  # Set the desired width for each event

    for i in range(7):
        day_number = (start_of_week + datetime.timedelta(days=i)).day
        day_label = Label(days_frame,
                          text=f'{(start_of_week + datetime.timedelta(days=i)).strftime("%a")}\n{day_number}',
                          font=('Open Sans', 12), bg='white', relief='solid', borderwidth=1,
                          width=16, height=2)

        day_label.bind("<Button-1>", lambda event, day=day_number: add_event(day))
        day_label.grid(row=1, column=i, padx=5, pady=0, ipadx=10, ipady=2)
        days_frame.columnconfigure(i, weight=1)

        if day_number in events_dict:
            canvas_width = event_width + 20  # Add some padding if needed
            canvas = Canvas(days_frame, bg='white', width=canvas_width, height=400, bd=0, highlightthickness=0)
            canvas.grid(row=2, column=i, padx=0, pady=0, ipadx=0, ipady=2, sticky='nsew')

            for j, event_info in enumerate(events_dict[day_number]):
                event_frame_width = event_width
                event_frame = Frame(canvas, bg='white', relief='solid', bd=1, width=event_frame_width, height=day_label.winfo_height())
                event_frame.pack(pady=5)

                event_label_text = f"Name: {event_info['name']}\nThời gian: {event_info['time']}"

                event_label = Label(event_frame, text=event_label_text,
                                    font=('Open Sans', 10), bg='white', anchor='w', justify='left', wraplength=event_frame_width)
                event_label.pack(pady=5)

                event_label.bind("<Button-1>", lambda event, day=day_number, index=j: show_event_details(day, index))

    days_frame.columnconfigure(7, weight=1)


weekly_window = Tk()

screen_width = 1250
screen_height = 800
weekly_window_width = weekly_window.winfo_screenwidth()
screen_height_height2 = weekly_window.winfo_screenheight() - 40
weekly_window.geometry('{}x{}+0+0'.format(weekly_window_width, screen_height_height2))

weekly_window.resizable(0, 0)
weekly_window.title('Weekly Page')

bgImage = ImageTk.PhotoImage(file='bg_main.png')
bgLabel = Label(weekly_window, image=bgImage)
bgLabel.place(x=0, y=0)

student_frame = Frame(weekly_window, bg='white', width=200, height=100)
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

func_frame = Frame(weekly_window, bg='white', width=250, height=140)
func_frame.place(x=10, y=260)

func_label = Label(func_frame, text='Tính năng', font=('Open Sans', 15, 'bold'), bg='white')
func_label.grid(row=0, column=0, columnspan=2, pady=5, sticky='w', padx=70)

notion_button = Button(func_frame, text='Mở Notion', command=open_notion, font=('Open Sans', 10, 'underline'), bg='white', width=10,
                       activebackground='white', bd=0)
notion_button.grid(row=1, column=0, padx=5, pady=5, sticky='w')

days_frame = Frame(weekly_window, bg='white')
days_frame.place(x=280, y=10)

update_gui()

weekly_window.mainloop()