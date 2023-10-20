import tkinter as tk
import tkinter.font as Font
from io import BytesIO
from tkinter import ttk
import json
from PIL import Image, ImageTk, ImageDraw
import webcolors
import datetime
import token_storage
from get_data_api import get_ds_nhom_to, get_token, get_image, get_info
from firebase_config import db
import requests
import base64
from define import *

token = token_storage.stored_token
doc_ref = db.collection("sinhVien").document(token).get().to_dict()
msv = doc_ref['msv']
password = doc_ref['password']


def get_datas():
    data = get_ds_nhom_to(get_token(msv, password))
    return data


datas = get_datas()
print(datas)


# Hàm cập nhật dữ liệu của ghi chú
def update_schedule_to_data_private(day, subject, time):
    # Bước 1: Mở tệp json
    with open("datas\home_screen\schedule.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    day_first_selected = combobox_weeks.get()[5:15] # Lấy dữ liệu ngày đầu tuần của combobox
    with open("datas\home_screen\weeks_time.json", "r", encoding="utf-8") as json2_file:
        week_select = json.load(json2_file)
    # Bước 2: Thay đổi dữ liệu
    data[week_select[day_first_selected]][day][time]['Ghi chú'] = subject

    # Bước 3: Lưu tệp JSON
    with open('datas\home_screen\schedule.json', 'w',encoding="utf-8") as json_file:
        json.dump(data, json_file,indent=4, ensure_ascii=False)
    update_schedule_from_json()


# Hàm thực hiện việc lấy dữ liệu từ file json khi bấm cập nhật dữ liệu
def update_schedule_from_json():
    day_first_selected = combobox_weeks.get()[5:15]
    with open("datas\home_screen\schedule.json", "r", encoding="utf-8") as json1_file:
        data = json.load(json1_file)
    with open("datas\home_screen\weeks_time.json", "r", encoding="utf-8") as json2_file:
        week_select = json.load(json2_file)
    for day in days_of_week:
        for time_slot in time_slots:
            subject = data.get(week_select[day_first_selected], {}).get(day, {}).get(time_slot, {})
            add_subject2(day, subject, time_slot)

# Hàm thực hiện việc đưa dữ liệu lấy từ file json vào ô khóa biểu, các tham số day và time cho biết vị trí ô khóa biểu
def add_subject2(day, subject, time):
    if(subject != {}) :
        if(subject['Môn học'] == '') :
            if(subject['Ghi chú'] == '') :
                schedule[time][day] = ""
            else :
                schedule[time][day] = subject['Ghi chú']
        else :
            if(subject['Ghi chú'] == '') :
                schedule[time][day] = subject['Môn học'] + "\n" + subject['Phòng học']
            else :
                schedule[time][day] = subject['Môn học'] + "\n" + subject['Phòng học'] + " (" + subject['Ghi chú'] + ')'
    else :
        schedule[time][day] = ""
    update_schedule_display() #Chuyển đến việc hiển thị

# Hàm thực hiện hiển thị dữ liệu lên các ô khóa biểu
def update_schedule_display():
    # Mở các file json
    for day in days_of_week:
        for time_slot in time_slots:
            subject = schedule[time_slot][day]
            
            text_widget = subject_entries[(day, time_slot)]
            text_widget.configure(state=tk.NORMAL, wrap = tk.WORD, yscrollcommand = None) # Trạng thái bình thường
            text_widget.delete('1.0', tk.END)  # Xóa toàn bộ nội dung trong Text widget
            if subject != '':
                text_widget.configure(background='#CFE2FF')
            else:
                text_widget.configure(background='white')
            text_widget.insert(tk.END, subject)  # Chèn dữ liệu mới từ đầu
            text_widget.configure(state=tk.DISABLED, yscrollcommand = None)
            # Tạo một kiểu dáng (tag) tùy chỉnh để căn giữa
            text_widget.tag_configure("center", justify = 'center')

            # Áp dụng kiểu dáng "center" cho văn bản trong Text Widget
            text_widget.tag_add("center", "1.0", "end")

            # Đặt phong cách chữ cho dòng đầu
            bold_font = (FONT_MAIN, SIZE_SMALL(screen_width, screen_height), "bold")
            text_widget.tag_configure("bold", font=bold_font)
            text_widget.tag_add("bold", "1.0", "1.end")

# Hàm lấy dữ liệu từ api về schdule.json
def update_json() :
    with open("datas/home_screen/weeks_time.json", "r", encoding="utf-8") as json2_file:
        week_select = json.load(json2_file)
    with open("datas/home_screen/schedule.json", "r", encoding="utf-8") as json2_file:
        data = json.load(json2_file)

    for data_week in datas :
        week = week_select[data_week['ngay_bat_dau']]
        for data_day in data_week["ds_thoi_khoa_bieu"] :
            d = data_day["thu_kieu_so"]
            if(d < 8 ) :
                day = "Thứ " + str(d)
            else :
                day = "Chủ Nhật"
            begin_lesson = data_day["tiet_bat_dau"]
            count_tiet = data_day["so_tiet"]
            for i in range(count_tiet) :
                time_slot = time_slots[begin_lesson + i - 1]
                data[week][day][time_slot]["Môn học"] = data_day["ten_mon"]
                phong = data_day["ma_phong"]
                phong_info = phong.split("-")
                phong = phong_info[0] + "-" + phong_info[1]
                data[week][day][time_slot]["Phòng học"] = phong
                data[week][day][time_slot]["Giáo viên"] = data_day["ten_giang_vien"]
    
    # Bước 3: Lưu tệp JSON
    with open('datas/home_screen/schedule.json', 'w', encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

# Hàm tạo bo góc cho frame
def create_rounded_frame(width, height, radius, color):
    image = Image.new("RGBA", (width, height), webcolors.hex_to_rgb( COLOR_BACKGROUND))
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, 2 * radius, 2 * radius), fill=color)
    draw.ellipse((width - 2 * radius, 0, width, 2 * radius), fill=color)
    draw.ellipse((0, height - 2 * radius, 2 * radius, height), fill=color)
    draw.ellipse((width - 2 * radius, height - 2 * radius, width, height), fill=color)
    draw.rectangle((radius, 0, width - radius, height), fill=color)
    draw.rectangle((0, radius, width, height - radius), fill=color)
    return ImageTk.PhotoImage(image)

