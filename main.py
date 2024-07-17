from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2
import numpy as np
import threading

import pull_up
import push_up
import squat

app = Flask(__name__)

model = YOLO("yolov8n-pose.pt")

# Global video capture variables
video_capture = None
capture_lock = threading.Lock()

# Global variables for counting and form tracking
exercise_count = {
    'push_ups': 0,
    'pull_ups': 0,
    'squat': 0
}

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
        video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def reset_globals():
    global exercise_count
    exercise_count = {
        'push_ups': 0,
        'pull_ups': 0,
        'squat': 0
    }

def generate_frames(exercise):
    global video_capture
    initialize_video_capture()
    reset_globals()
    while True:
        with capture_lock:
            if video_capture is None:
                break
            success, frame = video_capture.read()
            if not success:
                break

        # Perform YOLO inference
        frame = cv2.resize(frame, (640, 480))
        results = model(frame)

        if len(results) > 0 and len(results[0]) > 0:  # Check if results contain keypoints
            if exercise == 'push_ups':
                reps, form = push_up.push_up_count(results)
            elif exercise == 'pull_ups':
                reps, form = pull_up.pull_up_count(results)
            elif exercise == "squat":
                reps, form = squat.squat_count(results)

            annotated_frame = results[0].plot()
            if form:
                exercise_count[exercise] = reps
                cv2.putText(annotated_frame, f'{exercise.capitalize()}: {exercise_count[exercise]}',
                            (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (10, 10, 255), 5)
            else:
                cv2.putText(annotated_frame, 'Correct the Posture',
                            (20, 70), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 10)
        else:
            annotated_frame = frame

        # Compress the frame before sending it
        ret, buffer = cv2.imencode('.jpg', annotated_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
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

@app.route('/video_feed_squat')
def video_feed_squat():
    return Response(generate_frames('squat'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('workout.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True, use_reloader=False)
