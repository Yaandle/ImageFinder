# ImageFinder
Object Detection model that predicts the number inside the image.
Flask back-end framework.

This uses a pre-trained dataset made in Roboflow with 100+ classes and 1800+ images. 

Ultralytics YOLOV8 model trained on 100 epochs in Google Collab.

The bike number is extracted from the Shopify webhook, and images containing the class in a source bucket are filtered to another bucket.


For the app with UI, use streamlit-ui branch.
