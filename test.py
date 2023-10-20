import tkinter as tk

def show_label(event):
    text_widget = event.widget  # Xác định Text Widget mà sự kiện được kích hoạt
    label.config(text="Thông tin bổ sung")
    
    x, y, _, _ = text_widget.bbox("insert")
    x_root = text_widget.winfo_rootx() + x
    y_root = text_widget.winfo_rooty() + y
    label.place(x=x_root + text_widget.winfo_width(), y=y_root)

def hide_label(event):
    label.place_forget()

root = tk.Tk()
root.title("Hiển thị Label khi hover vào Text Widget")

# Tạo nhiều Text Widget
text_widgets = []
for i in range(5):
    text_widget = tk.Text(root, width=30, height=5)
    text_widget.pack()
    text_widget.bind("<Enter>", show_label)
    text_widget.bind("<Leave>", hide_label)
    text_widgets.append(text_widget)

# Tạo Label ẩn ban đầu
label = tk.Label(root, text="", bg="lightgray")
label.place_forget()

root.mainloop()
