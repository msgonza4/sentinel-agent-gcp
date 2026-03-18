![Build Status](https://github.com/msgonza4/sentinel-agent-gcp/actions/workflows/deploy.yml/badge.svg)

UIW Sentinel Agent (GCP)


🛡️ Project Overview

The UIW Sentinel Agent is a cloud-native cybersecurity implementation designed for autonomous, agentic threat detection. This project demonstrates a "loosely coupled" architecture using Vertex AI and GitHub Actions, focusing on Spec-Driven Development to prevent model drift.


🚀 Phase 1: Infrastructure & Identity (Complete)


We have successfully established the foundational environment for the Sentinel Agent.

Zero-Trust Authentication: Implemented Workload Identity Federation for a keyless "Handshake" between GitHub and GCP.

Automated CI/CD: Configured GitHub Actions to handle secure, automated deployments.

Cloud Provisioning: Enabled 30+ Google Cloud APIs, including the Vertex AI Platform and Cloud Run.

Identity Hardening: Provisioned sentinel-bot with "Least Privilege" permissions.



🏗️ The Architecture


Source Control: GitHub (msgonza4/sentinel-agent-gcp)

Cloud Provider: Google Cloud Platform (uiw-sentinel-agent)

Compute: Cloud Run (Serverless)

Database: Cloud Firestore (Native Mode)

AI Orchestration: Vertex AI Agent Builder

Model: Cloud Opus 4.6 (Reasoning Engine)

Security: IAM Workload Identity Federation



👥 The Team


Mia G. (@msgonza4): Security & DevOps Lead (IAM, Identity Federation, System Specs)

Terrel E. (@telliottks44): Infrastructure & Cloud Architect (GCP Setup, API Ecosystem, Agent Builder)



📅 Roadmap


[x] Phase 1: Infrastructure, IAM Handshake, and Vertex AI Enablement (Done)

[ ] Phase 2: Agentic Orchestration & Spec-Driven Development

[ ] Phase 3: Integration Testing & Model Drift Evaluation

[ ] Phase 4: Final Security Audit and Project Presentationg

