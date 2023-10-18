import tkinter as tk
from tkinter import ttk

def get_previous_value():
    current_value = combobox.get()
    current_index = combobox.current()

    if current_index > 0:
        previous_index = current_index - 1
        previous_value = combobox['values'][previous_index]
        print(f"Giá trị đứng trên {current_value} là {previous_value}")
    else:
        print(f"{current_value} là giá trị đầu tiên, không có giá trị đứng trên")

root = tk.Tk()
root.title("Lấy giá trị đứng trên Combobox")

# Tạo combobox
combobox = ttk.Combobox(root)
combobox['values'] = ["Mục 1", "Mục 2", "Mục 3"]

combobox.pack()

# Tạo button để lấy giá trị đứng trên
button = tk.Button(root, text="Lấy giá trị đứng trên", command=get_previous_value)
button.pack()

root.mainloop()
