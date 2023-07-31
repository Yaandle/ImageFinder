import os
import shutil
from ultralytics import YOLO
import streamlit as st
import zipfile
import base64

model = YOLO("")
folder_path = ''
destination_folder = ''
filtered_images = []

class_name = st.text_input("Enter the desired class name")

for image_name in os.listdir(folder_path):
    image_path = os.path.join(folder_path, image_name)

    results = model(image_path, conf=0.1)
    boxes = results[0].boxes
    for box in boxes:
        if box.cls == class_name:
            filtered_images.append(image_path)
            source_file = os.path.join(folder_path, image_name)
            dest_file = os.path.join(destination_folder, image_name)
            shutil.copy2(source_file, dest_file)
            break


for image_path in filtered_images:
    shutil.copy2(image_path, destination_folder)

zip_filename = 'filtered_images.zip'
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for root, dirs, files in os.walk(destination_folder):
        for file in files:
            zipf.write(os.path.join(root, file), file)

b64_zip_data = base64.b64encode(open(zip_filename, 'rb').read()).decode()
download_link = f'<a href="data:application/zip;base64,{b64_zip_data}" download="{zip_filename}">Download Filtered Images</a>'
st.markdown(download_link, unsafe_allow_html=True)
