from flask import Flask, request, jsonify, send_from_directory, render_template
import time
import os
from ultralytics import YOLO 
import zipfile
import tempfile
import shutil
import base64
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 Megabytes
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
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        with tempfile.TemporaryDirectory() as temp_dir:
            if file.filename.endswith('.zip'):
                zip_path = os.path.join(temp_dir, 'images.zip')
                file.save(zip_path)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                source_folder = temp_dir
            else:
                image_path = os.path.join(temp_dir, file.filename)
                file.save(image_path)
                source_folder = temp_dir
            output_dir = os.path.join(temp_dir, 'runs', 'detect', 'predict5')
            os.makedirs(output_dir, exist_ok=True)
            for folder_name, _, filenames in os.walk(source_folder):
                for filename in filenames:
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                        image_path = os.path.join(folder_name, filename)
                        results = model(image_path, save=True, save_txt=True, conf=0.1, project=output_dir, name='')
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
