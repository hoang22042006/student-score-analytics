# Hướng dẫn Deploy lên Vercel từ GitHub

## Bước 1: Chuẩn bị code

✅ Đã tạo các file cần thiết:
- `vercel.json` - Cấu hình Vercel
- `api/index.py` - Entry point cho Vercel
- `requirements.txt` - Dependencies

## Bước 2: Push code lên GitHub (nếu chưa push)

```bash
git add .
git commit -m "Add Vercel configuration"
git push
```

## Bước 3: Đăng ký/Đăng nhập Vercel

1. Vào https://vercel.com
2. Click **"Sign Up"** hoặc **"Log In"**
3. Chọn **"Continue with GitHub"** để đăng nhập bằng tài khoản GitHub

## Bước 4: Import Project từ GitHub

1. Sau khi đăng nhập, click **"Add New..."** → **"Project"**
2. Tìm repository **"student-score-analytics"**
3. Click **"Import"**

## Bước 5: Cấu hình Project

Vercel sẽ tự động phát hiện:
- **Framework Preset:** Other (hoặc Python)
- **Root Directory:** `./` (giữ nguyên)
- **Build Command:** Để trống (hoặc `pip install -r requirements.txt`)
- **Output Directory:** Để trống
- **Install Command:** `pip install -r requirements.txt`

**Quan trọng:** Đảm bảo:
- Python Version: 3.x
- Build Command: Để trống hoặc không cần
- Output Directory: Để trống

## Bước 6: Deploy

1. Click **"Deploy"**
2. Chờ quá trình build (khoảng 1-2 phút)
3. Khi hoàn thành, bạn sẽ nhận được URL như: `https://student-score-analytics.vercel.app`

## Bước 7: Kiểm tra

Mở URL được cung cấp và kiểm tra ứng dụng hoạt động.

## Lưu ý quan trọng:

### Vercel và Flask:

Vercel chủ yếu được thiết kế cho serverless functions và static sites. Flask app có thể hoạt động nhưng có một số hạn chế:

1. **Cold Start:** Lần đầu request có thể chậm (serverless)
2. **Timeout:** Mỗi function có giới hạn thời gian thực thi
3. **File System:** Chỉ đọc được, không ghi được

### Nếu gặp lỗi:

**Lỗi 404 hoặc không tìm thấy route:**
- Kiểm tra `vercel.json` đã đúng chưa
- Đảm bảo `api/index.py` import đúng `app`

**Lỗi import module:**
- Kiểm tra `requirements.txt` đã có đủ dependencies
- Đảm bảo Python version đúng

**Lỗi template không tìm thấy:**
- Kiểm tra đường dẫn `templates/` và `static/` đúng
- Vercel có thể cần cấu hình thêm cho static files

## Alternative: Dùng Render hoặc Railway (khuyến nghị cho Flask)

Nếu Vercel gặp vấn đề, có thể dùng:

### Render (miễn phí):
1. Vào https://render.com
2. Connect GitHub
3. Chọn "New Web Service"
4. Chọn repository
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `python app.py` hoặc `gunicorn app:app`

### Railway (miễn phí):
1. Vào https://railway.app
2. Connect GitHub
3. Deploy từ GitHub
4. Tự động detect Flask

## Cập nhật sau khi deploy:

Mỗi khi push code mới lên GitHub, Vercel sẽ tự động deploy lại (nếu bật Auto-deploy).

Hoặc deploy thủ công:
1. Vào Vercel Dashboard
2. Chọn project
3. Click "Redeploy"

