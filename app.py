from flask import Flask, request, render_template, send_file
from PyPDF2 import PdfMerger
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
MERGED_FILE = 'merged.pdf'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index() :
    return render_template('index.html')

@app.route('/merge', methods=['GET', 'POST'])
def merge():

    app.config['UPLOAD_FOLDER'] = 'uploads'

    file1 = request.files.get('pdf1')
    file2 = request.files.get('pdf2')

    if not file1 or not file2:
        return "Both PDF files are required."

    #save
    file1_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file1.filename))
    file2_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file2.filename))

    file1.save(file1_path)
    file2.save(file2_path)

    # Gabungkan PDF
    merger=PdfMerger()

    merger.append(file1_path)
    merger.append(file2_path)

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], MERGED_FILE)
    merger.write(output_path)
    merger.close()

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug = True)
