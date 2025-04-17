# 🎧 Spotify Clone – Backend (Django)

## 🔎 Giới thiệu

- Đây là dự án clone ứng dụng Spotify, chia thành 2 phần:
  - **Backend** (Django + MySQL) – source tại repo hiện tại
  - **Frontend** (React) – [Xem tại đây](https://github.com/MinhTriTech/spotify-clone-fe)
- Ngôn ngữ sử dụng: **Python 3.12.3**
- Cơ sở dữ liệu: **MySQL**

---

## 🚀 Cách chạy dự án trên hệ điều hành Linux

### 1. Clone repo & tạo môi trường ảo
- Clone repo
```bash
git clone https://github.com/tranlinh102/Spotify_Clone_BE.git
```

- Vào project sau khi clone xong
```bash
cd Spotify_Clone_BE
```

- Nếu bạn chưa cài python thì thực hiện các câu lệnh sau:
```bash
sudo apt update
sudo apt install python3.12
sudo apt install python3-venv
sudo apt install python3-pip
```

- Nếu có python rồi thì thực hiện
```bash
python3 -m venv venv
```

- Khởi tạo môi trường ảo
```bash
source venv/bin/activate
```
hoặc máy bạn chạy hệ điều hành Window
```bash
venv/Scripts/activate
```

### 2. Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```

### 3. Cấu hình database
Vào trình quản lý dữ liệu MySQL trên máy bạn và chạy script sql trong file **database.sql**

Sửa file Spotify_Clone_BE/core/settings.py chứa thông tin kết nối MySQL dể phù hợp với máy bạn:

```python
'ENGINE': 'django.db.backends.mysql',
'NAME': 'spotify',
'USER': 'root',
'PASSWORD': '',
'HOST': 'localhost',
'PORT': '3306',
```

### 4. Cuối cùng là khởi chạy project
```bash
python manage.py runserver
```
