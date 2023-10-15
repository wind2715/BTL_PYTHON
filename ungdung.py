import tkinter as tk
import tkinter.font as Font
from tkinter import ttk
import json
from PIL import Image, ImageTk, ImageDraw
import webcolors

def center_text(entry):
    text = entry.get()
    text_width = len(text)
    entry.config(justify="center")
    entry.delete(0, tk.END)
    entry.insert(0, text)

def add_subject(day, subject, time):
    if(subject != {}) :
        schedule[time][day] = subject['Môn học'] + "\n" + subject['Phòng học'] + "\n" + subject['Giáo viên']
    update_schedule_display()

def update_schedule_display():
    for day in days_of_week:
        for time_slot in time_slots:
            subject = schedule[time_slot][day]
            subject_entries[(day, time_slot)].configure(state = tk.NORMAL)
            if(subject != '') :
                subject_entries[(day, time_slot)].configure(disabledbackground = '#CFE2FF')
            else :
                subject_entries[(day, time_slot)].configure(disabledbackground = 'white')
            subject_entries[(day, time_slot)].delete(0, tk.END)
            subject_entries[(day, time_slot)].insert(0, subject)
            subject_entries[(day, time_slot)].configure(state = tk.DISABLED)
            center_text(subject_entries[(day, time_slot)])

def update_schedule_from_json():
    with open("schedule.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    for day in days_of_week:
        for time_slot in time_slots:
            subject = data.get(day, {}).get(time_slot, {})
            add_subject(day, subject, time_slot)

def create_rounded_frame(width, height, radius, color):
    image = Image.new("RGBA", (width, height), webcolors.hex_to_rgb('#EA4463'))
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, 2 * radius, 2 * radius), fill=color)
    draw.ellipse((width - 2 * radius, 0, width, 2 * radius), fill=color)
    draw.ellipse((0, height - 2 * radius, 2 * radius, height), fill=color)
    draw.ellipse((width - 2 * radius, height - 2 * radius, width, height), fill=color)
    draw.rectangle((radius, 0, width - radius, height), fill=color)
    draw.rectangle((0, radius, width, height - radius), fill=color)

    return ImageTk.PhotoImage(image)

# Create the main window
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight() - 80
root.geometry(f"{screen_width}x{screen_height}+0+0")
# root.resizable(width=False, height=False)
root.title("Thời Khóa Biểu Học Tập")

# Create a table for the schedule
days_of_week = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"]
time_slots = ["7h-8h", "8h-9h", "9h-10h", "10h-11h", "11h-12h", "12h-13h", "13h-14h", "14h-15h", "15h-16h", "16h-17h", "17h-18h"]
lession_slots = ["Tiết 1", "Tiết 2", "Tiết 3", "Tiết 4", "Tiết 5", "Tiết 6", "Tiết 7", "Tiết 8", "Tiết 9", "Tiết 10", "Tiết 11"]
schedule = {time: {day: "" for day in days_of_week} for time in time_slots}
subject_entries = {(day, time_slot): None for day in days_of_week for time_slot in time_slots}

# Tạo frame gốc và thiết lập để mở rộng theo cả chiều ngang và chiều dọc
frame0 = tk.Frame(root)
frame0.pack(fill=tk.BOTH, expand=True)

bgImage = ImageTk.PhotoImage(file='images/bg_main.png')
bgLabel = tk.Label(frame0, image=bgImage)
bgLabel.place(x=0, y=0)

# Tạo frame con 1 và đặt vào cột 0
frame1 = tk.Frame(frame0, background='#EA4463', width=400, height=screen_height)
frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx= 20, pady= 40)

# Tạo frame con 2 và đặt vào cột 1
frame2 = tk.Frame(frame0, background='#EA4463', width=screen_width - 400, height=screen_height)
frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx= 20, pady=40)

frame3 = tk.Frame(frame2, background= '#EA4463')
frame4 = tk.Frame(frame2, background= '#EA4463')
frame2.rowconfigure(0, weight= 8)
frame2.rowconfigure(1, weight= 1)
frame2.columnconfigure(0, weight= 1)

frame3.grid(row=0, column=0, sticky="nsew", pady = 10)
frame4.grid(row=1, column=0, sticky="nsew")

# frame1.pack(side = tk.TOP, fill = tk.BOTH, expand = True, pady = 20)
# frame2.pack(side = tk.TOP, fill = tk.BOTH, expand = True, padx= 10, pady= 20)
# frame2.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

