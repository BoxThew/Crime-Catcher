# Crime Catcher

**Transforming passive surveillance into active protection.**

Crime Catcher is an intelligent video surveillance platform designed to detect crimes, suspicious activities, and life-threatening events in real-time. Moving beyond simple recording, this system understands and analyzes video feeds to identify critical situations such as fights, weapons, fainting, or choking and instantly notifies security personnel.

By combining local real-time analysis with advanced cloud-based verification, Crime Catcher ensures that security teams are alerted only when it matters most, providing them with time-stamped incident reports and video evidence to act swiftly.

---

## Demo

![Dashboard Overview](images/frontend-1.png)
<br>
_*Real-time admin dashboard displaying active feeds and recent alerts.*_

![Eyepop Detection](images/frontend-2.png) 
<br>
_*Crime Assessment using EyePop.ai*_

![Alert](images/email-log.png)
<br>
_*Detailed incident report with snapshots.*_

---

## Key Features

* **Real-Time Threat Detection:** Instantly identifies criminal activities (e.g., fighting, vandalism) and dangerous objects using computer vision.
* **Health & Safety Monitoring:** Capable of detecting medical emergencies such as fainting or choking, ensuring immediate assistance.
* **Dual-Layer Verification:** Uses OpenCV for preliminary real-time screening and **Eyepop.AI** for deep, accurate verification to minimize false alarms.
* **Instant Mobile Alerts:** Sends immediate phone notifications to security personnel when a threat is confirmed.
* **Automated Incident Reporting:** Generates comprehensive reports with time-stamped snapshots and video evidence.
* **Centralized Admin Panel:** A user-friendly React dashboard for monitoring live logs, reviewing past incidents, and managing system status.

---

## How It Works

1.  **Input & Analysis:** The system connects to CCTV or webcam feeds. **OpenCV** processes the video in real-time to detect initial signs of suspicious activity or distress.
2.  **Verification:** Once a potential incident is flagged, snapshots are sent to a custom-trained model on **Eyepop.AI**.
3.  **Assessment:** Eyepop.AI analyzes the visual data to verify the threat and generates a detailed assessment report.
4.  **Alerting:** If the threat is confirmed, the backend triggers an immediate phone alert to the designated security team.
5.  **Logging:** The incident is logged in the **React** admin panel, where administrators can view the footage, read the AI-generated report, and archive the evidence.

---

## Tech Stack

* **Frontend:**
    * ⚛️ **React** (Admin Dashboard)
* **Backend & AI:**
    * 🐍 **Python** (Core Logic)
    * 👁️ **OpenCV** (Real-time Computer Vision)
    * 🧠 **Eyepop.AI** (Advanced Image Analysis & Verification)
    * 🚀 **YOLOv8** (Object Detection Model)
* **Infrastructure:**
    * 📂 **Local Storage/Database** (Evidence logging)

---

##  Future Applications

* **Emergency Service Integration:** Automatically dispatch GPS coordinates to police or EMS upon detecting life-threatening events.
* **Multi-Camera Tracking:** Re-identify and track suspects across different camera feeds in a large facility.
* **Audio Analysis:** Incorporate sound detection (e.g., screaming, breaking glass) to corroborate visual data.

---

## Acknowledgements

— Built during SanD Hacks 2026 as a better surveillance system prototype.
<br>
— Inspired by the increasing incidents of criminal activities throughout the world and the need to turn existing passive security systems into intelligent security guardians. 

---


