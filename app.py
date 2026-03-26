import os
from flask import Flask, render_template, request, send_file
import img2pdf

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    uploaded_files = request.files.getlist("files")

    if not uploaded_files or uploaded_files[0].filename == '':
        return "No Files Selected"
    
    file_paths = []

    for file in uploaded_files:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        file_paths.append(path)

    output_pdf = os.path.join(UPLOAD_FOLDER, "merged_document.pdf")

    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(file_paths))
    
    for path in file_paths:
        os.remove(path)
    
    return send_file(output_pdf, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)

