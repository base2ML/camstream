import json
import os
import time
from datetime import datetime
from collections import deque
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from PIL import ImageGrab  # Import ImageGrab from PIL library

# Global variable for image counter
image_counter = 0

# Load folder_id from config.json
with open('config.json', 'r') as f:
    config = json.load(f)
folder_id = config['folder_id']

# Define maximum number of images to keep
max_images = 10

# Create a deque to store image paths
image_queue = deque(maxlen=max_images)

# Function to capture and upload image
def capture_and_upload():
    global image_counter
    
    # Capture image using ImageGrab
    image = ImageGrab.grab()  # Capture the screen (including all monitors)
    
    # Convert image to RGB mode
    image = image.convert("RGB")
    
    # Save captured image
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_path = f'webcam_image_{timestamp}_{image_counter}.jpg'
    image.save(image_path)
    
    # Close the image explicitly
    image.close()
    
    # Increment image counter
    image_counter += 1
    
    # Add image path to the queue
    image_queue.append(image_path)
    
    # Upload image to Google Drive
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'camstream-415716-17864761f302.json'  # Path to your service account credentials file
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=credentials)
    
    file_metadata = {
        'name': image_path,
        'parents': [folder_id]
    }
    media = MediaFileUpload(image_path)
    try:
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Uploaded image: {file.get('id')} - {image_path}")
    except PermissionError:
        print(f"Permission error: {image_path}")
    
    # Remove oldest image from queue and delete corresponding file
    if len(image_queue) >= max_images:
        oldest_image_path = image_queue.popleft()
        try:
            os.remove(oldest_image_path)
            print(f"Removed image: {oldest_image_path}")
        except PermissionError:
            print(f"Failed to remove image: {oldest_image_path}")

# Capture and upload images continuously
while True:
    capture_and_upload()
    time.sleep(0.02)  # Adjust the delay as needed to achieve desired FPS
