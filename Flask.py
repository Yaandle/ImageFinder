from flask import Flask, render_template, make_response, request, jsonify
import os
import time
from google.cloud import storage

app = Flask(__name__)

def format_server_time():
  server_time = time.localtime()
  return time.strftime("%I:%M:%S %p", server_time)

@app.route('/')
def index():
    context = { 'server_time': format_server_time() }
    
    template = render_template('index.html', context=context)
    
    response = make_response(template)
    
    response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
    return response



os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "server/src/GoogleKey/googlekey.json"


@app.route('/filter_images', methods=['POST'])
def filter_images():
    source_bucket_name = request.form.get('source_bucket')
    destination_bucket_name = request.form.get('destination_bucket')

    # Initialize the Google Cloud Storage client
    storage_client = storage.Client()

    # Get the source and destination buckets
    source_bucket = storage_client.bucket(source_bucket_name)
    destination_bucket = storage_client.bucket(destination_bucket_name)

    if not source_bucket.exists() or not destination_bucket.exists():
        return jsonify({"error": "Source or destination bucket does not exist."}), 400

    filtered_images = []

    blobs = source_bucket.list_blobs()

    for blob in blobs:
        if blob.name.lower().endswith(('.jpg', '.jpeg')):
            # Copy the image from the source to the destination bucket
            source_blob = source_bucket.blob(blob.name)
            destination_blob = destination_bucket.blob(blob.name)
            source_blob.download_to_filename('/tmp/temp_image.jpg')
            destination_blob.upload_from_filename('/tmp/temp_image.jpg')
            filtered_images.append(blob.name)

    return jsonify({"message": "Images copied to the destination bucket.", "filtered_images": filtered_images})
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
