# Hướng dẫn nhanh - Push lên GitHub

## Repository name: `student-score-analytics`

### Các bước thực hiện:

1. **Tạo repository trên GitHub:**
   - Vào https://github.com/new
   - Tên repository: `student-score-analytics`
   - Chọn Public hoặc Private
   - **KHÔNG** tích "Initialize with README"
   - Click "Create repository"

2. **Chạy các lệnh sau trong terminal:**

```bash
# Thêm tất cả file
git add .

# Commit
git commit -m "Initial commit: Student Score Analytics - Web tính điểm GPA"

# Thêm remote (thay YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/student-score-analytics.git

# Đổi branch thành main
git branch -M main

# Push lên GitHub
git push -u origin main
```

### Hoặc chạy file batch (Windows):

```bash
push_to_github.bat
```

### Lưu ý khi push:

- Nếu hỏi username: nhập username GitHub của bạn
- Nếu hỏi password: **KHÔNG** dùng password GitHub
- Thay vào đó, dùng **Personal Access Token**:
  1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
  2. Generate new token (classic)
  3. Chọn quyền: `repo` (full control)
  4. Copy token và dán khi hỏi password

### Sau khi push thành công:

Truy cập: `https://github.com/YOUR_USERNAME/student-score-analytics`

