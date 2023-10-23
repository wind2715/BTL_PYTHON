from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from firebase_config import auth, db
from collections.abc import MutableMapping
import re
import tkinter as tk


# Func Part

# khi ấn nút Login (khi đã có tài khoản)
def login_page():
    signup_window.destroy()
    import login


def check():
    patternMSV = r'^B2[0-3]DC[A-Z]{2}\d{3}$'  # kiểm tra định dạng mã sinh viên: ví dụ B21DCCN129, chỉ lấy các khoá D20 -> D23
    patternEmail = '@gmail.com'
    user_input = usernameEntry.get()
    print(user_input)
    email = emailEntry.get()
    passnhap = passwordEntry.get()  # pass
    confirmPass = confirmEntry.get()  # confirm pass

    if ((email.endswith(patternEmail)) and (passnhap == confirmPass) and (re.match(patternMSV, user_input)) and (
            getcheckbox % 2 == 1)):
        #dang ky thong tin
        user = auth.create_user_with_email_and_password(email, passnhap)

        #dua thong tin len firestore
        doc_ref = db.collection("sinhVien").document(user['localId'])
        doc_ref.set({"mail": email, "password": passnhap, "msv": user_input})
        return True
    else:
        return False


def getGtri():  # getcheckbox lưu số lan click checkbox
    global getcheckbox
    getcheckbox += 1


# khi đăng kí
def signup():
    # msv = usernameEntry.get() # ma sinh vien
    # email = emailEntry.get() #email
    # pass_ = passwordEntry.get() #pass
    # confirmPass = confirmEntry.get() #confirm pass
    if (check() == True):
        signup_window.destroy()
        import login
    else:
        messagebox.showerror("Lỗi", "Đăng kí không thành công. Vui lòng kiểm tra lại.")


# GUI Part

# ======================================================================================

signup_window = Tk()

screen_width = signup_window.winfo_screenwidth()
screen_height = signup_window.winfo_screenheight()

# Tính toán vị trí để cửa sổ nằm chính giữa màn hình
x_position = (screen_width - 990) // 2
y_position = (screen_height - 660) // 2

signup_window.geometry('990x660+{}+{}'.format(x_position, y_position))
signup_window.resizable(0, 0)

# signup_window.geometry('990x660+50+50')
signup_window.title('Signup Page')
# signup_window.resizable(0, 0)
background = ImageTk.PhotoImage(file='images/login_screen/bg.jpg')
bgLabel = Label(signup_window, image=background)
bgLabel.grid()

# ======================================================================================
frame = Frame(signup_window, bg='white')
frame.place(x=554, y=100)
# ======================================================================================
heading = Label(frame, text='CREATE AN ACCOUNT',
                font=('Open Sans', 16, 'bold'),
                bg='white', fg='firebrick1')
heading.grid(row=0, column=0, padx=13, pady=10)
# ======================================================================================
emailLabel = Label(frame, text='Email', font=('Microsoft YaHei UI Light', 10, 'bold'),
                   bg='white', fg='firebrick1')
emailLabel.grid(row=1, column=0, sticky='w', padx=25, pady=(10, 0))
emailEntry = Entry(frame, width=30, font=('Microsoft YaHei UI Light', 10, 'bold'),
                   fg='black', bg='white', bd=1)
emailEntry.grid(row=2, column=0, sticky='news', padx=25)
# ======================================================================================
usernameLabel = Label(frame, text='Mã sinh viên', font=('Microsoft YaHei UI Light', 10, 'bold'),
                      bg='white', fg='firebrick1')
usernameLabel.grid(row=3, column=0, sticky='w', padx=25, pady=(10, 0))
usernameEntry = Entry(frame, width=30, font=('Microsoft YaHei UI Light', 10, 'bold'),
                      fg='black', bg='white')
usernameEntry.grid(row=4, column=0, sticky='w', padx=25)
# ======================================================================================
passwordLabel = Label(frame, text='Password', font=('Microsoft YaHei UI Light', 10, 'bold'),
                      bg='white', fg='firebrick1')
passwordLabel.grid(row=5, column=0, sticky='w', padx=25, pady=(10, 0))
passwordEntry = Entry(frame, width=30, font=('Microsoft YaHei UI Light', 10, 'bold'),
                      fg='black', bg='white')
passwordEntry.grid(row=6, column=0, sticky='w', padx=25)
# ======================================================================================
confirmLabel = Label(frame, text='Confirm Password', font=('Microsoft YaHei UI Light', 10, 'bold'),
                     bg='white', fg='firebrick1')
confirmLabel.grid(row=7, column=0, sticky='w', padx=25, pady=(10, 0))
confirmEntry = Entry(frame, width=30, font=('Microsoft YaHei UI Light', 10, 'bold'),
                     fg='black', bg='white')
confirmEntry.grid(row=8, column=0, sticky='w', padx=25)
# ======================================================================================
getcheckbox = 0
termsandconditions = Checkbutton(frame, text='I agree to the Terms and Conditions',
                                 font=('Microsoft YaHei UI Light', 9, 'bold'),
                                 fg='firebrick1', bg='white', activebackground='white',
                                 activeforeground='firebrick1', cursor='hand2', command=getGtri)
termsandconditions.grid(row=9, column=0, pady=10, padx=15)

# ======================================================================================
signupButton = Button(frame, text='Sign up', font=('Open Sans', 16, 'bold'),
                      bd=0, bg='firebrick1', fg='white', activebackground='firebrick1', command=signup,
                      activeforeground='white', width=17)
signupButton.grid(row=10, column=0, pady=10)
# ======================================================================================
alreadyaccount = Label(frame, text="Already have an account?", font=('Open Sans', 9, 'bold'),
                       bg='white', fg='firebrick1')
alreadyaccount.grid(row=12, column=0, sticky='w', pady=10, padx=52)
# ======================================================================================
loginButton = Button(frame, text='Log in', font=('Open Sans', 9, 'bold underline'),
                     bg='white', fg='blue', cursor='hand2', activebackground='white',
                     activeforeground='blue', command=login_page, bd=0)
loginButton.place(x=201, y=397)
# ======================================================================================
signup_window.mainloop()
