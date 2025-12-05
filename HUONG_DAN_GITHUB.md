# Hướng dẫn đưa dự án lên GitHub

## Bước 1: Khởi tạo Git repository (nếu chưa có)

```bash
git init
```

## Bước 2: Thêm tất cả các file vào staging

```bash
git add .
```

## Bước 3: Commit lần đầu

```bash
git commit -m "Initial commit: Web tính điểm GPA"
```

## Bước 4: Tạo repository trên GitHub

1. Đăng nhập vào GitHub: https://github.com
2. Click nút **"New"** hoặc **"+"** → **"New repository"**
3. Đặt tên repository: **`student-score-analytics`**
4. Mô tả (tùy chọn): "Web application tính điểm GPA và phân tích điểm số sinh viên"
5. Chọn **Public** hoặc **Private** (tùy bạn)
6. **KHÔNG** tích vào "Initialize with README" (vì đã có code rồi)
7. Click **"Create repository"**

## Bước 5: Kết nối với GitHub và push code

Sau khi tạo repository, GitHub sẽ hiển thị các lệnh. Chạy:

```bash
# Thêm remote (thay YOUR_USERNAME bằng username GitHub của bạn)
git remote add origin https://github.com/YOUR_USERNAME/student-score-analytics.git

# Đổi tên branch chính thành main (nếu cần)
git branch -M main

# Push code lên GitHub
git push -u origin main
```

## Ví dụ cụ thể:

Nếu username GitHub của bạn là `nguyenvana`:

```bash
git remote add origin https://github.com/nguyenvana/student-score-analytics.git
git branch -M main
git push -u origin main
```

## Lần sau khi cập nhật code:

```bash
git add .
git commit -m "Mô tả thay đổi"
git push
```

## Lưu ý:

- File `.gitignore` đã được tạo sẵn để không commit các file không cần thiết
- Không commit file `__pycache__`, `venv/`, `.env` (nếu có)
- README.md đã có sẵn, GitHub sẽ tự động hiển thị

## Nếu gặp lỗi authentication:

GitHub yêu cầu xác thực. Có 2 cách:

### Cách 1: Dùng Personal Access Token (khuyến nghị)
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Copy token và dùng thay password khi push

### Cách 2: Dùng GitHub CLI
```bash
gh auth login
```

