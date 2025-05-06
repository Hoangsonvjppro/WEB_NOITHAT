# Hệ Thống Quản Lý Bán Nội Thất

Hệ thống quản lý bán hàng nội thất cho doanh nghiệp vừa và nhỏ, phù hợp cho quy mô 10-15 cửa hàng.

## Tính năng chính

- **Quản lý người dùng và phân quyền**: Phân chia rõ quyền giữa chủ doanh nghiệp, quản lý chi nhánh, nhân viên bán hàng, nhân viên kho và khách hàng
- **Quản lý sản phẩm**: Thêm, sửa, xóa và phân loại sản phẩm
- **Quản lý kho hàng**: Kiểm soát tồn kho, nhập xuất hàng, chuyển kho
- **Quản lý đơn hàng**: Xử lý đơn hàng, theo dõi trạng thái, in hóa đơn
- **Quản lý nhà cung cấp**: Theo dõi thông tin và lịch sử nhập hàng từ nhà cung cấp
- **Quản lý chi nhánh**: Thông tin chi nhánh, nhân viên tại từng chi nhánh
- **Báo cáo thống kê**: Báo cáo bán hàng, tồn kho, hiệu suất và tài chính
- **Giao diện khách hàng**: Tìm kiếm, lọc sản phẩm, mua hàng và theo dõi đơn hàng

## Kiến trúc hệ thống

- Framework: Django 5.2 (Python)
- Database: SQLite (phát triển), PostgreSQL (sản phẩm)
- Frontend: HTML, CSS, JavaScript, Bootstrap 5
- Template Engine: Jinja2

## Yêu cầu hệ thống

- Python 3.10+
- Django 5.2
- Các thư viện phụ thuộc được liệt kê trong `requirements.txt`

## Cài đặt và chạy dự án

1. Cài đặt Python và pip (Nếu chưa có)

2. Tạo môi trường ảo:
   ```
   python -m venv .venv
   ```

3. Kích hoạt môi trường ảo:
   - Trên Windows: `.venv\Scripts\activate`
   - Trên Linux/Mac: `source .venv/bin/activate`

4. Cài đặt các gói phụ thuộc:
   ```
   pip install -r requirements.txt
   ```

5. Thực hiện các thao tác migration:
   ```
   python manage.py migrate
   ```

6. Tạo tài khoản admin:
   ```
   python manage.py createsuperuser
   ```

7. Chạy server phát triển:
   ```
   python manage.py runserver
   ```

8. Truy cập trang admin tại http://localhost:8000/admin/

## Phân quyền người dùng

Hệ thống phân chia thành 5 nhóm người dùng chính:

1. **Chủ doanh nghiệp**: Có toàn quyền trên hệ thống, chỉ có thể tạo bằng lệnh và truy cập thông qua URL riêng
2. **Quản lý chi nhánh**: Quản lý một chi nhánh cụ thể, chỉ được tạo bởi chủ doanh nghiệp
3. **Nhân viên bán hàng**: Xử lý đơn hàng, in hóa đơn, xem báo cáo bán hàng
4. **Nhân viên quản lý kho**: Quản lý tồn kho, nhập xuất hàng
5. **Khách hàng**: Xem sản phẩm, đặt hàng, theo dõi đơn hàng

## Cấu trúc dự án

- `accounts/`: Quản lý người dùng và phân quyền
- `products/`: Quản lý sản phẩm và danh mục
- `orders/`: Quản lý đơn hàng và thanh toán
- `cart/`: Giỏ hàng
- `inventory/`: Quản lý kho, tồn kho và chuyển kho
- `suppliers/`: Quản lý nhà cung cấp
- `branches/`: Quản lý chi nhánh cửa hàng
- `reports/`: Báo cáo thống kê
- `static/`: Tài nguyên tĩnh (CSS, JS, hình ảnh)
- `templates/`: Templates HTML
- `media/`: Tệp tin người dùng tải lên

## Hướng dẫn sử dụng

### Dành cho Chủ doanh nghiệp và Quản lý

1. Truy cập trang quản trị tại `/admin/`
2. Đăng nhập với tài khoản và mật khẩu đã được cấp
3. Sử dụng sidebar để điều hướng đến các chức năng quản lý

### Dành cho Nhân viên

1. Đăng nhập vào hệ thống bằng tài khoản được cấp
2. Tùy theo vai trò, giao diện sẽ hiển thị các chức năng phù hợp
3. Thực hiện các tác vụ được phân quyền

### Dành cho Khách hàng

1. Truy cập trang chủ
2. Đăng ký tài khoản hoặc đăng nhập nếu đã có
3. Duyệt sản phẩm, thêm vào giỏ hàng và đặt hàng
4. Theo dõi trạng thái đơn hàng trong trang cá nhân

## Liên hệ và hỗ trợ

- Email: support@noithat.com
- Điện thoại: 0123 456 789
- Website: https://noithat.com 