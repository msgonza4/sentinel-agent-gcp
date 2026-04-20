import json
import datetime
from google.cloud import firestore

PROJECT_ID = "uiw-sentinel-agent"

# Initialize Firestore
db = firestore.Client(project=PROJECT_ID)

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

def analyze_and_save(sample):
    print(f"\nAnalyzing {sample['id']} ({sample['type']})...")

    import subprocess
    result = subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True, text=True
    )
    token = result.stdout.strip()

    import urllib.request
    url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/us-central1/publishers/google/models/gemini-2.5-flash-preview-09-2025:generateContent"

    payload = json.dumps({
        "contents": [{
            "role": "user",
            "parts": [{"text": f"{SYSTEM_PROMPT}\n\nAnalyze this email:\nSubject: {sample['subject']}\nBody: {sample['body']}"}]
        }]
    }).encode('utf-8')

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )

    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        raw = data['candidates'][0]['content']['parts'][0]['text'].strip()

    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    result_data = json.loads(raw.strip())

    doc_ref = db.collection("agent-findings").document(sample['id'])
    doc_ref.set({
        "sample_id": sample['id'],
        "type": sample['type'],
        "subject": sample['subject'],
        "threat_score": result_data["threat_score"],
        "threat_vectors": result_data["threat_vectors"],
        "mitigation_recommendation": result_data["mitigation_recommendation"],
        "timestamp": datetime.datetime.utcnow()
    })

    print(f"Saved! Threat Score: {result_data['threat_score']}")

if __name__ == "__main__":
    print("UIW Sentinel Agent - Running Analysis...")
    for sample in email_samples:
        analyze_and_save(sample)
    print("\nAll samples analyzed and saved!")
