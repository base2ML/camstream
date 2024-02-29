import json
import os
import time
from datetime import datetime
from collections import deque
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import cv2
import threading

# Load config from config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# Global variables
image_counter = 0
max_images = 10
image_queue = deque(maxlen=max_images)
fps = config.get('fps', 10)

# Function to capture images
def capture_images():
    global image_counter
    cap = cv2.VideoCapture(0)  # Open webcam
    while True:
        ret, frame = cap.read()  # Read frame from webcam
        if not ret:
            print("Failed to capture image from webcam")
            continue
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        folder_path = os.path.join(config['image_folder'], timestamp)  # Create folder path
        os.makedirs(folder_path, exist_ok=True)  # Create folder if not exists
        
        image_path = os.path.join(folder_path, f'webcam_image_{timestamp}_{image_counter}.jpg')
        cv2.imwrite(image_path, frame)  # Save image
        
        # Add image path to the queue
        image_queue.append(image_path)
        image_counter += 1
        
        time.sleep(1 / fps)  # Adjust for specified FPS

    # Release the VideoCapture object when done
    cap.release()

# Function to upload images from the queue with a delay
def upload_images():
    while True:
        if len(image_queue) >= 3 * fps:
            for _ in range(3 * fps):
                image_path = image_queue.popleft()
            try:
                credentials = service_account.Credentials.from_service_account_file('credentials.json')
                drive_service = build('drive', 'v3', credentials=credentials)
                file_metadata = {'name': os.path.basename(image_path), 'parents': [config['folder_id']]}
                media = MediaFileUpload(image_path)
                file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                print(f"Uploaded image: {file.get('id')} - {image_path}")
            except Exception as e:
                print(f"Failed to upload image: {e}")
            finally:
                time.sleep(3)  # Delay for 3 seconds before next upload attempt
        else:
            time.sleep(1)  # Sleep if there are not enough images in the queue

# Start capturing images in a separate thread
capture_thread = threading.Thread(target=capture_images)
capture_thread.daemon = True
capture_thread.start()

# Start uploading images in a separate thread
upload_thread = threading.Thread(target=upload_images)
upload_thread.daemon = True
upload_thread.start()

# Keep the main thread alive
while True:
    time.sleep(1)
