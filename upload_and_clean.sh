#!/bin/bash

# Directory of images
TARGET_DIR='/var/lib/motion'

FOLDER_NAME='picamaaa'

# Your GCS bucket name
BUCKET_NAME='camstream'

# Log file to keep track of uploaded files
LOG_FILE='/home/picamaaa/log_file.txt'

# Ensure the log file directory exists
LOG_DIR=$(dirname "$LOG_FILE")
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

# Ensure log file exists
touch "$LOG_FILE"

# Perform the upload in parallel
echo "Starting parallel upload..."
gsutil -m cp -r "$TARGET_DIR"/* gs://$BUCKET_NAME/$FOLDER_NAME

# Check if the upload was successful
if [ $? -eq 0 ]; then
    echo "Upload successful. Logging filenames..."
    # Log filenames
    for file in "$TARGET_DIR"/*; do
        if [ -f "$file" ]; then
            echo "$file" >> "$LOG_FILE"
        fi
    done
    
    # Delete the files listed in the log file
    while IFS= read -r file; do
        echo "Deleting $file..."
        rm "$file"
    done < "$LOG_FILE"

    # Optionally, clear the log file after deletion
    > "$LOG_FILE"
else
    echo "Upload failed. Please check your files and try again."
fi
