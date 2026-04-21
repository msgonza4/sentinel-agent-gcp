from google.cloud import firestore

def save_threat_analysis():
    project_id = "uiw-sentinel-agent"
    collection_name = "agent-findings"
    
    print(f"Initializing Firestore Client for project: {project_id}")
    try:
        db = firestore.Client(project=project_id, database="default")
        
        data = [
            {
                "id": "sample_1",
                "threat_score": 0.9,
                "threat_vectors": ["Urgency Markers", "Account Suspension Threat", "QR Code"],
                "mitigation_recommendation": "Do not scan QR code, report to IT"
            },
            {
                "id": "sample_2",
                "threat_score": 1.0,
                "threat_vectors": ["Executive Impersonation", "Gift Card Scam"],
                "mitigation_recommendation": "Do not purchase gift cards, verify with sender"
            },
            {
                "id": "sample_3",
                "threat_score": 0.0,
                "threat_vectors": [],
                "mitigation_recommendation": "Safe email, no action needed"
            }
        ]
        {
        "id": "sample_4",
        "type": "phishing",
        "subject": "Your PayPal Account Has Been Compromised",
        "body": "Your PayPal account has been compromised. Click here immediately to verify your identity or your account will be permanently suspended within 24 hours."
    },
    {
        "id": "sample_5",
        "type": "safe",
        "subject": "Team Lunch Tomorrow",
        "body": "Hey team, don't forget we have a lunch meeting tomorrow at noon in the conference room. See you all there!"
    }
        
        for item in data:
            doc_id = item.pop("id")
            db.collection(collection_name).document(doc_id).set(item)
            print(f"Successfully saved {doc_id} to {collection_name}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    save_threat_analysis()
