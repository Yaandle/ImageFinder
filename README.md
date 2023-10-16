# ImageFinder
Object Detection model that predicts the number inside the image.
Flask back-end framework.

This uses a pre-trained dataset made in Roboflow with 200+ classes and 3800+ images. 

Ultralytics YOLOV8 model trained on 100 epochs in Google Collab.

The bike number is extracted from the JSON Shopify webhook, images from a source bucket containing the bike number in the predictions are filtered to another bucket.

## Prerequisites

- Python (3.10.10)
- Ultralytics YOLO model (`model1800.pt`)
- Google Cloud Storage credentials (JSON key file) 
- Ngrok (for webhook URL)

The  streamlit-ui branch allows you to define an input folder and a number, and will perform object detection on the images in the folder.
