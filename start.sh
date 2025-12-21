#!/bin/bash

# Script để chạy cả Backend và Frontend (Linux/Mac)

echo "========================================"
echo "  KHỞI ĐỘNG ATTENDANCE SYSTEM"
echo "========================================"
echo ""

# Kiểm tra Python
echo "Kiểm tra Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ $PYTHON_VERSION"
else
    echo "✗ Python chưa được cài đặt!"
    exit 1
fi

# Kiểm tra Node.js
echo "Kiểm tra Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✓ Node.js $NODE_VERSION"
else
    echo "✗ Node.js chưa được cài đặt!"
    exit 1
fi

# Kiểm tra file .env
echo "Kiểm tra file .env..."
if [ -f ".env" ]; then
    echo "✓ File .env đã tồn tại"
else
    echo "⚠ File .env chưa tồn tại, đang tạo..."
    python3 setup_env.py
fi

echo ""
echo "========================================"
echo "  ĐANG KHỞI ĐỘNG..."
echo "========================================"
echo ""

# Kiểm tra dependencies frontend
if [ ! -d "frontend/node_modules" ]; then
    echo "Đang cài đặt frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Khởi động Backend trong background
echo "Khởi động Backend API (port 8000)..."
cd api
uvicorn main:app --reload --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..
echo "✓ Backend đã khởi động (PID: $BACKEND_PID)"

# Đợi một chút để backend khởi động
sleep 3

# Khởi động Frontend
echo "Khởi động Frontend (port 3000)..."
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo "✓ Frontend đã khởi động (PID: $FRONTEND_PID)"

echo ""
echo "========================================"
echo "  ĐÃ KHỞI ĐỘNG!"
echo "========================================"
echo ""
echo "Backend API:  http://localhost:8000"
echo "Frontend:     http://localhost:3000"
echo "API Docs:     http://localhost:8000/docs"
echo ""
echo "Backend PID:  $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Logs:"
echo "  Backend:  tail -f backend.log"
echo "  Frontend: tail -f frontend.log"
echo ""
echo "Để dừng: kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Giữ script chạy
wait

