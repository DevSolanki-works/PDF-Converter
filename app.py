import os
import uuid
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

    custom_name = request.form.get("pdf_name") or "my_pdf"

    if not uploaded_files or uploaded_files[0].filename == '':
        return "No Files Selected"
    
    unique_id = str(uuid.uuid4())
    user_session_folder = os.path.join(UPLOAD_FOLDER, unique_id)
    os.makedirs(user_session_folder)
    
    file_paths = []
    for file in uploaded_files:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        file_paths.append(path)

    output_pdf_path = os.path.join(user_session_folder, f"{custom_name}.pdf")

    with open(output_pdf_path, "wb") as f:
        f.write(img2pdf.convert(file_paths))
    
    for path in file_paths:
        os.remove(path)
    
    return send_file(output_pdf_path, as_attachment=True, download_name=f"{custom_name}.pdf")

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)

