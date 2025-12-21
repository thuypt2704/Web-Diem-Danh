import mysql.connector
from mysql.connector import Error
import os
from typing import Optional
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

class DatabaseConnection:
    """Quản lý kết nối MySQL database"""
    
    def __init__(self):
        self.connection: Optional[mysql.connector.MySQLConnection] = None
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'ai_attendance'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci'
        }
    
    def connect(self):
        """Tạo kết nối đến database"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print(f"Kết nối thành công đến database: {self.config['database']}")
                return True
        except Error as e:
            print(f"Lỗi kết nối database: {e}")
            return False
    
    def disconnect(self):
        """Đóng kết nối database"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Đã đóng kết nối database")
    
    def get_connection(self):
        """Lấy connection object"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection
    
    def execute_query(self, query: str, params: tuple = None):
        """Thực thi query SELECT và trả về kết quả"""
        try:
            cursor = self.get_connection().cursor(dictionary=True)
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"Lỗi thực thi query: {e}")
            return []
    
    def execute_update(self, query: str, params: tuple = None):
        """Thực thi query INSERT/UPDATE/DELETE"""
        try:
            cursor = self.get_connection().cursor()
            cursor.execute(query, params)
            self.connection.commit()
            affected_rows = cursor.rowcount
            last_id = cursor.lastrowid
            cursor.close()
            return affected_rows, last_id
        except Error as e:
            if self.connection:
                self.connection.rollback()
            print(f"Lỗi thực thi update: {e}")
            return 0, None

# Singleton instance
db = DatabaseConnection()

