from tkinter import *
from tkinter import simpledialog
from PIL import ImageTk, Image
import datetime
import os
import webbrowser
from tkinter import messagebox

class DailyWindow:
    def __init__(self, master):
        self.master = master
        self.master.geometry('{}x{}+0+0'.format(self.master.winfo_screenwidth(), self.master.winfo_screenheight() - 40))
        self.master.resizable(0, 0)
        self.master.title('10 Min Planner Daily Page')

        bgImage = ImageTk.PhotoImage(file='bg_main.png')
        bgLabel = Label(self.master, image=bgImage)
        bgLabel.place(x=0, y=0)

        self.student_frame = Frame(self.master, bg='white', width=200, height=100)
        self.student_frame.place(x=10, y=10)

        login_label = Label(self.student_frame, text='Đăng nhập', font=('Open Sans', 15, 'bold'), bg='white')
        login_label.grid(row=0, column=0, columnspan=2, pady=5, sticky='w', padx=70)

        id_label = Label(self.student_frame, text='Tài khoản:', font=('Open Sans', 10), bg='white')
        id_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        name_label = Label(self.student_frame, text='Họ và tên:', font=('Open Sans', 10), bg='white')
        name_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

        id_entry = Entry(self.student_frame, width=15, font=('Open Sans', 10), bd=0)
        id_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        name_entry = Entry(self.student_frame, width=15, font=('Open Sans', 10), bd=0)
        name_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        id_entry.insert(0, '123456')
        name_entry.insert(0, 'John Doe')

        id_entry.config(width=20)
        name_entry.config(width=20)

        logout_button = Button(self.student_frame, text='Đăng xuất', command=self.logout, font=('Open Sans', 12), bg='white', width=10,
                               activebackground='white', bd=1)
        logout_button.grid(row=3, column=0, columnspan=2, pady=5, padx=70, sticky='w')

        self.func_frame = Frame(self.master, bg='white', width=250, height=140)
        self.func_frame.place(x=10, y=260)

        func_label = Label(self.func_frame, text='Tính năng', font=('Open Sans', 15, 'bold'), bg='white')
        func_label.grid(row=0, column=0, columnspan=2, pady=5, sticky='w', padx=70)

        notion_button = Button(self.func_frame, text='Mở Notion', command=self.open_notion, font=('Open Sans', 10, 'underline'), bg='white', width=10,
                               activebackground='white', bd=0)
        notion_button.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.create_hourly_table()

    def create_hourly_table(self):
        cell_width = 50
        cell_height = 30

        for row in range(24):
            for col in range(6):
                x1 = col * cell_width
                y1 = row * cell_height
                x2 = (col + 1) * cell_width
                y2 = (row + 1) * cell_height

                self.master.create_rectangle(x1, y1, x2, y2, fill="white", outline="black", tags=f"{row * 6 + col}")

    def logout(self):
        self.master.destroy()
        import Login

    def open_notion(self):
        webbrowser.open('https://www.notion.so/')

if __name__ == "__main__":
    daily_window = Tk()
    app = DailyWindow(daily_window)
    daily_window.mainloop()
