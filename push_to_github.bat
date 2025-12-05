@echo off
echo ========================================
echo Push code len GitHub - student-score-analytics
echo ========================================
echo.

echo Buoc 1: Kiem tra trang thai...
git status
echo.

echo Buoc 2: Them tat ca file...
git add .
echo.

echo Buoc 3: Commit...
git commit -m "Initial commit: Student Score Analytics - Web tinh diem GPA"
echo.

echo ========================================
echo Buoc 4: Ket noi voi GitHub
echo ========================================
echo.
echo Vui long nhap username GitHub cua ban:
set /p GITHUB_USERNAME=

echo.
echo Dang ket noi voi: https://github.com/%GITHUB_USERNAME%/student-score-analytics.git
git remote add origin https://github.com/%GITHUB_USERNAME%/student-score-analytics.git
echo.

echo Buoc 5: Doi ten branch thanh main...
git branch -M main
echo.

echo Buoc 6: Push code len GitHub...
echo (Ban se can nhap username va password/token)
git push -u origin main
echo.

echo ========================================
echo Hoan thanh!
echo ========================================
pause

