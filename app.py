from flask import Flask, request, jsonify
import os
import shutil
from ultralytics import YOLO
import zipfile

app = Flask(__name__)
model = YOLO('')

@app.route('/detect_and_filter', methods=['POST'])
def detect_and_filter():
    data = request.get_json()

    class_name = data['class_name']
    folder_path = data['folder_path']
    filtered_images = []

    if os.path.exists(folder_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
        destination_dir = os.path.join(script_dir, 'static', 'filtered_images')
        os.makedirs(destination_dir, exist_ok=True)

        for image_name in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_name)

            results = model(image_path, conf=0.2)
            boxes = results[0].boxes
            for box in boxes:
                if box.cls == class_name:
                    filtered_images.append(image_path)
                    source_file = os.path.join(folder_path, image_name)
                    dest_file = os.path.join(destination_dir, image_name)  # Use the correct destination path
                    shutil.copy2(source_file, dest_file)
                    break

        zip_filename = 'filtered_images.zip'
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for root, dirs, files in os.walk(destination_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), file)

        response_data = {'filtered_images': filtered_images, 'zip_filename': zip_filename}
        return jsonify(response_data)
    else:
        return jsonify({'error': "Invalid source folder path. Please enter a valid path."})
if __name__ == "__main__":
    app.run(debug=True)
