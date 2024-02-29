import os
import json
import csv
import threading
from datetime import datetime, timedelta
from google.oauth2 import service_account
from google.cloud import storage  # Import the Google Cloud Storage client library

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'credentials.json'

def get_subfolders(folder_path):
    return [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

def upload_to_gcs(bucket_name, file_path, destination_blob_name):
    """Uploads a file to Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(file_path)

    print(f"File {file_path} uploaded to {destination_blob_name} in bucket {bucket_name}")

def upload_files_to_folder(bucket_name, folder_path, files, credentials_path):
    for file_name in files:
        if file_name.lower().endswith('.jpg'):
            file_path = os.path.join(folder_path, file_name)  # Construct the full file path
            destination_blob_name = f"test_loc/{file_name}"  # Destination path in GCS bucket
            upload_to_gcs(bucket_name, file_path, destination_blob_name)

            # Write the GCS file path to a CSV file after successful upload
            with open('uploaded_images.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([file_path])

# Main function
def main():
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    image_path = config['image_folder']  # Specify the path to the image folder
    bucket_name = config['bucket_name']  # Get the GCS bucket name from config.json
    credentials_path = 'credentials.json'  # Specify the path to your service account key file

    # Calculate the timestamp for three minutes ago
    three_minutes_ago = datetime.now() - timedelta(minutes=3)

    # Get all subfolders in the specified image path
    subfolders = [f for f in os.listdir(image_path) if os.path.isdir(os.path.join(image_path, f))]

    for folder_name in subfolders:
        # Check if the folder name matches the format 'YYYY-MM-DD_HH-MM'
        try:
            folder_timestamp = datetime.strptime(folder_name, '%Y-%m-%d_%H-%M')
        except ValueError:
            continue  # Skip folders with invalid names
        
        # Check if the folder timestamp is at least 3 minutes behind the current time
        if folder_timestamp <= three_minutes_ago:
            # Construct the full path of the folder to upload
            full_folder_path = os.path.join(image_path, folder_name)
            files = os.listdir(full_folder_path)

            if files:
                upload_thread = threading.Thread(target=upload_files_to_folder, args=(bucket_name, full_folder_path, files, credentials_path))
                upload_thread.start()
                upload_thread.join()
                print(f"Upload for folder {folder_name} complete.")

if __name__ == "__main__":
    main()