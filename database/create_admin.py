"""
Script để tạo tài khoản admin mặc định
Chạy file này sau khi đã chạy database/create_database.py
"""

import sys
import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Thêm thư mục gốc của project vào path để tìm module service
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from service import db, UsersRepository

def create_admin():
    """Tạo tài khoản admin mặc định"""
    print("=" * 60)
    print("TẠO TÀI KHOẢN ADMIN MẶC ĐỊNH")
    print("=" * 60)
    
    # Kết nối database
    if not db.connect():
        print("✗ Không thể kết nối database!")
        print("\nHãy chạy database/create_database.py trước!")
        return False
    
    try:
        # Kiểm tra xem đã có admin chưa
        admin = UsersRepository.get_user_by_username("admin")
        if admin:
            print("⚠ Tài khoản admin đã tồn tại!")
            print(f"   Username: admin")
            print(f"   User ID: {admin['user_id']}")
            response = input("\nBạn có muốn đặt lại mật khẩu? (y/n): ")
            if response.lower() == 'y':
                new_password = input("Nhập mật khẩu mới: ")
                UsersRepository.update_user(admin['user_id'], password=new_password)
                print("✓ Đã cập nhật mật khẩu admin!")
            return True
        
        # Tạo admin mới
        print("\nTạo tài khoản admin mặc định...")
        admin_id = UsersRepository.create_user(
            username="admin",
            email="admin@example.com",
            password="admin123",
            role="admin",
            full_name="Administrator"
        )
        
        print(f"\n✓ Đã tạo tài khoản admin thành công!")
        print(f"   Username: admin")
        print(f"   Password: admin123")
        print(f"   Email: admin@example.com")
        print(f"   Role: admin")
        print("\n⚠ LƯU Ý: Hãy đổi mật khẩu sau khi đăng nhập!")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        db.disconnect()

if __name__ == "__main__":
    success = create_admin()
    sys.exit(0 if success else 1)

