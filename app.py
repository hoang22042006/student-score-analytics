from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

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

# API endpoint để tính GPA
@app.route('/api/calculate', methods=['POST'])
def calculate_gpa():
    """API endpoint để tính GPA từ danh sách môn học"""
    try:
        data = request.json
        subjects = data.get('subjects', [])
        
        if not subjects:
            return jsonify({
                'total_credits': 0,
                'gpa_4': 0,
                'avg_10': 0
            })
        
        total_credits = 0
        sum_weighted_4 = 0
        sum_weighted_10 = 0
        
        for subject in subjects:
            credits = float(subject.get('credits', 0))
            input_grade = float(subject.get('inputGrade', 0))
            input_scale = subject.get('inputScale', '10')
            
            if input_scale == '10':
                point_10 = input_grade
                point_4 = convert10_to_4(input_grade)
            else:  # input_scale == '4'
                point_4 = input_grade
                point_10 = convert4_to_10(input_grade)
            
            total_credits += credits
            sum_weighted_4 += point_4 * credits
            sum_weighted_10 += point_10 * credits
        
        if total_credits > 0:
            gpa_4 = round(sum_weighted_4 / total_credits, 2)
            avg_10 = round(sum_weighted_10 / total_credits, 2)
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

@app.route('/')
def index():
    """Trang chủ"""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

