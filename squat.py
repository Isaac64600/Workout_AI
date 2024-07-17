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

def check_form(keypoints, transition):
    f = open("demofile0.txt", "a")
    leg_angle = calculate_angle(keypoints[0][11], keypoints[0][13], keypoints[0][15])
    body_angle = calculate_angle(keypoints[0][5], keypoints[0][11], keypoints[0][13])


    if leg_angle > 159 and not transition:
        if body_angle > 163:
            return True
        else:
            f.write(f"Body Angle: {body_angle}\n")
            f.close()
            return False


    elif leg_angle < 120 and not transition:
        if body_angle < 100:
            return True
        else:
            f.write(f"Body Angle: {body_angle}\n, Leg Angle: {leg_angle}\n")
            f.close()
            return False


    elif 120 <= leg_angle <= 175 and transition:
        if 100 <= body_angle <= 170:
            return True


def squat_count(results):
    if len(results) > 0 and len(results[0]) > 0:  # Check if results contain keypoints
        global count, transition, is_down, form
        for r in results[0]:
                keypoints = r.keypoints.xy
                angle = calculate_angle(keypoints[0][11], keypoints[0][13], keypoints[0][15])
                form = check_form(keypoints, transition)
                print("Form: ", check_form(keypoints, transition))
                print("Is Down: ", is_down)
                print("Transition: ", transition)
                print("Angle: ", angle)
                Body_angle = calculate_angle(keypoints[0][5], keypoints[0][11], keypoints[0][13])
                print("Body: ", Body_angle)
                if angle > 160:
                    if not is_down and transition:
                        transition = False
                        is_down = True
                        if form:
                            count += 1
                            print("count: ", count)
                elif 123 < angle < 160:
                    if not transition:
                        transition = True
                elif angle < 123:
                    if is_down and transition:
                        transition = False
                        is_down = False

        return count, form


