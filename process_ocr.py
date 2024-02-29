import os
import csv
from google.cloud import storage
from PIL import Image
import pytesseract

def download_images_from_storage(bucket_name, destination_folder):
    """Download all images from Google Cloud Storage to local folder."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    # Create destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    blobs = bucket.list_blobs()
    for blob in blobs:
        if blob.name.endswith('.jpg') or blob.name.endswith('.jpeg') or blob.name.endswith('.png'):
            destination_file = os.path.join(destination_folder, os.path.basename(blob.name))
            blob.download_to_filename(destination_file)
            print(f"Downloaded {blob.name}")

def perform_ocr_on_images(image_folder, output_csv, dump_folder, confidence_threshold=0.85):
    """Perform OCR on images and record results in CSV file."""
    with open(output_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Filename', 'Detected Text'])
        
        for filename in os.listdir(image_folder):
            if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
                image_path = os.path.join(image_folder, filename)
                text = perform_ocr(image_path)
                if text:
                    confidence = 1.0  # Placeholder for confidence level (can be obtained from OCR library)
                    if confidence >= confidence_threshold:
                        csvwriter.writerow([filename, text])
                    else:
                        move_to_dump(image_path, dump_folder)
                else:
                    move_to_dump(image_path, dump_folder)

def perform_ocr(image_path):
    """Perform OCR on the given image and return detected text."""
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text.strip()
    except Exception as e:
        print(f"Failed to perform OCR on {image_path}: {e}")
        return None

def move_to_dump(image_path, dump_folder):
    """Move the image file to the dump folder."""
    try:
        os.makedirs(dump_folder, exist_ok=True)
        filename = os.path.basename(image_path)
        new_path = os.path.join(dump_folder, filename)
        os.rename(image_path, new_path)
        print(f"Moved {filename} to dump folder")
    except Exception as e:
        print(f"Failed to move {image_path} to dump folder: {e}")

def main():
    # Configuration
    bucket_name = 'your_bucket_name'
    destination_folder = 'downloaded_images'
    output_csv = 'observations.csv'
    dump_folder = 'dump'
    
    # Step 1: Download images from Google Cloud Storage
    download_images_from_storage(bucket_name, destination_folder)
    
    # Step 2-4: Perform OCR on images and record results in CSV file
    perform_ocr_on_images(destination_folder, output_csv, dump_folder)

if __name__ == "__main__":
    main()
