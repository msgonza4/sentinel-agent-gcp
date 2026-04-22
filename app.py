import os
import json
import re
import datetime
from flask import Flask, request, jsonify
from google.cloud import firestore
import vertexai
from vertexai.generative_models import GenerativeModel

app = Flask(__name__)

# --- Config ---
PROJECT_ID = "uiw-sentinel-agent"
LOCATION = "us-central1"
MODEL_ID = "gemini-2.0-flash-001"

# --- Init ---
vertexai.init(project=PROJECT_ID, location=LOCATION)
db = firestore.Client(project=PROJECT_ID, database="default")
model = GenerativeModel(MODEL_ID)

SYSTEM_PROMPT = """You are UIW-Sentinel-Alpha, a cybersecurity threat analysis agent.
Analyze the provided email text for phishing indicators and threats.

Respond ONLY with a valid JSON object in this exact format (no markdown, no extra text):
{
  "threat_score": <float between 0.0 and 1.0>,
  "threat_vectors": [<list of identified threat indicators as strings>],
  "mitigation_recommendation": "<clear action the recipient should take>",
  "category": "<one of: Phishing, Spear Phishing, Business Email Compromise, Malware, Spam, Legitimate>"
}

Threat score guide:
- 0.0 - 0.3: Low risk / likely legitimate
- 0.4 - 0.6: Moderate risk / suspicious
- 0.7 - 0.9: High risk / likely phishing
- 1.0: Critical / confirmed phishing attempt
"""


def get_threat_level(score):
    if score >= 0.9:
        return "CRITICAL"
    elif score >= 0.7:
        return "HIGH"
    elif score >= 0.4:
        return "MODERATE"
    else:
        return "LOW"


def generate_doc_id():
    now = datetime.datetime.utcnow()
    return f"threat_{now.strftime('%Y%m%d_%H%M%S')}"


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    # --- PATH 1: Raw email text → Gemini analyzes it ---
    if "email_text" in data:
        raw_email = data["email_text"]

        try:
            prompt = f"{SYSTEM_PROMPT}\n\nEmail to analyze:\n\n{raw_email}"
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            response_text = re.sub(r"^```json\s*", "", response_text)
            response_text = re.sub(r"\s*```$", "", response_text)
            analysis = json.loads(response_text)

        except json.JSONDecodeError as e:
            return jsonify({
                "error": "Gemini returned invalid JSON",
                "raw_response": response_text,
                "details": str(e)
            }), 500
        except Exception as e:
            return jsonify({"error": f"Gemini call failed: {str(e)}"}), 500

        threat_score = analysis.get("threat_score", 0.0)
        threat_level = get_threat_level(threat_score)
        doc_id = generate_doc_id()

        finding = {
            "email_text": raw_email,
            "threat_score": threat_score,
            "threat_level": threat_level,
            "threat_vectors": analysis.get("threat_vectors", []),
            "mitigation_recommendation": analysis.get("mitigation_recommendation", ""),
            "category": analysis.get("category", "Phishing"),
            "analyzed_by": "UIW-Sentinel-Alpha",
            "status": "flagged" if threat_score >= 0.4 else "clean",
            "timestamp": datetime.datetime.utcnow(),
        }

        doc_ref = db.collection("agent-findings").document(doc_id)
        doc_ref.set(finding)

        return jsonify({
            "status": "saved",
            "id": doc_id,
            "threat_score": threat_score,
            "threat_level": threat_level,
            "threat_vectors": finding["threat_vectors"],
            "mitigation_recommendation": finding["mitigation_recommendation"],
            "category": finding["category"],
        }), 200

    # --- PATH 2: Pre-scored JSON (original behavior) ---
    threat_score = data.get("threat_score", 0.0)
    doc_id = generate_doc_id()

    doc_ref = db.collection("agent-findings").document(doc_id)
    doc_ref.set({
        "subject": data.get("subject", "Unknown"),
        "threat_score": threat_score,
        "threat_level": get_threat_level(threat_score),
        "threat_vectors": data.get("threat_vectors", []),
        "mitigation_recommendation": data.get("mitigation_recommendation", ""),
        "category": data.get("category", "Phishing"),
        "analyzed_by": "UIW-Sentinel-Alpha",
        "status": "flagged" if threat_score >= 0.4 else "clean",
        "timestamp": datetime.datetime.utcnow(),
    })

    return jsonify({"status": "saved", "id": doc_id}), 200


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
