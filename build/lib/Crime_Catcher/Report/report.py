import smtplib
from dotenv import load_dotenv
import os
import json
import cv2
from email.message import EmailMessage
from pathlib import Path

load_dotenv()
BASE_DIR = Path(__file__).resolve().parents[3]
ASSETS_DIR = BASE_DIR / "evidence"

class Report:
    def __init__(self):
        self.email = os.getenv("EMAIL_ADDRESS")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.recipient = os.getenv("RECIPIENT_EMAIL")

        self.subject: str = "Crime Catcher Alert!"

    def send_email(self, data):
        #dont forget tp add image in parameters^^^
        
        
        #have date, time, image, event, confidence in email
    

    #make try catch block more descriptive if have time
        try:
            timestamp = data["timestamp"]
            event = data["event_type"]
            desc = data["description"]
            confidence_lvl = data["confidence_score"]
            img_path = ASSETS_DIR / data["evidence_file"]

            msg = EmailMessage()
            msg["From"] = self.email
            msg["To"] = self.recipient
            msg["Subject"] = self.subject


            with open(img_path, "rb") as img:
                img_bytes = img.read()

            msg.set_content(
                f"Event: {event}\n"
                f"Description: {desc}\n"
                f"Time: {timestamp}\n"
                f"Confidence: {confidence_lvl}\n"
            )
            msg.add_attachment(
                img_bytes,
                maintype = "image",
                subtype = "jpeg",
                filename = data["evidence_file"]
            )

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()

            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()


        except Exception as e:
            print("Unable to report crime.", type(e).__name__, e)