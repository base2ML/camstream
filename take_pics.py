import os
import pygame.camera
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

    # Initialize Pygame
    pygame.init()
    pygame.camera.init()

    # Get the list of available cameras
    camera_list = pygame.camera.list_cameras()
    if not camera_list:
        print("No cameras found")
        return

    # Use the first camera in the list (change index if needed)
    camera = pygame.camera.Camera(camera_list[0])

    # Initialize the camera
    camera.start()

    try:
        while True:
            # Capture an image
            img = camera.get_image()

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            folder_path = os.path.join(config['image_folder'], timestamp)  # Create folder path
            os.makedirs(folder_path, exist_ok=True)  # Create folder if not exists
            
            image_path = os.path.join(folder_path, f'webcam_image_{timestamp}_{image_counter}.bmp')

            # Save the captured image to a file (in BMP format)
            pygame.image.save(img, image_path)
            
            print("Image saved at:", image_path)  # Print the image path

            image_counter += 1

            time.sleep(1 / fps)  # Adjust for specified FPS

    except KeyboardInterrupt:
        print("Script stopped by user")

    finally:
        # Stop the camera when done
        camera.stop()

# Start capturing images
capture_images()
