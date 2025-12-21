"""
FastAPI Backend để lấy dữ liệu từ các bảng database
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import date, datetime
import sys
import os
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()

# Thêm thư mục service vào path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from service import (
    db,
    StudentsRepository,
    TeachersRepository,
    ClassesRepository,
    UsersRepository
)
from api.auth import (
    create_access_token,
    get_current_active_user,
    require_role
)

app = FastAPI(title="Attendance System API", version="1.0.0")

# Pydantic models cho request/response
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None
    role: str = "student"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: Dict

# Cấu hình CORS để cho phép React frontend kết nối
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Kết nối database khi khởi động
@app.on_event("startup")
async def startup_event():
    """Kết nối database khi khởi động"""
    db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """Đóng kết nối database khi tắt"""
    db.disconnect()

# ===========================================================
# Endpoints cho Authentication
# ===========================================================

@app.post("/api/auth/register", response_model=Dict)
async def register(user_data: RegisterRequest):
    """Đăng ký tài khoản mới"""
    try:
        user_id = UsersRepository.create_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            role=user_data.role,
            full_name=user_data.full_name
        )
        user = UsersRepository.get_user_by_id(user_id)
        return {"message": "Đăng ký thành công", "user_id": user_id, "user": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """Đăng nhập"""
    user = UsersRepository.authenticate_user(
        username=login_data.username,
        password=login_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không đúng"
        )
    
    # Tạo access token
    access_token = create_access_token(
        data={
            "user_id": user["user_id"],
            "username": user["username"],
            "role": user["role"],
            "is_active": user.get("is_active", True)
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@app.get("/api/auth/me", response_model=Dict)
async def get_current_user_info(current_user: dict = Depends(get_current_active_user)):
    """Lấy thông tin user hiện tại"""
    user = UsersRepository.get_user_by_id(current_user["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ===========================================================
# Endpoints cho Teachers
# ===========================================================

@app.get("/api/teachers", response_model=List[Dict])
async def get_all_teachers(current_user: dict = Depends(get_current_active_user)):
    """Lấy tất cả giáo viên (yêu cầu đăng nhập)"""
    try:
        return TeachersRepository.get_all_teachers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/teachers/{teacher_id}", response_model=Dict)
async def get_teacher_by_id(teacher_id: int):
    """Lấy giáo viên theo ID"""
    teacher = TeachersRepository.get_teacher_by_id(teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@app.get("/api/teachers/{teacher_id}/classes", response_model=List[Dict])
async def get_teacher_classes(teacher_id: int):
    """Lấy các lớp học của giáo viên"""
    try:
        return TeachersRepository.get_teacher_classes(teacher_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===========================================================
# Endpoints cho Classes
# ===========================================================

@app.get("/api/classes", response_model=List[Dict])
async def get_all_classes():
    """Lấy tất cả lớp học"""
    try:
        return ClassesRepository.get_all_classes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/classes/{class_id}", response_model=Dict)
async def get_class_by_id(class_id: int):
    """Lấy lớp học theo ID"""
    class_info = ClassesRepository.get_class_by_id(class_id)
    if not class_info:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_info

@app.get("/api/classes/{class_id}/students", response_model=List[Dict])
async def get_class_students(class_id: int):
    """Lấy học sinh trong lớp"""
    try:
        return ClassesRepository.get_class_students(class_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/classes/{class_id}/full", response_model=Dict)
async def get_class_with_students(class_id: int):
    """Lấy lớp học kèm danh sách học sinh"""
    class_info = ClassesRepository.get_class_with_students(class_id)
    if not class_info:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_info

# ===========================================================
# Endpoints cho Students
# ===========================================================

@app.get("/api/students", response_model=List[Dict])
async def get_all_students(current_user: dict = Depends(get_current_active_user)):
    """Lấy tất cả học sinh (yêu cầu đăng nhập)"""
    try:
        # Student chỉ xem được thông tin của mình
        if current_user["role"] == "student":
            # Tìm student theo email
            student = StudentsRepository.get_student_by_email(current_user.get("email", ""))
            if student:
                return [student]
            return []
        # Admin và teacher xem được tất cả
        return StudentsRepository.get_all_students()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/students/{student_id}", response_model=Dict)
async def get_student_by_id(student_id: int):
    """Lấy học sinh theo ID"""
    student = StudentsRepository.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.get("/api/students/class/{class_id}", response_model=List[Dict])
async def get_students_by_class(class_id: int):
    """Lấy học sinh theo lớp"""
    try:
        return StudentsRepository.get_students_by_class(class_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===========================================================
# Health check
# ===========================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Attendance System API", "status": "running"}

@app.get("/api/health")
async def health_check():
    """Health check với database"""
    try:
        if db.connection and db.connection.is_connected():
            return {"status": "healthy", "database": "connected"}
        else:
            return {"status": "unhealthy", "database": "disconnected"}
    except:
        return {"status": "unhealthy", "database": "error"}

