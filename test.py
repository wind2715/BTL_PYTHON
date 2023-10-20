from io import BytesIO
import requests

from get_data_api import get_image, get_token
from PIL import Image, ImageTk, ImageDraw
import base64


# Thay đường link dưới đây bằng đường link ảnh thực tế bạn muốn sử dụng
username = 'B21DCCN589'
password = 'phong2715'
data_uri = get_image(username, get_token(username, password))
head, data = data_uri.split(',', 1)
image_data = base64.b64decode(data)

# Lưu dữ liệu ảnh vào một tệp
with open("image.png", "wb") as file:
    file.write(image_data)

print("Ảnh đã được lưu thành công.")
