import os
import csv

def delete_local_file(file_path):
    try:
        os.remove(file_path)
        print(f"Deleted local file: {file_path}")
        return True  # Return True if deletion is successful
    except FileNotFoundError:
        print(f"File not found: {file_path}. Removing entry from CSV.")
        return True  # Return True if file is not found
    except Exception as e:
        print(f"Failed to delete local file: {file_path}. Error: {e}")
        return False  # Return False if deletion fails

def main():
    # Read the list of uploaded file paths from uploaded_images.csv
    uploaded_files = []
    with open('uploaded_images.csv', 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            file_path = row[0].strip()  # Remove leading/trailing whitespaces
            if file_path:  # Check if the line is not empty
                uploaded_files.append(file_path)

    # Delete each corresponding local file
    with open('uploaded_images.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for file_path in uploaded_files:
            if delete_local_file(file_path):
                print(f"Removed entry for {file_path} from CSV")
            else:
                csvwriter.writerow([file_path])  # Rewrite the entry if deletion fails

if __name__ == "__main__":
    main()
