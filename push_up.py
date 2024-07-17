from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO("yolov8n-pose.pt")

form = None
count = 0
transition = False
is_down = True


def calculate_angle(p1, p2, p3):
    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p3) - np.array(p2)

    angle_rad = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    angle_deg = np.degrees(angle_rad)

    return angle_deg


def check_form(keypoints, facing, transition):
    f = open("demofile2.txt", "a")
    left_elbow_angle = calculate_angle(keypoints[0][5], keypoints[0][7], keypoints[0][9])
    left_hip_angle = calculate_angle(keypoints[0][5], keypoints[0][11], keypoints[0][15])
    right_elbow_angle = calculate_angle(keypoints[0][6], keypoints[0][8], keypoints[0][10])
    right_hip_angle = calculate_angle(keypoints[0][6], keypoints[0][12], keypoints[0][16])
    head = keypoints[0][0][1]

    if facing:
        elbow_angle = left_elbow_angle
        hip_angle = left_hip_angle
    else:
        elbow_angle = right_elbow_angle
        hip_angle = right_hip_angle

    # Ensure head detection is considered properly
    if head <= 90:
        f.write(f"Elbow angle: {elbow_angle}\nHip angle: {hip_angle}\nTransition: {transition}\nHead: {head}\n")
        f.close()
        return False

    if (elbow_angle >= 155 and hip_angle >= 148 and not transition) or (
            elbow_angle <= 80 and hip_angle >= 148 and not transition):
        return True
    elif 170 > elbow_angle > 74 and hip_angle >= 148 and transition:
        return True
    else:
        f.write(f"Elbow angle: {elbow_angle}\nHip angle: {hip_angle}\nTransition: {transition}\nHead: {head}\n")
        f.close()
        return False


def check_position(keypoints):
    is_right = False
    is_left = False
    angle = 0

    head_x = keypoints[0][0][0]
    left_wrist_x = keypoints[0][9][0]
    right_wrist_x = keypoints[0][10][0]

    print(f"Head X position: {head_x}")
    print(f"Left wrist X position: {left_wrist_x}")
    print(f"Right wrist X position: {right_wrist_x}")

    # Check if the head is positioned between the wrists
    if head_x > left_wrist_x and head_x < right_wrist_x:
        print("Head is between wrists, no clear direction")
    elif head_x < left_wrist_x:
        is_right = False
        is_left = True
        angle = calculate_angle(keypoints[0][5], keypoints[0][7], keypoints[0][9])
        print("Left arm detected")
    elif head_x > right_wrist_x:
        is_right = True
        is_left = False
        angle = calculate_angle(keypoints[0][6], keypoints[0][8], keypoints[0][10])
        print("Right arm detected")
    else:
        print("No arm detected correctly")

    print(f"Calculated angle: {angle}")
    return is_right, is_left, angle


def push_up_count(results):
    if len(results) > 0 and len(results[0]) > 0:  # Check if results contain keypoints
        global count, transition, is_down, form
        for r in results[0]:
            keypoints = r.keypoints.xy

            angle = check_position(keypoints)[2]
            # Assuming keypoints is a list of keypoints detected
            is_right, is_left, angle = check_position(keypoints)
            hip_angle = calculate_angle(keypoints[0][5], keypoints[0][11], keypoints[0][15])
            form = check_form(keypoints, is_left, transition)

            print("Angle: ", angle)
            print("hip_angle: ", hip_angle)
            print("transition: ", transition)
            print("is_down: ", is_down)
            print("form: ", form)
            print("Head: ", keypoints[0][0])
            print("Left: ", is_left)
            print("Right arm: ", calculate_angle(keypoints[0][6], keypoints[0][8], keypoints[0][10]))
            print("Left arm: ", calculate_angle(keypoints[0][5], keypoints[0][7], keypoints[0][9]))

            if angle > 155:
                if not is_down and transition:
                    transition = False
                    is_down = True
                    if form:
                        count += 1
                        print("count: ", count)
                    else:
                        print("FAIL")
            elif 95 < angle < 155:
                if not transition:
                    transition = True
            elif angle < 95:
                if is_down and transition:
                    transition = False
                    is_down = False


    return count, form
