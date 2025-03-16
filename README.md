# Exam Center Allocation Tool

This repository contains a Python-based Exam Center Allocation Tool that helps allocate students to their nearest exam centers based on their pincodes. The tool is built using PyQt5 for the graphical user interface (GUI) and pandas for data manipulation.

## Files

### 1. `students.csv`
This CSV file contains the list of students and their respective pincodes. The file has two columns:
- **Student Name**: The name of the student.
- **Pincode**: The pincode of the student's location.

Example:
```
Student Name,Pincode
Tom,600129
Gokul,600055
Nandhaa Baala,600091
```

### 2. `centers.csv`
This CSV file contains the list of exam centers and their respective pincodes. The file has two columns:
- **Exam Center Name**: The name of the exam center.
- **Pincode**: The pincode of the exam center's location.

Example:
```
Exam Center Name,Pincode
Fortune Towers,600129
CIT,600069
Sdnbvc,600044
```

### 3. `exam_allocator.py`
This is the main Python script that runs the Exam Center Allocation Tool. It provides a GUI for uploading the `students.csv` and `centers.csv` files, allocates the nearest exam center to each student based on their pincode, and displays the results in a table. The tool also allows users to download the results in Excel or PDF format.

#### Features:
- **Upload Students File**: Upload the `students.csv` file containing student names and pincodes.
- **Upload Exam Centers File**: Upload the `centers.csv` file containing exam center names and pincodes.
- **Allocate Centers**: Automatically allocates the nearest exam center to each student based on the pincode.
- **Download Results**: Download the allocation results in Excel or PDF format.

#### Dependencies:
- **PyQt5**: For the graphical user interface.
- **pandas**: For reading and manipulating CSV files.
- **fpdf**: For generating PDF files.

## How to Use

1. **Install Dependencies**:
   Ensure you have Python installed, then install the required dependencies using pip:
   ```bash
   pip install PyQt5 pandas fpdf
   ```

2. **Run the Script**:
   Run the `exam_allocator.py` script to start the application:
   ```bash
   python exam_allocator.py
   ```

3. **Upload Files**:
   - Click on "Upload Students File (CSV)" to upload the `students.csv` file.
   - Click on "Upload Exam Centers File (CSV)" to upload the `centers.csv` file.

4. **View Results**:
   Once both files are uploaded, the tool will automatically allocate the nearest exam center to each student and display the results in a table.

5. **Download Results**:
   - Click on "Download Excel" to save the results as an Excel file.
   - Click on "Download PDF" to save the results as a PDF file.

## Example Data

### `students.csv`
```
Student Name,Pincode
Tom,600129
Gokul,600055
Nandhaa Baala,600091
```

### `centers.csv`
```
Exam Center Name,Pincode
Fortune Towers,600129
CIT,600069
Sdnbvc,600044
```

## License
This project is open-source and available under the MIT License. Feel free to use, modify, and distribute it as per the license terms.

## Author
Made with ❤️ by Tom Joe James.

---

For any issues or suggestions, please open an issue on the GitHub repository.