#Xu ly frame1 : Thong tin sinh vien va dang xuat

rounded_frame1_image = create_rounded_frame(400, screen_height - 100, 30, "white")
rounded_frame1_label = tk.Label(frame1, image=rounded_frame1_image, borderwidth=0)
rounded_frame1_label.place(relx=0.5, rely=0.5, anchor="center")

label_frame1_info = tk.Label(rounded_frame1_label,width= rounded_frame1_label.winfo_width() - 20, height= rounded_frame1_label.winfo_height() - 20, background= 'white')
label_frame1_info.place(relx=0.5, rely=0.5, anchor="s")

tensinhvien = "Trần Hoàng Tuấn Vũ"
masinhvien = "B21DCCN800"
lop = "D21CQCN08-B"
gioitinh = "Nam"
ngaysinh = "21/20/2003"
nganh = "Công nghệ thông tin"

label_ten = tk.Label(label_frame1_info, text = "Họ và tên : {}".format(tensinhvien), background = '#ffffff', fg = '#000000', font = ("Arial", 19, 'bold')).pack(pady= 5)

# Mở hình ảnh bằng PIL
image = Image.open("user_ava_images\Trần Hoàng Tuấn Vũ.jpg")  # Thay đổi đường dẫn đến hình ảnh của bạn

# Thu nhỏ hình ảnh để có kích thước 100x100
image = image.resize((200, 200), Image.ADAPTIVE)

# Tạo một đối tượng ImageTk từ hình ảnh và đặt kích thước của nó
image_tk = ImageTk.PhotoImage(image)
image_label = tk.Label(label_frame1_info, image=image_tk)
image_label.pack(pady= 10)

label_ma = tk.Label(label_frame1_info, text = "Mã sinh viên : {}".format(masinhvien), background = '#ffffff', fg = '#000000', font = ("Arial", 15, )).pack(pady= 5)
label_lop = tk.Label(label_frame1_info, text = "Lớp : {}".format(lop), background = '#ffffff', fg = '#000000', font = ("Arial", 15, )).pack(pady= 5)
label_gioitinh = tk.Label(label_frame1_info, text = "Giới tính : {}".format(gioitinh), background = '#ffffff', fg = '#000000', font = ("Arial", 15, )).pack(pady= 5)
label_nganh = tk.Label(label_frame1_info, text = "Ngành : {}".format(nganh), background = '#ffffff', fg = '#000000', font = ("Arial", 15, )).pack(pady= 5)

button_signout = tk.Button(rounded_frame1_label, text = "Đăng xuất", borderwidth= 1, relief= "solid", background= '#A0151A', fg= 'white', font= ("Arial", 15))
button_signout.place(relx=0.5, rely=0.9, anchor= 's')

# Create a button to update the schedule from a JSON file
update_button = tk.Button(rounded_frame1_label, text="Cập nhật Thời Khóa Biểu", command=update_schedule_from_json, borderwidth= 1, relief= "solid", background= '#A0151A', fg= 'white', font= ("Arial", 15))
update_button.place(relx=0.5, rely=0.83, anchor= 's')

# Xu lys frame2 : TKB

frame3.rowconfigure(0, weight = 1)
frame3.rowconfigure(1, weight = 1)
frame3.rowconfigure(2, weight = 1)
frame3.rowconfigure(3, weight = 1)
frame3.rowconfigure(4, weight = 1)
frame3.rowconfigure(5, weight = 1)
frame3.rowconfigure(6, weight = 1)
frame3.rowconfigure(7, weight = 1)
frame3.rowconfigure(8, weight = 1)
frame3.rowconfigure(9, weight = 1)
frame3.rowconfigure(10, weight = 1)
frame3.rowconfigure(11, weight = 1)

frame3.columnconfigure(0, weight = 1, minsize=100)
frame3.columnconfigure(1, weight = 1, minsize=100)
frame3.columnconfigure(2, weight = 1, minsize=100)
frame3.columnconfigure(3, weight = 1, minsize=100)
frame3.columnconfigure(4, weight = 1, minsize=100)
frame3.columnconfigure(5, weight = 1, minsize=100)
frame3.columnconfigure(6, weight = 1, minsize=100)
frame3.columnconfigure(7, weight = 1, minsize=100)
frame3.columnconfigure(8, weight = 1, minsize=100)

