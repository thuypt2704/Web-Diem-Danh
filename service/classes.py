from service.db_connection import db
from typing import List, Dict, Optional

class ClassesRepository:
    """Repository để trích xuất và quản lý dữ liệu lớp học"""
    
    @staticmethod
    def get_all_classes() -> List[Dict]:
        """Lấy tất cả lớp học"""
        query = """
            SELECT 
                c.class_id,
                c.class_name,
                c.teacher_id,
                t.full_name as teacher_name,
                t.email as teacher_email
            FROM classes c
            JOIN teachers t ON c.teacher_id = t.teacher_id
            ORDER BY c.class_name
        """
        return db.execute_query(query)
    
    @staticmethod
    def get_class_by_id(class_id: int) -> Optional[Dict]:
        """Lấy lớp học theo ID"""
        query = """
            SELECT 
                c.class_id,
                c.class_name,
                c.teacher_id,
                t.full_name as teacher_name,
                t.email as teacher_email,
                t.phone as teacher_phone
            FROM classes c
            JOIN teachers t ON c.teacher_id = t.teacher_id
            WHERE c.class_id = %s
        """
        results = db.execute_query(query, (class_id,))
        return results[0] if results else None
    
    @staticmethod
    def get_classes_by_teacher(teacher_id: int) -> List[Dict]:
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
    def search_classes(keyword: str) -> List[Dict]:
        """Tìm kiếm lớp học theo tên lớp hoặc tên giáo viên"""
        query = """
            SELECT 
                c.class_id,
                c.class_name,
                c.teacher_id,
                t.full_name as teacher_name
            FROM classes c
            JOIN teachers t ON c.teacher_id = t.teacher_id
            WHERE c.class_name LIKE %s OR t.full_name LIKE %s
            ORDER BY c.class_name
        """
        search_pattern = f"%{keyword}%"
        return db.execute_query(query, (search_pattern, search_pattern))
    
    @staticmethod
    def get_class_students(class_id: int) -> List[Dict]:
        """Lấy tất cả học sinh trong một lớp"""
        query = """
            SELECT 
                s.student_id,
                s.full_name,
                s.age,
                s.address,
                s.email,
                s.face_embedding,
                s.class_id
            FROM students s
            WHERE s.class_id = %s
            ORDER BY s.full_name
        """
        return db.execute_query(query, (class_id,))
    
    @staticmethod
    def get_class_with_students(class_id: int) -> Optional[Dict]:
        """Lấy thông tin lớp học kèm danh sách học sinh"""
        class_info = ClassesRepository.get_class_by_id(class_id)
        if not class_info:
            return None
        
        students = ClassesRepository.get_class_students(class_id)
        class_info['students'] = students
        class_info['student_count'] = len(students)
        return class_info
    
    @staticmethod
    def create_class(class_name: str, teacher_id: int) -> int:
        """Tạo lớp học mới"""
        query = """
            INSERT INTO classes (class_name, teacher_id)
            VALUES (%s, %s)
        """
        params = (class_name, teacher_id)
        _, last_id = db.execute_update(query, params)
        return last_id
    
    @staticmethod
    def update_class(
        class_id: int,
        class_name: str = None,
        teacher_id: int = None
    ) -> bool:
        """Cập nhật thông tin lớp học"""
        updates = []
        params = []
        
        if class_name:
            updates.append("class_name = %s")
            params.append(class_name)
        if teacher_id:
            updates.append("teacher_id = %s")
            params.append(teacher_id)
        
        if not updates:
            return False
        
        params.append(class_id)
        query = f"UPDATE classes SET {', '.join(updates)} WHERE class_id = %s"
        affected_rows, _ = db.execute_update(query, tuple(params))
        return affected_rows > 0
    
    @staticmethod
    def delete_class(class_id: int) -> bool:
        """Xóa lớp học"""
        query = "DELETE FROM classes WHERE class_id = %s"
        affected_rows, _ = db.execute_update(query, (class_id,))
        return affected_rows > 0
    
    @staticmethod
    def get_class_statistics(class_id: int) -> Dict:
        """Lấy thống kê lớp học (số học sinh)"""
        query = """
            SELECT 
                c.class_id,
                c.class_name,
                COUNT(DISTINCT s.student_id) as total_students
            FROM classes c
            LEFT JOIN students s ON c.class_id = s.class_id
            WHERE c.class_id = %s
            GROUP BY c.class_id, c.class_name
        """
        results = db.execute_query(query, (class_id,))
        return results[0] if results else {
            'class_id': class_id,
            'total_students': 0
        }

