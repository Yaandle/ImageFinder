from flask import (
    Flask, request, jsonify, send_from_directory, render_template,
    redirect, url_for, session
)
import time, os, zipfile, tempfile, shutil, base64
from ultralytics import YOLO
from google.cloud import storage, secretmanager
from PIL import Image
from io import BytesIO
import firebase_admin
from firebase_admin import credentials, auth, initialize_app
import json
from datetime import timedelta
from flask import redirect

app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'zip'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_server_time():
    server_time = time.localtime()
    return time.strftime("%I:%M:%S %p", server_time)

@app.route("/")
def index():
    context = {'server_time': format_server_time()}
    return render_template("index.html", **context)

@app.route('/verify-token', methods=['POST'])
def verify_token():
    id_token = request.json.get('idToken')
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        session['user_id'] = uid
        return jsonify({'message': 'Successfully set session'}), 200
    except:
        return jsonify({'message': 'Invalid token'}), 401


@app.route("/submit", methods=["POST"])
def submit():
    num_list = ['1', '10', '100', '103', '104', '105', '106', '11', '111', '112', '113', '114', '115', '117', '118', '12', '123', '126', '128', '13', '132', '133', '137', '14', '145', '147', '15', '150', '151', '153', '159', '16', '160', '162', '164', '165', '166', '17', '171', '172', '174', '178', '18', '180', '182', '188', '189', '19', '191', '199', '2', '20', '202', '204', '209', '21', '210', '211', '215', '217', '22', '222', '225', '226', '227', '23', '231', '235', '238', '24', '241', '243', '247', '25', '252', '257', '26', '266', '267', '27', '270', '272', '273', '275', '277', '28', '286', '29', '290', '291', '295', '298', '299', '3', '30', '309', '31', '310', '311', '313', '315', '317', '318', '32', '323', '325', '33', '332', '338', '340', '346', '348', '35', '355', '36', '37', '376', '38', '39', '392', '394', '4', '40', '404', '41', '410', '411', '414', '42', '421', '427', '428', '43', '44', '445', '45', '46', '47', '474', '48', '480', '49', '5', '50', '504', '51', '514', '518', '521', '523', '53', '532', '547', '549', '55', '555', '557', '56', '57', '58', '585', '59', '599', '6', '609', '61', '612', '613', '616', '62', '622', '627', '65', '650', '66', '666', '673', '687', '69', '690', '7', '71', '710', '711', '72', '724', '725', '74', '742', '768', '77', '775', '782', '789', '79', '8', '80', '81', '818', '82', '823', '826', '829', '83', '84', '85', '852', '86', '875', '876', '877', '88', '89', '893', '9', '914', '915', '916', '94', '95', '952', '96', '97', '972', '99', '997', '999']  # Your number list here
    number = request.form.get("number")
    if number in num_list:
        position = num_list.index(number)
        return jsonify({"number": number, "position": position}), 200
    else:
        return jsonify({"error": "Number not found in the list."}), 404

@app.route("/object_detection", methods=["POST"])
def object_detection():
    model = YOLO('/app/model4k.pt')
    if 'files[]' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('files[]')
    if not files:
        return jsonify({'error': 'No selected files'}), 400

    with tempfile.TemporaryDirectory() as temp_dir:
        for file in files:
            if file and allowed_file(file.filename):
                file_path = os.path.join(temp_dir, file.filename)
                file.save(file_path)

        output_dir = os.path.join(temp_dir, 'runs', 'detect', 'predict5')
        os.makedirs(output_dir, exist_ok=True)

        for file in os.listdir(temp_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(temp_dir, file)
                model(image_path, save=True, save_txt=True, conf=0.1, project=output_dir, name='')

        zip_filename = 'results.zip'
        zip_path = os.path.join(temp_dir, zip_filename)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, _, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, temp_dir))

        with open(zip_path, "rb") as zip_file:
            b64_zip_data = base64.b64encode(zip_file.read()).decode()

        return jsonify({'message': 'Object detection completed', 'zip_file_base64': b64_zip_data}), 200

    return jsonify({'error': 'Invalid file type'}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}


storage_client = storage.Client()

@app.route('/predict_filter', methods=['POST'])
def predict_and_filter_folder():
    class_name = request.form.get('class_name')
    if not class_name:
        return jsonify({'error': 'Class name is not provided.'}), 400
    try:
        class_name_int = int(class_name)
    except ValueError:
        return jsonify({'error': 'Class name must be a valid integer.'}), 400
    model = YOLO('/app/Model4600.pt')
    source_bucket_name = os.environ.get('SOURCE_BUCKET_NAME')
    destination_bucket_name = os.environ.get('DESTINATION_BUCKET_NAME')
    source_bucket = storage_client.bucket(source_bucket_name)
    destination_bucket = storage_client.bucket(destination_bucket_name)
    blobs = source_bucket.list_blobs()
    filtered_images = []
    for blob in blobs:
        if blob.name.lower().endswith(('.jpg', '.jpeg')):
            image_data = blob.download_as_bytes()
            image = Image.open(BytesIO(image_data))
            results = model(image, conf=0.01, device='cuda:0')
            boxes = results[0].boxes
            for box in boxes:
                if box.cls == class_name_int:
                    filtered_images.append(blob.name)
                    source_blob = source_bucket.blob(blob.name)
                    destination_blob = destination_bucket.blob(blob.name)
                    temp_image_path = f'/tmp/{blob.name}'
                    source_blob.download_to_filename(temp_image_path)
                    destination_blob.upload_from_filename(temp_image_path)
                    os.remove(temp_image_path)
                    break
    if not filtered_images:
        return jsonify({'message': 'No images matching the class name were found.'}), 404
    success_message = "The images have been filtered and saved to the destination bucket."
    return jsonify({'filtered_images': filtered_images,'message': success_message}), 200

@app.route('/secure-page')
def secure_page():
    if 'user_id' in session:
        user = auth.get_user(session['user_id'])
        return render_template('secure.html', user=user)
    else:
        return redirect(url_for('login'))
    
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/download_page')
def download_page():
    return render_template('download_page.html')

@app.route('/download_model')
def download_model():
    storage_client = storage.Client()
    bucket_name = os.environ.get('MODEL_BUCKET')  # Assuming the bucket name is stored in an environment variable
    blob_name = 'Model4600.pt'

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Generate a signed URL valid for a short duration
    signed_url = blob.generate_signed_url(timedelta(minutes=10))

    # Redirect user to the signed URL
    return redirect(signed_url)

@app.route('/download_model2')
def download_model2():
    model_path = "/app"  
    model_filename = "MODEL3200.pt"  
    return send_from_directory(model_path, model_filename, as_attachment=True, download_name="MODEL3200.pt")
