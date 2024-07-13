from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2
import numpy as np
import threading

app = Flask(__name__)

model = YOLO("yolov8n-pose.pt")

# Global video capture variables
video_capture = None
capture_lock = threading.Lock()

def calculate_angle(p1, p2, p3):
    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p3) - np.array(p2)
    angle_rad = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    angle_deg = np.degrees(angle_rad)
    return angle_deg

def release_video_capture():
    global video_capture
    with capture_lock:
        if video_capture is not None:
            video_capture.release()
            video_capture = None

def initialize_video_capture():
    global video_capture
    release_video_capture()
    with capture_lock:
        video_capture = cv2.VideoCapture(0)
        video_capture.set(3, 640)
        video_capture.set(4, 480)

def generate_frames(exercise):
    global video_capture
    initialize_video_capture()
    count = 0
    is_down = False

    while True:
        with capture_lock:
            if video_capture is None:
                break
            success, frame = video_capture.read()
            if not success:
                break

        frame = cv2.resize(frame, (640, 480))
        results = model(frame)
        for r in results[0]:
            keypoints = r.keypoints.xy
            if exercise == 'push_ups':
                angle = calculate_angle(keypoints[0][6], keypoints[0][8], keypoints[0][10])
                if angle > 90 and not is_down:
                    is_down = True
                elif angle < 45 and is_down:
                    is_down = False
                    count += 1
            elif exercise == 'pull_ups':
                angle = calculate_angle(keypoints[0][6], keypoints[0][8], keypoints[0][10])
                if angle > 90 and not is_down:
                    is_down = True
                elif angle < 14 and is_down:
                    is_down = False
                    count += 1

        annotated_frame = results[0].plot()
        if exercise == 'push_ups':
            cv2.putText(annotated_frame, f'Push-ups: {count}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (10, 10, 255), 5)
        elif exercise == 'pull_ups':
            cv2.putText(annotated_frame, f'Pull-ups: {count}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 10, 10), 5)
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    release_video_capture()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames('push_ups'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_pull_up')
def video_feed_pull_up():
    return Response(generate_frames('pull_ups'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('workout.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True, use_reloader=False)
