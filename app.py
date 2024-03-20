from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Get uploaded file
    file1 = request.files['file1']
    file2 = request.files['file2']

    # Read Excel files
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # Perform merge operation
    merged_df = pd.merge(df1, df2, on='Name', how='inner')

    # Write merged data to a new Excel file
    merged_df.to_excel('Book3.xlsx', index=False)

    return 'Process Completed!'

if __name__ == '__main__':
    app.run(debug=True)
