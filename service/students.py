from service.db_connection import db
from typing import List, Dict, Optional
import json

class StudentsRepository:
    """Repository để trích xuất và quản lý dữ liệu học sinh"""
    
    @staticmethod
    def get_all_students() -> List[Dict]:
        """Lấy tất cả học sinh"""
        query = """
            SELECT 
                student_id,
                full_name,
                age,
                address,
                email,
                face_embedding,
                class_id
            FROM students
            ORDER BY full_name
        """
        return db.execute_query(query)
    
    @staticmethod
    def get_student_by_id(student_id: int) -> Optional[Dict]:
        """Lấy học sinh theo ID"""
        query = """
            SELECT 
                student_id,
                full_name,
                age,
                address,
                email,
                face_embedding,
                class_id
            FROM students
            WHERE student_id = %s
        """
        results = db.execute_query(query, (student_id,))
        return results[0] if results else None
    
    @staticmethod
    def get_students_by_class(class_id: int) -> List[Dict]:
        """Lấy tất cả học sinh trong một lớp"""
        query = """
            SELECT 
                s.student_id,
                s.full_name,
                s.age,
                s.address,
                s.email,
                s.face_embedding,
                s.class_id,
                c.class_name
            FROM students s
            JOIN classes c ON s.class_id = c.class_id
            WHERE s.class_id = %s
            ORDER BY s.full_name
        """
        return db.execute_query(query, (class_id,))
    
    @staticmethod
    def get_student_by_email(email: str) -> Optional[Dict]:
        """Lấy học sinh theo email"""
        query = """
            SELECT 
                student_id,
                full_name,
                age,
                address,
                email,
                face_embedding,
                class_id
            FROM students
            WHERE email = %s
        """
        results = db.execute_query(query, (email,))
        return results[0] if results else None
    
    @staticmethod
    def search_students(keyword: str) -> List[Dict]:
        """Tìm kiếm học sinh theo tên hoặc email"""
        query = """
            SELECT 
                s.student_id,
                s.full_name,
                s.age,
                s.address,
                s.email,
                s.face_embedding,
                s.class_id,
                c.class_name
            FROM students s
            LEFT JOIN classes c ON s.class_id = c.class_id
            WHERE s.full_name LIKE %s OR s.email LIKE %s
            ORDER BY s.full_name
        """
        search_pattern = f"%{keyword}%"
        return db.execute_query(query, (search_pattern, search_pattern))
    
    @staticmethod
    def create_student(
        full_name: str,
        class_id: int,
        age: int = None,
        address: str = None,
        email: str = None,
        face_embedding: List[float] = None
    ) -> int:
        """Tạo học sinh mới"""
        # Chuyển face_embedding từ list sang JSON string nếu có
        face_embedding_json = json.dumps(face_embedding) if face_embedding else None
        
        query = """
            INSERT INTO students 
            (full_name, age, address, email, face_embedding, class_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (full_name, age, address, email, face_embedding_json, class_id)
        _, last_id = db.execute_update(query, params)
        return last_id
    
    @staticmethod
    def update_student(
        student_id: int,
        full_name: str = None,
        age: int = None,
        address: str = None,
        email: str = None,
        face_embedding: List[float] = None,
        class_id: int = None
    ) -> bool:
        """Cập nhật thông tin học sinh"""
        updates = []
        params = []
        
        if full_name:
            updates.append("full_name = %s")
            params.append(full_name)
        if age is not None:
            updates.append("age = %s")
            params.append(age)
        if address:
            updates.append("address = %s")
            params.append(address)
        if email:
            updates.append("email = %s")
            params.append(email)
        if face_embedding is not None:
            updates.append("face_embedding = %s")
            params.append(json.dumps(face_embedding))
        if class_id:
            updates.append("class_id = %s")
            params.append(class_id)
        
        if not updates:
            return False
        
        params.append(student_id)
        query = f"UPDATE students SET {', '.join(updates)} WHERE student_id = %s"
        affected_rows, _ = db.execute_update(query, tuple(params))
        return affected_rows > 0
    
    @staticmethod
    def delete_student(student_id: int) -> bool:
        """Xóa học sinh"""
        query = "DELETE FROM students WHERE student_id = %s"
        affected_rows, _ = db.execute_update(query, (student_id,))
        return affected_rows > 0
    
    @staticmethod
    def get_student_count_by_class() -> List[Dict]:
        """Đếm số học sinh theo từng lớp"""
        query = """
            SELECT 
                c.class_id,
                c.class_name,
                COUNT(s.student_id) as student_count
            FROM classes c
            LEFT JOIN students s ON c.class_id = s.class_id
            GROUP BY c.class_id, c.class_name
            ORDER BY c.class_name
        """
        return db.execute_query(query)
