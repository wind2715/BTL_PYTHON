import tkinter as tk
from datetime import datetime, timedelta

def chuyen_doi_tuan(tuan_hien_tai, buoc):
    ngay_dau_tuan = tuan_hien_tai - timedelta(days=tuan_hien_tai.weekday())
    ngay_cuoi_tuan = ngay_dau_tuan + timedelta(days=6)
    
    tuan_moi = tuan_hien_tai + timedelta(weeks=buoc)
    
    ngay_dau_tuan_moi = tuan_moi - timedelta(days=tuan_moi.weekday())
    ngay_cuoi_tuan_moi = ngay_dau_tuan_moi + timedelta(days=6)
    
    return ngay_dau_tuan_moi, ngay_cuoi_tuan_moi

def chuyen_tuan_truoc():
    global tuan_hien_tai
    tuan_hien_tai, _ = chuyen_doi_tuan(tuan_hien_tai, -1)
    hien_thi_tuan()

def chuyen_tuan_sau():
    global tuan_hien_tai
    _, tuan_hien_tai = chuyen_doi_tuan(tuan_hien_tai, 1)
    hien_thi_tuan()

def hien_thi_tuan():
    global tuan_hien_tai
    lbl_tuan.config(text=tuan_hien_tai.strftime('%d/%m/%Y'))

tuan_hien_tai = datetime.today()
app = tk.Tk()
app.title("Chuyen Doi Tuan")

lbl_tuan = tk.Label(app, text=tuan_hien_tai.strftime('%d/%m/%Y'))
lbl_tuan.pack()

btn_tuan_truoc = tk.Button(app, text="Tuần Trước", command=chuyen_tuan_truoc)
btn_tuan_truoc.pack()

btn_tuan_sau = tk.Button(app, text="Tuần Sau", command=chuyen_tuan_sau)
btn_tuan_sau.pack()

hien_thi_tuan()

app.mainloop()
