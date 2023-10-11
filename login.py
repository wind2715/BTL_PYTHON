import tkinter as tk
from tkinter import messagebox
from firebase_config import auth, firebase

def on_login():
    username = entry_username.get()
    password = entry_password.get()

    # Kiểm tra đăng nhập (thêm logic xác thực tại đây)
    try:
        # Thực hiện đăng nhập
        auth.sign_in_with_email_and_password(username, password)
        messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
    except Exception:
        # Xử lý lỗi đăng nhập
        messagebox.showerror("Lỗi", f"Đăng nhập không thành công.")
# Tạo cửa sổ
root = tk.Tk()
root.title("Đăng Nhập")

# Tạo các widget
label_username = tk.Label(root, text="Tên người dùng:")
label_password = tk.Label(root, text="Mật khẩu:")
entry_username = tk.Entry(root)
entry_password = tk.Entry(root, show="*")  # Hiển thị dấu * thay vì ký tự thật

button_login = tk.Button(root, text="Đăng Nhập", command=on_login)

# Định vị các widget trên lưới
label_username.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
label_password.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
entry_username.grid(row=0, column=1, padx=10, pady=5)
entry_password.grid(row=1, column=1, padx=10, pady=5)
button_login.grid(row=2, column=1, pady=10)

# Chạy ứng dụng
root.mainloop()
