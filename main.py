from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO("yolov8n-pose.pt")

def calculate_angle(p1, p2, p3):
    # p1, p2, p3 are the points in format [x, y]
    # Calculate the vectors
    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p3) - np.array(p2)

    # Calculate the angle in radians
    angle_rad = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    # Convert to degrees
    angle_deg = np.degrees(angle_rad)

    return angle_deg


push_up_count = 0
is_down = False
cap = cv2.VideoCapture("push_ups.mp4")
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)
try:
    while(cap.isOpened()):
        success, frame = cap.read()

        if success:
            results = model(frame)
            for r in results[0]:
                keypoints = r.keypoints.xy

                angle = calculate_angle(keypoints[0][6], keypoints[0][8], keypoints[0][10])
                print("Angle:", angle)

                if angle > 90 and is_down == False:
                    is_down = True
                elif angle < 45 and is_down == True:
                    is_down = False
                    push_up_count += 1
                print('push up count:', push_up_count)


            annotated_frame = results[0].plot()
            bar_length = int(570 * angle / 180)
            # cv2.rectangle(annotated_frame, (10, 10), (10 + 300, 20), (0, 255, 0), -1)
            # cv2.rectangle(annotated_frame, (10, 10), (10 + bar_length, 20), (10, 10, 255), -1)
            cv2.putText(annotated_frame, f'Push-ups: {push_up_count}', (20, 70), 2, 2, (10, 10, 255), 5)
            cv2.rectangle(annotated_frame, (50,100), (100,600), (0, 0, 255), thickness=-1, lineType=cv2.LINE_8)
            cv2.rectangle(annotated_frame, (50,100 + bar_length), (100,600), (9, 255, 0), thickness=-1, lineType=cv2.LINE_8)
            cv2.imshow("Inference",annotated_frame)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
except ValueError:
    print("Get into position !")

cap.release()
cv2.destroyAllWindows()

