from service.db_connection import db
from typing import List, Dict, Optional

class TeachersRepository:
    """Repository để trích xuất và quản lý dữ liệu giáo viên"""
    
    @staticmethod
    def get_all_teachers() -> List[Dict]:
        """Lấy tất cả giáo viên"""
        query = """
            SELECT 
                teacher_id,
                full_name,
                email,
                phone
            FROM teachers
            ORDER BY full_name
        """
        return db.execute_query(query)
    
    @staticmethod
    def get_teacher_by_id(teacher_id: int) -> Optional[Dict]:
        """Lấy giáo viên theo ID"""
        query = """
            SELECT 
                teacher_id,
                full_name,
                email,
                phone
            FROM teachers
            WHERE teacher_id = %s
        """
        results = db.execute_query(query, (teacher_id,))
        return results[0] if results else None
    
    @staticmethod
    def get_teacher_by_email(email: str) -> Optional[Dict]:
        """Lấy giáo viên theo email"""
        query = """
            SELECT 
                teacher_id,
                full_name,
                email,
                phone
            FROM teachers
            WHERE email = %s
        """
        results = db.execute_query(query, (email,))
        return results[0] if results else None
    
    @staticmethod
    def search_teachers(keyword: str) -> List[Dict]:
        """Tìm kiếm giáo viên theo tên hoặc email"""
        query = """
            SELECT 
                teacher_id,
                full_name,
                email,
                phone
            FROM teachers
            WHERE full_name LIKE %s OR email LIKE %s
            ORDER BY full_name
        """
        search_pattern = f"%{keyword}%"
        return db.execute_query(query, (search_pattern, search_pattern))
    
    @staticmethod
    def get_teacher_classes(teacher_id: int) -> List[Dict]:
        """Lấy tất cả lớp học của một giáo viên"""
        query = """
            SELECT 
                c.class_id,
                c.class_name,
                c.teacher_id,
                t.full_name as teacher_name
            FROM classes c
            JOIN teachers t ON c.teacher_id = t.teacher_id
            WHERE c.teacher_id = %s
            ORDER BY c.class_name
        """
        return db.execute_query(query, (teacher_id,))
    
    @staticmethod
    def create_teacher(
        full_name: str,
        email: str = None,
        phone: str = None
    ) -> int:
        """Tạo giáo viên mới"""
        query = """
            INSERT INTO teachers (full_name, email, phone)
            VALUES (%s, %s, %s)
        """
        params = (full_name, email, phone)
        _, last_id = db.execute_update(query, params)
        return last_id
    
    @staticmethod
    def update_teacher(
        teacher_id: int,
        full_name: str = None,
        email: str = None,
        phone: str = None
    ) -> bool:
        """Cập nhật thông tin giáo viên"""
        updates = []
        params = []
        
        if full_name:
            updates.append("full_name = %s")
            params.append(full_name)
        if email:
            updates.append("email = %s")
            params.append(email)
        if phone:
            updates.append("phone = %s")
            params.append(phone)
        
        if not updates:
            return False
        
        params.append(teacher_id)
        query = f"UPDATE teachers SET {', '.join(updates)} WHERE teacher_id = %s"
        affected_rows, _ = db.execute_update(query, tuple(params))
        return affected_rows > 0
    
    @staticmethod
    def delete_teacher(teacher_id: int) -> bool:
        """Xóa giáo viên"""
        query = "DELETE FROM teachers WHERE teacher_id = %s"
        affected_rows, _ = db.execute_update(query, (teacher_id,))
        return affected_rows > 0
    
    @staticmethod
    def get_teacher_statistics(teacher_id: int) -> Dict:
        """Lấy thống kê của giáo viên (số lớp, số học sinh)"""
        query = """
            SELECT 
                t.teacher_id,
                t.full_name,
                COUNT(DISTINCT c.class_id) as total_classes,
                COUNT(DISTINCT s.student_id) as total_students
            FROM teachers t
            LEFT JOIN classes c ON t.teacher_id = c.teacher_id
            LEFT JOIN students s ON c.class_id = s.class_id
            WHERE t.teacher_id = %s
            GROUP BY t.teacher_id, t.full_name
        """
        results = db.execute_query(query, (teacher_id,))
        return results[0] if results else {
            'teacher_id': teacher_id,
            'total_classes': 0,
            'total_students': 0
        }

