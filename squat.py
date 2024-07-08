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

def check_form(keypoints):
    f = open("demofile0.txt", "a")
    angle = calculate_angle(keypoints[0][11], keypoints[0][13], keypoints[0][15])
    if angle > 160 :
        if calculate_angle(keypoints[0][5], keypoints[0][11], keypoints[0][13]) > 160:
            return True
        else:
            f.write(f"Body Angle: {calculate_angle(keypoints[0][5], keypoints[0][11], keypoints[0][13])}\n")
            f.close()
            return False
    if angle < 120 :
        if calculate_angle(keypoints[0][5], keypoints[0][11], keypoints[0][13]) < 110:
            return True
        else:
            f.write(f"Body Angle: {calculate_angle(keypoints[0][5], keypoints[0][11], keypoints[0][13])}\n")
            f.close()
            return False


squat_count = 0
is_down = False
cap = cv2.VideoCapture("squat.mp4")
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)
while(cap.isOpened()):
    try:
        success, frame = cap.read()

        if success:
            results = model(frame)
            for r in results[0]:
                keypoints = r.keypoints.xy
                angle = calculate_angle(keypoints[0][11], keypoints[0][13], keypoints[0][15])
                # print("Form: ", check_form(keypoints))
                print("Form: ", check_form(keypoints))
                print("Angle: ", angle)
                Body_angle = calculate_angle(keypoints[0][5],keypoints[0][11],keypoints[0][13])
                print("Body: ", Body_angle)
                print("Head: ",keypoints[0][0][1])
                # print("left Hand: ", keypoints[0][9][1])
                # print("right Hand: ", keypoints[0][10][1])

                if angle > 160 and is_down == False:
                    is_down = True
                elif angle < 120 and is_down == True:
                    is_down = False
                    squat_count += 1
                print('push up count:', squat_count)

            annotated_frame = results[0].plot()
            bar_length = int(570 * angle / 180)
            cv2.putText(annotated_frame, f'Squats: {squat_count}', (20, 70), 2, 2, (10, 10, 255), 5)
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

