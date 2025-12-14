# Đáp ứng yêu cầu đề tài thi cuối kỳ

## Danh sách yêu cầu và trạng thái

### ✅ 1. Python
- **Trạng thái**: Đã đáp ứng
- **Chi tiết**: 
  - Ứng dụng web: `app.py` (Flask)
  - Ứng dụng GUI: `gui_app.py` (Tkinter)
  - Xử lý dữ liệu: `database.py`

### ✅ 2. Giao diện người dùng đồ họa (GUI)
- **Trạng thái**: Đã đáp ứng
- **Chi tiết**:
  - **Ứng dụng Desktop GUI**: `gui_app.py` sử dụng Tkinter
    - Giao diện đồ họa đầy đủ với các widget: Entry, Button, Treeview, LabelFrame
    - Hiển thị danh sách môn học trong bảng
    - Form nhập liệu với validation
    - Tích hợp Matplotlib để vẽ biểu đồ trực tiếp trong GUI
  - **Ứng dụng Web**: `templates/index.html` với giao diện web hiện đại

### ✅ 3. Xử lý dữ liệu
- **Trạng thái**: Đã đáp ứng đầy đủ
- **Chi tiết**:
  - **MySQL**: Hỗ trợ kết nối MySQL database (có thể cấu hình qua environment variables)
    - File: `database.py`
    - Cấu hình: `USE_MYSQL`, `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`
  - **SQLite**: Database mặc định (không cần cấu hình)
  - **NumPy**: Sử dụng để tính toán weighted average
    - File: `app.py` (dòng 85-89)
    - File: `gui_app.py` (hàm calculate_gpa)
  - **Pandas**: Xử lý dữ liệu dạng DataFrame
    - File: `app.py` (dòng 61, 182)
    - File: `gui_app.py` (hàm calculate_gpa, update_charts)
  - **Network**: Ứng dụng web sử dụng Flask với RESTful API
    - Endpoints: `/api/calculate`, `/api/subjects`, `/api/charts`, `/api/charts/matplotlib`

### ✅ 4. Dashboard (vẽ biểu đồ) - Matplotlib
- **Trạng thái**: Đã đáp ứng đầy đủ
- **Chi tiết**:
  - **Backend API**: `/api/charts/matplotlib` trong `app.py`
    - Tạo biểu đồ cột (Bar Chart) bằng Matplotlib
    - Tạo biểu đồ tròn (Pie Chart) bằng Matplotlib
    - Trả về dưới dạng base64 để hiển thị trên web
  - **GUI Application**: Tích hợp Matplotlib trực tiếp trong Tkinter
    - File: `gui_app.py`
    - Hàm `create_charts()`: Tạo Figure và Canvas
    - Hàm `update_charts()`: Vẽ biểu đồ cột và biểu đồ tròn
    - Sử dụng `FigureCanvasTkAgg` để nhúng vào Tkinter

## Cấu trúc dự án

```
student-score-analytics-main/
├── app.py                 # Flask web application với Matplotlib API
├── gui_app.py            # Tkinter GUI application với Matplotlib
├── database.py           # Database layer (SQLite/MySQL)
├── requirements.txt      # Dependencies (bao gồm matplotlib, mysql-connector-python)
├── templates/
│   └── index.html        # Web interface
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## Cách chạy ứng dụng

### 1. Web Application (Flask)
```bash
pip install -r requirements.txt
python app.py
```
Truy cập: http://localhost:5000

### 2. GUI Application (Tkinter)
```bash
pip install -r requirements.txt
python gui_app.py
```

### 3. Cấu hình MySQL (tùy chọn)
Thiết lập các biến môi trường:
```bash
export USE_MYSQL=True
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DATABASE=gpa_db
```

## Tính năng chính

1. **Nhập và quản lý môn học**
   - Thêm môn học với tên, tín chỉ, điểm
   - Hỗ trợ cả thang điểm 10 và thang điểm 4
   - Xóa từng môn hoặc xóa tất cả

2. **Tính toán GPA**
   - Sử dụng NumPy để tính weighted average
   - Sử dụng Pandas để xử lý dữ liệu
   - Tự động quy đổi giữa thang 10 và thang 4

3. **Lưu trữ dữ liệu**
   - SQLite (mặc định)
   - MySQL (tùy chọn)

4. **Dashboard với Matplotlib**
   - Biểu đồ cột: So sánh điểm từng môn
   - Biểu đồ tròn: Phân bố học lực (A, B, C, D, F)
   - Tích hợp trong cả web và GUI

## Dependencies

- Flask==3.0.0
- pandas==2.1.4
- numpy==1.26.2
- matplotlib==3.8.2 ✅
- mysql-connector-python==8.2.0 ✅
- Pillow==10.2.0 (cho GUI)

## Kết luận

✅ **Tất cả yêu cầu đã được đáp ứng đầy đủ:**
- ✅ Python
- ✅ Giao diện người dùng đồ họa (Tkinter GUI)
- ✅ Xử lý dữ liệu (MySQL/numpy/Pandas/Network)
- ✅ Dashboard (vẽ biểu đồ) - Matplotlib


