import time
import threading
from flask import Flask, send_file
from picamera2 import Picamera2
from PIL import Image

app = Flask(__name__)
picam2 = Picamera2()
current_image_path = "latest_image.jpg"  # Path to the latest captured image

def take_photo_every_minute():
    """Function to take a photo every 1 minute and save it."""
    global current_image_path
    
    # Configure the camera
    photo_config = picam2.create_still_configuration(main={"size": (640, 480)})
    picam2.configure(photo_config)
    picam2.start()

    try:
        while True:
            # Capture a frame
            frame = picam2.capture_array()

            # Convert frame to RGB and save as JPEG
            image = Image.fromarray(frame)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Save image to a file
            current_image_path = f"photo_{int(time.time())}.jpg"  # Save with a timestamp
            image.save(current_image_path, format='JPEG')
            
            print(f"Saved photo: {current_image_path}")

            # Wait for 1 minute
            time.sleep(60)
    except KeyboardInterrupt:
        # Stop the camera on manual interruption
        picam2.stop()
        print("Camera stopped.")

# Start the photo-taking function in a separate thread
photo_thread = threading.Thread(target=take_photo_every_minute, daemon=True)
photo_thread.start()

@app.route('/photo')
def photo():
    """Serve the last captured photo."""
    return send_file(current_image_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