# Hàm thay đổi font chữ dựa theo độ phân giải màn hình, có 3 mức là small, normal và big
def SIZE_SMALL(width, height):
    if(width >= 1920 and height >= 1080 - 80) :
        return 11
    elif (width >= 1600 and height >=  900 - 80) :
        return 9
    elif (width >= 1280 and height >=  720 - 80) :
        return 8
    elif(width >= 800 and height >=  600 - 80) :
        return 6
    
def SIZE_NORMAL(width, height):
    if(width >= 1920 and height >= 1080 - 80) :
        return 15
    elif (width >= 1600 and height >=  900 - 80) :
        return 13
    elif (width >= 1280 and height >=  720 - 80) :
        return 11
    elif(width >= 800 and height >=  600 - 80) :
        return 9
    
def SIZE_BIG(width, height):
    if(width >= 1920 and height >= 1080 - 80) :
        return 19
    elif (width >= 1600 and height >=  900 - 80) :
        return 16
    elif (width >= 1280 and height >=  720 - 80) :
        return 14
    elif(width >= 800 and height >=  600 - 80) :
        return 12

# Tạo một main window
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight() - 80
root.geometry(f"{screen_width}x{screen_height}+0+0")
root.resizable(width=False, height=False) # Không cho phép thay đổi kích thước
root.title("Thời Khóa Biểu Học Tập") # Đặt tiêu đề cho ứng dụng


# Khai báo các mảng thứ, giờ học, tiết học
days_of_week = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"] #Mảng thứ
time_slots = ["7h-8h", "8h-9h", "9h-10h", "10h-11h", "11h-12h", "12h-13h", "13h-14h", "14h-15h", "15h-16h", "16h-17h", "17h-18h", "18h-19h", "19h-20h", "20h-21h"] # Mảng khung giờ học
lession_slots = ["Tiết 1", "Tiết 2", "Tiết 3", "Tiết 4", "Tiết 5", "Tiết 6", "Tiết 7", "Tiết 8", "Tiết 9", "Tiết 10", "Tiết 11", "Tiết 12", "Tiết 13", "Tiết 14"] # Mảng tiết học
schedule = {time: {day: "" for day in days_of_week} for time in time_slots} # dict chứa dữ liệu các ô khóa biểu
subject_entries = {(day, time_slot): None for day in days_of_week for time_slot in time_slots} # dict chứa các ô khóa biểu dạng Text Widget



