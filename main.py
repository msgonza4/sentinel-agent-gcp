import datetime
from google.cloud import firestore


def get_threat_level(score):
    if score >= 0.9:
        return "CRITICAL"
    elif score >= 0.7:
        return "HIGH"
    elif score >= 0.4:
        return "MODERATE"
    else:
        return "LOW"


def generate_doc_id(suffix):
    now = datetime.datetime.utcnow()
    return f"threat_{now.strftime('%Y%m%d_%H%M%S')}_{suffix}"


def save_threat_analysis():
    project_id = "uiw-sentinel-agent"
    collection_name = "agent-findings"

    print(f"Initializing Firestore Client for project: {project_id}")
    try:
        db = firestore.Client(project=project_id, database="default")

        data = [
            {
                "email_text": "URGENT: Your UIW student account will be suspended in 24 hours. Scan the QR code below to verify your identity immediately.",
                "threat_score": 0.9,
                "threat_vectors": ["Urgency Markers", "Account Suspension Threat", "QR Code"],
                "mitigation_recommendation": "Do not scan QR code. Report to UIW IT security immediately.",
                "category": "Phishing",
            },
            {
                "email_text": "Hi, this is the CEO. I need you to urgently purchase 5 x $200 Apple gift cards and send me the redemption codes. Keep this confidential.",
                "threat_score": 1.0,
                "threat_vectors": ["Executive Impersonation", "Gift Card Scam", "Urgency Markers", "Confidentiality Request"],
                "mitigation_recommendation": "Do not purchase gift cards. Verify request directly with the CEO via phone.",
                "category": "Business Email Compromise",
            },
            {
                "email_text": "Hi Terrell, just a reminder that our team meeting is scheduled for Thursday at 2pm in conference room B. Please bring your laptop. See you then, Dr. Parra",
                "threat_score": 0.0,
                "threat_vectors": [],
                "mitigation_recommendation": "No action needed. This email appears legitimate.",
                "category": "Legitimate",
            },
        ]

        for i, item in enumerate(data):
            threat_score = item["threat_score"]
            doc_id = generate_doc_id(str(i + 1))

            doc = {
                "email_text": item["email_text"],
                "threat_score": threat_score,
                "threat_level": get_threat_level(threat_score),
                "threat_vectors": item["threat_vectors"],
                "mitigation_recommendation": item["mitigation_recommendation"],
                "category": item["category"],
                "analyzed_by": "UIW-Sentinel-Alpha",
                "status": "flagged" if threat_score >= 0.4 else "clean",
                "timestamp": datetime.datetime.utcnow(),
            }

            db.collection(collection_name).document(doc_id).set(doc)
            print(f"Successfully saved {doc_id} | category: {doc['category']} | threat_level: {doc['threat_level']}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    save_threat_analysis()
