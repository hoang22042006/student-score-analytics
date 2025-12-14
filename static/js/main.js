// Lưu trữ danh sách môn học
let subjects = [];
let nextId = 1;

// Hàm quy đổi điểm từ thang 10 sang thang 4
function convert10To4(grade10) {
    if (grade10 >= 8.5) return 4.0;
    if (grade10 >= 8.0) return 3.7;
    if (grade10 >= 7.0) return 3.0;
    if (grade10 >= 6.0) return 2.0;
    if (grade10 >= 5.0) return 1.0;
    return 0.0;
}

// Hàm quy đổi điểm từ thang 4 sang thang 10 (xấp xỉ)
function convert4To10(grade4) {
    if (grade4 >= 4.0) return 9.0;
    if (grade4 >= 3.7) return 8.5;
    if (grade4 >= 3.0) return 7.5;
    if (grade4 >= 2.0) return 6.5;
    if (grade4 >= 1.0) return 5.5;
    return 4.0;
}

// Load dữ liệu từ database
async function loadFromDatabase() {
    try {
        const response = await fetch('/api/subjects', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            subjects = data.subjects || [];
            
            if (subjects.length > 0) {
                nextId = Math.max(...subjects.map(s => s.id)) + 1;
            } else {
                nextId = 1;
            }
            
            renderTable();
            calculateGPA();
            drawCharts();
        } else {
            console.error('Error loading from database:', response.statusText);
            // Fallback to localStorage nếu không load được từ database
            loadFromLocalStorage();
        }
    } catch (error) {
        console.error('Error loading from database:', error);
        // Fallback to localStorage nếu không load được từ database
        loadFromLocalStorage();
    }
}

// Load dữ liệu từ localStorage (backup)
function loadFromLocalStorage() {
    const saved = localStorage.getItem('gpaSubjects');
    if (saved) {
        subjects = JSON.parse(saved);
        if (subjects.length > 0) {
            nextId = Math.max(...subjects.map(s => s.id)) + 1;
        }
        renderTable();
        calculateGPA();
    }
}

// Lưu dữ liệu vào localStorage (backup)
function saveToLocalStorage() {
    localStorage.setItem('gpaSubjects', JSON.stringify(subjects));
}

// Validation form
function validateForm(name, credits, grade, scale) {
    const errors = [];
    
    if (!name || name.trim() === '') {
        errors.push('Vui lòng nhập tên môn');
    }
    
    if (!credits || credits <= 0) {
        errors.push('Tín chỉ phải lớn hơn 0');
    }
    
    if (scale === '10') {
        if (grade < 0 || grade > 10) {
            errors.push('Điểm phải nằm trong khoảng 0–10');
        }
    } else {
        if (grade < 0 || grade > 4) {
            errors.push('Điểm phải nằm trong khoảng 0–4');
        }
    }
    
    return errors;
}

