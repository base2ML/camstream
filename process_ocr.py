import io
import time
import numpy as np
import cv2
from picamera import PiCamera
from multiprocessing import Process, Queue

def capture_images(queue):
    with PiCamera() as camera:
        camera.resolution = (1024, 768)
        time.sleep(2)  # Camera warm-up time
        
        for _ in range(10):  # Capture 10 images for demonstration
            stream = io.BytesIO()
            camera.capture(stream, format='jpeg')
            stream.seek(0)
            queue.put(stream.getvalue())  # Put image data into the queue
            time.sleep(1)
    
    queue.put(None)  # Signal that capturing is done

def process_images(queue):
    while True:
        image_data = queue.get()
        if image_data is None:
            break  # Stop if capturing is done
        
        # Convert bytes to numpy array and then to OpenCV image
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Placeholder for processing logic
        # Display the image for demonstration
        cv2.imshow('Image', img)
        cv2.waitKey(1000)  # Wait for 1 sec

    cv2.destroyAllWindows()

if __name__ == '__main__':
    queue = Queue()

    # Start the image capture process
    capture_process = Process(target=capture_images, args=(queue,))
    capture_process.start()

    # Start the image processing process
    process_process = Process(target=process_images, args=(queue,))
    process_process.start()

    # Wait for processes to finish
    capture_process.join()
    process_process.join()
