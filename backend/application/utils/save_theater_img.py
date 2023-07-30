import os
from flask import current_app
from werkzeug.utils import secure_filename

def save_theater_image(theater_image):
    filename = secure_filename(theater_image.filename)
    file_path = os.path.join(current_app.config['THEATER_UPLOAD_FOLDER'], filename)

    theater_image.save(file_path)
    return file_path