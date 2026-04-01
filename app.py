import os
import uuid
import shutil
import threading
import time
from flask import Flask, render_template, request, send_file
import img2pdf
from PIL import Image
from pypdf import PdfReader, PdfWriter

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def cleanup_worker():
    while True:
        time.sleep(600)
        now = time.time()
        if os.path.exists(UPLOAD_FOLDER):
            for folder in os.listdir(UPLOAD_FOLDER):
                folder_path = os.path.join(UPLOAD_FOLDER, folder)
                if os.path.getmtime(folder_path) < now - 900:
                    shutil.rmtree(folder_path)

threading.Thread(target=cleanup_worker, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    uploaded_files = request.files.getlist("files")
    custom_name = request.form.get("pdf_name") or "my_pdf"
    page_size = request.form.get("page_size", "A4").upper()
    orientation = request.form.get("orientation", "portrait").lower()
    compression = request.form.get("compression", "none").lower()
    password = request.form.get("pdf_password", "").strip()

    if not uploaded_files or uploaded_files[0].filename == '':
        return "No Files Selected", 400
    
    unique_id = str(uuid.uuid4())
    user_session_folder = os.path.join(UPLOAD_FOLDER, unique_id)
    os.makedirs(user_session_folder)
    
    file_paths = []
    for file in uploaded_files:
        original_path = os.path.join(user_session_folder, file.filename)
        file.save(original_path)
        
        fixed_path = os.path.join(user_session_folder, f"proc_{file.filename}.jpg")
        try:
            with Image.open(original_path) as img:
                rgb_img = img.convert('RGB')
                
                if compression == "medium":
                    rgb_img.thumbnail((1920, 1920))
                    qual = 75
                elif compression == "high":
                    rgb_img.thumbnail((1080, 1080))
                    qual = 55
                else:
                    qual = 100 
                    
                rgb_img.save(fixed_path, "JPEG", quality=qual, optimize=True)
                file_paths.append(fixed_path)
        except Exception:
            continue

    sizes = {
        "A4": (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297)),
        "LETTER": (img2pdf.mm_to_pt(216), img2pdf.mm_to_pt(279)),
        "A3": (img2pdf.mm_to_pt(297), img2pdf.mm_to_pt(420))
    }

    width, height = sizes.get(page_size, sizes["A4"])
    if orientation == "landscape":
        width, height = height, width

    layout_fun = img2pdf.get_layout_fun(pagesize=(width, height))
    output_pdf_path = os.path.join(user_session_folder, f"{custom_name}.pdf")

    with open(output_pdf_path, "wb") as f:
        f.write(img2pdf.convert(file_paths, layout_fun=layout_fun))

    if password:
        encrypted_path = os.path.join(user_session_folder, f"locked_{custom_name}.pdf")
        reader = PdfReader(output_pdf_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(password)
        with open(encrypted_path, "wb") as f:
            writer.write(f)
        output_pdf_path = encrypted_path
    
    return send_file(output_pdf_path, as_attachment=True, download_name=f"{custom_name}.pdf")

if __name__ == '__main__':
    app.run(debug=True)
