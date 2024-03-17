import picamera
import time
from PIL import Image, ImageEnhance
import pytesseract
import re

def capture_image(filename):
    """Captures an image to the specified filename."""
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        time.sleep(2)  # Camera warm-up time
        camera.capture(filename)

def process_image(filename):
    """Preprocesses the image and performs OCR."""
    try:
        # Load the image
        with Image.open(filename) as img:
            # Preprocess (optional)
            # Convert to grayscale
            img = img.convert('L')
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2.0)  # Adjust contrast factor as needed

            # Perform OCR
            text = pytesseract.image_to_string(img)
            return text
    except Exception as e:
        print(f"Error processing image: {e}")
        return ""

def extract_valid_text(text):
    """Extracts valid text based on specific criteria."""
    # Criteria: Uppercase letters and/or numbers, length between 3 and 10 characters
    valid_texts = re.findall(r'\b[A-Z0-9]{3,10}\b', text)
    return valid_texts

def main():
    image_filename = 'test_image.jpg'
    
    # Step 1: Capture image
    capture_image(image_filename)
    print("Image captured successfully.")

    # Step 2: Process image
    text = process_image(image_filename)
    if text:
        print("OCR Text:", text)
        
        # Step 3: Extract valid texts
        valid_texts = extract_valid_text(text)
        if valid_texts:
            print("Valid Texts Found:", valid_texts)
        else:
            print("No valid texts match the criteria.")
    else:
        print("No text found in image.")

if __name__ == '__main__':
    main()
