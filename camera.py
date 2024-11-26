import io
from flask import Flask, Response
from picamera2 import Picamera2
from PIL import Image

app = Flask(__name__)

def generate_frames():
    # Initialize Picamera2
    picam2 = Picamera2()
    
    # Configure camera for video stream
    video_config = picam2.create_video_configuration(main={"size": (640, 480)})
    picam2.configure(video_config)
    
    # Start the camera
    picam2.start()
    
    try:
        while True:
            # Capture frame
            frame = picam2.capture_array()
            
            # Convert frame to RGB if needed
            image = Image.fromarray(frame)
            if image.mode != 'RGB':
                image = image.convert('RGB')  # Convert RGBA to RGB
            
            # Convert frame to JPEG
            stream = io.BytesIO()
            image.save(stream, format='JPEG')
            stream.seek(0)
            
            # Yield frame as part of multipart HTTP response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n')
            stream.seek(0)
            stream.truncate()
    finally:
        # Stop the camera when done
        picam2.stop()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
