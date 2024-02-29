import cv2
import threading
import time
import datetime
import json

class VideoRecorder(threading.Thread):
    def __init__(self, filename, offset_seconds, fps):
        super().__init__()
        self.filename = filename
        self.offset_seconds = offset_seconds
        self.fps = fps
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            start_time = time.time() + self.offset_seconds

            # Initialize video writer
            height, width = 480, 640  # Default resolution, you can adjust as needed
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(self.filename, fourcc, self.fps, (width, height))

            # Capture frames for one minute
            while time.time() - start_time < 60:
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
                cap.release()

            # Save the video file with timestamp as filename
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            save_filename = f"{timestamp}.mp4"
            cv2.destroyAllWindows()
            out.release()
            cv2.imwrite(save_filename, cv2.VideoCapture(self.filename).read()[1])

            time.sleep(60)  # Wait for the next minute

    def stop(self):
        self.stop_event.set()

# Load config from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

# Extract FPS from config
fps = config.get('fps', 20)  # Default FPS is 20 if not specified in config

# Create two video recorder instances with different filenames and start times
recorder1 = VideoRecorder("video1.mp4", 0, fps)  # Offset of 0 seconds for the first recorder
recorder2 = VideoRecorder("video2.mp4", 30, fps)  # Offset of 30 seconds for the second recorder

# Start recording threads
recorder1.start()
recorder2.start()

# Wait for a KeyboardInterrupt to stop the script
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Script stopped by user")

# Stop both recorder threads
recorder1.stop()
recorder2.stop()

# Wait for both recorder threads to finish
recorder1.join()
recorder2.join()

print("Both recordings complete.")
