# ⚒️ PDF Forge Pro

A lightweight, privacy-focused web application built with **Flask** and **Python** that transforms images into professional, secure PDF documents. Whether you're uploading local files or capturing live documents via your camera, PDF Forge Pro handles the "forging" process entirely in memory for speed and security.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v3.0-green.svg)

## 🚀 Key Features

* 📷 **Live Camera Capture:** Snap photos directly from your browser (mobile-friendly).
* 🖐️ **Drag-and-Drop Reordering:** Change the page sequence by simply dragging the image thumbnails.
* 🔒 **PDF Encryption:** Protect your documents with password security (AES-256).
* 📉 **Smart Compression:** Reduce file size without losing document legibility.
* 🌓 **Grayscale Mode:** Convert color photos into clean, black-and-white "scanned" documents.
* 📏 **Custom Layouts:** Support for A4, Letter, and A3 sizes in both Portrait and Landscape.
* 🖼️ **Smart Margins:** Automatically add white borders to prevent text cutoff during printing.

## 🛠️ Tech Stack

- **Backend:** Python / Flask
- **Image Processing:** Pillow (PIL)
- **PDF Generation:** img2pdf
- **PDF Security:** pypdf
- **Frontend:** HTML5, CSS3 (Modern Dark Theme), JavaScript (Vanilla)

## ⚙️ Installation & Local Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/pdf-forge-pro.git](https://github.com/yourusername/pdf-forge-pro.git)
    cd pdf-forge-pro
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```
    The app will be available at `http://127.0.0.1:5000`.

## 🌐 Deployment (Render)

This project is optimized for deployment on **Render**. 

1.  Connect your GitHub repository to a new **Render Web Service**.
2.  **Build Command:** `pip install -r requirements.txt`
3.  **Start Command:** `gunicorn app:app` (or `python app.py` for simpler setups).

## 🛡️ Privacy & Security

PDF Forge Pro is designed with a **privacy-first** approach:
- Files are processed in a temporary session folder.
- A background worker automatically purges all uploaded data and generated PDFs every 15 minutes.
- No permanent database storage is used.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
