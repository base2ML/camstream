import cv2
import pytesseract
from PIL import Image
import numpy as np
from datetime import datetime
import os

# Configure PyTesseract path to the executable
# For Windows, it might look like this: pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# Update the path according to your Tesseract-OCR installation

stream_url = 'http://173.74.16.151:8081'
cap = cv2.VideoCapture(stream_url)

# Create a set to store unique texts
detected_texts = set()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Convert frame to PIL Image
        cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_image)

        # Perform OCR
        text = pytesseract.image_to_string(pil_image).strip()

        if text:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("detected_text_log.txt", "a") as file:
                file.write(f"[{timestamp}, \"entrance\", \"{text}\"]\n")
            
            if text not in detected_texts:
                detected_texts.add(text)
                # Save the image with timestamp
                image_filename = f"image_{timestamp.replace(':', '-')}.jpg"
                pil_image.save(image_filename)
                print(f"Unique text detected and image saved: {image_filename}")

except KeyboardInterrupt:
    print("Stream stopped")

finally:
    cap.release()
    cv2.destroyAllWindows()
