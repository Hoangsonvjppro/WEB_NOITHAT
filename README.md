# Hệ Thống Quản Lý Bán Hàng Nội Thất

Hệ thống quản lý bán hàng nội thất toàn diện cho doanh nghiệp vừa và nhỏ, phù hợp với quy mô 10-15 chi nhánh. Được xây dựng bằng Django và Bootstrap, cung cấp giao diện quản lý theo vai trò và đầy đủ các tính năng quản lý cửa hàng nội thất.

## Tính năng chính

- **Quản lý người dùng và phân quyền**
  - Phân chia quyền hạn cho: Chủ doanh nghiệp, Quản lý chi nhánh, Nhân viên bán hàng, Nhân viên kho
  - Hệ thống xác thực và phân quyền theo vai trò
  - Quản lý thông tin cá nhân người dùng

- **Quản lý sản phẩm**
  - Theo dõi thông tin sản phẩm đầy đủ: tên, giá, danh mục, mô tả, SKU, hình ảnh...
  - Quản lý danh mục sản phẩm
  - Tìm kiếm và lọc sản phẩm

- **Quản lý kho hàng**
  - Theo dõi tồn kho theo thời gian thực
  - Nhập và xuất kho với ghi chép đầy đủ
  - Cảnh báo hết hàng và sắp hết hàng
  - Chuyển kho giữa các chi nhánh

- **Quản lý đơn hàng**
  - Tạo và xử lý đơn hàng
  - Theo dõi trạng thái đơn hàng
  - In hóa đơn và phiếu giao hàng
  - Quản lý thanh toán

- **Quản lý chi nhánh**
  - Theo dõi hoạt động từng chi nhánh
  - Báo cáo hiệu suất chi nhánh
  - Quản lý nhân viên theo chi nhánh

- **Quản lý nhà cung cấp**
  - Thông tin nhà cung cấp
  - Lịch sử mua hàng
  - Đánh giá nhà cung cấp

- **Báo cáo và thống kê**
  - Báo cáo doanh thu
  - Báo cáo tồn kho
  - Phân tích xu hướng bán hàng
  - Xuất báo cáo định dạng CSV, Excel, PDF

## Cấu trúc dự án

```
FinalProduct/
│
├── accounts/              # Quản lý người dùng và phân quyền
├── branches/              # Quản lý chi nhánh
├── cart/                  # Giỏ hàng và xử lý mua sắm
├── FinalProduct/          # Cấu hình dự án Django chính
├── inventory/             # Quản lý kho hàng và tồn kho
├── media/                 # Lưu trữ file người dùng tải lên
│   ├── categories/        # Hình ảnh danh mục
│   ├── products/          # Hình ảnh sản phẩm
│   └── user_uploads/      # Các file người dùng tải lên khác
├── orders/                # Quản lý đơn hàng và thanh toán
├── products/              # Quản lý sản phẩm và danh mục
├── reports/               # Báo cáo và thống kê
├── staff/                 # Giao diện dành cho nhân viên
├── static/                # File tĩnh (CSS, JS, hình ảnh)
│   ├── css/
│   ├── img/
│   └── js/
├── suppliers/             # Quản lý nhà cung cấp
├── templates/             # HTML templates
│   ├── accounts/
│   ├── base/
│   ├── branches/
│   ├── cart/
│   ├── home/
│   ├── orders/
│   ├── products/
│   └── staff/
│       ├── branch_manager/
│       ├── dashboard/
│       ├── inventory/
│       ├── orders/
│       ├── products/
│       ├── reports/
│       └── sales/
├── manage.py              # Quản lý dự án Django
└── requirements.txt       # Các thư viện phụ thuộc
```

## Yêu cầu hệ thống

- Python 3.10+
- Django 5.2
- Các thư viện phụ thuộc được liệt kê trong `requirements.txt`

## Cài đặt

1. **Cài đặt Python và pip** (nếu chưa có)

2. **Clone repository**
   ```bash
   git clone <repository-url>
   cd FinalProduct
   ```

3. **Tạo môi trường ảo**
   ```bash
   python -m venv .venv
   ```

4. **Kích hoạt môi trường ảo**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

5. **Cài đặt các gói phụ thuộc**
   ```bash
   pip install -r requirements.txt
   ```

6. **Thực hiện migration**
   ```bash
   python manage.py migrate
   ```

7. **Tạo tài khoản admin**
   ```bash
   python manage.py createsuperuser
   ```

8. **Chạy server phát triển**
   ```bash
   python manage.py runserver
   ```

9. **Truy cập hệ thống**
   - Trang admin: http://localhost:8000/admin/
   - Trang chủ: http://localhost:8000/
   - Giao diện nhân viên: http://localhost:8000/staff/

## Hướng dẫn sử dụng

### Dành cho Quản trị viên

1. **Đăng nhập vào trang Admin**
   - Truy cập http://localhost:8000/admin/
   - Đăng nhập bằng tài khoản superuser

2. **Quản lý người dùng**
   - Thêm người dùng mới
   - Gán quyền và nhóm người dùng
   - Quản lý thông tin người dùng

3. **Quản lý chi nhánh**
   - Tạo chi nhánh mới
   - Phân công quản lý chi nhánh

### Dành cho Quản lý chi nhánh

1. **Đăng nhập vào giao diện nhân viên**
   - Truy cập http://localhost:8000/staff/
   - Đăng nhập bằng tài khoản quản lý

2. **Dashboard**
   - Xem tổng quan hoạt động chi nhánh
   - Theo dõi doanh số và hiệu suất

3. **Quản lý nhân viên**
   - Xem danh sách nhân viên
   - Theo dõi hiệu suất nhân viên

4. **Quản lý hàng tồn kho**
   - Kiểm tra tình trạng kho
   - Yêu cầu nhập hàng

### Dành cho Nhân viên bán hàng

1. **Đăng nhập vào giao diện nhân viên**
   - Truy cập http://localhost:8000/staff/
   - Đăng nhập bằng tài khoản nhân viên

2. **Quản lý đơn hàng**
   - Tạo đơn hàng mới
   - Theo dõi trạng thái đơn hàng
   - In hóa đơn

3. **Tìm kiếm sản phẩm**
   - Xem thông tin sản phẩm
   - Kiểm tra tồn kho

### Dành cho Nhân viên kho

1. **Đăng nhập vào giao diện nhân viên**
   - Truy cập http://localhost:8000/staff/
   - Đăng nhập bằng tài khoản nhân viên kho

2. **Quản lý kho**
   - Nhập kho
   - Xuất kho
   - Kiểm kê hàng tồn

3. **Quản lý nhà cung cấp**
   - Xem thông tin nhà cung cấp
   - Lịch sử giao dịch

## Phân quyền người dùng

Hệ thống phân chia thành các nhóm người dùng chính:

1. **Chủ doanh nghiệp (Superuser)**
   - Có toàn quyền trên hệ thống
   - Quản lý tất cả các chi nhánh
   - Truy cập trang Django Admin

2. **Quản lý chi nhánh**
   - Quản lý một chi nhánh cụ thể
   - Xem báo cáo chi nhánh
   - Quản lý nhân viên trong chi nhánh

3. **Nhân viên bán hàng**
   - Tạo và quản lý đơn hàng
   - Xem thông tin sản phẩm
   - In hóa đơn và báo cáo

4. **Nhân viên quản lý kho**
   - Quản lý hàng tồn kho
   - Nhập và xuất kho
   - Cảnh báo tồn kho

## Liên hệ và hỗ trợ

- **Email**: support@noithat.com
- **Điện thoại**: 0123 456 789
- **Website**: https://noithat.com 