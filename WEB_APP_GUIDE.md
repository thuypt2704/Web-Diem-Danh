# 🚀 Hướng dẫn chạy Web Application

Giao diện web React với các button để xem chi tiết thông tin các bảng trong database.

## 📋 Yêu cầu

1. **Python 3.8+** với các thư viện:
   - fastapi
   - uvicorn
   - python-dotenv
   - mysql-connector-python

2. **Node.js 16+** và npm

3. **MySQL Server** đang chạy

4. **Database đã được tạo** (chạy `python database/create_database.py`)

## 🔧 Cài đặt

### 1. Cài đặt Backend Dependencies

```bash
pip install fastapi uvicorn python-dotenv mysql-connector-python
```

Hoặc từ requirements.txt:
```bash
pip install -r requirements.txt
```

### 2. Cài đặt Frontend Dependencies

```bash
cd frontend
npm install
```

## 🎬 Chạy ứng dụng

### Bước 1: Khởi động Backend API

Mở terminal 1:

```bash
cd api
uvicorn main:app --reload --port 8000
```

Backend sẽ chạy tại: **http://localhost:8000**

Kiểm tra API: http://localhost:8000/docs (Swagger UI)

### Bước 2: Khởi động Frontend

Mở terminal 2:

```bash
cd frontend
npm run dev
```

Frontend sẽ chạy tại: **http://localhost:3000**

## 📱 Sử dụng

1. Mở trình duyệt và truy cập: **http://localhost:3000**

2. Click vào các button để xem dữ liệu:
   - 👨‍🏫 **Giáo viên** - Xem danh sách giáo viên
   - 📚 **Lớp học** - Xem danh sách lớp học
   - 👨‍🎓 **Học sinh** - Xem danh sách học sinh
   - 🖼️ **Face Embeddings** - Xem face embeddings
   - 📷 **Camera** - Xem danh sách camera
   - ✅ **Điểm danh** - Xem bản ghi điểm danh

3. Click nút **"Chi tiết"** để xem thông tin chi tiết của từng bản ghi

4. Click **"🔄 Làm mới"** để reload dữ liệu

## 🎨 Tính năng

- ✅ Giao diện đẹp, hiện đại với gradient background
- ✅ Responsive design (hoạt động trên mobile)
- ✅ Xem tất cả các bảng trong database
- ✅ Xem chi tiết từng bản ghi
- ✅ Tự động format dữ liệu (date, JSON, etc.)
- ✅ Loading states và error handling
- ✅ Modal popup để xem chi tiết

## 📁 Cấu trúc Project

```
Attendance_System/
├── api/
│   ├── main.py              # FastAPI backend
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ButtonGroup.jsx
│   │   │   ├── DataViewer.jsx
│   │   │   └── *.css
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
├── service/                  # MySQL repositories
├── database/                 # Database scripts
└── .env                     # Environment variables
```

## 🔍 API Endpoints

Tất cả endpoints bắt đầu với `/api/`:

- `GET /api/teachers` - Lấy tất cả giáo viên
- `GET /api/classes` - Lấy tất cả lớp học
- `GET /api/students` - Lấy tất cả học sinh
- `GET /api/embeddings` - Lấy tất cả embeddings
- `GET /api/cameras` - Lấy tất cả camera
- `GET /api/attendance` - Lấy tất cả điểm danh

Xem chi tiết tại: http://localhost:8000/docs

## ❓ Xử lý lỗi

### Lỗi "ModuleNotFoundError: No module named 'fastapi'"
```bash
pip install fastapi uvicorn
```

### Lỗi "Cannot find module 'react'"
```bash
cd frontend
npm install
```

### Lỗi kết nối database
- Kiểm tra file `.env` đã được tạo và điền đúng thông tin
- Đảm bảo MySQL server đang chạy
- Kiểm tra database đã được tạo: `python database/create_database.py`

### Lỗi CORS
- Đảm bảo backend đang chạy trên port 8000
- Kiểm tra frontend đang chạy trên port 3000
- Xem cấu hình CORS trong `api/main.py`

## 🎯 Next Steps

- Thêm chức năng tìm kiếm và filter
- Thêm pagination cho bảng lớn
- Thêm chức năng CRUD (Create, Update, Delete)
- Thêm biểu đồ thống kê
- Export dữ liệu ra Excel/PDF