# ---------------Phân chia các vùng để làm giao diện----------------------
# Tạo frame0 bao phủ toàn bộ cửa sổ 
frame0 = tk.Frame(root, background= COLOR_BACKGROUND)
frame0.pack(fill=tk.BOTH, expand=True)
# bgImage = ImageTk.PhotoImage(file='images/bg_main.png') #Đặt ảnh cho background
# bgLabel = tk.Label(frame0, image=bgImage)
# bgLabel.place(x=0, y=0)

# Tạo frame con 1 và đặt vào cột 0 của frame0
frame1_width = width=screen_width / 4
frame1_height = screen_height
frame1 = tk.Frame(frame0, background= COLOR_BACKGROUND, width=frame1_width, height=frame1_height)
frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx= 20, pady= 40)

# Tạo frame con 2 và đặt vào cột 1 của frame0
frame2_width = screen_width - frame1_width
frame2_height = screen_height
frame2 = tk.Frame(frame0, background= COLOR_BACKGROUND, width=frame2_width, height=frame2_height)
frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx= 20, pady= 10)

# Tạo 3 frame con của frame2 xếp chồng lên nhau
frame5_height = frame2_height * (1/9)
frame5_width = frame2_width
frame4_height = frame2_height * (1/9)
frame4_width = frame2_width
frame3_height = frame2_height - frame4_height - frame5_height
frame3_width = frame2_width
frame5 = tk.Frame(frame2, background=  COLOR_BACKGROUND) # Chứa box chọn ngày
frame3 = tk.Frame(frame2, background=  COLOR_BACKGROUND) # Chứa bảng tkb
frame4 = tk.Frame(frame2, background=  COLOR_BACKGROUND) # Chứa các chức năng ghi chú

frame2.rowconfigure(0, weight= 1) #Chia ô cho frame2
frame2.rowconfigure(1, weight= 6)
frame2.rowconfigure(2, weight= 1)
frame2.columnconfigure(0, weight= 1)

frame5.grid(row=0, column=0, sticky="nsew")
frame3.grid(row=1, column=0, sticky="nsew", pady = 10)
frame4.grid(row=2, column=0, sticky="nsew")

#----Xử lý frame1 : Thông tin sinh viên và đăng xuất----
# Tạo bo góc frame1
rounded_frame1_image = create_rounded_frame(int(frame1_width), int(frame1_height * (8/9)), 30, COLOR_LABEL)
rounded_frame1_label = tk.Label(frame1, image=rounded_frame1_image, borderwidth=0)
rounded_frame1_label.place(relx=0.5, rely=0.5, anchor="center")

# Tạo một nhãn chưa thông tin nằm trong bo góc
label_frame1_info = tk.Label(rounded_frame1_label, background= COLOR_LABEL)
label_frame1_info.place(relx=0.5, rely=0.05, anchor="n")

infor = get_info(get_token(msv,password))

tensinhvien = infor['ten_day_du']
masinhvien = infor['ma_sv']
lop = infor['lop']
gioitinh = infor["gioi_tinh"]
ngaysinh = infor["ngay_sinh"]
nganh = infor['nganh']

label_ten = tk.Label(label_frame1_info, text="Họ và tên : {}".format(tensinhvien), background='#ffffff', fg='#000000',
                     font=("Arial", SIZE_BIG(screen_width, screen_height), 'bold')).pack(pady=5)


# Mở hình ảnh bằng PIL
data_uri = get_image(msv, get_token(msv, password))
head, data = data_uri.split(',', 1)
image_data = base64.b64decode(data)

# Đọc hình ảnh từ dữ liệu base64 mà không cần lưu vào tệp
image = Image.open(BytesIO(image_data))