tk.Label(frame3, text= "TRUOC", font = ('Arial', 15, 'bold'), bg= '#AD171C', fg = '#FFFFFF').grid(row=0, column=0, sticky=tk.W + tk.E + tk.S + tk.N)
tk.Label(frame3, text= "SAU", font = ('Arial', 15, 'bold'), bg= '#AD171C', fg = '#FFFFFF').grid(row=0, column=len(days_of_week) + 1, sticky=tk.W + tk.E + tk.S + tk.N)

for j, time_slot in enumerate(time_slots):
    tk.Label(frame3, text=time_slot, font = ('Arial', 15, 'bold'), bg= '#AD171C', fg = '#FFFFFF').grid(row=j+1, column=0, sticky=tk.W + tk.E + tk.S + tk.N)

for j, lession_slot in enumerate(lession_slots):
    tk.Label(frame3, text=lession_slot, font = ('Arial', 15, 'bold'), bg= '#AD171C', fg = '#FFFFFF').grid(row=j+1, column=len(days_of_week) + 1, sticky=tk.W + tk.E + tk.S + tk.N)


for i, day in enumerate(days_of_week):
    tk.Label(frame3, text=day, font = ('Arial', 15, 'bold'), bg= '#AD171C', fg = '#FFFFFF').grid(row=0, column=i+1, sticky=tk.W + tk.E + tk.S + tk.N)
    for j, time_slot in enumerate(time_slots):
        entry = tk.Entry(frame3, width= 19, state = tk.DISABLED, font = ("Arial", 12, 'bold'), disabledforeground="#000000", disabledbackground="white")
        entry.grid(row=j+1, column=i+1, sticky= tk.W + tk.E + tk.S + tk.N)
        subject_entries[(day, time_slot)] = entry

#Xử lý frame 4 các chức năng 


rounded_frame4_image = create_rounded_frame(1400, 52, 20, "white")
rounded_frame4_label = tk.Label(frame4, image=rounded_frame4_image, borderwidth=0)
rounded_frame4_label.place(relx=0.5, rely=0, anchor="n")


label_frame4_info = tk.Label(rounded_frame4_label,width= 175, height= 2, background= 'white')
label_frame4_info.place(relx= 0.5, rely = 0.5, anchor= 'center')

label_frame4_info.rowconfigure(0, weight=1)
label_frame4_info.columnconfigure(0, weight= 1)
label_frame4_info.columnconfigure(1, weight= 1)
label_frame4_info.columnconfigure(2, weight= 1)
label_frame4_info.columnconfigure(3, weight= 1)
label_frame4_info.columnconfigure(4, weight= 1)
label_frame4_info.columnconfigure(5, weight= 1)
label_frame4_info.columnconfigure(6, weight= 1)


subject_label = tk.Label(frame4, text="Môn học", bg= '#AD171C', font = ("Arial", 12, 'bold'), fg = 'white', width= 10)
subject_label.place(relx= 0.18, rely= 0.4, anchor= 'center')

subject_entry = tk.Entry(frame4, borderwidth= 1, relief='solid', font = ("Arial", 12))
subject_entry.place(relx= 0.29, rely= 0.4, anchor= 'center')

time_label = tk.Label(frame4, text="Thời gian", bg= '#AD171C', font = ("Arial", 12, 'bold'), fg = 'white', width= 10)
time_label.place(relx= 0.4, rely= 0.4, anchor= 'center')

style = ttk.Style()
style.theme_use("winnative")
style.configure("TCombobox", font=("Arial", 12))

time_combobox = tk.StringVar(value=time_slots[0])
time_combobox_widget = ttk.Combobox(frame4, textvariable=time_combobox, values=time_slots, state="readonly")
time_combobox_widget.place(relx= 0.495, rely= 0.4, anchor= 'center')

day_label = tk.Label(frame4, text="Thứ", bg= '#AD171C', font = ("Arial", 12, 'bold'), fg = 'white', width= 5)
day_label.place(relx= 0.575, rely= 0.4, anchor= 'center')

day_combobox = tk.StringVar(value=days_of_week[0])

day_combobox_widget = ttk.Combobox(frame4, textvariable=day_combobox, values=days_of_week, state="readonly")
day_combobox_widget.place(relx=0.655, rely=0.4, anchor='center')

add_button = tk.Button(frame4, text="Thêm Môn Học", bg= '#AD171C', font = ("Arial", 12, 'bold'), fg = 'white', command=lambda: add_subject(day_combobox.get(), subject_entry.get(), time_combobox.get()))
add_button.place(relx= 0.8, rely= 0.4, anchor= 'center')

# Open the window
root.mainloop()
