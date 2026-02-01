import cv2
from flask import Flask, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import threading
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# 1. Load your model (pointing to the file in your root)
model = YOLO("yolov8n.pt")

# 2. Shared list to store detections
incidents = []

def run_ai_detection():
    global incidents
    # Open the webcam (0 is usually the default camera)
    cap = cv2.VideoCapture(0)
    
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Run YOLO inference
        results = model(frame, conf=0.5, verbose=False)
        
        # Check for specific objects (e.g., "person" is class 0)
        for r in results:
            classes = r.boxes.cls.tolist()
            if 0 in classes:  # If a person is detected
                new_incident = {
                    "id": int(time.time()),
                    "title": "Person Detected",
                    "time": datetime.now().strftime("%I:%M:%S %p"),
                    "description": "AI identified an individual in the restricted frame.",
                    "color": "bg-red-600/40"
                }
                
                # Add to the front of the list and keep only the last 10
                incidents = [new_incident] + incidents
                incidents = incidents[:10]
                
                # Sleep briefly to avoid flooding the dashboard with the same detection
                time.sleep(5)

    cap.release()

# Start the AI in a separate thread so Flask can still handle requests
threading.Thread(target=run_ai_detection, daemon=True).start()

@app.route('/api/incidents', methods=['GET'])
def get_incidents():
    return jsonify(incidents)

if __name__ == '__main__':
    app.run(debug=True, port=5001, use_reloader=False)