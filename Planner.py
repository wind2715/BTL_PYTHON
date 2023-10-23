import base64
import tkinter as tk
import token_storage
from get_data_api import get_image, get_token, get_info
from firebase_config import db
from io import BytesIO
from PIL import Image, ImageTk, ImageDraw
import webcolors
from tkinter import Text
from tkinter import Frame
import re, requests

token = token_storage.stored_token
doc_ref = db.collection("sinhVien").document(token).get().to_dict()
msv = doc_ref['msv']
password = doc_ref['password']
def back_to_login():
    root.destroy()
    import login


def color_cell(row, column, color):
    # Check if the cell exists
    if 0 <= row < len(time_slots) + 1 and 0 <= column < len(days_of_week) + 1:
        # Get the widget at the specified row and column
        widget = frame3.grid_slaves(row=row, column=column)[0]

        # Set the background color
        widget.configure(bg=color)
    else:
        print("Cell does not exist")
task_entries = [""] * 30  # Danh sách lưu trữ giá trị của cột "Tên nhiệm vụ"
time_entries = [""] * 30  # Danh sách lưu trữ giá trị của cột "Thời gian"
check_entries = [""] * 30  # Danh sách lưu trữ giá trị của cột "Thời gian"

task_entry_widgets = []  # Danh sách lưu trữ widget Entry cho cột "Tên nhiệm vụ"
check_entry_widgets = []  # Danh sách lưu trữ widget Entry cho cột "Tên nhiệm vụ"
time_entry_widgets = []  # Danh sách lưu trữ widget Entry cho cột "Thời gian"

def on_key_release(event, entry, row_index, col_index):
    entry.after(10, lambda: update_entries(row_index, col_index))

def update_entries(row_index, col_index):
    if col_index == 0:
        task_entries[row_index] = task_entry_widgets[row_index].get()
    elif col_index == 1:
        time_entries[row_index] = time_entry_widgets[row_index].get()
def fetch_and_display_quote(): # get link quote api rồi get lấy text
    try:
        # Make a request to the Quotable API for a random quote
        response = requests.get("https://api.quotable.io/random")
        data = response.json()

        # Extract the quote from the response
        quote = data['content']
        author = data['author']

        # Display the quote in the quotes_frame
        quote_text.config(state="normal")  # Enable editing
        quote_text.delete("1.0", "end")  # Clear previous content
        quote_text.insert("1.0", f'"{quote}"\n\n- {author}')  # Insert new quote
        quote_text.config(state="disabled")  # Disable editing

    except Exception as e:
        print(f"Error fetching quote: {e}")
def clearcolor(): #xoá tất cả màu ở các ô, khi load tô lại hết các màu từ các chuỗi string ngày
    for i in range(1, 25):
        for j in range(1, 7):
            color_cell(i, j, 'white')

def back_to_tkb():
    root.destroy()
    import home
def applyColorForCell(time_entry):
    pattern = re.compile(r'^\d{2}:\d{2} - \d{2}:\d{2}$')
    check = bool(pattern.match(time_entry))
    if check:
        a = int(str(time_entry[0]) + str(time_entry[1]))
        b = int(str(time_entry[3]) + str(time_entry[4])) / 10
        c = int(str(time_entry[8]) + str(time_entry[9]))
        d = int(str(time_entry[11]) + str(time_entry[12])) / 10
        for k in range(a, c + 1):
            for n in range(1, 7):
                if (k == a and n > b):
                    color_cell(k + 1, n, "red")
                elif (k > a and k < c):
                    color_cell(k + 1, n, "red")
                elif (a == c and n > b):
                    color_cell(k + 1, n, "red")
                elif (a != c and k == c and n <= d):
                    color_cell(k + 1, n, "red")

def update_schedule_from_json():
    clearcolor()
    # Mở tệp để ghi
    with open(f"datas/{msv}.txt", "w", encoding="utf-8") as file:
        for i, (task_entry, time_entry, check_entry) in enumerate(
                zip(task_entries, time_entries, check_entries)):
            task_info = f"{task_entry},{time_entry},{check_entry}\n"
            applyColorForCell(time_entry)
            # Ghi nội dung vào tệp
            file.write(task_info)



