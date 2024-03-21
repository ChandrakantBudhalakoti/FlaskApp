from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import shutil

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESUME_FOLDER = 'resumes'
MERGED_RESUME_FOLDER = 'merged_resumes'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESUME_FOLDER'] = RESUME_FOLDER
app.config['MERGED_RESUME_FOLDER'] = MERGED_RESUME_FOLDER

# Ensure the folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESUME_FOLDER, exist_ok=True)
os.makedirs(MERGED_RESUME_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Get uploaded files
    file1 = request.files['file1']
    file2 = request.files['file2']
    resumes = request.files.getlist('resumes')

    # Save uploaded files
    file1_path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
    file2_path = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)

    file1.save(file1_path)
    file2.save(file2_path)

    # Read Excel files
    df1 = pd.read_excel(file1_path)
    df2 = pd.read_excel(file2_path)

    # Perform merge operation
    merged_df = pd.merge(df1, df2, on='Name', how='inner')

    # Save merged Excel file
    merged_excel_path = os.path.join(app.config['UPLOAD_FOLDER'], 'Book3.xlsx')
    merged_df.to_excel(merged_excel_path, index=False)

    # Find resumes for merged students
    merged_students = merged_df['Name'].tolist()
    for resume in resumes:
        if resume.filename.split('.')[0] in merged_students:
            resume_path = os.path.join(app.config['RESUME_FOLDER'], resume.filename)
            resume.save(resume_path)

    # Move matched resumes to merged resumes folder
    for student in merged_students:
        resume_file = f"{student}.pdf"  # Assuming resumes are in PDF format
        src = os.path.join(app.config['RESUME_FOLDER'], resume_file)
        dest = os.path.join(app.config['MERGED_RESUME_FOLDER'], resume_file)
        if os.path.exists(src):
            shutil.move(src, dest)

    return jsonify({'message': 'Process Completed!', 'excel_path': merged_excel_path})

if __name__ == '__main__':
    app.run(debug=True)
