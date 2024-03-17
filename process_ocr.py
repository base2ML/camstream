from picamera2 import Picamera2
from picamera2.previews import Preview

# Initialize Picamera2
picam2 = Picamera2()

# Prepare the camera configuration
config = picam2.create_still_configuration()

# Start the camera with the configuration
picam2.start_and_configure(config)

# Optionally, start a preview if you're connected to a display
preview = Preview(picam2)
preview.start()

# Capture and save an image
picam2.capture_file("captured_image.jpg")

# Stop the preview if it was started
preview.stop()

print("Image captured successfully as 'captured_image.jpg'")
