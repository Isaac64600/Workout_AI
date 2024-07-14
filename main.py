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

def reset_globals():
    global count, transition, is_down, form
    count = 0
    transition = False
    is_down = False
    form = None

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

        frame = cv2.resize(frame, (640, 480))
        results = model(frame)

        if len(results) > 0 and len(results[0]) > 0:  # Check if results contain keypoints
            if exercise == 'push_ups':
                push_up_count, form = push_up.push_up_count(results)
            elif exercise == 'pull_ups':
                pull_up_count, form = pull_up.pull_up_count(results)
            elif exercise == "squat":
                squat_count, form = squat.squat_count(results)

            annotated_frame = results[0].plot()
            if exercise == 'push_ups':
                cv2.putText(annotated_frame, f'Push-ups: {push_up_count}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (10, 10, 255), 5)
            elif exercise == 'pull_ups':
                cv2.putText(annotated_frame, f'Pull-ups: {pull_up_count}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 10, 10), 5)
            elif exercise == "squat":
                cv2.putText(annotated_frame, f'Squat: {squat_count}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 10, 10), 5)
        else:
            annotated_frame = frame

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

@app.route('/video_feed_squat')
def video_feed_squat():
    return Response(generate_frames('squat'), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('workout.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True, use_reloader=False)
