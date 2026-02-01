
from Crime_Catcher.Report.report import Report


data = {"timestamp": "2026-02-01T00:00:10.207434",
       "event_type": "THREAT DETECTED",
       "description": "Active Fighting Detected",
       "confidence_score": 98,
       "evidence_file": "evidence_2026-02-01_00-00-10.jpg"}


o = Report()
o.send_email(data)