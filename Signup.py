from tkinter import *
from PIL import ImageTk
#Func Part
def login_page():
    signup_window.destroy()
    import Login
#GUI Part

#======================================================================================

signup_window = Tk()
signup_window.geometry('990x660+50+50')
signup_window.title('Signup Page')
signup_window.resizable(0, 0)
backdgound = ImageTk.PhotoImage(file = 'bg.jpg')
bgLabel = Label(signup_window, image=backdgound)
bgLabel.grid()
#======================================================================================
frame = Frame(signup_window, bg = 'white')
frame.place(x = 554, y = 100)
#======================================================================================
heading = Label(frame, text='CREATE AN ACCOUNT',
                font = ('Microsoft YaHei UI Light', 18, 'bold'),
                bg = 'white', fg = 'firebrick1')
heading.grid(row = 0, column = 0, padx = 13, pady = 10)
#======================================================================================
emailLabel = Label(frame, text='Email',font = ('Microsoft YaHei UI Light', 10, 'bold'),
                   bg = 'white', fg = 'firebrick1')
emailLabel.grid(row = 1, column  = 0, sticky = 'w', padx = 25,pady = (10, 0))
emailEntry = Entry(frame, width=30,font = ('Microsoft YaHei UI Light', 10, 'bold'),
                   fg='white', bg='firebrick1')
emailEntry.grid(row = 2, column = 0, sticky = 'w', padx = 25)
#======================================================================================
usernameLabel = Label(frame, text='Username',font = ('Microsoft YaHei UI Light', 10, 'bold'),
                   bg = 'white', fg = 'firebrick1')
usernameLabel.grid(row = 3, column  = 0, sticky = 'w', padx = 25, pady = (10, 0))
usernameEntry = Entry(frame, width=30,font = ('Microsoft YaHei UI Light', 10, 'bold'),
                      fg = 'white', bg = 'firebrick1')
usernameEntry.grid(row = 4, column = 0, sticky = 'w', padx = 25)
#======================================================================================
passwordLabel = Label(frame, text='Password',font = ('Microsoft YaHei UI Light', 10, 'bold'),
                   bg = 'white', fg = 'firebrick1')
passwordLabel.grid(row = 5, column  = 0, sticky = 'w', padx = 25, pady = (10, 0))
passwordEntry = Entry(frame, width=30,font = ('Microsoft YaHei UI Light', 10, 'bold'),
                      fg = 'white', bg = 'firebrick1')
passwordEntry.grid(row = 6, column = 0, sticky = 'w', padx = 25)
#======================================================================================
confirmLabel = Label(frame, text='Confirm Password',font = ('Microsoft YaHei UI Light', 10, 'bold'),
                   bg = 'white', fg = 'firebrick1')
confirmLabel.grid(row = 7, column  = 0, sticky = 'w', padx = 25, pady = (10, 0))
confirmEntry = Entry(frame, width=30,font = ('Microsoft YaHei UI Light', 10, 'bold'),
                      fg = 'white', bg = 'firebrick1')
confirmEntry.grid(row = 8, column = 0, sticky = 'w', padx = 25)
#======================================================================================
termsandconditions = Checkbutton(frame, text='I agree to the Terms and Conditions',
                                 font = ('Microsoft YaHei UI Light', 9, 'bold'),
                                 fg = 'firebrick1', bg = 'white', activebackground='white',
                                 activeforeground='firebrick1', cursor='hand2')
termsandconditions.grid(row = 9, column = 0, pady = 10, padx = 15)
#======================================================================================
signupButton = Button(frame, text = 'Register',font = ('Open Sans', 16, 'bold'),
                      bd = 0, bg = 'firebrick1', fg = 'white', activebackground='firebrick1',
                      activeforeground='white', width=17)
signupButton.grid(row = 10, column = 0, pady = 10)
#======================================================================================
alreadyaccount = Label(frame, text="Already have an account?", font = ('Open Sans',9, 'bold'),
                       bg = 'white', fg = 'firebrick1')
alreadyaccount.grid(row = 12, column = 0, sticky = 'w', pady = 10, padx = 52)
#======================================================================================
loginButton = Button(frame, text='Log in', font = ('Open Sans',9, 'bold underline'),
                       bg = 'white', fg = 'blue', cursor='hand2', activebackground='white',
                     activeforeground='blue', command=login_page, bd = 0)
loginButton.place(x = 201, y = 403)
#======================================================================================
signup_window.mainloop()