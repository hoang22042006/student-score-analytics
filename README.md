# Student Score Analytics - Web Tính Điểm GPA

**Đề tài:** Xây dựng Web Tính Điểm GPA

## Mô tả dự án

Ứng dụng web đơn giản giúp sinh viên tính điểm GPA (thang 4.0) theo các môn đã học. Web cho phép nhập danh sách môn học, tín chỉ và điểm, sau đó tự động tính toán GPA và điểm trung bình thang 10.

## Tính năng chính

1. **Nhập thông tin môn học**
   - Tên môn
   - Số tín chỉ (hỗ trợ số thập phân như 1.5, 2, 3, 4...)
   - Điểm (hỗ trợ cả thang 10 và thang 4)
   - Validation đầy đủ cho tất cả các trường

2. **Quản lý danh sách môn**
   - Thêm môn học mới
   - Xóa từng môn học
   - Xóa tất cả môn học (có xác nhận)
   - Lưu trữ tự động trên trình duyệt (localStorage)

3. **Tính toán kết quả**
   - Tổng số tín chỉ
   - GPA thang 4.0 (tự động quy đổi nếu nhập thang 10)
   - Điểm trung bình thang 10 (có trọng số theo tín chỉ)

4. **Giao diện**
   - Thiết kế hiện đại, responsive
   - Dễ sử dụng, trực quan
   - Hiển thị bảng quy đổi điểm thang 10 → 4

## Công nghệ sử dụng

- **Backend**: Python 3.x với Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS)
- **Lưu trữ**: localStorage (trình duyệt)

## Cài đặt và chạy

### Yêu cầu hệ thống

- Python 3.7 trở lên
- pip (Python package manager)

### Các bước cài đặt

1. **Clone hoặc tải dự án về máy**

2. **Cài đặt các thư viện cần thiết:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Chạy ứng dụng:**
   ```bash
   python app.py
   ```

4. **Mở trình duyệt và truy cập:**
   ```
   http://localhost:5000
   ```

## Cấu trúc dự án

```
do_an_py/
├── app.py                 # File chính Flask backend
├── requirements.txt       # Danh sách thư viện Python
├── README.md             # File hướng dẫn
├── templates/
│   └── index.html        # Giao diện HTML
└── static/
    ├── css/
    │   └── style.css     # File CSS styling
    └── js/
        └── main.js       # File JavaScript xử lý logic
```

## Hướng dẫn sử dụng

1. **Thêm môn học:**
   - Chọn hệ điểm nhập (Thang 10 hoặc Thang 4)
   - Nhập tên môn, số tín chỉ và điểm
   - Click nút "Thêm môn"

2. **Xem kết quả:**
   - Sau khi thêm môn, kết quả sẽ tự động được tính
   - Hoặc click nút "Tính lại GPA" để cập nhật

3. **Quản lý danh sách:**
   - Click nút "Xóa" ở mỗi dòng để xóa môn đó
   - Click "Xóa tất cả" để xóa toàn bộ danh sách

4. **Lưu trữ:**
   - Dữ liệu tự động được lưu trên trình duyệt
   - Khi refresh trang (F5), dữ liệu vẫn được giữ lại

## Bảng quy đổi điểm

| Thang 10 | Thang 4.0 |
|----------|-----------|
| 8.5 - 10.0 | 4.0 |
| 8.0 - 8.4 | 3.7 |
| 7.0 - 7.9 | 3.0 |
| 6.0 - 6.9 | 2.0 |
| 5.0 - 5.9 | 1.0 |
| < 5.0 | 0.0 |

**Lưu ý:** Bảng quy đổi chỉ mang tính tham khảo, hãy chỉnh theo quy định của trường bạn.

## Công thức tính GPA

### GPA thang 4.0:
```
GPA = Σ(điểm 4.0 × tín chỉ) / Σ tín chỉ
```

### Điểm trung bình thang 10:
```
Điểm TB = Σ(điểm 10 × tín chỉ) / Σ tín chỉ
```

## Test cases

### Test cơ bản:
- Nhập 1 môn: Toán cao cấp, 3 tín chỉ, điểm 8.0 (thang 10)
- Kiểm tra: Tổng tín chỉ = 3, GPA = 3.7

### Test nhiều môn:
- Thêm 3-5 môn với tín chỉ khác nhau
- Kiểm tra công thức tính chính xác

### Test validation:
- Bỏ trống tên môn → Hiện lỗi
- Điểm > 10 hoặc < 0 → Hiện lỗi
- Tín chỉ ≤ 0 → Hiện lỗi

## Tác giả

Đồ án được thực hiện cho môn học Python.

## License

Dự án này được tạo cho mục đích học tập.

