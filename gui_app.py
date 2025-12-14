"""
Ứng dụng GUI tính điểm GPA sử dụng Tkinter
Yêu cầu: Giao diện người dùng đồ họa
"""
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import init_database, save_subject, get_all_subjects, delete_subject, delete_all_subjects

class GPAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tính điểm GPA - Ứng dụng Desktop")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f5f5f5')
        
        # Khởi tạo database
        init_database()
        
        # Danh sách môn học
        self.subjects = []
        self.load_subjects_from_db()
        
        # Tạo giao diện
        self.create_widgets()
        self.update_display()
        
    def convert10_to_4(self, grade_10):
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
    
    def convert4_to_10(self, grade_4):
        """Quy đổi điểm từ thang 4.0 sang thang 10"""
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
    
    def load_subjects_from_db(self):
        """Tải môn học từ database"""
        try:
            db_subjects = get_all_subjects()
            self.subjects = []
            for subj in db_subjects:
                self.subjects.append({
                    'id': subj['id'],
                    'name': subj['name'],
                    'credits': subj['credits'],
                    'inputGrade': subj['inputGrade'],
                    'inputScale': subj['inputScale'],
                    'point4': subj['point4'],
                    'point10': subj['point10']
                })
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")
    
    def create_widgets(self):
        """Tạo các widget cho giao diện"""
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="Tính điểm GPA", 
                               font=('Arial', 20, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame nhập liệu (bên trái)
        input_frame = ttk.LabelFrame(main_frame, text="Thêm môn học", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 10))
        
        # Hệ điểm
        ttk.Label(input_frame, text="Hệ điểm:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.grade_scale = ttk.Combobox(input_frame, values=["10", "4"], state="readonly", width=10)
        self.grade_scale.set("10")
        self.grade_scale.grid(row=0, column=1, pady=5, padx=5)
        
        # Tên môn
        ttk.Label(input_frame, text="Tên môn:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(input_frame, width=25)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Số tín chỉ
        ttk.Label(input_frame, text="Số tín chỉ:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.credits_entry = ttk.Entry(input_frame, width=25)
        self.credits_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Điểm
        ttk.Label(input_frame, text="Điểm:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.grade_entry = ttk.Entry(input_frame, width=25)
        self.grade_entry.grid(row=3, column=1, pady=5, padx=5)
        
        # Nút thêm
        add_btn = ttk.Button(input_frame, text="Thêm môn", command=self.add_subject)
        add_btn.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Frame kết quả
        result_frame = ttk.LabelFrame(main_frame, text="Kết quả", padding="10")
        result_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N))
        
        # Tổng tín chỉ
        ttk.Label(result_frame, text="Tổng số tín chỉ:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.total_credits_label = ttk.Label(result_frame, text="0", font=('Arial', 12, 'bold'))
        self.total_credits_label.grid(row=0, column=1, sticky=tk.W, padx=10)
        
        # GPA thang 4
        ttk.Label(result_frame, text="GPA (thang 4.0):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.gpa4_label = ttk.Label(result_frame, text="–", font=('Arial', 12, 'bold'), foreground='blue')
        self.gpa4_label.grid(row=1, column=1, sticky=tk.W, padx=10)
        
        # Điểm TB thang 10
        ttk.Label(result_frame, text="Điểm TB (thang 10):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.avg10_label = ttk.Label(result_frame, text="–", font=('Arial', 12, 'bold'), foreground='green')
        self.avg10_label.grid(row=2, column=1, sticky=tk.W, padx=10)
        
        # Nút xóa tất cả
        clear_btn = ttk.Button(result_frame, text="Xóa tất cả", command=self.clear_all)
        clear_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Frame danh sách môn học
        list_frame = ttk.LabelFrame(main_frame, text="Danh sách môn học", padding="10")
        list_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview để hiển thị danh sách
        columns = ('STT', 'Tên môn', 'Tín chỉ', 'Điểm nhập', 'Hệ điểm', 'Điểm 4.0', 'Điểm 10')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Nút xóa môn đã chọn
        delete_btn = ttk.Button(list_frame, text="Xóa môn đã chọn", command=self.delete_selected)
        delete_btn.grid(row=1, column=0, pady=5)
        
        # Frame biểu đồ Matplotlib
        chart_frame = ttk.LabelFrame(main_frame, text="Dashboard - Biểu đồ Matplotlib", padding="10")
        chart_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        chart_frame.columnconfigure(0, weight=1)
        chart_frame.columnconfigure(1, weight=1)
        chart_frame.rowconfigure(0, weight=1)
        
        # Tạo biểu đồ
        self.create_charts(chart_frame)
    
    def create_charts(self, parent):
        """Tạo biểu đồ Matplotlib"""
        # Biểu đồ cột
        self.fig_bar = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax_bar = self.fig_bar.add_subplot(111)
        self.canvas_bar = FigureCanvasTkAgg(self.fig_bar, parent)
        self.canvas_bar.get_tk_widget().grid(row=0, column=0, padx=5)
        
        # Biểu đồ tròn
        self.fig_pie = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax_pie = self.fig_pie.add_subplot(111)
        self.canvas_pie = FigureCanvasTkAgg(self.fig_pie, parent)
        self.canvas_pie.get_tk_widget().grid(row=0, column=1, padx=5)
    
    def validate_input(self, name, credits, grade, scale):
        """Kiểm tra dữ liệu đầu vào"""
        errors = []
        
        if not name or name.strip() == '':
            errors.append("Vui lòng nhập tên môn")
        
        try:
            credits_val = float(credits)
            if credits_val <= 0:
                errors.append("Tín chỉ phải lớn hơn 0")
        except ValueError:
            errors.append("Tín chỉ phải là số")
        
        try:
            grade_val = float(grade)
            if scale == '10':
                if grade_val < 0 or grade_val > 10:
                    errors.append("Điểm phải nằm trong khoảng 0-10")
            else:
                if grade_val < 0 or grade_val > 4:
                    errors.append("Điểm phải nằm trong khoảng 0-4")
        except ValueError:
            errors.append("Điểm phải là số")
        
        return errors
    
    def add_subject(self):
        """Thêm môn học"""
        name = self.name_entry.get()
        credits = self.credits_entry.get()
        grade = self.grade_entry.get()
        scale = self.grade_scale.get()
        
        # Validation
        errors = self.validate_input(name, credits, grade, scale)
        if errors:
            messagebox.showerror("Lỗi", "\n".join(errors))
            return
        
        # Tính điểm
        credits_val = float(credits)
        grade_val = float(grade)
        
        if scale == '10':
            point_4 = self.convert10_to_4(grade_val)
            point_10 = grade_val
        else:
            point_4 = grade_val
            point_10 = self.convert4_to_10(grade_val)
        
        # Lưu vào database
        try:
            subject_id = save_subject(name, credits_val, grade_val, scale, point_4, point_10)
            
            # Thêm vào danh sách
            self.subjects.append({
                'id': subject_id,
                'name': name,
                'credits': credits_val,
                'inputGrade': grade_val,
                'inputScale': scale,
                'point4': point_4,
                'point10': point_10
            })
            
            # Cập nhật hiển thị
            self.update_display()
            
            # Xóa form
            self.name_entry.delete(0, tk.END)
            self.credits_entry.delete(0, tk.END)
            self.grade_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu môn học: {str(e)}")
    
    def delete_selected(self):
        """Xóa môn học đã chọn"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn môn học cần xóa")
            return
        
        item = self.tree.item(selected[0])
        subject_name = item['values'][1]
        
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa môn '{subject_name}'?"):
            # Tìm ID của môn học
            index = int(item['values'][0]) - 1
            if 0 <= index < len(self.subjects):
                subject_id = self.subjects[index]['id']
                
                try:
                    delete_subject(subject_id)
                    self.subjects.pop(index)
                    self.update_display()
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Không thể xóa môn học: {str(e)}")
    
    def clear_all(self):
        """Xóa tất cả môn học"""
        if not self.subjects:
            messagebox.showinfo("Thông báo", "Danh sách đã trống")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa tất cả môn học?"):
            try:
                delete_all_subjects()
                self.subjects = []
                self.update_display()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa: {str(e)}")
    
    def calculate_gpa(self):
        """Tính GPA sử dụng Pandas và NumPy"""
        if not self.subjects:
            return 0, 0, 0
        
        # Tạo DataFrame từ danh sách môn học
        df = pd.DataFrame(self.subjects)
        df['credits'] = pd.to_numeric(df['credits'])
        df['point4'] = pd.to_numeric(df['point4'])
        df['point10'] = pd.to_numeric(df['point10'])
        
        # Tính tổng tín chỉ
        total_credits = df['credits'].sum()
        
        # Tính GPA bằng numpy (weighted average)
        if total_credits > 0:
            weighted_sum_4 = np.sum(df['point4'] * df['credits'])
            weighted_sum_10 = np.sum(df['point10'] * df['credits'])
            
            gpa_4 = round(weighted_sum_4 / total_credits, 2)
            avg_10 = round(weighted_sum_10 / total_credits, 2)
        else:
            gpa_4 = 0
            avg_10 = 0
        
        return total_credits, gpa_4, avg_10
    
    def update_charts(self):
        """Cập nhật biểu đồ Matplotlib"""
        if not self.subjects:
            self.ax_bar.clear()
            self.ax_pie.clear()
            self.canvas_bar.draw()
            self.canvas_pie.draw()
            return
        
        # Tạo DataFrame
        df = pd.DataFrame(self.subjects)
        df['point4'] = pd.to_numeric(df['point4'])
        
        # Biểu đồ cột
        self.ax_bar.clear()
        self.ax_bar.bar(df['name'], df['point4'], color='#667eea', alpha=0.7)
        self.ax_bar.set_xlabel('Môn học', fontweight='bold')
        self.ax_bar.set_ylabel('Điểm thang 4.0', fontweight='bold')
        self.ax_bar.set_title('Biểu đồ cột - Điểm từng môn học', fontweight='bold')
        self.ax_bar.set_ylim(0, 4.0)
        self.ax_bar.tick_params(axis='x', rotation=45)
        self.ax_bar.grid(axis='y', alpha=0.3)
        self.fig_bar.tight_layout()
        self.canvas_bar.draw()
        
        # Biểu đồ tròn - Phân bố học lực
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
        
        self.ax_pie.clear()
        self.ax_pie.pie(grade_counts.values, labels=grade_counts.index, autopct='%1.1f%%',
                       colors=colors, startangle=90, textprops={'fontweight': 'bold'})
        self.ax_pie.set_title('Biểu đồ tròn - Phân bố học lực', fontweight='bold')
        self.fig_pie.tight_layout()
        self.canvas_pie.draw()
    
    def update_display(self):
        """Cập nhật hiển thị"""
        # Xóa dữ liệu cũ trong treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Thêm dữ liệu mới
        for idx, subject in enumerate(self.subjects, 1):
            self.tree.insert('', tk.END, values=(
                idx,
                subject['name'],
                subject['credits'],
                subject['inputGrade'],
                f"Thang {subject['inputScale']}",
                f"{subject['point4']:.2f}",
                f"{subject['point10']:.2f}"
            ))
        
        # Tính và hiển thị GPA
        total_credits, gpa_4, avg_10 = self.calculate_gpa()
        
        self.total_credits_label.config(text=f"{total_credits:.1f}")
        self.gpa4_label.config(text=f"{gpa_4:.2f}" if gpa_4 > 0 else "–")
        self.avg10_label.config(text=f"{avg_10:.2f}" if avg_10 > 0 else "–")
        
        # Cập nhật biểu đồ
        self.update_charts()

def main():
    """Hàm main để chạy ứng dụng"""
    root = tk.Tk()
    app = GPAApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()


