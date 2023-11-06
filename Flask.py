from flask import Flask, render_template, request, jsonify, make_response
import time
from google.cloud import storage
import os
import json
from google.oauth2 import service_account
from google.cloud import secretmanager
import json

app = Flask(__name__)

def format_server_time():
    server_time = time.localtime()
    return time.strftime("%I:%M:%S %p", server_time)

@app.route('/')
def index():
    context = { 'server_time': format_server_time() }
    
    template = render_template('index.html', context=context)
    
    response = make_response(template)
    
    response.headers['Cache-Control'] = 'public, max-age=180, s-maxage=600'
    return response

@app.route("/submit", methods=["POST"])
def submit():
    num_list = [str(i) for i in range(1000)]  
    number = request.form.get("number")
    if number in num_list:
        position = num_list.index(number)
        return jsonify({"number": number, "position": position}), 200
    else:
        return jsonify({"error": "Number not found in the list."}), 404
    
def get_storage_client():
    return storage.Client()

@app.route('/transfer_images', methods=['POST'])
def transfer_images():
    try:
        client = storage.Client()

        source_bucket_name = 'odissourcebucket'
        destination_bucket_name = 'odisoutputbucket'

        source_bucket = client.bucket(source_bucket_name)
        destination_bucket = client.bucket(destination_bucket_name)

        blobs = source_bucket.list_blobs()
        for blob in blobs:
            if blob.content_type.startswith('image/'):
                source_bucket.copy_blob(blob, destination_bucket, new_name=blob.name)

        response = jsonify(message='Images transferred successfully!')
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response, 200
    
    except Exception as e:

        app.logger.error('An internal error occurred: %s', e, exc_info=True)
        response = jsonify(error='An internal server error occurred.')
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response, 500
