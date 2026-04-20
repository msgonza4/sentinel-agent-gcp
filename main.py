import json
import datetime
from google.cloud import firestore
import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize GCP
PROJECT_ID = "uiw-sentinel-agent"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)
db = firestore.Client(project=PROJECT_ID)

# Initialize Agent
model = GenerativeModel(
    model_name="gemini-2.5-pro-preview-05-06",
    system_instruction="""
    You are UIW-Sentinel-Alpha. Perform autonomous linguistic analysis 
    to identify External Threats via Social Engineering.
    
    Always respond ONLY in this exact JSON format with no extra text:
    {
        "threat_score": 0.0,
        "threat_vectors": ["list of specific indicators found"],
        "mitigation_recommendation": "specific security advice"
    }
    """
)

# Mia's test email samples
email_samples = [
    {
        "id": "sample_1",
        "type": "phishing",
        "subject": "Action Required: [Urgent] UIW Account Verification",
        "body": "Scan the QR Code below to verify securely via your mobile device. Failure to verify will result in a lockout."
    },
    {
        "id": "sample_2", 
        "type": "phishing",
        "subject": "Quick Request - Mia",
        "body": "Can you pick up 5 $100 Apple gift cards from the CVS on Broadway? I need the photos of the PINs."
    },
    {
        "id": "sample_3",
        "type": "safe",
        "subject": "WiCyS UIW: Reminder - General Meeting",
        "body": "Hi everyone! Meeting this Friday at 3:00 PM in the SEC building. See you there!"
    }
]

def analyze_and_save(sample):
    print(f"\nAnalyzing {sample['id']} ({sample['type']})...")
    
    # Send to agent
    response = model.generate_content(sample['body'])
    
    # Clean and parse response
    raw = response.text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    
    result = json.loads(raw.strip())
    
    # Save to Firestore
    doc_ref = db.collection("agent-findings").document(sample['id'])
    doc_ref.set({
        "sample_id": sample['id'],
        "type": sample['type'],
        "subject": sample['subject'],
        "threat_score": result["threat_score"],
        "threat_vectors": result["threat_vectors"],
        "mitigation_recommendation": result["mitigation_recommendation"],
        "timestamp": datetime.datetime.utcnow()
    })
    
    print(f"✅ Saved to Firestore!")
    print(f"   Threat Score: {result['threat_score']}")
    return result

if __name__ == "__main__":
    print("🛡️ UIW Sentinel Agent — Running Analysis...")
    for sample in email_samples:
        analyze_and_save(sample)
    print("\n✅ All samples analyzed and saved to Firestore!")
