# Frontend React - Attendance System

Giao diện web React để xem chi tiết thông tin các bảng trong database.

## Cài đặt

```bash
cd frontend
npm install
```

## Chạy ứng dụng

```bash
npm run dev
```

Ứng dụng sẽ chạy tại: http://localhost:3000

## Tính năng

- ✅ Xem danh sách tất cả các bảng: Teachers, Classes, Students, Embeddings, Cameras, Attendance
- ✅ Xem chi tiết từng bản ghi
- ✅ Giao diện đẹp, responsive
- ✅ Làm mới dữ liệu
- ✅ Hiển thị số lượng bản ghi

## Cấu trúc

```
frontend/
├── src/
│   ├── components/
│   │   ├── ButtonGroup.jsx    # Các button chọn bảng
│   │   └── DataViewer.jsx     # Hiển thị dữ liệu
│   ├── App.jsx                # Component chính
│   ├── main.jsx               # Entry point
│   └── index.css              # Global styles
├── index.html
├── package.json
└── vite.config.js
```

