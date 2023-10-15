import tkinter as tk
from tkinter import ttk

def on_combobox_select(event):
    selected_option.set(day_combobox.get())

root = tk.Tk()
root.geometry("400x300")
root.title("Combobox Đẹp")

frame4 = tk.Frame(root)
frame4.pack(pady=20)

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

selected_option = tk.StringVar()
selected_option.set("Chọn một ngày")

day_combobox = ttk.Combobox(frame4, textvariable=selected_option, values=days_of_week)
day_combobox.bind("<<ComboboxSelected>>", on_combobox_select)
day_combobox.set("Monday")  # Mặc định hiển thị ngày "Monday"
day_combobox['state'] = 'readonly'  # Chỉ cho phép chọn, không cho phép nhập
day_combobox.pack()

style = ttk.Style()
style.theme_use("winnative")  # Chọn giao diện theme "clam" (có thể sử dụng các theme khác)

root.mainloop()
