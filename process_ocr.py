import cv2
import pytesseract
from pytesseract import Output
import re

def capture_image():
    """Captures an image from the camera and returns it."""
    cap = cv2.VideoCapture(0)  # Initialize the camera
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None
    
    # Capture a single frame
    ret, frame = cap.read()
    cap.release()  # Release the camera
    if not ret:
        print("Error: Could not read frame.")
        return None
    
    return frame

def save_image(image, path='captured_image.jpg'):
    """Saves the image to a file."""
    cv2.imwrite(path, image)

def process_image_with_ocr(image_path):
    """Processes the saved image with OCR to extract text."""
    # Load the image with OpenCV
    img = cv2.imread(image_path)

    # Convert to grayscale for better OCR results
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use pytesseract to perform OCR on the image
    text = pytesseract.image_to_string(gray, config='--psm 6')
    return text

def extract_valid_text(text):
    """Extracts valid text based on specific criteria."""
    # Criteria: Uppercase letters and/or numbers, length between 3 and 10 characters
    valid_texts = re.findall(r'\b[A-Z0-9]{3,10}\b', text)
    return valid_texts

def main():
    image = capture_image()
    if image is not None:
        # Save captured image for processing
        image_path = 'captured_image.jpg'
        save_image(image, image_path)
        
        # Process image to extract text
        text = process_image_with_ocr(image_path)
        print("Extracted Text:", text)
        
        # Extract and print valid texts
        valid_texts = extract_valid_text(text)
        if valid_texts:
            print("Valid Texts:", valid_texts)
        else:
            print("No valid texts found.")
    else:
        print("Failed to capture image.")

if __name__ == '__main__':
    main()
