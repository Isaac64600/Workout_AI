from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO("yolov8n-pose.pt")

form = None
count = 0
transition = False
is_down = False

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


def pull_up_count(results):
    if len(results) > 0 and len(results[0]) > 0:  # Check if results contain keypoints
        global count, transition, is_down, form
        for r in results[0]:
                keypoints = r.keypoints.xy
                angle = calculate_angle(keypoints[0][6], keypoints[0][8], keypoints[0][10])
                form = check_form(keypoints)
                print("Form: ", check_form(keypoints))
                print("Angle: ", angle)
                print("IsDown: ", is_down)
                print("Count: ", count)
                # Body_angle = calculate_angle(keypoints[0][11],keypoints[0][5],keypoints[0][7])
                # print("Body: ", Body_angle)
                # print("Head: ",keypoints[0][0][1])
                # print("left Hand: ", keypoints[0][9][1])
                # print("right Hand: ", keypoints[0][10][1])
                if angle > 90 and is_down == False:
                        is_down = True
                elif angle < 68 and is_down == True:
                        is_down = False
                        count += 1

    return count, form
