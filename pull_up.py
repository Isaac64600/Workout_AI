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

def check_form(keypoints):
    f = open("demofile1.txt", "a")
    if keypoints[0][9][1] < 200 and keypoints[0][10][1] < 200:
        return True
    else:
        f.write(f"Head: {keypoints[0][0]}\n, Left Hand: {keypoints[0][9]}\n, Right Hand: {keypoints[0][10]}\n, "
                f"Left Feet: {keypoints[0][15]}\n, Right Feet: {keypoints[0][16]}\n")
        f.close()
        return False


pull_up_count = 0
is_down = False
cap = cv2.VideoCapture("pull_ups.mp4")
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
                angle = calculate_angle(keypoints[0][6], keypoints[0][8], keypoints[0][10])
                print("Form: ", check_form(keypoints))
                print("Angle: ", angle)
                Body_angle = calculate_angle(keypoints[0][11],keypoints[0][5],keypoints[0][7])
                print("Body: ", Body_angle)
                print("Head: ",keypoints[0][0][1])
                print("left Hand: ", keypoints[0][9][1])
                print("right Hand: ", keypoints[0][10][1])
                if check_form(keypoints):
                    if angle > 90 and is_down == False:
                        is_down = True
                    elif angle < 14 and is_down == True:
                        is_down = False
                        pull_up_count += 1
                    print('pull up count:', pull_up_count)
                else:
                    position = 'Correct the Posture'
                    cv2.putText(frame, position, (800, 100), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 10)


            annotated_frame = results[0].plot()
            cv2.putText(annotated_frame, f'Pull-ups: {pull_up_count}', (20, 70), 2, 2, (10, 10, 255), 5)
            cv2.imshow("Inference",annotated_frame)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    except ValueError:
        print("Get into position !")


cap.release()
cv2.destroyAllWindows()