// Thêm môn học
async function addSubject(name, credits, grade, scale) {
    const subject = {
        name: name.trim(),
        credits: parseFloat(credits),
        inputGrade: parseFloat(grade),
        inputScale: scale
    };
    
    try {
        // Lưu vào database
        const response = await fetch('/api/subjects', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(subject)
        });
        
        if (response.ok) {
            const data = await response.json();
            // Load lại từ database để có ID chính xác
            await loadFromDatabase();
        } else {
            const errorData = await response.json();
            console.error('Error saving to database:', errorData.error);
            alert('Lỗi khi lưu môn học vào database: ' + (errorData.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error saving to database:', error);
        alert('Lỗi khi lưu môn học: ' + error.message);
    }
}

// Xóa môn học
async function removeSubject(id) {
    try {
        const response = await fetch(`/api/subjects/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            // Load lại từ database
            await loadFromDatabase();
        } else {
            const errorData = await response.json();
            console.error('Error deleting from database:', errorData.error);
            alert('Lỗi khi xóa môn học: ' + (errorData.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error deleting from database:', error);
        alert('Lỗi khi xóa môn học: ' + error.message);
    }
}

// Xóa tất cả môn học
function clearAllSubjects() {
    const modal = document.getElementById('confirmModal');
    modal.classList.add('show');
}

// Xác nhận xóa
async function confirmDeleteAll() {
    try {
        const response = await fetch('/api/subjects', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            subjects = [];
            nextId = 1;
            saveToLocalStorage(); // Xóa localStorage backup
            renderTable();
            calculateGPA();
            drawCharts();
            closeModal();
        } else {
            const errorData = await response.json();
            console.error('Error deleting all from database:', errorData.error);
            alert('Lỗi khi xóa tất cả môn học: ' + (errorData.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error deleting all from database:', error);
        alert('Lỗi khi xóa tất cả môn học: ' + error.message);
    }
}

// Đóng modal
function closeModal() {
    const modal = document.getElementById('confirmModal');
    modal.classList.remove('show');
}

// Render bảng môn học
function renderTable() {
    const tbody = document.getElementById('subjectsTableBody');
    const emptyMessage = document.getElementById('emptyMessage');
    const subjectCount = document.getElementById('subjectCount');
    
    subjectCount.textContent = `${subjects.length} môn`;
    
    if (subjects.length === 0) {
        tbody.innerHTML = '';
        emptyMessage.classList.add('show');
        return;
    }
    
    emptyMessage.classList.remove('show');
    
    tbody.innerHTML = subjects.map((subject, index) => `
        <tr>
            <td>${index + 1}</td>
            <td>${subject.name}</td>
            <td>${subject.credits}</td>
            <td>${subject.inputGrade}</td>
            <td>Thang ${subject.inputScale}</td>
            <td>${subject.point4.toFixed(2)}</td>
            <td>${subject.point10.toFixed(2)}</td>
            <td>
                <button class="btn btn-delete" onclick="removeSubject(${subject.id})">Xóa</button>
            </td>
        </tr>
    `).join('');
}

// Tính GPA
async function calculateGPA() {
    if (subjects.length === 0) {
        document.getElementById('totalCredits').textContent = '0';
        document.getElementById('gpa4').textContent = '–';
        document.getElementById('avg10').textContent = '–';
        return;
    }
    
    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ subjects: subjects })
        });
        
        const data = await response.json();
        
        document.getElementById('totalCredits').textContent = data.total_credits;
        document.getElementById('gpa4').textContent = data.gpa_4.toFixed(2);
        document.getElementById('avg10').textContent = data.avg_10.toFixed(2);
    } catch (error) {
        console.error('Error calculating GPA:', error);
        // Fallback tính toán phía client
        calculateGPAClient();
    }
}

// Tính GPA phía client (fallback)
function calculateGPAClient() {
    let totalCredits = 0;
    let sumWeighted4 = 0;
    let sumWeighted10 = 0;
    
    subjects.forEach(subject => {
        totalCredits += subject.credits;
        sumWeighted4 += subject.point4 * subject.credits;
        sumWeighted10 += subject.point10 * subject.credits;
    });
    
    const gpa4 = totalCredits > 0 ? sumWeighted4 / totalCredits : 0;
    const avg10 = totalCredits > 0 ? sumWeighted10 / totalCredits : 0;
    
    document.getElementById('totalCredits').textContent = totalCredits.toFixed(1);
    document.getElementById('gpa4').textContent = gpa4.toFixed(2);
    document.getElementById('avg10').textContent = avg10.toFixed(2);
}

// Cập nhật max của input điểm khi thay đổi hệ điểm
function updateGradeInput() {
    const gradeScale = document.getElementById('gradeScale').value;
    const gradeInput = document.getElementById('grade');
    
    if (gradeScale === '10') {
        gradeInput.max = 10;
        gradeInput.placeholder = '8.5';
    } else {
        gradeInput.max = 4;
        gradeInput.placeholder = '3.7';
    }
}

// Xử lý submit form
document.getElementById('subjectForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const name = document.getElementById('subjectName').value;
    const credits = document.getElementById('credits').value;
    const grade = document.getElementById('grade').value;
    const scale = document.getElementById('gradeScale').value;
    const errorMessage = document.getElementById('errorMessage');
    
    // Validation
    const errors = validateForm(name, credits, grade, scale);
    
    if (errors.length > 0) {
        errorMessage.textContent = errors.join(', ');
        return;
    }
    
    errorMessage.textContent = '';
    
    // Thêm môn (async)
    await addSubject(name, credits, grade, scale);
    
    // Reset form
    document.getElementById('subjectForm').reset();
    updateGradeInput();
});

// Xử lý thay đổi hệ điểm
document.getElementById('gradeScale').addEventListener('change', updateGradeInput);

// Xử lý nút tính lại GPA
document.getElementById('calculateBtn').addEventListener('click', calculateGPA);

// Xử lý nút xóa tất cả
document.getElementById('clearAllBtn').addEventListener('click', clearAllSubjects);

// Xử lý modal xác nhận
document.getElementById('confirmYes').addEventListener('click', confirmDeleteAll);
document.getElementById('confirmNo').addEventListener('click', closeModal);

// Đóng modal khi click bên ngoài
document.getElementById('confirmModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeModal();
    }
});

// Biến lưu Chart instances
let barChart = null;
let pieChart = null;

// Vẽ biểu đồ
async function drawCharts() {
    if (subjects.length === 0) {
        // Xóa biểu đồ nếu không có dữ liệu
        if (barChart) {
            barChart.destroy();
            barChart = null;
        }
        if (pieChart) {
            pieChart.destroy();
            pieChart = null;
        }
        return;
    }
    
    try {
        const response = await fetch('/api/charts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ subjects: subjects })
        });
        
        const data = await response.json();
        
        // Vẽ Bar Chart
        const barCtx = document.getElementById('barChart').getContext('2d');
        if (barChart) {
            barChart.destroy();
        }
        barChart = new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: data.barChart.labels,
                datasets: [{
                    label: 'Điểm thang 4.0',
                    data: data.barChart.data,
                    backgroundColor: 'rgba(102, 126, 234, 0.7)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 2,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'Điểm: ' + context.parsed.y.toFixed(2);
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 4.0,
                        ticks: {
                            stepSize: 0.5
                        },
                        title: {
                            display: true,
                            text: 'Điểm thang 4.0'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Môn học'
                        }
                    }
                }
            }
        });
        
        // Vẽ Pie Chart
        const pieCtx = document.getElementById('pieChart').getContext('2d');
        if (pieChart) {
            pieChart.destroy();
        }
        pieChart = new Chart(pieCtx, {
            type: 'pie',
            data: {
                labels: data.pieChart.labels,
                datasets: [{
                    data: data.pieChart.data,
                    backgroundColor: data.pieChart.colors,
                    borderColor: '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'right'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return label + ': ' + value + ' môn (' + percentage + '%)';
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error drawing charts:', error);
    }
}

// Khởi tạo
document.addEventListener('DOMContentLoaded', function() {
    loadFromDatabase(); // Load từ database thay vì localStorage
    updateGradeInput();
});