# Thu nhỏ hình ảnh để có kích thước 100x100
image = image.resize((200, 200), Image.ADAPTIVE)
# Tạo một đối tượng ImageTk từ hình ảnh và đặt kích thước của nó
image_tk = ImageTk.PhotoImage(image)
image_label = tk.Label(label_frame1_info, image=image_tk)
image_label.pack(pady= 10)
#--Thông tin còn lại đưa vào các nhãn--
label_ma = tk.Label(label_frame1_info, text = "Mã sinh viên : {}".format(masinhvien), background = COLOR_TEXT, fg = COLOR_TEXT_INFO, font = (FONT_MAIN, SIZE_NORMAL(screen_width,screen_height), ), bg= COLOR_LABEL).pack(pady= 5)
label_lop = tk.Label(label_frame1_info, text = "Lớp : {}".format(lop), background = COLOR_TEXT, fg = COLOR_TEXT_INFO, font = (FONT_MAIN, SIZE_NORMAL(screen_width,screen_height), ), bg= COLOR_LABEL).pack(pady= 5)
label_gioitinh = tk.Label(label_frame1_info, text = "Giới tính : {}".format(gioitinh), background = COLOR_TEXT, fg = COLOR_TEXT_INFO, font = (FONT_MAIN, SIZE_NORMAL(screen_width,screen_height), ), bg= COLOR_LABEL).pack(pady= 5)
label_nganh = tk.Label(label_frame1_info, text = "Ngành : {}".format(nganh), background = COLOR_TEXT, fg = COLOR_TEXT_INFO, font = (FONT_MAIN, SIZE_NORMAL(screen_width,screen_height), ), bg= COLOR_LABEL).pack(pady= 5)

# Nút dailynote
daily_note = tk.Button(rounded_frame1_label, text = "Daily Note", borderwidth= 1, relief= "solid", background= COLOR_MAIN, fg= 'white', font= (FONT_MAIN, SIZE_NORMAL(screen_width,screen_height)))
daily_note.place(relx=0.5, rely=0.76, anchor= 's')

# Nút cập nhật dữ liệu từ file schedule.json
update_button = tk.Button(rounded_frame1_label, text="Cập nhật Thời Khóa Biểu", command=update_schedule_from_json, borderwidth= 1, relief= "solid", background= COLOR_MAIN, fg= 'white', font= (FONT_MAIN, SIZE_NORMAL(screen_width,screen_height)))
update_button.place(relx=0.5, rely=0.83, anchor= 's')

# Nút đăng xuất
button_signout = tk.Button(rounded_frame1_label, text = "Đăng xuất", borderwidth= 1, relief= "solid", background= COLOR_MAIN, fg= 'white', font= (FONT_MAIN, SIZE_NORMAL(screen_width,screen_height)))
button_signout.place(relx=0.5, rely=0.9, anchor= 's')


#----Xử lý frame3 : Bảng TKB ----
# Chia cột và hàng
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
frame3.rowconfigure(12, weight = 1)
frame3.rowconfigure(13, weight = 1)
frame3.rowconfigure(14, weight = 1)

frame3.columnconfigure(0, weight = 1, minsize=100)
frame3.columnconfigure(1, weight = 1, minsize=100)
frame3.columnconfigure(2, weight = 1, minsize=100)
frame3.columnconfigure(3, weight = 1, minsize=100)
frame3.columnconfigure(4, weight = 1, minsize=100)
frame3.columnconfigure(5, weight = 1, minsize=100)
frame3.columnconfigure(6, weight = 1, minsize=100)
frame3.columnconfigure(7, weight = 1, minsize=100)
frame3.columnconfigure(8, weight = 1, minsize=100)

# 2 nút chuyển tuần kế tiếp và trước đó
icon_previous = Image.open(r"images\home_screen\icon\previous.png").resize((SIZE_BIG(screen_width, screen_height),SIZE_BIG(screen_width, screen_height)), Image.ADAPTIVE) # Ảnh
photo_previous = ImageTk.PhotoImage(icon_previous)
icon_next = Image.open(r"images\home_screen\icon\next.png").resize((SIZE_BIG(screen_width, screen_height),SIZE_BIG(screen_width, screen_height)), Image.ADAPTIVE) #Ảnh
photo_next = ImageTk.PhotoImage(icon_next)
# Hàm cập nhật dữ liệu trên combobox_weeks thành ngày trước ngày hiện tại
def get_previous_value():
    current_index = combobox_weeks.current()
    if(current_index >= 0) :
        combobox_weeks.set(combobox_weeks['values'][current_index-1])
        update_schedule_from_json()

