# ImageFinder
Object Detection model that predicts the number inside the image.
Flask back-end framework.

This uses a pre-trained dataset made in Roboflow with 200+ classes and 3800+ images. 

Ultralytics YOLOV8 model trained on 100 epochs in Google Collab.

The bike number is extracted from the JSON Shopify webhook, images from a source bucket containing the bike number in the predictions are filtered to another bucket.

## Prerequisites

Before running the application, ensure you have the following:

- Python (>=3.6)
- Ultralytics YOLO model (`model1800.pt`)
- Google Cloud Storage credentials (JSON key file)
- Flask and required Python libraries (see `requirements.txt`)
- Ngrok (for webhook testing and public URL)

  
For the app with UI, use streamlit-ui branch.
