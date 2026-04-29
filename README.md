![Build Status](https://github.com/msgonza4/sentinel-agent-gcp/actions/workflows/deploy.yml/badge.svg)

🛡️ UIW Sentinel Agent (GCP)

Cloud-Native Agentic Threat Detection

The UIW Sentinel Agent is an autonomous cybersecurity system engineered to provide a digital safety net against sophisticated social engineering. By leveraging Gemini 2.5 Pro, the system moves beyond traditional filtering to Agentic Threat Analysis, providing real-time reasoning for every email analyzed. 

🏗️ Architecture & Technology Stack
The system is built on a "loosely coupled" architecture to ensure scalability and high availability:

Model: Gemini 2.5 Pro (Google’s most advanced reasoning engine). 

Compute: Google Cloud Run (Serverless API hosting).  

Database: Cloud Firestore (Real-time, structured threat repository).  CI/CD: GitHub Actions (Automated testing and deployment pipeline).

Security: IAM Workload Identity Federation for keyless, zero-trust authentication.  

👥 The Team

Mia Gonzalez (@msgonza4): Security & DevOps Lead. Responsible for the Zero-Trust security posture, IAM Identity Federation, system specifications, and documentation of the human element in cybersecurity.  

Terrell Elliott (@T-Elliott01): Infrastructure & Cloud Architect. Responsible for GCP API ecosystem setup, Cloud Run orchestration, and core Python/Flask API development.  

🚀 Project Phases

*Phase 1: Infrastructure & Identity (Complete)

We established a hardened environment following the principle of "Least Privilege": 

Zero-Trust Handshake: Implemented Workload Identity Federation between GitHub and GCP to eliminate the need for long-lived service account keys.

Cloud Provisioning: Enabled the Vertex AI Platform and Cloud Run ecosystems.  

Identity Hardening: Provisioned a dedicated service account (sentinel-bot) with minimal scoped permissions.

*Phase 2: Agentic Orchestration & Deployment (Complete)

Automated Pipeline: Configured GitHub Actions to build Docker containers and deploy to Cloud Run automatically upon every code push.  

Threat Scoring: Developed a 0.0 to 1.0 scoring system to categorize threats from "Clean" to "Critical".

Live API: Launched a 24/7 API endpoint that processes email submissions and returns structured JSON analysis.  

*Phase 3: Integration & Evaluation (Complete)

Real-World Testing: Validated the system against diverse scenarios, including Phishing, Business Email Compromise (BEC), and legitimate institutional communications.

Persistence: Ensured every finding is instantly saved to Firestore with full mitigation recommendations.  

📅 Roadmap

[x] Phase 1: Infrastructure & IAM Handshake

[x]Phase 2: Agentic Orchestration & Cloud Run Deployment

[x]Phase 3: Integration Testing & Threat Database Population
