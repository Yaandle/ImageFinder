# ImageFinder
Object Detection model that predicts the number inside the image.
Flask back-end framework.

This uses a pre-trained dataset made in Roboflow with 200+ classes and 4k+ images. 

Ultralytics YOLOV8 model trained on 100 epochs in Google Collab.

The bike number is extracted from the JSON Shopify webhook, images from a source bucket containing the bike number in the predictions are filtered to another bucket.


Master branch uses a React frontend that handles a JSON request from Shopify that is triggered by order creation.
The streamlit-ui branch allows you to define an input folder and a number, and will perform object detection on the images in the folder.
