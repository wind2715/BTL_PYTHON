import tkinter as tk
import tkinter.font as Font
from tkinter import ttk
import json
from PIL import Image, ImageTk, ImageDraw
import webcolors
import datetime
import token_storage
from get_data_api import get_ds_nhom_to, get_token
from firebase_config import db


def get_datas():
    token = token_storage.stored_token
    doc_ref = db.collection("sinhVien").document(token).get().to_dict()
    msv = doc_ref['msv']
    password = doc_ref['password']
    data = get_ds_nhom_to(get_token(msv, password))
    return data


datas = get_datas()
print(datas)


def center_text(entry):
    text = entry.get()
    text_width = len(text)
    entry.config(justify="center")
    entry.delete(0, tk.END)
    entry.insert(0, text)


def add_subject1(day, subject, time):
    update_schedule_to_data_private(day, subject, time)


def update_schedule_to_data_private(day, subject, time):
    with open("datas/home_screen/data_private.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    day_first_selected = combobox_weeks.get()[5:15]
    with open("datas/home_screen/weeks_time.json", "r", encoding="utf-8") as json2_file:
        week_select = json.load(json2_file)
    # Bước 2: Thay đổi dữ liệu
    data[week_select[day_first_selected]][day][time] = subject

    # Bước 3: Lưu tệp JSON
    with open('datas/home_screen/data_private.json', 'w', encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def add_subject2(day, subject, time):
    if (subject != {} and (subject['Môn học'] != '')):
        schedule[time][day] = subject['Môn học'] + "\n" + subject['Phòng học']
    else:
        schedule[time][day] = ""
    update_schedule_display()


def update_schedule_display():
    with open("datas/home_screen/data_private.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    day_first_selected = combobox_weeks.get()[5:15]
    with open("datas/home_screen/weeks_time.json", "r", encoding="utf-8") as json2_file:
        week_select = json.load(json2_file)
    for day in days_of_week:
        for time_slot in time_slots:
            subject = schedule[time_slot][day]
            if data.get(week_select[day_first_selected], {}).get(day, {}).get(time_slot, "") != '':
                subject += " ( " + data.get(week_select[day_first_selected], {}).get(day, {}).get(time_slot, "") + " )"
            text_widget = subject_entries[(day, time_slot)]
            text_widget.configure(state=tk.NORMAL)
            text_widget.delete('1.0', tk.END)  # Xóa toàn bộ nội dung trong Text widget
            if subject != '':
                text_widget.configure(background='#CFE2FF')
            else:
                text_widget.configure(background='white')
            text_widget.insert(tk.END, subject)  # Chèn dữ liệu mới từ đầu
            text_widget.configure(state=tk.DISABLED)
            # Tạo một kiểu dáng (tag) tùy chỉnh để căn giữa
            text_widget.tag_configure("center", justify='center', spacing1=5, spacing2=1)

            # Áp dụng kiểu dáng "center" cho văn bản trong Text Widget
            text_widget.tag_add("center", "1.0", "end")

            bold_font = ("Arial", SIZE_SMALL(screen_width, screen_height), "bold")

            # Đặt phong cách chữ cho dòng đầu
            text_widget.tag_configure("bold", font=bold_font)
            text_widget.tag_add("bold", "1.0", "1.end")


def update_schedule_from_json():
    day_first_selected = combobox_weeks.get()[5:15]
    with open("datas/home_screen/schedule.json", "r", encoding="utf-8") as json1_file:
        data = json.load(json1_file)
    with open("datas/home_screen/weeks_time.json", "r", encoding="utf-8") as json2_file:
        week_select = json.load(json2_file)
    for day in days_of_week:
        for time_slot in time_slots:
            subject = data.get(week_select[day_first_selected], {}).get(day, {}).get(time_slot, {})
            add_subject2(day, subject, time_slot)


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
print(screen_width, screen_height)
root.geometry(f"{screen_width}x{screen_height}+0+0")
# root.resizable(width=False, height=False)
root.title("Thời Khóa Biểu Học Tập")


def SIZE_SMALL(width, height):
    if (width >= 1920 and height >= 1080 - 80):
        return 12
    elif (width >= 1600 and height >= 900 - 80):
        return 10
    elif (width >= 1280 and height >= 720 - 80):
        return 8
    elif (width >= 800 and height >= 600 - 80):
        return 6


def SIZE_NORMAL(width, height):
    if (width >= 1920 and height >= 1080 - 80):
        return 15
    elif (width >= 1600 and height >= 900 - 80):
        return 13
    elif (width >= 1280 and height >= 720 - 80):
        return 11
    elif (width >= 800 and height >= 600 - 80):
        return 9


def SIZE_BIG(width, height):
    if (width >= 1920 and height >= 1080 - 80):
        return 19
    elif (width >= 1600 and height >= 900 - 80):
        return 16
    elif (width >= 1280 and height >= 720 - 80):
        return 14
    elif (width >= 800 and height >= 600 - 80):
        return 12


# Create a table for the schedule
days_of_week = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"]
time_slots = ["7h-8h", "8h-9h", "9h-10h", "10h-11h", "11h-12h", "12h-13h", "13h-14h", "14h-15h", "15h-16h", "16h-17h",
              "17h-18h", "18h-19h", "19h-20h", "20h-21h"]
lession_slots = ["Tiết 1", "Tiết 2", "Tiết 3", "Tiết 4", "Tiết 5", "Tiết 6", "Tiết 7", "Tiết 8", "Tiết 9", "Tiết 10",
                 "Tiết 11", "Tiết 12", "Tiết 13", "Tiết 14"]
schedule = {time: {day: "" for day in days_of_week} for time in time_slots}
subject_entries = {(day, time_slot): None for day in days_of_week for time_slot in time_slots}

# Tạo frame gốc và thiết lập để mở rộng theo cả chiều ngang và chiều dọc
frame0 = tk.Frame(root)
frame0.pack(fill=tk.BOTH, expand=True)

bgImage = ImageTk.PhotoImage(file='images/login_screen/bg_main.png')
bgLabel = tk.Label(frame0, image=bgImage)
bgLabel.place(x=0, y=0)

# Tạo frame con 1 và đặt vào cột 0
frame1_width = width = screen_width / 4
frame1_height = screen_height
frame1 = tk.Frame(frame0, background='#EA4463', width=frame1_width, height=frame1_height)
frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=40)

# Tạo frame con 2 và đặt vào cột 1
frame2_width = screen_width - frame1_width
frame2_height = screen_height
frame2 = tk.Frame(frame0, background='#EA4463', width=frame2_width, height=frame2_height)
frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=40)

frame5_height = frame2_height * (1 / 9)
frame5_width = frame2_width
frame4_height = frame2_height * (1 / 9)
frame4_width = frame2_width
frame3_height = frame2_height - frame4_height - frame5_height
frame3_width = frame2_width
frame5 = tk.Frame(frame2, background='#EA4463')
frame3 = tk.Frame(frame2, background='#EA4463')
frame4 = tk.Frame(frame2, background='#EA4463')

frame2.rowconfigure(0, weight=1)
frame2.rowconfigure(1, weight=6)
frame2.rowconfigure(2, weight=1)
frame2.columnconfigure(0, weight=1)

frame5.grid(row=0, column=0, sticky="nsew")
frame3.grid(row=1, column=0, sticky="nsew", pady=10)
frame4.grid(row=2, column=0, sticky="nsew")

# frame1.pack(side = tk.TOP, fill = tk.BOTH, expand = True, pady = 20)
# frame2.pack(side = tk.TOP, fill = tk.BOTH, expand = True, padx= 10, pady= 20)
# frame2.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

# Xu ly frame1 : Thong tin sinh vien va dang xuat

rounded_frame1_image = create_rounded_frame(int(frame1_width), int(frame1_height * (8 / 9)), 30, "white")
rounded_frame1_label = tk.Label(frame1, image=rounded_frame1_image, borderwidth=0)
rounded_frame1_label.place(relx=0.5, rely=0.5, anchor="center")

label_frame1_info = tk.Label(rounded_frame1_label, background='white')
label_frame1_info.place(relx=0.5, rely=0.05, anchor="n")

with open("datas/home_screen/studen_info.json", "r", encoding="utf-8") as json_file:
    data_info = json.load(json_file)

tensinhvien = data_info['Họ và tên']
masinhvien = data_info['Mã sinh viên']
lop = data_info['Lớp']
gioitinh = data_info["Giới tính"]
ngaysinh = data_info["Ngày sinh"]
nganh = data_info['Ngành học']

label_ten = tk.Label(label_frame1_info, text="Họ và tên : {}".format(tensinhvien), background='#ffffff', fg='#000000',
                     font=("Arial", SIZE_BIG(screen_width, screen_height), 'bold')).pack(pady=5)

# Mở hình ảnh bằng PIL
image = Image.open("images/home_screen/user_ava_images/avatar.jpg")
# Thay đổi đường dẫn đến hình ảnh của bạn

# Thu nhỏ hình ảnh để có kích thước 100x100
image = image.resize((200, 200), Image.ADAPTIVE)

# Tạo một đối tượng ImageTk từ hình ảnh và đặt kích thước của nó
image_tk = ImageTk.PhotoImage(image)
image_label = tk.Label(label_frame1_info, image=image_tk)
image_label.pack(pady=10)

label_ma = tk.Label(label_frame1_info, text="Mã sinh viên : {}".format(masinhvien), background='#ffffff', fg='#000000',
                    font=("Arial", SIZE_NORMAL(screen_width, screen_height),)).pack(pady=5)
label_lop = tk.Label(label_frame1_info, text="Lớp : {}".format(lop), background='#ffffff', fg='#000000',
                     font=("Arial", SIZE_NORMAL(screen_width, screen_height),)).pack(pady=5)
label_gioitinh = tk.Label(label_frame1_info, text="Giới tính : {}".format(gioitinh), background='#ffffff', fg='#000000',
                          font=("Arial", SIZE_NORMAL(screen_width, screen_height),)).pack(pady=5)
label_nganh = tk.Label(label_frame1_info, text="Ngành : {}".format(nganh), background='#ffffff', fg='#000000',
                       font=("Arial", SIZE_NORMAL(screen_width, screen_height),)).pack(pady=5)

button_signout = tk.Button(rounded_frame1_label, text="Đăng xuất", borderwidth=1, relief="solid", background='#A0151A',
                           fg='white', font=("Arial", SIZE_NORMAL(screen_width, screen_height)))
button_signout.place(relx=0.5, rely=0.9, anchor='s')

# Create a button to update the schedule from a JSON file
update_button = tk.Button(rounded_frame1_label, text="Cập nhật Thời Khóa Biểu", command=update_schedule_from_json,
                          borderwidth=1, relief="solid", background='#A0151A', fg='white',
                          font=("Arial", SIZE_NORMAL(screen_width, screen_height)))
update_button.place(relx=0.5, rely=0.83, anchor='s')

# Xu lys frame3 : TKB

frame3.rowconfigure(0, weight=1)
frame3.rowconfigure(1, weight=1)
frame3.rowconfigure(2, weight=1)
frame3.rowconfigure(3, weight=1)
frame3.rowconfigure(4, weight=1)
frame3.rowconfigure(5, weight=1)
frame3.rowconfigure(6, weight=1)
frame3.rowconfigure(7, weight=1)
frame3.rowconfigure(8, weight=1)
frame3.rowconfigure(9, weight=1)
frame3.rowconfigure(10, weight=1)
frame3.rowconfigure(11, weight=1)
frame3.rowconfigure(12, weight=1)
frame3.rowconfigure(13, weight=1)
frame3.rowconfigure(14, weight=1)

frame3.columnconfigure(0, weight=1, minsize=100)
frame3.columnconfigure(1, weight=1, minsize=100)
frame3.columnconfigure(2, weight=1, minsize=100)
frame3.columnconfigure(3, weight=1, minsize=100)
frame3.columnconfigure(4, weight=1, minsize=100)
frame3.columnconfigure(5, weight=1, minsize=100)
frame3.columnconfigure(6, weight=1, minsize=100)
frame3.columnconfigure(7, weight=1, minsize=100)
frame3.columnconfigure(8, weight=1, minsize=100)

icon_previous = Image.open(r"images\home_screen\icon\previous.png")
photo_previous = ImageTk.PhotoImage(icon_previous)
icon_next = Image.open(r"images\home_screen\icon\next.png")
photo_next = ImageTk.PhotoImage(icon_next)

tk.Button(frame3, image=photo_previous, font=('Arial', SIZE_NORMAL(screen_width, screen_height), 'bold'), bg='#AD171C',
          fg='#FFFFFF', borderwidth=0, relief='solid', highlightcolor='white').grid(row=0, column=0,
                                                                                    sticky=tk.W + tk.E + tk.S + tk.N)
tk.Button(frame3, image=photo_next, font=('Arial', SIZE_NORMAL(screen_width, screen_height), 'bold'), bg='#AD171C',
          fg='#FFFFFF', borderwidth=0, relief='solid', highlightcolor='white').grid(row=0, column=len(days_of_week) + 1,
                                                                                    sticky=tk.W + tk.E + tk.S + tk.N)

for j, time_slot in enumerate(time_slots):
    tk.Label(frame3, text=time_slot, font=('Arial', SIZE_NORMAL(screen_width, screen_height), 'bold'), bg='#AD171C',
             fg='#FFFFFF').grid(row=j + 1, column=0, sticky=tk.W + tk.E + tk.S + tk.N)

for j, lession_slot in enumerate(lession_slots):
    tk.Label(frame3, text=lession_slot, font=('Arial', SIZE_NORMAL(screen_width, screen_height), 'bold'), bg='#AD171C',
             fg='#FFFFFF').grid(row=j + 1, column=len(days_of_week) + 1, sticky=tk.W + tk.E + tk.S + tk.N)

for i, day in enumerate(days_of_week):
    tk.Label(frame3, text=day, font=('Arial', SIZE_NORMAL(screen_width, screen_height), 'bold'), bg='#AD171C',
             fg='#FFFFFF').grid(row=0, column=i + 1, sticky=tk.W + tk.E + tk.S + tk.N)
    for j, time_slot in enumerate(time_slots):
        text_widget = tk.Text(frame3, height=1, width=40, font=("Arial", SIZE_SMALL(screen_width, screen_height) - 2),
                              state=tk.DISABLED)
        text_widget.grid(row=j + 1, column=i + 1, sticky=tk.W + tk.E + tk.S + tk.N)
        subject_entries[(day, time_slot)] = text_widget

# Xử lý frame 4 :Thêm ghi chú


rounded_frame4_image = create_rounded_frame(int(frame2_width * (8 / 9)), int(49 * (screen_height / 1000)), 15, "white")
rounded_frame4_label = tk.Label(frame4, image=rounded_frame4_image, borderwidth=0)
rounded_frame4_label.place(relx=0.5, rely=0.5, anchor="center")

label_frame4_info = tk.Label(rounded_frame4_label, width=175, height=2, background='white')
label_frame4_info.place(relx=0.5, rely=0.5, anchor='center')

subject_label = tk.Label(label_frame4_info, text="Ghi chú", bg='#AD171C',
                         font=("Arial", SIZE_SMALL(screen_width, screen_height), 'bold'), fg='white', width=10)
subject_label.pack(side=tk.LEFT, padx=5)

subject_entry = tk.Entry(label_frame4_info, borderwidth=1, relief='solid',
                         font=("Arial", SIZE_SMALL(screen_width, screen_height)))
subject_entry.pack(side=tk.LEFT, padx=5)

time_label = tk.Label(label_frame4_info, text="Thời gian", bg='#AD171C',
                      font=("Arial", SIZE_SMALL(screen_width, screen_height), 'bold'), fg='white', width=10)
time_label.pack(side=tk.LEFT, padx=5)

style = ttk.Style()
style.theme_use("winnative")
style.configure("TCombobox", font=("Arial", SIZE_SMALL(screen_width, screen_height)))

time_combobox = tk.StringVar(value=time_slots[0])
time_combobox_widget = ttk.Combobox(label_frame4_info, textvariable=time_combobox, values=time_slots, state="readonly")
time_combobox_widget.pack(side=tk.LEFT, padx=5)

day_label = tk.Label(label_frame4_info, text="Thứ", bg='#AD171C',
                     font=("Arial", SIZE_SMALL(screen_width, screen_height), 'bold'), fg='white', width=5)
day_label.pack(side=tk.LEFT, padx=5)

day_combobox = tk.StringVar(value=days_of_week[0])

day_combobox_widget = ttk.Combobox(label_frame4_info, textvariable=day_combobox, values=days_of_week, state="readonly")
day_combobox_widget.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(label_frame4_info, text="Thêm Ghi Chú", bg='#AD171C',
                       font=("Arial", SIZE_SMALL(screen_width, screen_height), 'bold'), fg='white',
                       command=lambda: add_subject1(day_combobox.get(), subject_entry.get(), time_combobox.get()))
add_button.pack(side=tk.LEFT, padx=5)

# Xử lý frame 5 : Thay đổi tuần


rounded_frame5_image = create_rounded_frame(int(frame2_width * (5 / 9)), int(49 * (screen_height / 1000)), 15, "white")
rounded_frame5_label = tk.Label(frame5, image=rounded_frame5_image, borderwidth=0)
rounded_frame5_label.place(relx=0.5, rely=0.5, anchor="center")


def get_week_label(start_date):
    end_date = start_date + datetime.timedelta(days=6)
    return f"Ngày {start_date.strftime('%d/%m/%Y')} đến {end_date.strftime('%d/%m/%Y')}"


combobox_weeks = ttk.Combobox(frame5, width=50, height=10, font=("Arial", SIZE_SMALL(screen_width, screen_height)),
                              justify='center')
combobox_weeks.place(relx=0.5, rely=0.5, anchor='center')

label = tk.Label(root)
label.pack()

start_date = datetime.date(2023, 8, 14)
data_week = {}
weeks = []
for i in range(17):
    data_week[(start_date + datetime.timedelta(weeks=i)).strftime('%d/%m/%Y')] = "Tuần " + str(i + 1)
    weeks.append(get_week_label(start_date + datetime.timedelta(weeks=i)))
with open('weeks_time.json', 'w', encoding="utf-8") as json_file:
    json.dump(data_week, json_file, indent=4, ensure_ascii=False)
combobox_weeks['values'] = weeks

# Lấy ngày tháng năm của hôm nay
day_current = datetime.date.today()

# Tính toán ngày đầu tuần bằng cách lùi ngày về ngày thứ hai (0 là thứ hai, 1 là thứ ba, v.v.)
day_first_week = day_current - datetime.timedelta(days=day_current.weekday())

# Tính toán ngày cuối tuần bằng cách cộng ngày với 6 (ngày thứ bảy)
day_end_week = day_current + datetime.timedelta(days=(6 - day_current.weekday()))

combobox_weeks.set(f"Ngày {day_first_week.strftime('%d/%m/%Y')} đến {day_end_week.strftime('%d/%m/%Y')}")

tmp = combobox_weeks.get()
tmp = tmp[5:15]
print(tmp)
# Open the window
root.mainloop()
