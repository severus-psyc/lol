from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from deepface import DeepFace
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'preset' not in request.files or 'target' not in request.files:
        return "No files provided"

    # Save preset photos
    preset_files = request.files.getlist('preset')
    preset_paths = []
    for preset in preset_files:
        filename = secure_filename(preset.filename)
        preset_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        preset.save(preset_path)
        preset_paths.append(preset_path)

    # Save target photo
    target = request.files['target']
    target_filename = secure_filename(target.filename)
    target_path = os.path.join(app.config['UPLOAD_FOLDER'], target_filename)
    target.save(target_path)

    # Perform recognition using DeepFace
    try:
        result = DeepFace.find(img_path=target_path, db_path=UPLOAD_FOLDER, model_name="Facenet")
        if len(result) > 0:
            return f"Match found: {result}"
        else:
            return "No match found."
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)

