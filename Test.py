import os
import shutil
import zipfile
import base64
from ultralytics import YOLO
import streamlit as st

# Load the YOLO model
model = YOLO('E:/Machine Learning/Object Detection/App 2.0/Models/v3.pt')

def main():
    st.title("Image Filter, Copy, and Download")
    rider_number = st.text_input("Enter a rider number, 0-999") 
    if rider_number:
        try:
            class_name = int(rider_number)
        except: ValueError:st.write("Please enter number. ")
        
    folder_path = st.text_input("Enter the path to the source folder:")
    destination_folder = 'filtered_images'
    os.makedirs(destination_folder, exist_ok=True)

    filtered_images = []

    if st.button("Filter and Copy Images"):
        if os.path.exists(folder_path):
            for image_name in os.listdir(folder_path):
                image_path = os.path.join(folder_path, image_name)
                results = model(image_path, conf=0.2)
                boxes = results[0].boxes
                for box in boxes:
                    if box.cls == class_name:  
                        filtered_images.append(image_path)
                        source_file = os.path.join(folder_path, image_name)
                        dest_file = os.path.join(destination_folder, image_name)
                        shutil.copy2(source_file, dest_file)
                        break

            st.write("Filtered images copied to 'filtered_images' folder:")
            for image in filtered_images:
                st.image(image, caption=image, use_column_width=True)

            
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
        else:
            st.write("Invalid source folder path. Please enter a valid path.")
        
if __name__ == "__main__":
    main()
