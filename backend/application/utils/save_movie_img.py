import os
from flask import current_app
from werkzeug.utils import secure_filename

def save_movie_image(movie_poster):
    filename = secure_filename(movie_poster.filename)
    file_path = os.path.join(current_app.config['MOVIE_UPLOAD_FOLDER'], filename)

    movie_poster.save(file_path)
    return file_path