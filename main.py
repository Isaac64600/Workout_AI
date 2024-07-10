from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO("yolov8n-pose.pt")

def calculate_angle(p1, p2, p3):

    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p3) - np.array(p2)


    angle_rad = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


    angle_deg = np.degrees(angle_rad)

    return angle_deg

def check_form(keypoints,facing,transition):
    f = open("demofile2.txt", "a")
    left_elbow_angle = calculate_angle(keypoints[0][5], keypoints[0][7], keypoints[0][9])
    left_hip_angle = calculate_angle(keypoints[0][5],keypoints[0][11], keypoints[0][15])
    right_elbow_angle = calculate_angle(keypoints[0][6], keypoints[0][8],keypoints[0][10])
    right_hip_angle = calculate_angle(keypoints[0][6],keypoints[0][12], keypoints[0][16])
    if facing:
        elbow_angle = left_elbow_angle
        hip_angle = left_hip_angle
    else :
        elbow_angle = right_elbow_angle
        hip_angle = right_hip_angle

    if elbow_angle >= 155 and hip_angle >= 150 and not transition:
        return True
    elif elbow_angle <= 80 and hip_angle >= 150 and not transition:
        return True
    elif  155 > elbow_angle > 80 and hip_angle>= 150 and transition:
        return True
    else :
        f.write(f"Elbow angle: {elbow_angle}\n, hip angle: {hip_angle}\n,transition: {transition}\n")
        f.close()
        return False
def check_position(keypoints):
    is_right = False
    is_left = False
    angle = 0
    if keypoints[0][0][0] < 600 and keypoints[0][9][0] > keypoints[0][0][0]:
        is_right = False
        is_left = True
        angle = calculate_angle(keypoints[0][5], keypoints[0][7], keypoints[0][9])
    if keypoints[0][0][0]>600 and keypoints[0][10][0] <  keypoints[0][0][0]:
        is_right = True
        is_left = False
        angle = calculate_angle(keypoints[0][6], keypoints[0][8], keypoints[0][10])

    return is_right, is_left, angle

push_up_count = 0
transition =False
is_down = False
cap = cv2.VideoCapture("p0.mp4")
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)
start = 0
while(cap.isOpened()):
    try:
        success, frame = cap.read()

        if success:
            results = model(frame)
            for r in results[0]:
                keypoints = r.keypoints.xy

                angle = check_position(keypoints)[2]

                print("Angle: ", angle)
                print("hip_angle: ", calculate_angle(keypoints[0][5], keypoints[0][11], keypoints[0][15]))
                print("transition: ", transition)
                print("is_down: ", is_down)
                print("form: ", check_form(keypoints, check_position(keypoints)[1], transition))

                if angle > 155 and not is_down:
                    is_down = True
                elif angle < 80 and is_down:
                    is_down = False
                    push_up_count += 1
                    print('Push up count:', push_up_count)
                elif 155 > angle > 80:
                    if not transition:
                        transition = True
                elif angle > 155 and is_down and transition:
                    transition = False
                elif angle < 80 and not is_down and transition:
                    transition = False


                form_correct = check_form(keypoints, check_position(keypoints)[1], transition)
                if not form_correct:
                    cv2.putText(frame, 'Correct the Posture', (800, 100), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 10)

            annotated_frame = results[0].plot()
            bar_length = int(570 * angle / 180)
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

