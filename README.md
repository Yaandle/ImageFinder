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

  
For the app with UI, use streamlit-ui branch.


@software{yolov8_ultralytics,
  author = {Glenn Jocher and Ayush Chaurasia and Jing Qiu},
  title = {Ultralytics YOLOv8},
  version = {8.0.0},
  year = {2023},
  url = {https://github.com/ultralytics/ultralytics},
  orcid = {0000-0001-5950-6979, 0000-0002-7603-6750, 0000-0003-3783-7069},
  license = {AGPL-3.0}
}
