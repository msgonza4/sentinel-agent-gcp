import json
import datetime
import os
from google.cloud import firestore
from google.auth import default
import urllib.request

# Initialize
PROJECT_ID = "uiw-sentinel-agent"
LOCATION = "us-east1"

# Get credentials
credentials, project = default()


# Initialize Firestore
db = firestore.Client(project=PROJECT_ID, credentials=credentials)

SYSTEM_PROMPT = """You are UIW-Sentinel-Alpha. Analyze text for social engineering threats.
Always respond ONLY in this exact JSON format with no extra text:
{
    "threat_score": 0.0,
    "threat_vectors": ["list of indicators"],
    "mitigation_recommendation": "security advice"
}"""

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

def call_gemini(text, credentials):
    url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/us-central1/publishers/google/models/gemini-1.0-pro:generateContent"
    
    payload = json.dumps({
        "contents": [{
            "role": "user",
            "parts": [{"text": f"{SYSTEM_PROMPT}\n\nAnalyze this:\n{text}"}]
        }]
    }).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json"
        }
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result['candidates'][0]['content']['parts'][0]['text']

def analyze_and_save(sample, credentials):
    print(f"\nAnalyzing {sample['id']} ({sample['type']})...")
    
    raw = call_gemini(sample['body'], credentials).strip()
    
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    
    result = json.loads(raw.strip())
    
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
    
    print(f"Saved! Threat Score: {result['threat_score']}")
    return result

if __name__ == "__main__":
    print("UIW Sentinel Agent - Running Analysis...")
    credentials, _ = default()
    
    for sample in email_samples:
        analyze_and_save(sample, credentials)
    print("\nAll samples analyzed and saved!")
