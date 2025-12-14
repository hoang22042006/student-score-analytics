import sqlite3
import os
from datetime import datetime

# Cấu hình database - mặc định sử dụng SQLite, có thể chuyển sang MySQL
USE_MYSQL = os.environ.get('USE_MYSQL', 'False').lower() == 'true'
MYSQL_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'port': int(os.environ.get('MYSQL_PORT', 3306)),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', ''),
    'database': os.environ.get('MYSQL_DATABASE', 'gpa_db')
}

# Đường dẫn database SQLite
DB_PATH = 'gpa_database.db'

def get_connection():
    """Lấy kết nối database (SQLite hoặc MySQL)"""
    if USE_MYSQL:
        try:
            import mysql.connector
            return mysql.connector.connect(**MYSQL_CONFIG)
        except ImportError:
            print("Warning: mysql-connector-python not installed, falling back to SQLite")
            return sqlite3.connect(DB_PATH)
        except Exception as e:
            print(f"Error connecting to MySQL: {e}, falling back to SQLite")
            return sqlite3.connect(DB_PATH)
    else:
        return sqlite3.connect(DB_PATH)

def init_database():
    """Khởi tạo database và bảng"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if USE_MYSQL:
        # Tạo bảng subjects cho MySQL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                credits DECIMAL(5,2) NOT NULL,
                input_grade DECIMAL(5,2) NOT NULL,
                input_scale VARCHAR(10) NOT NULL,
                point_4 DECIMAL(5,2) NOT NULL,
                point_10 DECIMAL(5,2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    else:
        # Tạo bảng subjects cho SQLite
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                credits REAL NOT NULL,
                input_grade REAL NOT NULL,
                input_scale TEXT NOT NULL,
                point_4 REAL NOT NULL,
                point_10 REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    conn.commit()
    conn.close()

def save_subject(name, credits, input_grade, input_scale, point_4, point_10):
    """Lưu môn học vào database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO subjects (name, credits, input_grade, input_scale, point_4, point_10)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''' if USE_MYSQL else '''
        INSERT INTO subjects (name, credits, input_grade, input_scale, point_4, point_10)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, credits, input_grade, input_scale, point_4, point_10))
    
    conn.commit()
    subject_id = cursor.lastrowid
    conn.close()
    return subject_id

def get_all_subjects():
    """Lấy tất cả môn học từ database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM subjects ORDER BY created_at DESC')
    rows = cursor.fetchall()
    
    conn.close()
    
    # Chuyển đổi sang dictionary
    subjects = []
    for row in rows:
        subjects.append({
            'id': row[0],
            'name': row[1],
            'credits': row[2],
            'inputGrade': row[3],
            'inputScale': row[4],
            'point4': row[5],
            'point10': row[6],
            'created_at': row[7] if len(row) > 7 else None
        })
    
    return subjects

def delete_subject(subject_id):
    """Xóa môn học khỏi database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM subjects WHERE id = %s' if USE_MYSQL else 'DELETE FROM subjects WHERE id = ?', (subject_id,))
    
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def delete_all_subjects():
    """Xóa tất cả môn học"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM subjects')
    
    conn.commit()
    conn.close()

def get_subjects_count():
    """Đếm số lượng môn học"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM subjects')
    count = cursor.fetchone()[0]
    
    conn.close()
    return count

