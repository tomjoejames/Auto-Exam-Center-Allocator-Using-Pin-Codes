import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog, 
    QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox, QMessageBox
)
from PyQt5.QtGui import QIcon, QColor, QFont, QPalette
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve

class ExamAllocator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Exam Center Allocation")
        self.setGeometry(100, 100, 900, 600)
        
        # Set dark-themed, modern style
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;  /* Soft dark gray */
                color: #ffffff;  /* White text */
                font-family: "Segoe UI", sans-serif;
            }
            QPushButton {
                background-color: #0078d4;  /* Blue accent */
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005bb5;  /* Darker blue on hover */
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
            QTableWidget {
                background-color: #2d2d2d;  /* Darker gray for table */
                border-radius: 10px;
                gridline-color: #444;
                color: white;
                selection-background-color: #005577;
            }
            QHeaderView::section {
                background-color: #333;
                padding: 8px;
                border: none;
                font-size: 14px;
            }
            QGroupBox {
                background-color: #2d2d2d;
                border: 1px solid #444;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
                font-size: 16px;
                color: white;
            }
        """)
        
        layout = QVBoxLayout()
        
        # File upload section in a group box
        upload_group = QGroupBox("Upload Files")
        upload_layout = QHBoxLayout()
        
        self.student_file_btn = QPushButton("Upload Students File (CSV)")
        self.student_file_btn.setIcon(QIcon.fromTheme("document-open"))  # Add upload icon
        self.exam_center_file_btn = QPushButton("Upload Exam Centers File (CSV)")
        self.exam_center_file_btn.setIcon(QIcon.fromTheme("document-open"))  # Add upload icon
        
        upload_layout.addWidget(self.student_file_btn)
        upload_layout.addWidget(self.exam_center_file_btn)
        upload_group.setLayout(upload_layout)
        
        # Connect buttons to functions
        self.student_file_btn.clicked.connect(self.load_students)
        self.exam_center_file_btn.clicked.connect(self.load_centers)
        
        # Results Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)  # Add columns for Pincode and Exam Center Pincode
        self.table.setHorizontalHeaderLabels(["Student Name", "Pincode", "Nearest Exam Center", "Exam Center Pincode"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Add zebra striping to table rows
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                alternate-background-color: #3d3d3d;  /* Alternate row color */
            }
        """)
        
        # Download buttons
        download_layout = QHBoxLayout()
        self.download_excel_btn = QPushButton("Download Excel")
        self.download_excel_btn.setIcon(QIcon.fromTheme("document-save"))  # Add download icon
        self.download_pdf_btn = QPushButton("Download PDF")
        self.download_pdf_btn.setIcon(QIcon.fromTheme("document-save"))  # Add download icon
        
        download_layout.addWidget(self.download_excel_btn)
        download_layout.addWidget(self.download_pdf_btn)
        
        # Connect download buttons to functions
        self.download_excel_btn.clicked.connect(self.download_excel)
        self.download_pdf_btn.clicked.connect(self.download_pdf)
        
        # Footer
        footer = QLabel("Made with ❤️ by Tom Joe James")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("font-size: 12px; color: #aaa;")  # GitHub gray text
        
        # Add widgets to layout
        layout.addWidget(upload_group)
        layout.addWidget(self.table)
        layout.addLayout(download_layout)
        layout.addWidget(footer)
        
        self.setLayout(layout)
        
        self.students = []
        self.centers = []
    
    def load_students(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Students File", "", "CSV Files (*.csv)")
        if file_name:
            df = pd.read_csv(file_name)
            self.students = df[["Student Name", "Pincode"]].values.tolist()  # Load student name and pincode
            self.check_and_allocate()  # Check if both files are loaded
    
    def load_centers(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Exam Centers File", "", "CSV Files (*.csv)")
        if file_name:
            df = pd.read_csv(file_name)
            # Ensure the column name matches the CSV file
            if "Exam Center Name" in df.columns and "Pincode" in df.columns:  # Check for the correct column names
                self.centers = df[["Exam Center Name", "Pincode"]].values.tolist()  # Load exam center name and pincode
            else:
                QMessageBox.critical(self, "Error", "The CSV file must contain 'Exam Center Name' and 'Pincode' columns.")
            self.check_and_allocate()  # Check if both files are loaded
    
    def check_and_allocate(self):
        # Allocate centers only if both students and centers are loaded
        if self.students and self.centers:
            self.allocate_centers()
    
    def calculate_distance(self, student_pincode, center_pincode):
        # Calculate the absolute difference between PIN codes
        return abs(int(student_pincode) - int(center_pincode))
    
    def allocate_centers(self):
        # Set headers
        self.table.setHorizontalHeaderLabels(["Student Name", "Pincode", "Nearest Exam Center", "Exam Center Pincode"])
        
        # Populate the table
        self.table.setRowCount(len(self.students))
        for i, (student_name, student_pincode) in enumerate(self.students):
            # Find the closest exam center
            min_distance = float("inf")
            closest_center = None
            closest_center_pincode = None
            for center_name, center_pincode in self.centers:
                distance = self.calculate_distance(student_pincode, center_pincode)
                if distance < min_distance:
                    min_distance = distance
                    closest_center = center_name
                    closest_center_pincode = center_pincode
            
            # Add Student Name
            self.table.setItem(i, 0, QTableWidgetItem(student_name))
            # Add Student Pincode
            self.table.setItem(i, 1, QTableWidgetItem(str(student_pincode)))
            # Add Nearest Exam Center
            self.table.setItem(i, 2, QTableWidgetItem(closest_center))
            # Add Exam Center Pincode
            self.table.setItem(i, 3, QTableWidgetItem(str(closest_center_pincode)))
    
    def download_excel(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Excel Files (*.xlsx)")
        if file_name:
            data = {
                "Student Name": [student[0] for student in self.students],
                "Pincode": [student[1] for student in self.students],
                "Nearest Exam Center": [self.centers[i % len(self.centers)][0] for i in range(len(self.students))],
                "Exam Center Pincode": [self.centers[i % len(self.centers)][1] for i in range(len(self.students))]
            }
            df = pd.DataFrame(data)
            df.to_excel(file_name, index=False)
    
    def download_pdf(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PDF Files (*.pdf)")
        if file_name:
            from fpdf import FPDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, "Exam Center Allocation", ln=True, align='C')
            pdf.ln(10)
            for i, (student_name, student_pincode) in enumerate(self.students):
                center, center_pincode = self.centers[i % len(self.centers)]
                pdf.cell(50, 10, student_name, border=1)  # Student Name
                pdf.cell(30, 10, str(student_pincode), border=1)  # Student Pincode
                pdf.cell(70, 10, center, border=1)  # Nearest Exam Center
                pdf.cell(30, 10, str(center_pincode), border=1, ln=True)  # Exam Center Pincode
            pdf.output(file_name)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ExamAllocator()
    ex.show()
    sys.exit(app.exec_())