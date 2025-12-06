import sqlite3
import os
from datetime import datetime

# Đường dẫn database
DB_PATH = 'gpa_database.db'

def init_database():
    """Khởi tạo database và bảng"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tạo bảng subjects
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
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO subjects (name, credits, input_grade, input_scale, point_4, point_10)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, credits, input_grade, input_scale, point_4, point_10))
    
    conn.commit()
    subject_id = cursor.lastrowid
    conn.close()
    return subject_id

def get_all_subjects():
    """Lấy tất cả môn học từ database"""
    conn = sqlite3.connect(DB_PATH)
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
            'created_at': row[7]
        })
    
    return subjects

def delete_subject(subject_id):
    """Xóa môn học khỏi database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM subjects WHERE id = ?', (subject_id,))
    
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def delete_all_subjects():
    """Xóa tất cả môn học"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM subjects')
    
    conn.commit()
    conn.close()

def get_subjects_count():
    """Đếm số lượng môn học"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM subjects')
    count = cursor.fetchone()[0]
    
    conn.close()
    return count

