import os
import shutil
from ultralytics import YOLO
import streamlit as st
import zipfile

#Streamlit
st.title('Image Object Detection')
st.header('Enter a rider number to return images within a folder')
class_name = st.text_input("0-999")

model = YOLO("yolov8m.pt")
folder_path = 'E:/Machine Learning/Object Detection/App 2.0/valid/images'
destination_folder = 'filtered_images'
filtered_images = []
for image_name in os.listdir(folder_path):
    image_path = os.path.join(folder_path, image_name)

    results = model(image_path)
    boxes = results[0].boxes
    for box in boxes:
        if box.cls == 23:
            filtered_images.append(image_path)
            source_file = os.path.join(folder_path, image_name)
            dest_file = os.path.join(destination_folder, image_name)
            shutil.copy2(source_file, dest_file)
            break



def create_zip_file(source_folder, destination_zip_path):
    with zipfile.ZipFile(destination_zip_path, 'w') as zipf:
        for root, _, files in os.walk(source_folder):
            for file in files:
                zipf.write(os.path.join(root, file), file)

def main():
    st.title("Image Filter and Zip Downloader")

    destination_folder = "filtered_images"
    
    if not os.path.exists(destination_folder):
        st.warning("The 'filtered_images' folder does not exist. Please add the filtered images to the folder and re-run the app.")
        return

    create_zip_file(destination_folder, "filtered_images.zip")

    st.success("Filtered images zip folder created!")
    st.download_button(
        label="Download Zip",
        data=open("filtered_images.zip", "rb").read(),
        file_name="filtered_images.zip",
    )

if __name__ == "__main__":
    main()
