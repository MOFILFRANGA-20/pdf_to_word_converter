from flask import Flask, render_template, request, redirect, url_for
from pdf2image import convert_from_path
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
POPPLER_PATH = r'C:\poppler-24.08.0\Library\bin'  # ← replace this with your actual path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    pdf_file = request.files['pdf']
    if pdf_file:
        file_id = str(uuid.uuid4())
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}.pdf")
        pdf_file.save(pdf_path)

        # Convert all pages of the PDF to images
        images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
        image_urls = []

        for i, image in enumerate(images):
            image_filename = f"{file_id}_page_{i+1}.png"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path, 'PNG')
            image_urls.append(f"/{image_path}")

        os.remove(pdf_path)  # Optional: delete original PDF after conversion
        return render_template('result.html', image_urls=image_urls)

    return redirect('/')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
