"""
Script helper để tạo file .env từ .env.example
"""

import os
import shutil

def create_env_file():
    """Tạo file .env từ template nếu chưa tồn tại"""
    # Thử tìm .env.example trước, nếu không có thì dùng env_template.txt
    env_example = '.env.example'
    env_template = 'env_template.txt'
    env_file = '.env'
    
    template_file = None
    if os.path.exists(env_example):
        template_file = env_example
    elif os.path.exists(env_template):
        template_file = env_template
    else:
        print(f"✗ Không tìm thấy file template (.env.example hoặc env_template.txt)")
        print("Hãy tạo file template trước!")
        return False
    
    if os.path.exists(env_file):
        print(f"⚠ File {env_file} đã tồn tại!")
        response = input("Bạn có muốn ghi đè không? (y/n): ")
        if response.lower() != 'y':
            print("Đã hủy.")
            return False
    
    try:
        shutil.copy(template_file, env_file)
        print(f"✓ Đã tạo file {env_file} từ {template_file}")
        print(f"\n📝 Hãy mở file {env_file} và điền thông tin MySQL của bạn:")
        print("   - DB_PASSWORD: Password MySQL của bạn")
        print("   - DB_USER: Username MySQL (mặc định: root)")
        print("   - DB_HOST: Host MySQL (mặc định: localhost)")
        return True
    except Exception as e:
        print(f"✗ Lỗi khi tạo file: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("THIẾT LẬP FILE .ENV")
    print("=" * 60)
    print()
    create_env_file()

