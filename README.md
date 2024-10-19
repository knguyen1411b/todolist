## Ứng dụng Quản lý TodoList với Flask

_Được viết bởi Khánh Nguyên_
_19-10-2024_

Đây là một ứng dụng **Flask** đơn giản giúp quản lý danh sách công việc (Todo List). Ứng dụng cho phép người dùng đăng ký, đăng nhập, và quản lý các ghi chú (note) hoặc công việc của mình. Ứng dụng được xây dựng bằng **Flask**, **Flask-SQLAlchemy**, **Flask-Login**, và **Python-dotenv** để quản lý cấu hình môi trường.

### Các tính năng

- Xác thực người dùng (Đăng ký, Đăng nhập, Đăng xuất)
- Thêm, hoàn thành, và xóa các ghi chú (note)
- Lưu trữ dữ liệu vĩnh viễn bằng SQLite và SQLAlchemy
- Thông báo flash để hiển thị thông tin phản hồi cho người dùng
- Theo dõi trạng thái hoàn thành của các ghi chú

### Công nghệ sử dụng

- flask
- Flask-SQLAlchemy
- flask-login
- python-dotenv

### Hướng dẫn dùng

**Yêu cầu:**

- Python 3.8
- pip

```bash
git clone https://github.com/knguyen-1411/todolist-flask.git
cd todolist-flask

python -m venv venv

.\venv\Scripts\activate

pip install -r requirements.txt

```

Set .env

- KEY=your-secret-key
- DB_NAME=todolist.db

```bash
python app.py
```

### Liên hệ

- Mọi phản hồi liên hệ đến Khánh Nguyên

### Giấy Phép

- Dự án này được cấp phép theo Giấy phép MIT. Xem tệp LICENSE để biết chi tiết.

_Hoàn thành 21/9/2024_
**_Cảm ơn bạn đã xem qua Chat App! Chúng tôi hy vọng bạn thấy nó hữu ích và thú vị. Chúc bạn lập trình vui vẻ!_**
