from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2
import numpy as np

app = Flask(__name__)

model = YOLO("yolov8n-pose.pt")

def calculate_angle(p1, p2, p3):
    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p3) - np.array(p2)
    angle_rad = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    angle_deg = np.degrees(angle_rad)
    return angle_deg

def generate_frames():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    push_up_count = 0
    is_down = False

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame = cv2.resize(frame, (640, 480))
            results = model(frame)
            for r in results[0]:
                keypoints = r.keypoints.xy
                angle = calculate_angle(keypoints[0][6], keypoints[0][8], keypoints[0][10])
                if angle > 90 and not is_down:
                    is_down = True
                elif angle < 45 and is_down:
                    is_down = False
                    push_up_count += 1

            annotated_frame = results[0].plot()
            cv2.putText(annotated_frame, f'Push-ups: {push_up_count}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (10, 10, 255), 5)
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('workout.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True, use_reloader=False)
