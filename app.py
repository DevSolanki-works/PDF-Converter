import os
from flask import Flask, render_template, request, send_file
import img2pdf

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected File"
    
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(img_path)

    pdf_path = img_path.rsplit('.', 1)[0] + ".pdf"

    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(img_path))
    
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

