import tkinter as tk

root = tk.Tk()
frame = tk.Frame(root)
frame.grid()

# Tạo và đặt trọng số cho các cột
for i in range(3):
    frame.columnconfigure(i, weight=1)

# Dữ liệu mẫu
data = ["Cột 1", "Cột 2", "Cột 3"]

# Tạo và đặt các label vào các cột
labels = []
for i, text in enumerate(data):
    label = tk.Label(frame, text=text, borderwidth=1, relief="solid")
    label.grid(row=0, column=i, sticky="ew")
    labels.append(label)

# Kiểm tra và điều chỉnh chiều rộng tối thiểu của cột dựa trên nội dung
for i, label in enumerate(labels):
    width = max(label.winfo_reqwidth(), 100)  # Đặt giá trị tối thiểu là 100
    frame.columnconfigure(i, minsize=width)

root.mainloop()
