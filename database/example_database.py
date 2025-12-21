"""
Script để khởi tạo database với dữ liệu mẫu
Chạy file này sau khi đã chạy database/create_database.py
"""

import sys
import os
from datetime import date, datetime
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Thêm thư mục gốc của project vào path để tìm module service
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from service import db, StudentsRepository, TeachersRepository, ClassesRepository

def create_sample_data():
    """Tạo dữ liệu mẫu"""
    print("=" * 60)
    print("KHỞI TẠO DỮ LIỆU MẪU")
    print("=" * 60)
    
    # Kết nối database
    if not db.connect():
        print("✗ Không thể kết nối database!")
        print("\nHãy chạy database/create_database.py trước!")
        return False
    
    try:
        # ===========================================================
        # 1. Tạo giáo viên
        # ===========================================================
        print("\n1. Tạo giáo viên...")
        teacher1_id = TeachersRepository.create_teacher(
            full_name="Nguyễn Văn A",
            email="nguyenvana@example.com",
            phone="0123456789"
        )
        print(f"   ✓ Đã tạo giáo viên ID: {teacher1_id}")
        
        teacher2_id = TeachersRepository.create_teacher(
            full_name="Trần Thị B",
            email="tranthib@example.com",
            phone="0987654321"
        )
        print(f"   ✓ Đã tạo giáo viên ID: {teacher2_id}")
        
        # ===========================================================
        # 2. Tạo lớp học
        # ===========================================================
        print("\n2. Tạo lớp học...")
        class1_id = ClassesRepository.create_class(
            class_name="Lớp 10A1",
            teacher_id=teacher1_id
        )
        print(f"   ✓ Đã tạo lớp ID: {class1_id} - Lớp 10A1")
        
        class2_id = ClassesRepository.create_class(
            class_name="Lớp 10A2",
            teacher_id=teacher2_id
        )
        print(f"   ✓ Đã tạo lớp ID: {class2_id} - Lớp 10A2")
        
        # ===========================================================
        # 3. Tạo học sinh
        # ===========================================================
        print("\n3. Tạo học sinh...")
        import random
        
        students_data = [
            ("Nguyễn Văn An", 16, "123 Đường ABC, Quận 1, TP.HCM", "nguyenvanan@example.com", class1_id),
            ("Trần Thị Bình", 16, "456 Đường XYZ, Quận 2, TP.HCM", "tranthibinh@example.com", class1_id),
            ("Lê Văn Cường", 17, "789 Đường DEF, Quận 3, TP.HCM", "levancuong@example.com", class1_id),
            ("Phạm Thị Dung", 16, "321 Đường GHI, Quận 4, TP.HCM", "phamthidung@example.com", class2_id),
            ("Hoàng Văn Em", 17, "654 Đường JKL, Quận 5, TP.HCM", "hoangvanem@example.com", class2_id),
        ]
        
        student_ids = []
        for name, age, address, email, cid in students_data:
            # Tạo embedding giả (512 chiều như InsightFace)
            fake_embedding = [random.random() for _ in range(512)]
            
            student_id = StudentsRepository.create_student(
                full_name=name,
                age=age,
                address=address,
                email=email,
                class_id=cid,
                face_embedding=fake_embedding
            )
            student_ids.append(student_id)
            print(f"   ✓ Đã tạo học sinh ID: {student_id} - {name} ({email})")
        
        # ===========================================================
        # Hiển thị thống kê
        # ===========================================================
        print("\n" + "=" * 60)
        print("THỐNG KÊ DỮ LIỆU")
        print("=" * 60)
        
        all_teachers = TeachersRepository.get_all_teachers()
        all_classes = ClassesRepository.get_all_classes()
        all_students = StudentsRepository.get_all_students()
        
        print(f"\nTổng số giáo viên: {len(all_teachers)}")
        print(f"Tổng số lớp học: {len(all_classes)}")
        print(f"Tổng số học sinh: {len(all_students)}")
        
        print("\n✓ Hoàn thành khởi tạo dữ liệu mẫu!")
        return True
        
    except Exception as e:
        print(f"\n✗ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        db.disconnect()

if __name__ == "__main__":
    success = create_sample_data()
    sys.exit(0 if success else 1)

