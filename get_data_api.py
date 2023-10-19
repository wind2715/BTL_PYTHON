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
    api_url = 'https://qldt.ptit.edu.vn/api/sch/w-locdstkbhockytheodoituong'
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    payload = {
        "hoc_ky": 20231,
        "loai_doi_tuong": 1,
        "id_du_lieu": None
    }
    response = session.post(api_url, headers=headers, json=payload)
    ds_nhom_to = response.json()['data']['ds_nhom_to']
    return ds_nhom_to


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
        return images
    else:
        print("no")
        return None


# Sử dụng hàm
if __name__ == "__main__":
    username = 'B21DCCN589'
    password = 'phong2715'
    print(get_image(username, get_token(username, password)))
    ds_nhom_to_result = get_ds_nhom_to(get_token(username, password))

    if ds_nhom_to_result:
        print("Danh sách nhóm tổ:")
        print(ds_nhom_to_result)
