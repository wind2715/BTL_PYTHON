import tkinter as tk

# Tạo cửa sổ giao diện đồ họa
root = tk.Tk()
root.title("Xóa nội dung trong Text Widget")

# Tạo một Text widget
text_widget = tk.Text(root)
text_widget.pack()

# Thêm nội dung vào Text widget
text_widget.insert("1.0", "Đây là nội dung trong Text widget.\nThêm một số dòng khác.")

# Xóa toàn bộ nội dung trong Text widget
text_widget.delete("1.0", "end")

# Hiển thị cửa sổ giao diện đồ họa
root.mainloop()
