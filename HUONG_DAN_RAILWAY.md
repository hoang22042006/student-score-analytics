# Hướng dẫn Deploy lên Railway từ GitHub

## Bước 1: Chuẩn bị code

✅ Đã tạo các file cần thiết:
- `Procfile` - Chỉ định lệnh chạy ứng dụng
- `runtime.txt` - Chỉ định phiên bản Python
- `railway.json` - Cấu hình Railway (tùy chọn)
- `requirements.txt` - Dependencies (đã có)

## Bước 2: Push code lên GitHub (nếu chưa push)

```bash
git add .
git commit -m "Add Railway configuration"
git push
```

## Bước 3: Đăng ký/Đăng nhập Railway

1. Vào https://railway.app
2. Click **"Start a New Project"** hoặc **"Login"**
3. Chọn **"Login with GitHub"** để đăng nhập bằng tài khoản GitHub

## Bước 4: Tạo Project mới

1. Sau khi đăng nhập, click **"New Project"**
2. Chọn **"Deploy from GitHub repo"**
3. Tìm và chọn repository **"student-score-analytics"**
4. Click **"Deploy Now"**

## Bước 5: Cấu hình (Railway tự động detect)

Railway sẽ tự động:
- ✅ Phát hiện đây là Python project
- ✅ Đọc `requirements.txt` và cài đặt dependencies
- ✅ Chạy lệnh từ `Procfile`: `python app.py`

**Nếu cần cấu hình thủ công:**
- **Build Command:** Để trống (Railway tự động)
- **Start Command:** `python app.py` (hoặc từ Procfile)
- **Python Version:** Từ `runtime.txt` hoặc tự động

## Bước 6: Thêm Environment Variables (nếu cần)

Thông thường Flask app này không cần env vars, nhưng nếu cần:
1. Vào **Settings** → **Variables**
2. Thêm các biến môi trường (nếu có)

## Bước 7: Deploy

1. Railway sẽ tự động build và deploy
2. Chờ quá trình hoàn thành (2-3 phút)
3. Khi xong, click vào **"Generate Domain"** để lấy URL công khai
4. URL sẽ có dạng: `https://student-score-analytics-production.up.railway.app`

## Bước 8: Kiểm tra

Mở URL được cung cấp và kiểm tra ứng dụng hoạt động.

## Lưu ý quan trọng:

### Port và Host:

Railway tự động cung cấp PORT qua environment variable. Cần sửa `app.py` để sử dụng PORT từ env:

```python
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
```

### Auto-deploy:

- Mỗi khi push code mới lên GitHub, Railway sẽ tự động deploy lại
- Có thể tắt auto-deploy trong Settings nếu muốn

### Logs:

- Xem logs real-time trong Railway Dashboard
- Rất hữu ích để debug nếu có lỗi

### Free Tier:

- Railway có free tier với $5 credit/tháng
- Đủ để chạy Flask app nhỏ
- Sau khi hết credit, cần upgrade hoặc dừng

## Troubleshooting:

**Lỗi "Port not found":**
- Đảm bảo app.py sử dụng PORT từ environment variable

**Lỗi "Module not found":**
- Kiểm tra `requirements.txt` có đủ dependencies
- Railway sẽ tự động cài từ requirements.txt

**Lỗi "Template not found":**
- Đảm bảo thư mục `templates/` và `static/` được commit lên GitHub

**App không chạy:**
- Kiểm tra logs trong Railway Dashboard
- Đảm bảo `Procfile` đúng format

## So sánh Railway vs Vercel:

| Tính năng | Railway | Vercel |
|-----------|---------|--------|
| Flask Support | ✅ Tốt | ⚠️ Hạn chế |
| Free Tier | ✅ $5/tháng | ✅ Miễn phí |
| Auto-deploy | ✅ Có | ✅ Có |
| Logs | ✅ Real-time | ✅ Có |
| Database | ✅ Hỗ trợ | ❌ Không |

**Kết luận:** Railway phù hợp hơn cho Flask app!

