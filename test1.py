import tkinter as tk

def show_label(event):
    label.config(text="Thông tin bổ sung")
    label.place(x=event.x_root + 10, y=event.y_root + 10)

def hide_label(event):
    label.place_forget()

root = tk.Tk()
root.title("Hiển thị Label khi hover vào Text Widget")

# Tạo Text Widget
text_widget = tk.Text(root, width=30, height=10)
text_widget.pack()

# Tạo Label ẩn ban đầu
label = tk.Label(root, text="", bg="lightgray")
label.place_forget()

# Gắn sự kiện khi di chuột vào Text Widget
text_widget.bind("<Enter>", show_label)
text_widget.bind("<Leave>", hide_label)

root.mainloop()