# Hàm cập nhật dữ liệu trên combobox_weeks thành ngày sau ngày hiện tại
def get_next_value():
    current_index = combobox_weeks.current()
    combobox_weeks.set(combobox_weeks['values'][current_index+1])
    update_schedule_from_json()

tk.Button(frame3, image= photo_previous, command= get_previous_value, font = (FONT_MAIN, SIZE_NORMAL(screen_width,screen_height), 'bold'), bg= COLOR_MAIN, fg = COLOR_TEXT, borderwidth = 0, relief = 'solid', highlightcolor= 'white').grid(row=0, column=0, sticky=tk.W + tk.E + tk.S + tk.N)
tk.Button(frame3, image= photo_next, command= get_next_value, font = (FONT_MAIN, SIZE_NORMAL(screen_width,screen_height), 'bold'), bg= COLOR_MAIN, fg = COLOR_TEXT, borderwidth = 0, relief = 'solid', highlightcolor= 'white').grid(row=0, column=len(days_of_week) + 1, sticky=tk.W + tk.E + tk.S + tk.N)

# Hiển thị cột khung thời gian
for j, time_slot in enumerate(time_slots):
    tk.Label(frame3, text=time_slot, font = (FONT_MAIN, SIZE_NORMAL(screen_width,screen_height), 'bold'), bg= COLOR_MAIN, fg = COLOR_TEXT).grid(row=j+1, column=0, sticky=tk.W + tk.E + tk.S + tk.N)

# Hiển thị hàng thứ
for j, lession_slot in enumerate(lession_slots):
    tk.Label(frame3, text=lession_slot, font = (FONT_MAIN, SIZE_NORMAL(screen_width,screen_height), 'bold'), bg= COLOR_MAIN, fg = COLOR_TEXT).grid(row=j+1, column=len(days_of_week) + 1, sticky=tk.W + tk.E + tk.S + tk.N)

# Đưa các ô khóa biểu dạng Text widget vào mảng đã khai báo trước đó
for i, day in enumerate(days_of_week):
    tk.Label(frame3, text=day, font=(FONT_MAIN, SIZE_NORMAL(screen_width,screen_height), 'bold'), bg=COLOR_MAIN, fg=COLOR_TEXT).grid(row=0, column=i+1, sticky=tk.W + tk.E + tk.S + tk.N)
    for j, time_slot in enumerate(time_slots):
        text_widget = tk.Text(frame3, height=2, width=40, font = (FONT_MAIN, SIZE_SMALL(screen_width, screen_height) - 1), state = tk.DISABLED)
        text_widget.grid(row=j+1, column=i+1, sticky=tk.W + tk.E + tk.S + tk.N)
        subject_entries[(day, time_slot)] = text_widget

#----Xử lý frame4 : Chức năng thêm ghi chú ----
# Bo góc frame 4
rounded_frame4_image = create_rounded_frame(int(frame2_width * (8/9)), int(49 * (screen_height / 1000)), 15, COLOR_LABEL)
rounded_frame4_label = tk.Label(frame4, image=rounded_frame4_image, borderwidth=0)
rounded_frame4_label.place(relx=0.5, rely=0.5, anchor="center")
# Nhãn chứa các dòng dữ liệu yêu cầu
label_frame4_info = tk.Label(rounded_frame4_label,width= 175, height= 2, background= COLOR_LABEL)
label_frame4_info.place(relx= 0.5, rely = 0.5, anchor= 'center')


subject_label = tk.Label(label_frame4_info, text="Ghi chú", bg= COLOR_MAIN, font = (FONT_MAIN, SIZE_SMALL(screen_width,screen_height), 'bold'), fg = COLOR_TEXT, width= 10)
subject_label.pack(side=tk.LEFT, padx = 5)

subject_entry = tk.Entry(label_frame4_info, borderwidth= 1, relief='solid', font = (FONT_MAIN, SIZE_SMALL(screen_width,screen_height)))
subject_entry.pack(side=tk.LEFT, padx = 5)

time_label = tk.Label(label_frame4_info, text="Thời gian", bg= COLOR_MAIN, font = (FONT_MAIN, SIZE_SMALL(screen_width,screen_height), 'bold'), fg = COLOR_TEXT, width= 10)
time_label.pack(side=tk.LEFT, padx = 5)

