from flask import Flask, request, jsonify
import os
from io import BytesIO
from PIL import Image
from ultralytics import YOLO
from google.cloud import storage
import shutil
import requests

app = Flask(__name__)

#Setup
model = YOLO('MODEL3200.pt')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "googlekey.json"
source_bucket_name = ''  
destination_bucket_name = ''  
storage_client = storage.Client()
source_bucket = storage_client.bucket(source_bucket_name)
destination_bucket = storage_client.bucket(destination_bucket_name)
num_list = ['1', '10', '100', '103', '104', '105', '106', '11', '111', '112', '113', '114', '115', '117', '118', '12', '123', '128', '13', '132', '133', '137', '14', '145', '147', '15', '150', '151', '153', '159', '16', '160', '162', '164', '165', '166', '17', '171', '172', '174', '178', '18', '180', '182', '189', '19', '191', '199', '2', '20', '202', '204', '209', '21', '210', '211', '215', '217', '22', '222', '225', '226', '227', '23', '231', '235', '238', '24', '241', '243', '247', '25', '252', '257', '26', '266', '267', '27', '270', '272', '273', '275', '277', '28', '286', '29', '290', '291', '295', '298', '299', '3', '30', '309', '31', '310', '311', '313', '315', '317', '318', '32', '323', '325', '33', '338', '340', '346', '348', '35', '355', '36', '37', '376', '38', '39', '392', '394', '4', '40', '404', '41', '410', '411', '414', '42', '421', '427', '428', '43', '44', '46', '47', '474', '48', '480', '49', '5', '50', '504', '51', '514', '518', '521', '53', '532', '547', '549', '55', '555', '557', '56', '57', '58', '585', '59', '599', '6', '609', '61', '612', '613', '616', '62', '622', '65', '650', '66', '666', '673', '687', '690', '7', '71', '710', '711', '72', '724', '725', '74', '742', '77', '775', '782', '789', '79', '8', '80', '81', '818', '82', '823', '826', '83', '84', '85', '852', '86', '875', '876', '877', '88', '89', '893', '9', '914', '915', '916', '95', '952', '96', '97', '972', '99', '997', '999']



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
        gcp_url = ''
        with requests.post(gcp_url + '/filter_images', json=data, timeout=5) as response:
            if response.status_code == 200:
                print(f"Bike number '{bike_number}' sent to Flask backend successfully on GCP.")
            else:
                print(f"Failed to send bike number '{bike_number}' to Flask backend on GCP.")
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
