import logging
from multiprocessing import Pool
from picamera import PiCamera
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Preprocessing options (easily tweakable)
PREPROCESS_GRAYSCALE = True
CONTRAST_ENHANCEMENT = 1.5  # Set to 1 for no enhancement
SHARPNESS_ENHANCEMENT = 1.0  # Set to 1 for no enhancement

# OCR function to process an image
def process_image(image_data):
    try:
        image = Image.open(BytesIO(image_data))
        
        # Preprocess the image
        if PREPROCESS_GRAYSCALE:
            image = image.convert('L')
        if CONTRAST_ENHANCEMENT != 1:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(CONTRAST_ENHANCEMENT)
        if SHARPNESS_ENHANCEMENT != 1:
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(SHARPNESS_ENHANCEMENT)
        
        text = pytesseract.image_to_string(image)
        # Filter text based on your criteria
        valid_texts = re.findall(r'\b[A-Z0-9]{3,10}\b', text)
        return valid_texts
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return []

# Function to take a picture and process it
def capture_and_process(camera):
    stream = BytesIO()
    camera.capture(stream, format='jpeg')
    stream.seek(0)
    texts = process_image(stream.getvalue())
    if texts:
        logging.info(f"Found texts: {texts}")
    else:
        # No valid text found; option to delete the image here
        logging.info("No valid text found in the image.")

# Main function to setup camera and multiprocessing
def main():
    camera = PiCamera()
    camera.resolution = (1024, 768)

    # Setup multiprocessing pool based on the number of cores
    pool = Pool()  # Automatically uses all available cores

    try:
        while True:
            # Using apply_async to not block the script while waiting for the process to finish
            pool.apply_async(capture_and_process, args=(camera,))
    except KeyboardInterrupt:
        logging.info("Stopping by user request.")
    finally:
        pool.close()
        pool.join()
        camera.close()

if __name__ == "__main__":
    main()
