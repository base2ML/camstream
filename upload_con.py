import os
import json
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import threading
import multiprocessing

def get_subfolders(folder_path):
    return [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

def upload_files_to_folder(drive_service, folder_id, folder_path, files):
    for file_name in files:
        if file_name.lower().endswith('.jpg'):
            file_path = os.path.join(folder_path, file_name)  # Construct the full file path
            file_metadata = {'name': file_name, 'parents': [folder_id]}
            media = MediaFileUpload(file_path)  # Provide the full path
            drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f"Uploaded file: {file_name}")

def upload_concurrently(drive_service, folder_id, folder_path, files, max_threads):
    num_threads = min(len(files), int(max_threads * multiprocessing.cpu_count()))
    threads = []
    for i in range(num_threads):
        start = i * len(files) // num_threads
        end = (i + 1) * len(files) // num_threads
        thread = threading.Thread(target=upload_files_to_folder, args=(drive_service, folder_id, folder_path, files[start:end]))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def main():
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)

    image_path = config['image_folder']  # Specify the path to the image folder
    folder_id = config['folder_id']  # Get the folder ID from config.json

    # Get all subfolders in the specified image path
    subfolders = get_subfolders(image_path)

    for folder_name in subfolders:
        full_folder_path = os.path.join(image_path, folder_name)
        files = os.listdir(full_folder_path)
        if files:
            credentials = service_account.Credentials.from_service_account_info(credentials)
            drive_service = build('drive', 'v3', credentials=credentials)
            upload_concurrently(drive_service, folder_id, full_folder_path, files, 0.8)
            print(f"Upload for folder {folder_name} complete.")

if __name__ == "__main__":
    main()
