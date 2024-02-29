import os
import cv2
import time
from datetime import datetime

# Load config from config.json
config = {
    "image_folder": "captured_images"
}

# Global variables
image_counter = 0
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
        
        image_counter += 1
        
        time.sleep(1 / fps)  # Adjust for specified FPS

    # Release the VideoCapture object when done
    cap.release()

# Start capturing images
capture_images()
