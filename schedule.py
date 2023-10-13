import tkinter as tk
from tkinter import ttk

class TimetableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý thời khóa biểu")

        # Tạo và thiết lập giao diện
        self.create_widgets()

    def create_widgets(self):
        # Thêm Treeview để hiển thị thời khóa biểu
        self.tree = ttk.Treeview(self.root, columns=("Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"))
        self.tree.grid(row=1, column=0, columnspan=7, padx=10, pady=10, sticky="nsew")

        self.tree.heading("#0", text="Giờ")
        for day in ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]:
            self.tree.heading(day, text=day)

        # Thêm dữ liệu giả định
        timetable_data = [
            ("8:00 - 9:00", "Môn 1", "Môn 2", "Môn 3", "", "", ""),
            ("9:00 - 10:00", "", "Môn 2", "Môn 3", "Môn 4", "", ""),
            ("10:00 - 11:00", "", "Môn 2", "Môn 3", "Môn 4", "Môn 5", ""),
            # Thêm dữ liệu thời khóa biểu khác nếu cần
        ]

        # Thêm dữ liệu vào Treeview
        for hour, *subjects in timetable_data:
            self.tree.insert("", "end", text=hour, values=subjects)

        # Thiết lập trọng số cột để chúng tự động mở rộng
        for col in range(8):
            self.root.grid_columnconfigure(col, weight=1)

        # Thiết lập trọng số hàng để chúng tự động mở rộng
        for row in range(len(timetable_data) + 1):
            self.root.grid_rowconfigure(row, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableApp(root)
    root.mainloop()
