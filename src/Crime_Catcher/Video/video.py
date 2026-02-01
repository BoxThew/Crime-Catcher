import cv2


class ThreatDetection:

    def __init__(self):

        pass

    def person_down_detection(self):

        pass

    def weapon_detection(self):
        pass

    def fighting_detection(self):

        pass


class Camera:

    def __init__(self):
        self.threat_detect = ThreatDetection()

        self.cap = cv2.VideoCapture(0)
        if not self.cam_opened():
            raise RuntimeError("Could not open camera.")


    def cam_opened(self) -> bool:
        return self.cap.isOpened()
    


    def person_detected(self) -> bool:
        #FIXME
        return True



    def active_cam(self):
        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("Failed to grab frame")
                break

            cv2.imshow("Security Cam", frame)


            #skips heavy worj if person not detected
            if not self.person_detected():
                continue

            #add threat detection stuff here



            #exit checkers
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if cv2.getWindowProperty("Security Cam", cv2.WND_PROP_VISIBLE)< 1:
                break

        self.cleanup()

    
    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()



