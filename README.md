UIW Sentinel Agent (GCP)

🛡️ Project Overview
The UIW Sentinel Agent is a cloud-native cybersecurity implementation designed to perform automated AI-driven sentiment analysis. This project demonstrates a "loosely coupled" architecture using Google Cloud Platform (GCP) and GitHub Actions, focusing on secure identity management and serverless scalability.

🚀 Phase 1: Infrastructure & Identity (Complete)
We have successfully established the foundational environment for the Sentinel Agent.



Key Technical Achievements:

Zero-Trust Authentication: Implemented Workload Identity Federation to establish a secure "Handshake" between GitHub and GCP. This eliminates the need for static JSON service account keys.

Automated CI/CD: Configured a GitHub Actions pipeline to handle automated deployments to the cloud.

Cloud Provisioning: Enabled 30+ Google Cloud APIs, including Cloud Run, Firestore, and the Natural Language AI API.

Service Account Management: Provisioned the sentinel-bot with "Least Privilege" permissions to manage cloud resources securely.



🏗️ The Architecture

Source Control: GitHub (msgonza4/sentinel-agent-gcp)

Cloud Provider: Google Cloud Platform (uiw-sentinel-agent)

Compute: Cloud Run (Serverless)

Database: Cloud Firestore (Native Mode)

AI Engine: Cloud Natural Language API

Security: IAM Workload Identity Federation



👥 The Team

Mia G. (msgonza4): Security & DevOps Lead (IAM, Identity Federation, GitHub Actions)

Terrel E. (telliottks44): Infrastructure & Cloud Architect (GCP Project Setup, API Management)



📅 Roadmap

[x] Phase 1: Infrastructure, IAM Handshake, and API Enablement (Done)

[ ] Phase 2: AI Logic & Python Agent Development

[ ] Phase 3: Deployment & Integration Testing

[ ] Phase 4: Final Documentation, Security Audit, and Project Presentation
