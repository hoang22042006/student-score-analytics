from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import io
import base64
from database import init_database, save_subject, get_all_subjects, delete_subject, delete_all_subjects

app = Flask(__name__)

# Khởi tạo database khi app khởi động
init_database()

# Hàm quy đổi điểm từ thang 10 sang thang 4
def convert10_to_4(grade_10):
    """Quy đổi điểm từ thang 10 sang thang 4.0"""
    if grade_10 >= 8.5:
        return 4.0
    elif grade_10 >= 8.0:
        return 3.7
    elif grade_10 >= 7.0:
        return 3.0
    elif grade_10 >= 6.0:
        return 2.0
    elif grade_10 >= 5.0:
        return 1.0
    else:
        return 0.0

# Hàm quy đổi điểm từ thang 4 sang thang 10 (xấp xỉ)
def convert4_to_10(grade_4):
    """Quy đổi điểm từ thang 4.0 sang thang 10 (xấp xỉ)"""
    if grade_4 >= 4.0:
        return 9.0
    elif grade_4 >= 3.7:
        return 8.5
    elif grade_4 >= 3.0:
        return 7.5
    elif grade_4 >= 2.0:
        return 6.5
    elif grade_4 >= 1.0:
        return 5.5
    else:
        return 4.0

# API endpoint để tính GPA (sử dụng Pandas DataFrame)
@app.route('/api/calculate', methods=['POST'])
def calculate_gpa():
    """API endpoint để tính GPA từ danh sách môn học - Sử dụng Pandas"""
    try:
        data = request.json
        subjects = data.get('subjects', [])
        
        if not subjects:
            return jsonify({
                'total_credits': 0,
                'gpa_4': 0,
                'avg_10': 0
            })
        
        # Tạo DataFrame từ danh sách môn học
        df = pd.DataFrame(subjects)
        
        # Chuyển đổi kiểu dữ liệu
        df['credits'] = pd.to_numeric(df['credits'])
        df['inputGrade'] = pd.to_numeric(df['inputGrade'])
        
        # Tính điểm 4.0 và 10.0 cho từng môn
        def calculate_points(row):
            if row['inputScale'] == '10':
                point_10 = row['inputGrade']
                point_4 = convert10_to_4(row['inputGrade'])
            else:
                point_4 = row['inputGrade']
                point_10 = convert4_to_10(row['inputGrade'])
            return pd.Series([point_4, point_10])
        
        df[['point4', 'point10']] = df.apply(calculate_points, axis=1)
        
        # Tính tổng tín chỉ
        total_credits = df['credits'].sum()
        
        # Tính GPA bằng numpy (weighted average)
        if total_credits > 0:
            # Sử dụng numpy để tính weighted average
            weighted_sum_4 = np.sum(df['point4'] * df['credits'])
            weighted_sum_10 = np.sum(df['point10'] * df['credits'])
            
            gpa_4 = round(weighted_sum_4 / total_credits, 2)
            avg_10 = round(weighted_sum_10 / total_credits, 2)
        else:
            gpa_4 = 0
            avg_10 = 0
        
        return jsonify({
            'total_credits': round(total_credits, 1),
            'gpa_4': gpa_4,
            'avg_10': avg_10
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API endpoint để lưu môn học vào database
@app.route('/api/subjects', methods=['POST'])
def save_subject_api():
    """Lưu môn học vào SQLite database"""
    try:
        data = request.json
        name = data.get('name')
        credits = float(data.get('credits', 0))
        input_grade = float(data.get('inputGrade', 0))
        input_scale = data.get('inputScale', '10')
        
        # Tính điểm
        if input_scale == '10':
            point_10 = input_grade
            point_4 = convert10_to_4(input_grade)
        else:
            point_4 = input_grade
            point_10 = convert4_to_10(input_grade)
        
        # Lưu vào database
        subject_id = save_subject(name, credits, input_grade, input_scale, point_4, point_10)
        
        return jsonify({
            'success': True,
            'id': subject_id,
            'message': 'Môn học đã được lưu vào database'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API endpoint để lấy tất cả môn học từ database
@app.route('/api/subjects', methods=['GET'])
def get_subjects_api():
    """Lấy tất cả môn học từ SQLite database"""
    try:
        subjects = get_all_subjects()
        return jsonify({'subjects': subjects})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API endpoint để xóa môn học
@app.route('/api/subjects/<int:subject_id>', methods=['DELETE'])
def delete_subject_api(subject_id):
    """Xóa môn học khỏi database"""
    try:
        deleted = delete_subject(subject_id)
        if deleted:
            return jsonify({'success': True, 'message': 'Đã xóa môn học'})
        else:
            return jsonify({'error': 'Không tìm thấy môn học'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API endpoint để xóa tất cả
@app.route('/api/subjects', methods=['DELETE'])
def delete_all_subjects_api():
    """Xóa tất cả môn học"""
    try:
        delete_all_subjects()
        return jsonify({'success': True, 'message': 'Đã xóa tất cả môn học'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API endpoint để lấy dữ liệu cho biểu đồ
@app.route('/api/charts', methods=['POST'])
def get_chart_data():
    """Lấy dữ liệu cho biểu đồ Bar Chart và Pie Chart"""
    try:
        data = request.json
        subjects = data.get('subjects', [])
        
        if not subjects:
            return jsonify({
                'barChart': {'labels': [], 'data': []},
                'pieChart': {'labels': [], 'data': [], 'colors': []}
            })
        
        # Tạo DataFrame
        df = pd.DataFrame(subjects)
        df['credits'] = pd.to_numeric(df['credits'])
        df['inputGrade'] = pd.to_numeric(df['inputGrade'])
        
        # Tính điểm 4.0
        def calculate_point4(row):
            if row['inputScale'] == '10':
                return convert10_to_4(row['inputGrade'])
            else:
                return row['inputGrade']
        
        df['point4'] = df.apply(calculate_point4, axis=1)
        
        # Dữ liệu cho Bar Chart (điểm từng môn)
        bar_labels = df['name'].tolist()
        bar_data = df['point4'].tolist()
        
        # Dữ liệu cho Pie Chart (phân bố học lực)
        def get_grade_level(point4):
            if point4 >= 3.7:
                return 'A'
            elif point4 >= 3.0:
                return 'B'
            elif point4 >= 2.0:
                return 'C'
            elif point4 >= 1.0:
                return 'D'
            else:
                return 'F'
        
        df['grade_level'] = df['point4'].apply(get_grade_level)
        grade_counts = df['grade_level'].value_counts()
        
        # Màu sắc cho từng học lực
        color_map = {
            'A': '#27ae60',  # Xanh lá
            'B': '#3498db',  # Xanh dương
            'C': '#f39c12',  # Vàng
            'D': '#e67e22',  # Cam
            'F': '#e74c3c'   # Đỏ
        }
        
        pie_labels = grade_counts.index.tolist()
        pie_data = grade_counts.values.tolist()
        pie_colors = [color_map.get(label, '#95a5a6') for label in pie_labels]
        
        return jsonify({
            'barChart': {
                'labels': bar_labels,
                'data': bar_data
            },
            'pieChart': {
                'labels': pie_labels,
                'data': pie_data,
                'colors': pie_colors
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API endpoint để tạo biểu đồ bằng Matplotlib
@app.route('/api/charts/matplotlib', methods=['POST'])
def generate_matplotlib_charts():
    """Tạo biểu đồ bằng Matplotlib và trả về dưới dạng base64"""
    try:
        data = request.json
        subjects = data.get('subjects', [])
        
        if not subjects:
            return jsonify({
                'barChart': '',
                'pieChart': ''
            })
        
        # Tạo DataFrame
        df = pd.DataFrame(subjects)
        df['credits'] = pd.to_numeric(df['credits'])
        df['inputGrade'] = pd.to_numeric(df['inputGrade'])
        
        # Tính điểm 4.0
        def calculate_point4(row):
            if row['inputScale'] == '10':
                return convert10_to_4(row['inputGrade'])
            else:
                return row['inputGrade']
        
        df['point4'] = df.apply(calculate_point4, axis=1)
        
        # Tạo Bar Chart bằng Matplotlib
        plt.figure(figsize=(10, 6))
        plt.bar(df['name'], df['point4'], color='#667eea', alpha=0.7, edgecolor='#667eea', linewidth=2)
        plt.xlabel('Môn học', fontsize=12, fontweight='bold')
        plt.ylabel('Điểm thang 4.0', fontsize=12, fontweight='bold')
        plt.title('Biểu đồ cột - Điểm từng môn học', fontsize=14, fontweight='bold')
        plt.ylim(0, 4.0)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        # Chuyển đổi sang base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
        img_buffer.seek(0)
        bar_chart_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        plt.close()
        
        # Tạo Pie Chart bằng Matplotlib
        def get_grade_level(point4):
            if point4 >= 3.7:
                return 'A'
            elif point4 >= 3.0:
                return 'B'
            elif point4 >= 2.0:
                return 'C'
            elif point4 >= 1.0:
                return 'D'
            else:
                return 'F'
        
        df['grade_level'] = df['point4'].apply(get_grade_level)
        grade_counts = df['grade_level'].value_counts()
        
        color_map = {
            'A': '#27ae60',
            'B': '#3498db',
            'C': '#f39c12',
            'D': '#e67e22',
            'F': '#e74c3c'
        }
        
        colors = [color_map.get(label, '#95a5a6') for label in grade_counts.index]
        
        plt.figure(figsize=(8, 8))
        plt.pie(grade_counts.values, labels=grade_counts.index, autopct='%1.1f%%',
                colors=colors, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
        plt.title('Biểu đồ tròn - Phân bố học lực', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        # Chuyển đổi sang base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
        img_buffer.seek(0)
        pie_chart_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        plt.close()
        
        return jsonify({
            'barChart': bar_chart_base64,
            'pieChart': pie_chart_base64
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/')
def index():
    """Trang chủ"""
    return render_template('index.html')

if __name__ == '__main__':
    # Railway sẽ cung cấp PORT qua environment variable
    port = int(os.environ.get('PORT', 5000))
    # Tắt debug mode khi chạy trên production (Railway)
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

