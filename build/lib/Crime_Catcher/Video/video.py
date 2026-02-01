import cv2
import mediapipe as mp
import time
from ultralytics import YOLO



#make demo video completely sideways for easy x and y coordinate changes
class ThreatDetection:

    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.yolo = YOLO("yolov8n.pt")
        self.PERSON_ID = 0

        self.pose = self.mp_pose.Pose(
            static_image_mode = False,
            model_complexity = 1,
            min_detection_confidence = 0.5,
            min_tracking_confidence = 0.5
        )

        self.prev_right_wrist_pxl = None
        self.prev_t = None

        self.prev_dist = None
        self.prev_dist_t = None


    def person_detected(self, frame) -> bool:
        #FIXME
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(rgb)


        #if exists, perso is detected
        return result.pose_landmarks is not None
    

    def get_ppl_center(self, frame):
        result = self.yolo.predict(frame, verbose=False)[0]

        people = []
        for box in result.boxes:
            cls_id = int(box.cls[0])
            if cls_id != self.PERSON_ID:
                continue

            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)
            people.append((int(x1), int(y1), int(x2), int(y2), cx, cy))

        return people

    def pick_target_center(self, wrist_pxl, people):
        if not people:
            return None

        wx, wy = wrist_pxl

        # sort people by distance from wrist
        def dist2(p):
            cx, cy = p[4], p[5]
            dx = wx - cx
            dy = wy - cy
            return dx*dx + dy*dy

        people_sorted = sorted(people, key=dist2)

        if len(people_sorted) < 2:
            return None

        # nearest person center as target
        return (people_sorted[0][4], people_sorted[1][5])



    def person_down_detection(self, frame) -> bool:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(rgb)

        #no one detected
        if result.pose_landmarks is None:
            return False
        
        lm = result.pose_landmarks.landmark

        left_shoulder_y = lm[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y
        right_shoulder_y = lm[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y
        left_hip_y = lm[self.mp_pose.PoseLandmark.LEFT_HIP].y
        right_hip_y = lm[self.mp_pose.PoseLandmark.RIGHT_HIP].y

        shoulder_y = (left_shoulder_y + right_shoulder_y) / 2.0
        hip_y = (left_hip_y + right_hip_y) / 2.0

        vert_gap = abs(hip_y - shoulder_y)


        #this gap determines if a person is down or not

        ans = vert_gap < .12
        
        return ans
        


    #will probably skip for now
    def weapon_detection(self):
        pass

    def get_cords(self, frame):
        h, w = frame.shape[:2]

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(rgb)


#if no one is detected
        if result.pose_landmarks is None:
            return None
        
        lm = result.pose_landmarks.landmark

        def to_pxl(landmark):
            return int(landmark.x * w), int(landmark.y * h)
        
        nose = lm[self.mp_pose.PoseLandmark.NOSE]
        left_wrist = lm[self.mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = lm[self.mp_pose.PoseLandmark.RIGHT_WRIST]

        return {
            "nose_norm": (nose.x, nose.y),
            "left_wrist_norm": (left_wrist.x, left_wrist.y),
            "right_wrist_norm": (right_wrist.x, right_wrist.y),
            "nose_px": to_pxl(nose),
            "left_wrist_pxl": to_pxl(left_wrist),
            "right_wrist_pxl": to_pxl(right_wrist),
        }


    def r_wrist_speed(self, frame) -> float:
        cords = self.get_cords(frame)

        #if person goes out of frame, we wanna reset cords
        if cords is None:
            self.prev_right_wrist_pxl = None
            self.prev_t = None
            return 0.0
        
        cur = cords["right_wrist_pxl"]
        now = time.time()

        if self.prev_right_wrist_pxl is None or self.prev_t is None:
            self.prev_right_wrist_pxl = cur
            self.prev_t = now
            return 0.0
        
        dx = cur[0] - self.prev_right_wrist_pxl[0]
        dy = cur[1] - self.prev_right_wrist_pxl[1]
        dt = now - self.prev_t


#updates for next call
        self.prev_right_wrist_pxl = cur
        self.prev_t = now

        if dt <= 0:
            return 0.0
        
        return ((dx * dx  + dy * dy) ** .5) / dt
    

    def mv_to_target(self, wrist_pxl, target_pxl, now_t) ->bool:

        dx = wrist_pxl[0] - target_pxl[0]
        dy = wrist_pxl[1] - target_pxl[1]
        dist = (dx * dx + dy * dy) ** .5

        if self.prev_dist is None or self.prev_dist_t is None:
            self.prev_dist = dist
            self.prev_dist_t = now_t

            return False
        
        dt = now_t - self.prev_dist_t
        prev = self.prev_dist

        self.prev_dist = dist
        self.prev_dist_t = now_t

        if dt <= 0:
            return False
        
        speed = (prev - dist) / dt

        MIN_SPEED = 150.0
        return speed > MIN_SPEED


    def fighting_detection(self, frame):

        cords = self.get_cords(frame)
        if cords is None:
            return False
        
        wrist = cords["right_wrist_pxl"]
    
        people = self.get_ppl_center(frame)
        target = self.pick_target_center(wrist, people)
        if target is None:
            return False
        
        wrist_sp = self.r_wrist_speed(frame)
        mv_fw = self.mv_to_target(wrist, target, time.time())

        MIN_SPEED = 250.0

        return wrist_sp > MIN_SPEED and mv_fw


class Camera:

    def __init__(self):
        self.threat_detect = ThreatDetection()

        self.cap = cv2.VideoCapture(0)
        if not self.cam_opened():
            raise RuntimeError("Could not open camera.")


    def cam_opened(self) -> bool:
        return self.cap.isOpened()
    


    def person_detected(self, frame) ->bool:
        return self.threat_detect.person_detected(frame)



    def active_cam(self):
        while True:
            print("hidwd")
            ret, frame = self.cap.read()

            if not ret:
                print("Failed to grab frame")
                break

            print("heh")
            cv2.imshow("Security Cam", frame)

            print("hi")

            #skips heavy worj if person not detected
            if not self.person_detected(frame):
                print("hi not")
                continue

            print("hi2")

            #add threat detection stuff here


            if self.threat_detect.person_down_detection(frame):

                print("person down?")


            if self.threat_detect.fighting_detection(frame):

                print("fighting detected?")


            #exit checkers
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if cv2.getWindowProperty("Security Cam", cv2.WND_PROP_VISIBLE)< 1:
                break

        self.cleanup()

    
    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()



