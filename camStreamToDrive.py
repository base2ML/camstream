import json
import os
import time
from datetime import datetime
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
    
    # Increment image counter
    image_counter += 1
    
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
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Uploaded image: {file.get('id')} - {image_path}")
    
    # Remove temporary image file
    os.remove(image_path)

# Capture and upload images continuously
while True:
    capture_and_upload()
    time.sleep(0.2)  # Adjust the delay as needed to achieve desired FPS
