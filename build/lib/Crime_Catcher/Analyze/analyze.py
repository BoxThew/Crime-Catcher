import cv2
import time
import json
import datetime
from pathlib import Path

from dotenv import load_dotenv
from eyepop import EyePopSdk
from eyepop.worker.worker_types import Pop, InferenceComponent
import os

load_dotenv()
BASE_DIR = Path(__file__).resolve().parents[3]
ASSETS_DIR = BASE_DIR / "evidence"

api_key = os.getenv("API_KEY")

objects_of_interest = "people, arms, and context"

questionList = [
   "Is there more than one person visible in the frame? (Yes/No)",
   "Is a human hand formed into a fist? (Yes/No)",
   "Is an arm extended in a punching motion? (Yes/No)",
   "Is a weapon visible? (Yes/No)",
   "Is someone lying on the ground? (Yes/No)"
]

#writes evidence to disk and appends to json file
def save_evidence(orig_img, status, detail, conf_score):

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    img_filename = f"evidence{timestamp}.jpg"

    cv2.imwrite(img_filename, orig_img)
    log_entry = {
       "timestamp": datetime.datetime.now().isoformat(),
       "event_type": status,
       "description": detail,
       "confidence_score": conf_score,
       "evidence_file": img_filename
   }

    json_file = ASSETS_DIR / "incident_log.json"
    data = []

    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []


    data.append(log_entry)

    with open(json_file, "w") as file:
        json.dump(data, file, indent = 4)


        print(f"\nIncident log saved: {json_file}")




def analyze_img(img_path):

   print(f"\Processing Image: {img_path}")
  
   #loads image
   frame = cv2.imread(img_path)
   if frame is None:
       print("Error: Could not find image file.")
       return


   #makes image480p for optimization
   height, width = frame.shape[:2]
   aspect_ratio = float(width) / float(height)
   new_width = 480
   new_height = int(new_width / aspect_ratio)
   small_frame = cv2.resize(frame, (new_width, new_height))
  
   temp_filename = "temp_upload.jpg"
   cv2.imwrite(temp_filename, small_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])


   #prompt for analysus
   prompt_text = (
       f"SECURITY ANALYSIS. Analyze {objects_of_interest}. "
       f"Step 1: Count the people. If there is only ONE person and NO WEAPON, it is SAFE (Shadow Boxing/Exercise). "
       f"Step 2: If there are TWO+ people and a fist/punch, it is a THREAT. "
       f"Determine: {' '.join(questionList)}. Report values as classLabels."
   )


   try:
      
       with EyePopSdk.workerEndpoint(api_key=api_key) as endpoint:
           endpoint.set_pop(
               Pop(components=[
                   InferenceComponent(
                       id=1,
                       ability='eyepop.image-contents:latest',
                       params={"prompts": [{"prompt": prompt_text}]}
                   )
               ])
           )
          
           try:
               result = endpoint.upload(temp_filename).predict()
           except Exception as e:
               # retry
               if "503" in str(e):
                   time.sleep(1.0)
                   result = endpoint.upload(temp_filename).predict()
               else:
                   raise e


           # Parsing
           multiple_people = False
           fist_visible = False
           punching = False
           weapon = False
           person_down = False
           threat_score = 0


           if 'classes' in result:
               for item in result['classes']:
                   cat = item['category'].lower()
                   ans = item['classLabel'].lower()
                   combined_text = f"{cat} {ans}"
                  
                   print(f"AI SAW: {combined_text}")


                   #Negative Check
                   ans_words = ans.split()
                   is_negative = "no" in ans_words or "none" in ans_words


                   if ("more than one" in combined_text or "multiple" in combined_text) and not is_negative:
                       multiple_people = True
                   if "fist" in combined_text and not is_negative:
                       fist_visible = True
                       threat_score += 1
                   if ("punching" in combined_text or "extended" in combined_text) and not is_negative:
                       punching = True
                       threat_score += 1
                   if "weapon" in combined_text and not is_negative:
                       weapon = True
                       threat_score += 5
                   if ("ground" in combined_text or "lying" in combined_text) and not is_negative:
                       person_down = True
                       threat_score += 2


           # Desicion
           status = "UNKNOWN"
           detail = ""
           conf_score = 0


           # Confidence
           if threat_score >= 2: conf_score = 98
           elif threat_score == 1: conf_score = 75
           else: conf_score = 99


           #weapon
           if weapon:
               status = "WEAPON DETECTED"
               detail = "Lethal threat identified"
          
           #single person
           elif not multiple_people:
               if person_down:
                   status = "PERSON DOWN"
                   detail = "Subject on floor (Medical)"
               else:
                   status = "SECURE"
                   detail = "Solo Subject (Safe)"


           #if more than one person
           else:
               if punching:
                   status = "THREAT DETECTED"
                   detail = "Active Fighting Detected"
               elif fist_visible:
                   status = "SUSPICIOUS"
                   detail = "Aggressive Stance"
               elif person_down:
                   status = "PERSON DOWN"
                   detail = "Subject on floor"
               else:
                   status = "SECURE"
                   detail = "Group Interaction (Safe)"


           print(f"RESULT: {status} ({detail})")


           # saves evidence if not secure
           if status != "SECURE":
               save_evidence(frame, status, detail, conf_score)


           return status


   except Exception as e:
       print(f"ERROR: {e}")
       return "ERROR"