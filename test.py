from ultralytics import YOLO
import streamlit as st
from PIL import Image
import cv2


    #VALIDATE
results = model.val()
    #Predict
source_path = "E:\Machine Learning\Object Detection\AppTest\images"
source = source_path
model.predict(source, save=True, imgsz=640, conf=0.5)
# from PIL
im1 = Image.open("image.jpg")
results = model.predict(source=im1, save=True)  # save plotted images
# from ndarray
im2 = cv2.imread("image.jpg")
results = model.predict(source=im2, save=True, save_txt=True)  # save predictions as labels
# from list of PIL/ndarray
results = model.predict(source=[im1, im2])

for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    probs = result.probs  # Class probabilities for classification outputs

# Set up the Streamlit app
st.title("YOLO Object Detection App")
st.subheader("Enter a number (0-999)")

