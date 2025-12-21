# Script để chạy cả Backend và Frontend (Windows PowerShell)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  KHỞI ĐỘNG ATTENDANCE SYSTEM" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kiểm tra Python
Write-Host "Kiểm tra Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python chưa được cài đặt!" -ForegroundColor Red
    exit 1
}

# Kiểm tra Node.js
Write-Host "Kiểm tra Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js chưa được cài đặt!" -ForegroundColor Red
    exit 1
}

# Kiểm tra file .env
Write-Host "Kiểm tra file .env..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ File .env đã tồn tại" -ForegroundColor Green
} else {
    Write-Host "⚠ File .env chưa tồn tại, đang tạo..." -ForegroundColor Yellow
    python setup_env.py
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ĐANG KHỞI ĐỘNG..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kiểm tra dependencies frontend
if (-not (Test-Path "frontend/node_modules")) {
    Write-Host "Đang cài đặt frontend dependencies..." -ForegroundColor Yellow
    Set-Location frontend
    npm install
    Set-Location ..
}

# Khởi động Backend trong tab mới
Write-Host "Khởi động Backend API (port 8000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\api'; Write-Host 'Backend API đang chạy tại http://localhost:8000' -ForegroundColor Green; uvicorn main:app --reload --port 8000"

# Đợi một chút để backend khởi động
Start-Sleep -Seconds 3

# Khởi động Frontend trong tab mới
Write-Host "Khởi động Frontend (port 3000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; Write-Host 'Frontend đang chạy tại http://localhost:3000' -ForegroundColor Green; npm run dev"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ĐÃ KHỞI ĐỘNG!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "Frontend:     http://localhost:3000" -ForegroundColor Yellow
Write-Host "API Docs:     http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Nhấn Ctrl+C để dừng tất cả" -ForegroundColor Gray

