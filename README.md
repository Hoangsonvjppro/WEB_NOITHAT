# 🪑 FurnitureStore

**FurnitureStore** là một nền tảng thương mại điện tử chuyên về nội thất, được xây dựng bằng framework [Django](https://www.djangoproject.com/). Dự án này hỗ trợ đầy đủ các chức năng cho người dùng và quản trị viên như: duyệt sản phẩm, quản lý giỏ hàng, đặt hàng, quản lý nhân viên & nhà cung cấp, thống kê báo cáo và nhiều chức năng khác.

## 📦 Tính năng nổi bật

- 🛒 **Quản lý sản phẩm**: Cho phép thêm, sửa, xóa sản phẩm nội thất thông qua giao diện quản trị.
- 👤 **Đăng nhập & phân quyền người dùng**: Phân biệt rõ giữa tài khoản khách hàng và nhân viên.
- 🛍️ **Giỏ hàng**: Khách hàng có thể thêm sản phẩm vào giỏ, cập nhật số lượng, và thực hiện thanh toán.
- 📦 **Xử lý đơn hàng**: Quản lý quy trình đặt hàng từ phía khách hàng cho đến khi hoàn tất.
- 📊 **Báo cáo**: Cung cấp các báo cáo về doanh thu, tồn kho và hiệu suất nhân viên.
- 👥 **Quản lý nhân viên & nhà cung cấp**: Hệ thống cho phép quản trị viên thêm, sửa, xóa thông tin nhân viên và nhà cung cấp.
- 📂 **Quản lý tệp tĩnh và media**: Hỗ trợ tải lên và hiển thị hình ảnh sản phẩm, các tài nguyên CSS, JS.
- 🌐 **Giao diện người dùng tách biệt**: Sử dụng hệ thống template Django để tách biệt giữa giao diện khách hàng và giao diện quản trị viên.

## 🏗️ Cấu trúc thư mục

```
FurnitureStore/
├── manage.py
├── FurnitureStore/           # Cấu hình chính của project Django
├── apps/
│   ├── products/             # Quản lý sản phẩm: models, views, forms
│   ├── accounts/             # Đăng nhập, đăng ký, phân quyền
│   ├── cart/                 # Giỏ hàng và xử lý thanh toán
│   ├── employees/            # Quản lý nhân viên
│   ├── orders/               # Quản lý đơn hàng
│   ├── reports/              # Thống kê và báo cáo
│   ├── suppliers/            # Quản lý nhà cung cấp
├── templates/                # Giao diện HTML
├── static/                   # Tài nguyên tĩnh: CSS, JS, ảnh
├── media/                    # Ảnh sản phẩm được tải lên
├── db.sqlite3                # Cơ sở dữ liệu SQLite cho môi trường dev
```

## ⚙️ Hướng dẫn cài đặt

### Bước 1: Clone project

```bash
git clone https://github.com/Hoangsonvjppro/WEB_NOITHAT.git
cd FurnitureStore
```

### Bước 2: Tạo môi trường ảo

```bash
python -m venv env
source env/bin/activate  # Trên Windows dùng `env\Scripts\activate`
```

### Bước 3: Cài đặt các thư viện cần thiết

```bash
pip install -r requirements.txt
```

Nếu file `requirements.txt` chưa có, có thể tạo bằng:

```bash
pip freeze > requirements.txt
```

### Bước 4: Khởi tạo cơ sở dữ liệu

```bash
python manage.py migrate
```

### Bước 5: Tạo tài khoản quản trị viên

```bash
python manage.py createsuperuser
```

### Bước 6: Chạy server

```bash
python manage.py runserver
```

Truy cập `http://127.0.0.1:8000` để xem trang chủ.

## 🧪 Kiểm thử

Chạy toàn bộ test:

```bash
python manage.py test
```

## 📸 Gợi ý ảnh chụp màn hình *(nếu có)*

- Trang chủ khách hàng
- Trang sản phẩm chi tiết
- Giao diện giỏ hàng
- Giao diện đăng nhập/đăng ký
- Giao diện admin quản lý sản phẩm/đơn hàng

## 📁 Định hướng phát triển trong tương lai

- Tích hợp cổng thanh toán (Stripe, Momo, PayPal,...)
- Xây dựng REST API với Django REST Framework
- Triển khai bằng Docker để dễ dàng deploy
- Tìm kiếm và lọc sản phẩm nâng cao
- Chức năng theo dõi đơn hàng cho khách

## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh. Hãy mở issue hoặc pull request để thảo luận và cải tiến hệ thống.

## 📄 Giấy phép sử dụng

Project này sử dụng giấy phép [MIT](LICENSE).

