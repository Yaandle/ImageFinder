import streamlit as st
from PIL import Image
from roboflow import Roboflow
import os

rf = Roboflow(api_key="")
project = rf.workspace().project("rider-number-finder")
model = project.version(2).model

# Create a Streamlit UI
st.title('Image Predictor')
st.header('Enter a rider number (0-999) to return images within a folder.')

confidence_threshold = st.slider("Confidence Threshold", 0, 100, 40)
overlap_threshold = st.slider("Overlap Threshold", 0, 100, 30)

# Get the desired class name from the user
class_name = st.text_input("Enter the desired class name")


  
folder_path = 'E:\Machine Learning\Object Detection\AppTest\images'  # Specify the path to the folder containing images

filtered_images = []

# Loop through the images in the folder
for image_name in os.listdir(folder_path):
    image_path = os.path.join(folder_path, image_name)

    # Make a prediction on the image
    prediction = model.predict(image_path, confidence=confidence_threshold, overlap=overlap_threshold)

    # Check if the desired class is present in the prediction results
    for result in prediction:
        if result["class"] == class_name:
            filtered_images.append(image_path)
            break  # Exit the loop after finding the desired class

# Display the filtered images
for image_path in filtered_images:
    image = Image.open(image_path)
    st.image(image, caption="Filtered Image", use_column_width=True)
    max_images = 5  # Set the maximum number of images to display
    
    
# Create a temporary download folder
download_folder = 'filtered_images'
os.makedirs(download_folder, exist_ok=True)

# Copy the filtered images to the download folder
for image_path in filtered_images:
    shutil.copy2(image_path, download_folder)

# Create a zip file of the downloadable folder
zip_filename = 'filtered_images.zip'
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for root, dirs, files in os.walk(download_folder):
        for file in files:
            zipf.write(os.path.join(root, file), file)

# Provide a download link for the zip file
b64_zip_data = base64.b64encode(open(zip_filename, 'rb').read()).decode()
download_link = f'<a href="data:application/zip;base64,{b64_zip_data}" download="{zip_filename}">Download Filtered Images</a>'
st.markdown(download_link, unsafe_allow_html=True)

# Remove the temporary download folder and zip file
shutil.rmtree(download_folder)
os.remove(zip_filename)
