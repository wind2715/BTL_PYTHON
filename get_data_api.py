import requests


def get_token(username, password):
    # Thông tin đăng nhập
    login_url = 'https://qldt.ptit.edu.vn/api/auth/login'

    # Tạo session để duy trì trạng thái đăng nhập
    session = requests.Session()

    # Gửi POST request để đăng nhập và lấy token
    login_payload = {
        'userName': username,
        'passWord': password,
        'grant_type': "password"
    }

    response_login = session.post(login_url, data=login_payload)

    # Kiểm tra xem đăng nhập có thành công hay không (kiểm tra mã trạng thái)
    if response_login.status_code == 200:
        # Đăng nhập thành công, giờ có thể gửi request API
        access_token = response_login.json().get('access_token')
        return access_token
    else:
        print("Đăng nhập không thành công.")
        return None


def get_ds_nhom_to(access_token):
    session = requests.Session()
    api_url = 'https://qldt.ptit.edu.vn/api/sch/w-locdstkbtuanusertheohocky'
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    payload = {
        "filter":
            {
                "hoc_ky": 20231,
                "ten_hoc_ky": ""
            },
        "additional":
            {
                "paging": {
                    "limit": 100,
                    "page": 1
                },
                "ordering":[
                    {
                        "name": None,
                        "order_type": None
                    }
                ]
            }
    }
    response = session.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:

        ds_nhom_to = response.json()['data']['ds_tuan_tkb']
        return ds_nhom_to
    else:
        print("no")


def get_image(msv, access_token):
    url_image = f'https://qldt.ptit.edu.vn/api/sms/w-locthongtinimagesinhvien?MaSV={msv}'
    session = requests.Session()
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    payload = msv
    response_image = session.post(url_image, headers=headers, data=payload)
    if response_image.status_code == 200:
        images = response_image.json()['data']['thong_tin_sinh_vien']['image']
        return "data:image/png;base64," + images
    else:
        print("no")
        return None
def get_info(access_token):
    url_infor = f'https://qldt.ptit.edu.vn/api/dkmh/w-locsinhvieninfo'
    session = requests.Session()
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response_infor = session.post(url_infor, headers=headers)
    if response_infor.status_code == 200:
        infor = response_infor.json()['data']
        return infor
    else:
        print("no")
        return None


# Sử dụng hàm
if __name__ == "__main__":
    username = 'B21DCCN589'
    password = 'phong2715'
    print(get_image(username, get_token(username, password)))
    ds_nhom_to_result = get_ds_nhom_to(get_token(username, password))
    infor = get_info(get_token(username, password))
    print(infor)

    if ds_nhom_to_result:
        print("Danh sách nhóm tổ:")
        print(ds_nhom_to_result)
