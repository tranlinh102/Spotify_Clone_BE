# 🎧 Spotify Clone – Backend (Django)

## 🔎 Giới thiệu

- Đây là dự án clone ứng dụng Spotify, chia thành 2 phần:
  - **Backend** (Django + MySQL) – source tại repo hiện tại
  - **Frontend** (React) – [Xem tại đây](https://github.com/MinhTriTech/spotify-clone-fe)
- Ngôn ngữ sử dụng: **Python 3.12.3**
- Cơ sở dữ liệu: **MySQL**

---

## 🚀 Cách chạy dự án

### 1. Clone repo & tạo môi trường ảo

```bash
git clone https://github.com/tranlinh102/Spotify_Clone_BE.git
cd Spotify_Clone_BE

python3.12 -m venv venv || python3 -m venv venv
source venv/bin/activate
```

### 2. Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```

###3. Cấu hình database
Tạo cơ sở dữ liệu MySQL có tên là spotify và chạy script sql trong file **database.sql**
Sửa file Spotify_Clone_BE/core/settings.py chứa thông tin kết nối MySQL:

```python
DB_NAME=spotify
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### 4. Cuối cùng là khởi chạy project
```bash
python manage.py runserver
```
