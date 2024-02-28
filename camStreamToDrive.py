import json
import os
import time
from datetime import datetime
from collections import deque
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import cv2

# Load credentials from credentials.json
with open('credentials.json', 'r') as f:
    credentials = json.load(f)

# Load config from config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# Global variables
image_counter = 0
max_images = 10
image_queue = deque(maxlen=max_images)

# Initialize webcam
cap = cv2.VideoCapture(0)  # 0 for the first webcam, 1 for the second, and so on

# Function to capture and upload image
def capture_and_upload():
    global image_counter
    
    # Capture image from webcam
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image from webcam")
        return
    
    # Save captured image
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_path = f'webcam_image_{timestamp}_{image_counter}.jpg'
    cv2.imwrite(image_path, frame)
    
    # Increment image counter
    image_counter += 1
    
    # Add image path to the queue
    image_queue.append(image_path)
    
    # Upload image to Google Drive
    try:
        drive_service = build('drive', 'v3', credentials=service_account.Credentials.from_service_account_info(credentials))
        file_metadata = {'name': image_path, 'parents': [config['folder_id']]}
        media = MediaFileUpload(image_path)
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Uploaded image: {file.get('id')} - {image_path}")
    except Exception as e:
        print(f"Failed to upload image: {e}")
    
    # Remove oldest image from queue and delete corresponding file
    if len(image_queue) >= max_images:
        oldest_image_path = image_queue.popleft()
        try:
            os.remove(oldest_image_path)
            print(f"Removed image: {oldest_image_path}")
        except Exception as e:
            print(f"Failed to remove image: {e}")

# Continuous image capture and upload loop
while True:
    start_time = time.time()
    capture_and_upload()
    elapsed_time = time.time() - start_time
    
    # Adjust the delay for desired FPS
    delay = 1.0 / config['fps'] - elapsed_time
    if delay > 0:
        time.sleep(delay)
