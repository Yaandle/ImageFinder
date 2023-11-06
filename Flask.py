from flask import Flask, render_template, request, jsonify, make_response
import time
from google.cloud import storage
import os
import json
from google.oauth2 import service_account

app = Flask(__name__)

def get_storage_client():
    creds_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if creds_json:
        creds_info = json.loads(creds_json)
        credentials = service_account.Credentials.from_service_account_info(creds_info)
        return storage.Client(credentials=credentials)
    else:
        return storage.Client()

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
    num_list = [str(i) for i in range(1000)]  # Simplified for demonstration
    number = request.form.get("number")
    if number in num_list:
        position = num_list.index(number)
        return jsonify({"number": number, "position": position}), 200
    else:
        return jsonify({"error": "Number not found in the list."}), 404

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
    
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
