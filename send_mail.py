import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

# Lấy user password, host, port
user = "mailtest011978@gmail.com"
pass_word = "mopb qlre cxif ltil"
host = "smtp.gmail.com"
port = 465
context = ssl.create_default_context()

# Đăng nhập mail
server = smtplib.SMTP_SSL(host, port, context=context)
server.login(user, pass_word)

# Content
def send(content, receiver_mail):
    msg = MIMEMultipart()
    msg['From'] = "PTIT CALENDAR"
    msg['Subject'] = "[THÔNG BÁO LỊCH HỌC]"
    # Chèn nội dung vào email
    msg.attach(MIMEText(content, 'plain'))
    server.sendmail(user, receiver_mail, msg.as_string())

# Sử dụng hàm send
if __name__ == "__main__":
    receiver_mail = "nguyenphong011978@gmail.com"  # Thay bằng địa chỉ email người nhận
    receiver_name = "Người Nhận"

    content = """Lịch học của bạn ngày 23/10:
    7h-10h: Cơ sở dữ liệu phòng 601-A2
    10h-12h: Lập trình với Python 201-A3"""
    send(content, receiver_mail)