def load_data_from_file():
    clearcolor()
    try:
        with open(f"datas/{msv}.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

            # Clear existing data
            task_entries.clear()
            time_entries.clear()
            check_entries.clear()

            for line in lines:
                # Split the line into task, time, and checkbox state
                parts = line.strip().split(",")

                if len(parts) == 3:
                    task_entries.append(parts[0])
                    time_entries.append(parts[1])
                    check_entries.append(parts[2])
                    applyColorForCell(parts[1])
                else:
                    print(f"Skipping invalid line: {line}")

            print("Data loaded successfully.")

    except FileNotFoundError:
        print("Error: Planner data file not found.")

# Call the function to load data from the file




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
screen_height = root.winfo_screenheight() - 40
root.geometry(f"{screen_width}x{screen_height}+0+0")

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
days_of_week = ["10", "20", "30", "40", "50", "60"]
time_slots = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']

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
#frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=40)
frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=20, pady=40)

# Tạo frame con 2 và đặt vào cột 1
frame2_width = screen_width - frame1_width
frame2_height = screen_height - 200
frame2 = tk.Frame(frame0, background='#EA4463', width=frame2_width, height=frame2_height)
#frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=40)
frame2.pack(side=tk.RIGHT, fill = tk.BOTH, expand=True, padx=0, pady=20)

# frame5_height = frame2_height * (1 / 9)
# frame5_width = frame2_width
# frame4_height = frame2_height * (1 / 9)
# frame4_width = frame2_width
# frame3_height = frame2_height - frame4_height - frame5_height
# frame3_width = frame2_width
frame5 = tk.Frame(frame2, background='#EA4463')
frame3 = tk.Frame(frame2, background='#EA4463')
frame4 = tk.Frame(frame2, background='#EA4463')

frame2.rowconfigure(0, weight=4)
frame2.rowconfigure(1, weight=3)

frame2.columnconfigure(0, weight = 1)
frame2.columnconfigure(1, weight=7)
frame2.columnconfigure(2, weight=4)
#
# frame5.grid(row=0, column=0, sticky="nsew")
frame4.grid(row=0, column=1, sticky="nsew")
frame3.grid(row=0, column=2, sticky="nsew", padx = 20)


# Xu ly frame1 : Thong tin sinh vien va dang xuat

rounded_frame1_image = create_rounded_frame(int(frame1_width), int(frame1_height * (8 / 9)), 30, "white")
rounded_frame1_label = tk.Label(frame1, image=rounded_frame1_image, borderwidth=0)
rounded_frame1_label.place(relx=0.5, rely=0.5, anchor="center")

label_frame1_info = tk.Label(rounded_frame1_label, background='white')
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
                           fg='white', font=("Arial", SIZE_NORMAL(screen_width, screen_height)), command=back_to_login)
button_signout.place(relx=0.5, rely=0.9, anchor='s')

# Create a button to update the schedule from a JSON file
update_button = tk.Button(rounded_frame1_label, text="Cập nhật Thời gian biểu", command=update_schedule_from_json,
                          borderwidth=1, relief="solid", background='#A0151A', fg='white',
                          font=("Arial", SIZE_NORMAL(screen_width, screen_height)))
update_button.place(relx=0.5, rely=0.83, anchor='s')



ungdung_button = tk.Button(rounded_frame1_label, text="Thời khoá biểu", command=back_to_tkb,
                          borderwidth=1, relief="solid", background='#A0151A', fg='white',
                          font=("Arial", SIZE_NORMAL(screen_width, screen_height)))
ungdung_button.place(relx=0.5, rely=0.75, anchor='s')
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
frame3.rowconfigure(15, weight=1)
frame3.rowconfigure(16, weight=1)
frame3.rowconfigure(17, weight=1)
frame3.rowconfigure(18, weight=1)
frame3.rowconfigure(19, weight=1)
frame3.rowconfigure(20, weight=1)
frame3.rowconfigure(21, weight=1)
frame3.rowconfigure(22, weight=1)
frame3.rowconfigure(23, weight=1)

