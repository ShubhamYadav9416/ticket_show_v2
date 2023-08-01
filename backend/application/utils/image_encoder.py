import base64
from io import BytesIO

def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            base64_encoded = base64.b64encode(image_data).decode('utf-8')
            return base64_encoded
    except FileNotFoundError:
        print("Image not found.")
        return None