import tkinter as tk
from tkinter import ttk

# Hàm lắng nghe sự kiện khi giá trị trong Combobox thay đổi
def on_combobox_select(event):
    selected_value = combo_var.get()  # Lấy giá trị đã chọn
    result_label.config(text=f"Đã chọn: {selected_value}")

# Tạo cửa sổ gốc
root = tk.Tk()
root.title("Combobox và tự động thay đổi Label")

# Tạo biến StringVar để lưu giá trị của Combobox
combo_var = tk.StringVar()

# Tạo Combobox
combo = ttk.Combobox(root, textvariable=combo_var, values=["Giá trị 1", "Giá trị 2", "Giá trị 3"])
combo.pack()

# Tạo một Label để hiển thị kết quả
result_label = tk.Label(root, text="")
result_label.pack()

# Khi giá trị trong Combobox thay đổi, gọi hàm on_combobox_select
combo.bind("<<ComboboxSelected>>", on_combobox_select)

# Hiển thị cửa sổ
root.mainloop()
