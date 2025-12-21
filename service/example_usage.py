"""
Ví dụ sử dụng các repository để trích xuất dữ liệu từ database
"""

from service import (
    db,
    StudentsRepository,
    TeachersRepository,
    ClassesRepository
)

# Kết nối database
db.connect()

# ===========================================================
# Ví dụ với StudentsRepository
# ===========================================================

# Lấy tất cả học sinh
all_students = StudentsRepository.get_all_students()
print(f"Tổng số học sinh: {len(all_students)}")

# Lấy học sinh theo ID
student = StudentsRepository.get_student_by_id(1)
if student:
    print(f"Học sinh: {student['full_name']}, Tuổi: {student['age']}, Email: {student['email']}")

# Lấy học sinh theo lớp
class_students = StudentsRepository.get_students_by_class(class_id=1)
print(f"Số học sinh trong lớp: {len(class_students)}")

# Tìm kiếm học sinh
search_results = StudentsRepository.search_students("Nguyễn")
print(f"Kết quả tìm kiếm: {len(search_results)} học sinh")

# ===========================================================
# Ví dụ với TeachersRepository
# ===========================================================

# Lấy tất cả giáo viên
all_teachers = TeachersRepository.get_all_teachers()
print(f"Tổng số giáo viên: {len(all_teachers)}")

# Lấy lớp học của giáo viên
teacher_classes = TeachersRepository.get_teacher_classes(teacher_id=1)
print(f"Số lớp của giáo viên: {len(teacher_classes)}")

# ===========================================================
# Ví dụ với ClassesRepository
# ===========================================================

# Lấy tất cả lớp học
all_classes = ClassesRepository.get_all_classes()
print(f"Tổng số lớp: {len(all_classes)}")

# Lấy thông tin lớp kèm học sinh
class_info = ClassesRepository.get_class_with_students(class_id=1)
if class_info:
    print(f"Lớp: {class_info['class_name']}, Số học sinh: {class_info['student_count']}")

# Lấy thống kê lớp học
class_stats = ClassesRepository.get_class_statistics(class_id=1)
print(f"Thống kê lớp: {class_stats['total_students']} học sinh")

# Đóng kết nối
db.disconnect()

