from service.db_connection import db
from typing import List, Dict, Optional
from passlib.context import CryptContext
from datetime import datetime

# Cấu hình password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsersRepository:
    """Repository để quản lý người dùng và authentication"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Xác thực password"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_all_users() -> List[Dict]:
        """Lấy tất cả người dùng"""
        query = """
            SELECT 
                user_id,
                username,
                email,
                role,
                full_name,
                created_at,
                is_active
            FROM users
            ORDER BY created_at DESC
        """
        return db.execute_query(query)
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict]:
        """Lấy người dùng theo ID"""
        query = """
            SELECT 
                user_id,
                username,
                email,
                role,
                full_name,
                created_at,
                is_active
            FROM users
            WHERE user_id = %s
        """
        results = db.execute_query(query, (user_id,))
        return results[0] if results else None
    
    @staticmethod
    def get_user_by_username(username: str) -> Optional[Dict]:
        """Lấy người dùng theo username"""
        query = """
            SELECT 
                user_id,
                username,
                email,
                password_hash,
                role,
                full_name,
                created_at,
                is_active
            FROM users
            WHERE username = %s
        """
        results = db.execute_query(query, (username,))
        return results[0] if results else None
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict]:
        """Lấy người dùng theo email"""
        query = """
            SELECT 
                user_id,
                username,
                email,
                password_hash,
                role,
                full_name,
                created_at,
                is_active
            FROM users
            WHERE email = %s
        """
        results = db.execute_query(query, (email,))
        return results[0] if results else None
    
    @staticmethod
    def create_user(
        username: str,
        email: str,
        password: str,
        role: str = 'student',
        full_name: str = None
    ) -> int:
        """Tạo người dùng mới"""
        # Kiểm tra username đã tồn tại chưa
        if UsersRepository.get_user_by_username(username):
            raise ValueError("Username đã tồn tại")
        
        # Kiểm tra email đã tồn tại chưa
        if UsersRepository.get_user_by_email(email):
            raise ValueError("Email đã tồn tại")
        
        # Hash password
        password_hash = UsersRepository.hash_password(password)
        
        query = """
            INSERT INTO users (username, email, password_hash, role, full_name)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (username, email, password_hash, role, full_name)
        _, last_id = db.execute_update(query, params)
        return last_id
    
    @staticmethod
    def update_user(
        user_id: int,
        username: str = None,
        email: str = None,
        password: str = None,
        role: str = None,
        full_name: str = None,
        is_active: bool = None
    ) -> bool:
        """Cập nhật thông tin người dùng"""
        updates = []
        params = []
        
        if username:
            # Kiểm tra username đã tồn tại chưa (trừ user hiện tại)
            existing = UsersRepository.get_user_by_username(username)
            if existing and existing['user_id'] != user_id:
                raise ValueError("Username đã tồn tại")
            updates.append("username = %s")
            params.append(username)
        
        if email:
            # Kiểm tra email đã tồn tại chưa (trừ user hiện tại)
            existing = UsersRepository.get_user_by_email(email)
            if existing and existing['user_id'] != user_id:
                raise ValueError("Email đã tồn tại")
            updates.append("email = %s")
            params.append(email)
        
        if password:
            password_hash = UsersRepository.hash_password(password)
            updates.append("password_hash = %s")
            params.append(password_hash)
        
        if role:
            updates.append("role = %s")
            params.append(role)
        
        if full_name:
            updates.append("full_name = %s")
            params.append(full_name)
        
        if is_active is not None:
            updates.append("is_active = %s")
            params.append(is_active)
        
        if not updates:
            return False
        
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = %s"
        affected_rows, _ = db.execute_update(query, tuple(params))
        return affected_rows > 0
    
    @staticmethod
    def delete_user(user_id: int) -> bool:
        """Xóa người dùng"""
        query = "DELETE FROM users WHERE user_id = %s"
        affected_rows, _ = db.execute_update(query, (user_id,))
        return affected_rows > 0
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[Dict]:
        """Xác thực người dùng"""
        user = UsersRepository.get_user_by_username(username)
        if not user:
            return None
        
        if not user.get('is_active', True):
            return None
        
        if not UsersRepository.verify_password(password, user['password_hash']):
            return None
        
        # Xóa password_hash khỏi kết quả trả về
        user.pop('password_hash', None)
        return user

