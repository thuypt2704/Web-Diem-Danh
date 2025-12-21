# API Backend - Attendance System

FastAPI backend để lấy dữ liệu từ MySQL database.

## Cài đặt

```bash
pip install fastapi uvicorn python-dotenv
```

Hoặc cài từ requirements.txt (đã có sẵn).

## Chạy API

```bash
cd api
uvicorn main:app --reload --port 8000
```

API sẽ chạy tại: http://localhost:8000

## API Documentation

Sau khi chạy, truy cập:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### Teachers
- `GET /api/teachers` - Lấy tất cả giáo viên
- `GET /api/teachers/{teacher_id}` - Lấy giáo viên theo ID
- `GET /api/teachers/{teacher_id}/classes` - Lấy lớp học của giáo viên

### Classes
- `GET /api/classes` - Lấy tất cả lớp học
- `GET /api/classes/{class_id}` - Lấy lớp học theo ID
- `GET /api/classes/{class_id}/students` - Lấy học sinh trong lớp
- `GET /api/classes/{class_id}/full` - Lấy lớp kèm danh sách học sinh

### Students
- `GET /api/students` - Lấy tất cả học sinh
- `GET /api/students/{student_id}` - Lấy học sinh theo ID
- `GET /api/students/class/{class_id}` - Lấy học sinh theo lớp

### Face Embeddings
- `GET /api/embeddings` - Lấy tất cả embeddings
- `GET /api/embeddings/student/{student_id}` - Lấy embeddings của học sinh

### Cameras
- `GET /api/cameras` - Lấy tất cả camera
- `GET /api/cameras/{camera_id}` - Lấy camera theo ID

### Attendance
- `GET /api/attendance` - Lấy tất cả điểm danh
- `GET /api/attendance/student/{student_id}` - Lấy điểm danh của học sinh
- `GET /api/attendance/class/{class_id}` - Lấy điểm danh của lớp
- `GET /api/attendance/statistics/class/{class_id}` - Thống kê điểm danh

## CORS

API đã được cấu hình CORS để cho phép React frontend kết nối từ:
- http://localhost:3000
- http://localhost:5173

