from tkinter import *
from tkinter import messagebox

from PIL import ImageTk, Image
from firebase_config import firebase, auth


# Func Part
def user_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)


def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)


def hide():
    openeye.config(file='images/closeye.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)


def show():
    openeye.config(file='images/openeye.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)


# def sign_up_page():
#     login_window.destroy()
#     import Signup

def Login():

    username = usernameEntry.get()
    password = passwordEntry.get()
    try:
        auth.sign_in_with_email_and_password(username, password)
        messagebox.showinfo("Thong bao", "Dang nhap thanh cong")
    except Exception:
        messagebox.showerror("Lỗi", f"Đăng nhập không thành công.")
    # import weekly


# GUI Part

# ======================================================================================
login_window = Tk()

# Lấy kích thước màn hình
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()

# Tính toán vị trí để cửa sổ nằm chính giữa màn hình
x_position = (screen_width - 990) // 2
y_position = (screen_height - 660) // 2

# Thiết lập kích thước và vị trí cửa sổ
login_window.geometry('990x660+{}+{}'.format(x_position, y_position))
login_window.resizable(0, 0)
login_window.title('Login Page')
print(screen_height, screen_width)
# ======================================================================================
bgImage = ImageTk.PhotoImage(file='images/bg.jpg')
bgLabel = Label(login_window, image=bgImage)
bgLabel.place(x=0, y=0)
# ======================================================================================
logoimg = PhotoImage(file='images/logoPtit.png')

# Thay đổi kích thước hình ảnh (ví dụ: giảm kích thước 50%)
new_width = int(logoimg.width() * 0.5)
new_height = int(logoimg.height() * 0.5)
logoimg = logoimg.subsample(2, 2)  # 2 là tỉ lệ giảm (subsample)
logoLabel = Label(login_window, image=logoimg, bd=0)
logoLabel.place(x=660, y=110)
# ======================================================================================
heading = Label(login_window, text='Login',
                font=('Times New Roman', 18),
                bg='white', fg='black')
heading.place(x=677, y=240)
# ======================================================================================
heading = Label(login_window, text='PTIT Study Planner',
                font=('Times New Roman', 20, 'bold'),
                bg='white', fg='firebrick1')
heading.place(x=582, y=280)
# ======================================================================================
usernameEntry = Entry(login_window, width=25,
                      font=('Microsoft YaHei UI Light', 11, 'bold'),
                      bd=0, fg='firebrick1')
usernameEntry.place(x=580, y=345)
usernameEntry.insert(0, 'Username')
usernameEntry.bind('<FocusIn>', user_enter)
frame1 = Frame(login_window, width=250, height=2, bg='firebrick1')
frame1.place(x=580, y=367)
# ======================================================================================
passwordEntry = Entry(login_window, width=25,
                      font=('Microsoft YaHei UI Light', 11, 'bold'),
                      bd=0, fg='firebrick1')
passwordEntry.place(x=580, y=400)
passwordEntry.insert(0, 'Password')
passwordEntry.bind('<FocusIn>', password_enter)
frame2 = Frame(login_window, width=250, height=2, bg='firebrick1')
frame2.place(x=580, y=422)
# ======================================================================================
openeye = PhotoImage(file='images/openeye.png')
eyeButton = Button(login_window, image=openeye,
                   bd=0, bg='white', activebackground='white',
                   cursor='hand2', command=hide)
eyeButton.place(x=800, y=396)
# ======================================================================================
forgetButton = Button(login_window, text='Forgot Password?',
                      bd=0, bg='white', activebackground='white',
                      cursor='hand2', font=('Microsoft YaHei UI Light', 9, 'bold'),
                      fg='firebrick1', activeforeground='firebrick1')
forgetButton.place(x=715, y=430)
# ======================================================================================
loginButton = Button(login_window, text='Login',
                     font=('Open Sans', 16, 'bold'), fg='white',
                     bg='firebrick1', activeforeground='white', activebackground='firebrick1',
                     cursor='hand2', bd=0, width=19, command=Login)
loginButton.place(x=578, y=475)
# ======================================================================================
# orLabel = Label(login_window, text='----------------OR----------------',
#                 font=('Open Sans', 16), fg = 'firebrick1',
#                 bg = 'white')
# orLabel.place(x = 575, y = 400)
#
# facebook_logo = PhotoImage(file='facebook.png')
# fbLabel = Label(login_window, image=facebook_logo, bg = 'white')
# fbLabel.place(x = 640, y = 440)
#
# google_logo = PhotoImage(file='google.png')
# ggLabel = Label(login_window, image=google_logo, bg = 'white')
# ggLabel.place(x = 690, y = 440)
#
# twitter_logo = PhotoImage(file='twitter.png')
# twLabel = Label(login_window, image=twitter_logo, bg = 'white')
# twLabel.place(x = 740, y = 440)
# #======================================================================================
# signupLabel = Label(login_window, text = "Don't have an account yet?",
#                     font=('Open Sans', 9, 'bold'), fg = 'firebrick1',
#                     bg = 'white')
# signupLabel.place(x = 580, y = 500)
# #======================================================================================
# newaccountButton = Button(login_window, text='Register now',
#                      font=('Open Sans', 10, 'bold underline'), fg = 'blue',
#                      bg = 'white', activeforeground='blue', activebackground='white',
#                      cursor='hand2', bd=0, command=sign_up_page)
# newaccountButton.place(x = 735, y = 498.3)
# #======================================================================================
login_window.mainloop()