frame3.columnconfigure(0, weight = 1)
frame3.columnconfigure(1, weight = 1)
frame3.columnconfigure(2, weight = 1)
frame3.columnconfigure(3, weight = 1)
frame3.columnconfigure(4, weight = 1)
frame3.columnconfigure(5, weight = 1)
frame3.columnconfigure(6, weight = 1)

icon_previous = Image.open(r"images\home_screen\icon\previous.png")
photo_previous = ImageTk.PhotoImage(icon_previous)
icon_next = Image.open(r"images\home_screen\icon\next.png")
photo_next = ImageTk.PhotoImage(icon_next)

tk.Button(frame3, font=('Arial', SIZE_NORMAL(screen_width, screen_height), 'bold'), bg='#AD171C',
          fg='#FFFFFF', borderwidth=0, relief='solid', highlightcolor='white').grid(row=0, column=0,
                                                                                    sticky=tk.W + tk.E + tk.S + tk.N)

for j, time_slot in enumerate(time_slots):
    tk.Label(frame3, text=time_slot, font=('Arial', SIZE_NORMAL(screen_width, screen_height), 'bold'), bg='#AD171C',
             fg='#FFFFFF').grid(row=j + 1, column=0, sticky=tk.W + tk.E + tk.S + tk.N)



for i, day in enumerate(days_of_week):
    tk.Label(frame3, text=day, font=('Arial', SIZE_NORMAL(screen_width, screen_height), 'bold'), bg='#AD171C',
             fg='#FFFFFF').grid(row=0, column=i + 1, sticky=tk.W + tk.E + tk.S + tk.N)
    for j, time_slot in enumerate(time_slots):
        text_widget = tk.Text(frame3, height=0, width=0, font=("Arial", SIZE_SMALL(screen_width, screen_height) - 2),
                              state=tk.DISABLED, bg='white')
        text_widget.grid(row=j + 1, column = i + 1,sticky=tk.W + tk.E + tk.S + tk.N)
        subject_entries[(day, time_slot)] = "0"
load_data_from_file()
rows_title = ["Tên nhiệm vụ", "Thời gian", "Checkbox"];

frame4.rowconfigure(0, weight=1)
frame4.rowconfigure(1, weight=1)
frame4.rowconfigure(2, weight=1)
frame4.rowconfigure(3, weight=1)
frame4.rowconfigure(4, weight=1)
frame4.rowconfigure(5, weight=1)
frame4.rowconfigure(6, weight=1)
frame4.rowconfigure(7, weight=1)
frame4.rowconfigure(8, weight=1)
frame4.rowconfigure(9, weight=1)
frame4.rowconfigure(10, weight=1)
frame4.rowconfigure(11, weight=1)
frame4.rowconfigure(12, weight=1)
frame4.rowconfigure(13, weight=1)
frame4.rowconfigure(14, weight=1)
frame4.rowconfigure(15, weight=1)
frame4.rowconfigure(16, weight=1)
frame4.rowconfigure(17, weight=1)
frame4.rowconfigure(18, weight=1)
frame4.rowconfigure(19, weight=1)
frame4.rowconfigure(20, weight=1)
frame4.rowconfigure(21, weight=1)
frame4.rowconfigure(22, weight=1)
frame4.rowconfigure(23, weight=1)

frame4.columnconfigure(0, weight = 1, minsize=1)
frame4.columnconfigure(1, weight = 6, minsize=100)
frame4.columnconfigure(2, weight = 3, minsize=10)




tk.Button(frame4, text= "STT", font=('Arial', SIZE_NORMAL(screen_width, screen_height), 'bold'), bg='#AD171C',
          fg='#FFFFFF', borderwidth=0, relief='solid', highlightcolor='white').grid(row=0, column=0, sticky=tk.W + tk.E + tk.S + tk.N )
for j, time_slot in enumerate(time_slots):
    tk.Label(frame4, text=time_slot, font=('Arial', SIZE_NORMAL(screen_width, screen_height), 'bold'), bg='#AD171C',
             fg='#FFFFFF').grid(row=j + 1, column=0, sticky=tk.W + tk.E + tk.S + tk.N)


notdone_image = Image.open("images/planner/notdone.png")
done_image = Image.open("images/planner/done.png")