# Phong cách combobox
style = ttk.Style()
style.theme_use("winnative")
style.configure("TCombobox", font=(FONT_MAIN, SIZE_SMALL(screen_width,screen_height)))

time_combobox = tk.StringVar(value=time_slots[0])
time_combobox_widget = ttk.Combobox(label_frame4_info, textvariable=time_combobox, values=time_slots, state="readonly")
time_combobox_widget.pack(side=tk.LEFT, padx = 5)

day_label = tk.Label(label_frame4_info, text="Thứ", bg= COLOR_MAIN, font = (FONT_MAIN, SIZE_SMALL(screen_width,screen_height), 'bold'), fg = COLOR_TEXT, width= 5)
day_label.pack(side=tk.LEFT, padx = 5)

day_combobox = tk.StringVar(value=days_of_week[0])

day_combobox_widget = ttk.Combobox(label_frame4_info, textvariable=day_combobox, values=days_of_week, state="readonly")
day_combobox_widget.pack(side=tk.LEFT, padx = 5)

add_button = tk.Button(label_frame4_info, text="Thêm Ghi Chú", bg= COLOR_MAIN, font = (FONT_MAIN, SIZE_SMALL(screen_width,screen_height), 'bold'), fg = COLOR_TEXT, command=lambda: update_schedule_to_data_private(day_combobox.get(), subject_entry.get(), time_combobox.get()))
add_button.pack(side=tk.LEFT, padx = 5)

#----Xử lý frame5 : Thời gian hiển thị ----

# Bo góc frame5
rounded_frame5_image = create_rounded_frame(int(frame2_width * (5/9)), int(49 * (screen_height / 1000)), 15, COLOR_LABEL)
rounded_frame5_label = tk.Label(frame5, image=rounded_frame5_image, borderwidth=0)
rounded_frame5_label.place(relx=0.5, rely=0.5, anchor="center")

#Hàm lấy dữ liệu ngày cuối trong tuần khi biết ngày đầu tuần
def get_week_label(start_date):
    end_date = start_date + datetime.timedelta(days=6)
    return f"Ngày {start_date.strftime('%d/%m/%Y')} đến {end_date.strftime('%d/%m/%Y')}"

#Tạo combobox chứa dữ liệu các tuần
combobox_weeks = ttk.Combobox(frame5, width= 50, height= 10, font = (FONT_MAIN, SIZE_SMALL(screen_width,screen_height)), justify= 'center', state= 'readonly')
combobox_weeks.place(relx= 0.5, rely= 0.5, anchor='center')

# Ngày bắt đầu khai báo
start_date = datetime.date(2023, 8, 14)
data_week = {}
weeks = []

# Đưa dữ liệu 17 tuần kể từ ngày bắt đầu vào combobox
for i in range(30):
    data_week[(start_date + datetime.timedelta(weeks=i)).strftime('%d/%m/%Y')] = "Tuần " + str(i + 1)
    weeks.append(get_week_label(start_date + datetime.timedelta(weeks=i)))
with open('datas\home_screen\weeks_time.json', 'w', encoding="utf-8") as json_file:
    json.dump(data_week, json_file, indent=4, ensure_ascii=False)
combobox_weeks['values'] = weeks

update_json() # Lấy dữ liệu từ api về schdule.json

# Lấy ngày tháng năm của hôm nay
day_current = datetime.date.today()

# Tính toán ngày đầu tuần bằng cách lùi ngày về ngày thứ hai (0 là thứ hai, 1 là thứ ba, v.v.)
day_first_week = day_current - datetime.timedelta(days=day_current.weekday())

# Tính toán ngày cuối tuần bằng cách cộng ngày với 6 (ngày thứ bảy)
day_end_week = day_current + datetime.timedelta(days=(6 - day_current.weekday()))

#Set mặc định hiển thị trên combobox
combobox_weeks.set(f"Ngày {day_first_week.strftime('%d/%m/%Y')} đến {day_end_week.strftime('%d/%m/%Y')}")

def get_event_box(event) :
    update_schedule_from_json()
combobox_weeks.bind("<<ComboboxSelected>>", get_event_box)

update_schedule_from_json()
# Open the window
root.mainloop()
