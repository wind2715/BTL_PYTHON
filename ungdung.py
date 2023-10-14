import tkinter as tk
import tkinter.font as Font
import json

def center_text(entry):
    text = entry.get()
    text_width = len(text)
    entry.config(justify="center")
    entry.delete(0, tk.END)
    entry.insert(0, text)

def add_subject(day, subject, time):
    schedule[time][day] = subject
    update_schedule_display()

def update_schedule_display():
    for day in days_of_week:
        for time_slot in time_slots:
            subject = schedule[time_slot][day]
            subject_entries[(day, time_slot)].configure(state = tk.NORMAL)
            if(subject != '') :
                subject_entries[(day, time_slot)].configure(disabledbackground = '#CFE2FF')
            subject_entries[(day, time_slot)].delete(0, tk.END)
            subject_entries[(day, time_slot)].insert(0, subject)
            subject_entries[(day, time_slot)].configure(state = tk.DISABLED)
            center_text(subject_entries[(day, time_slot)])

def update_schedule_from_json():
    with open("D:\GIAO DIEN BTL\CODE_GIAO_DIEN_BTL\schedule.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    for day in days_of_week:
        for time_slot in time_slots:
            subject = data.get(day, {}).get(time_slot, "")
            add_subject(day, subject, time_slot)
    update_schedule_display()

# Create the main window
root = tk.Tk()
# root.geometry("1200x800+100+100")
root.title("Thời Khóa Biểu Học Tập")

# Create a table for the schedule
days_of_week = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"]
time_slots = ["7h-8h", "8h-9h", "9h-10h", "10h-11h", "11h-12h", "12h-13h", "13h-14h", "14h-15h", "15h-16h", "16h-17h", "17h-18h"]

schedule = {time: {day: "" for day in days_of_week} for time in time_slots}
subject_entries = {(day, time_slot): None for day in days_of_week for time_slot in time_slots}

frame1 = tk.Frame(root, height = 100, background = 'white')
frame2 = tk.Frame(root, height = 500, background = 'white')
frame3 = tk.Frame(root, height = 200, background = 'red')

frame1.pack(side = tk.TOP, fill = tk.BOTH, expand = True, pady = 20)
frame2.pack(side = tk.TOP, fill = tk.BOTH, expand = True, padx= 10, pady= 20)
frame3.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

#Xu ly frame1 : Thong tin sinh vien

tensinhvien = "Trần Hoàng Tuấn Vũ"
masinhvien = "B21DCCN800"

label_ten = tk.Label(frame1, text = "Họ và tên : {}".format(tensinhvien), background = '#ffffff', fg = '#000000', font = ("Arial", 20, 'bold')).pack()
label_ma = tk.Label(frame1, text = "Mã sinh viên : {}".format(masinhvien), background = '#ffffff', fg = '#000000', font = ("Arial", 15, )).pack()


# Xu lys frame2 : TKB

frame2.rowconfigure(0, weight = 1)
frame2.rowconfigure(1, weight = 1)
frame2.rowconfigure(2, weight = 1)
frame2.rowconfigure(3, weight = 1)
frame2.rowconfigure(4, weight = 1)
frame2.rowconfigure(5, weight = 1)
frame2.rowconfigure(6, weight = 1)
frame2.rowconfigure(7, weight = 1)
frame2.rowconfigure(8, weight = 1)
frame2.rowconfigure(9, weight = 1)
frame2.rowconfigure(10, weight = 1)
frame2.rowconfigure(11, weight = 1)

frame2.columnconfigure(0, weight = 1)
frame2.columnconfigure(1, weight = 1)
frame2.columnconfigure(2, weight = 1)
frame2.columnconfigure(3, weight = 1)
frame2.columnconfigure(4, weight = 1)
frame2.columnconfigure(5, weight = 1)
frame2.columnconfigure(6, weight = 1)
frame2.columnconfigure(7, weight = 1)


for i, day in enumerate(days_of_week):
    tk.Label(frame2, text=day, font = ('Arial', 15, 'bold'), bg= '#AD171C', fg = '#FFFFFF').grid(row=0, column=i+1, sticky=tk.W + tk.E + tk.S + tk.N)
    for j, time_slot in enumerate(time_slots):
        entry = tk.Entry(frame2, state = tk.DISABLED, font = ("Arial", 12, 'bold'), disabledforeground="#000000")
        entry.grid(row=j+1, column=i+1, sticky= tk.W + tk.E + tk.S + tk.N)
        subject_entries[(day, time_slot)] = entry

for j, time_slot in enumerate(time_slots):
    tk.Label(frame2, text=time_slot, font = ('Arial', 15, 'bold'), bg= '#AD171C', fg = '#FFFFFF').grid(row=j+1, column=0, sticky=tk.W + tk.E + tk.S + tk.N)

# Create a button to update the schedule from a JSON file
update_button = tk.Button(frame3, text="Cập nhật Thời Khóa Biểu", command=update_schedule_from_json)
update_button.grid(row=len(time_slots) + 1, column=3, columnspan=5)


subject_label = tk.Label(frame3, text="Môn học:")
subject_label.grid(row=0, column=0, padx=10, pady=10)

subject_entry = tk.Entry(frame3)
subject_entry.grid(row=0, column=1, padx=10, pady=10)

time_label = tk.Label(frame3, text="Thời gian:")
time_label.grid(row=0, column=2, padx=10, pady=10)

time_combobox = tk.StringVar(value=time_slots[0])
time_combobox_widget = tk.OptionMenu(frame3, time_combobox, *time_slots)
time_combobox_widget.grid(row=0, column=3, padx=10, pady=10)

day_label = tk.Label(frame3, text="Thứ:")
day_label.grid(row=0, column=4, padx=10, pady=10)

day_combobox = tk.StringVar(value=days_of_week[0])
day_combobox_widget = tk.OptionMenu(frame3, day_combobox, *days_of_week)
day_combobox_widget.grid(row=0, column=5, padx=10, pady=10)

add_button = tk.Button(frame3, text="Thêm Môn Học", command=lambda: add_subject(day_combobox.get(), subject_entry.get(), time_combobox.get()))
add_button.grid(row=0, column=6, padx=10, pady=10)

# Open the window
root.mainloop()