# Resize the images to fit the cell size
cell_width = 100  # Adjust according to your needs
cell_height = 50  # Adjust according to your needs



notdone_photo = ImageTk.PhotoImage(notdone_image)
done_photo = ImageTk.PhotoImage(done_image)


checkbox_states = {(day, time_slot): {"state": False, "button": None} for day in days_of_week for time_slot in time_slots}

image_paths = [""] * len(time_slots)  # Danh sách lưu trữ đường dẫn hình ảnh

for i, day in enumerate(rows_title):
    tk.Label(frame4, text=day, font=('Arial', SIZE_NORMAL(screen_width, screen_height), 'bold'), bg='#AD171C',
             fg='#FFFFFF').grid(row=0, column=i + 1, sticky="nsew")
    for j, time_slot in enumerate(time_slots):
        if i == 0 and j < len(task_entries):  # Check if j is a valid index for task_entries
            text_widget = tk.Entry(frame4, font=("Arial", SIZE_SMALL(screen_width, screen_height)))
            text_widget.grid(row=j + 1, column=i + 1, sticky="nsew")
            text_widget.insert(tk.END, task_entries[j])  # Set the value from task_entries
            text_widget.bind("<KeyRelease>", lambda event, entry=text_widget, index=j, col_index=i: on_key_release(event, entry, index, col_index))
            task_entry_widgets.append(text_widget)
        elif i == 1 and j < len(time_entries):  # Check if j is a valid index for time_entries
            text_widget = tk.Entry(frame4, font=("Arial", SIZE_SMALL(screen_width, screen_height)))
            text_widget.grid(row=j + 1, column=i + 1, sticky="nsew")
            text_widget.insert(tk.END, time_entries[j])  # Set the value from time_entries

            text_widget.bind("<KeyRelease>", lambda event, entry=text_widget, index=j, col_index=i: on_key_release(event, entry, index, col_index))
            time_entry_widgets.append(text_widget)
        elif i == 2:  # Assuming "Checkbox" column is the third column (index 2)
            text_widget = tk.Text(frame4, height=0, width=0, font=("Arial", SIZE_SMALL(screen_width, screen_height) - 2), state=tk.DISABLED)
            text_widget.grid(row=j + 1, column=i + 1, sticky="nsew")
            if j < len(check_entries):  # Check if j is a valid index for check_entries
                if check_entries[j] == 'True':
                    checkbox_button = tk.Button(frame4, image=done_photo, bd=0, bg='white', command=lambda widget=text_widget, state_var=checkbox_states, day=day, time_slot=time_slot, index=j: toggle_checkbox(widget, state_var, day, time_slot, index))
                else:
                    checkbox_button = tk.Button(frame4, image=notdone_photo, bd=0, bg='white', command=lambda widget=text_widget, state_var=checkbox_states, day=day, time_slot=time_slot, index=j: toggle_checkbox(widget, state_var, day, time_slot, index))
                checkbox_button.grid(row=j + 1, column=i + 1)
                checkbox_states[(day, time_slot)] = {"widget": text_widget, "state": check_entries[j], "button": checkbox_button}
# Function to toggle checkbox state and update image
checkbox_states2 = {(day, time_slot): {"state": False, "button": None} for day in days_of_week for time_slot in time_slots}



# Tiếp theo, cập nhật hàm toggle_checkbox như sau:
def toggle_checkbox(widget, state_var, day, time_slot, index):
    current_state = state_var[(day, time_slot)]["state"]
    if current_state:
        state_var[(day, time_slot)]["button"].config(image=notdone_photo)
    else:
        state_var[(day, time_slot)]["button"].config(image=done_photo)
    state_var[(day, time_slot)]["state"] = not current_state
    check_entries[index] = not current_state


quotes_frame = Frame(root, width=1330, height=70, bg='white')
quotes_frame.place(x=570, y=920)

quote_text = Text(quotes_frame, font=('Open Sans', 12), bd=0, wrap="word", state="disabled", height=5)
quote_text.place(x=10, y=10, width=1330, height=70)



# Fetch and display a quote when the program starts
fetch_and_display_quote()

root.mainloop()
