from ultralytics import YOLO
import torch
import torchvision
import time
import os

source = ' ' 
model = YOLO("")


image_files = [f for f in os.listdir(source) if f.endswith(('.jpg', '.jpeg', '.png'))]

for image_file in image_files:
    image_path = os.path.join(source, image_file)
    results = model(image_path, save=True, save_txt=True, conf=0.1, device='cuda:0')
    

    time.sleep(0.5)