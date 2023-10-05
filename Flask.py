from flask import Flask, request, jsonify
import os
from io import BytesIO
from PIL import Image
from ultralytics import YOLO
from google.cloud import storage
import shutil
import requests

app = Flask(__name__)
model = YOLO('model1800.pt')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "goglekey.json"
source_bucket_name = 'source-bucket'  
destination_bucket_name = 'filtered-images-bucket'  
storage_client = storage.Client()
source_bucket = storage_client.bucket(source_bucket_name)
destination_bucket = storage_client.bucket(destination_bucket_name)

@app.route('/webhook', methods=['POST'])
def webhook():
    webhook_data = request.get_json()
    bike_number = None
    if 'line_items' in webhook_data:
        for item in webhook_data['line_items']:
            if 'properties' in item:
                for prop in item['properties']:
                    if 'name' in prop and prop['name'] == 'Bike Number' and 'value' in prop:
                        bike_number = prop['value']
                        print(f"Bike number: {bike_number}")
                        break 
    if bike_number:
        data = {'Bike Number': bike_number}
        ngrok_url = ''                                                                                          #Add Network URL
        with requests.post(ngrok_url + '/filter_images', json=data, timeout=5) as response:
            if response.status_code == 200:
                print(f"Bike number '{bike_number}' sent to Flask backend successfully.")
            else:
                print(f"Failed to send bike number '{bike_number}' to Flask backend.")
    else:
        print("No 'Bike Number' properties found in the JSON data.")
    return jsonify({'message': 'Webhook received successfully'}), 200

@app.route('/filter_images', methods=['POST'])
def filter_images():
    if "Bike Number" not in request.json:
        return jsonify({"error": "Bike Number key not found in JSON data."}), 400
    rider_number = request.json["Bike Number"]
    if rider_number:
        try:
            position = int(rider_number)
            if position < 0 or position >= len(num_list):
                return jsonify({"error": "Invalid rider number."}), 400
            class_name = position
        except ValueError:
            return jsonify({"error": "Invalid rider number."}), 400

    if class_name is not None:
        filtered_images = []
        temp_dir = './temp_images'
        os.makedirs(temp_dir, exist_ok=True)
        blobs = source_bucket.list_blobs()
        processed_images_count = 0
        max_processed_images = 40  
        for blob in blobs:
            if blob.name.lower().endswith(('.jpg', '.jpeg')):
                image_data = blob.download_as_bytes()
                image = Image.open(BytesIO(image_data))
                results = model(image, conf=0.01)
                boxes = results[0].boxes
                for box in boxes:
                    if box.cls == class_name:
                        filtered_images.append(blob.name)
                        source_blob = source_bucket.blob(blob.name)
                        destination_blob = destination_bucket.blob(blob.name)
                        temp_image_path = os.path.join(temp_dir, 'temp_image.jpg')
                        source_blob.download_to_filename(temp_image_path)
                        destination_blob.upload_from_filename(temp_image_path)

                        processed_images_count += 1
                        if processed_images_count >= max_processed_images:
                            break
        if not filtered_images:
            return "No images matching the criteria were found."
        
        success_message = "The images have been filtered and saved to the destination bucket."
        response_data = {'filtered_images': filtered_images, 'message': success_message}
        shutil.rmtree(temp_dir, ignore_errors=True)
        return jsonify(response_data)
    else:
        return "Rider number not found in the list."

if __name__ == "__main__":
    app.run(debug=True)
