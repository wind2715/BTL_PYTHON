from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from firebase_config import firebase, auth
import token_storage

# Func Part
def user_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)


def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)


def hide():
    openeye.config(file='images/login_screen/closeye.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)


def show():
    openeye.config(file='images/login_screen/openeye.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)






def Login():

    username = usernameEntry.get()
    password = passwordEntry.get()
    try:
        user = auth.sign_in_with_email_and_password(username, password)
        print(user)
        token = user['localId']
        token_storage.stored_token = token
        print(token_storage.stored_token)
        login_window.destroy()
        open_window_home()
    except Exception as err:
        print(err)
        messagebox.showerror("Lỗi", f"Đăng nhập không thành công.")
def open_window_home():
    import home

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
# ======================================================================================
bgImage = ImageTk.PhotoImage(file='images/login_screen/bg.jpg')
bgLabel = Label(login_window, image=bgImage)
bgLabel.place(x=0, y=0)
# ======================================================================================
logoimg = PhotoImage(file='images/login_screen/logoPtit.png')

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
openeye = PhotoImage(file='images/login_screen/openeye.png')
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
login_window.mainloop()


