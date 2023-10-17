from tkinter import *
from PIL import Image, ImageTk

root = Tk()

# Tạo hình ảnh từ một tệp ảnh (ví dụ: icon.png)
image = Image.open("icon\previous.png")
photo = ImageTk.PhotoImage(image)

# Tạo label và đặt hình ảnh vào label
label = Label(root, image=photo)
label.pack()

root.mainloop()
