import json
import datetime
from flask import Flask, request, jsonify
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client(project="uiw-sentinel-agent")

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    doc_ref = db.collection("agent-findings").document()
    doc_ref.set({
        "subject": data.get("subject", "Unknown"),
        "threat_score": data.get("threat_score", 0.0),
        "threat_vectors": data.get("threat_vectors", []),
        "mitigation_recommendation": data.get("mitigation_recommendation", ""),
        "timestamp": datetime.datetime.utcnow()
    })
    
    return jsonify({"status": "saved", "id": doc_ref.id}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
