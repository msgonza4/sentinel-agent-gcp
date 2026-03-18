      Service Inventory: uiw-sentinel-agent
This document lists the Google Cloud Platform (GCP) services enabled for the Sentinel Agent project. Per the CIS 4355 requirements, we have identified the core IaaS components that underpin our PaaS/SaaS choices.


      1. Core Infrastructure (IaaS)
While we utilize serverless tools, these components form the physical foundation of our environment:

Compute Engine API (compute.googleapis.com): Provides the underlying virtual machine resources for our AI agent and container execution.

VPC & Networking: Managed via servicemanagement and serviceusage to ensure secure, isolated communication for the sentinel.

Cloud Storage (storage.googleapis.com): Provides object storage for project artifacts and long-term data persistence.


      2. Serverless & Automation (PaaS)
Cloud Run (run.googleapis.com): Hosts the backend logic for our autonomous agent.

Cloud Build (cloudbuild.googleapis.com): Orchestrates the CI/CD pipeline from GitHub to GCP.

Artifact Registry (artifactregistry.googleapis.com): Stores secure container images for deployment.


      3. Advanced AI & Agentic Services (Updated)
Vertex AI Platform (aiplatform.googleapis.com): The primary environment for our Agentic Framework and Spec-Driven Development.

Vertex AI Agent Builder: Used to construct the autonomous "Sentinel" without manual scripting, per professor guidance.

Cloud Opus 4.6 / Gemini 1.5 Pro: The high-reasoning LLMs used as the "Brain" of the agent for complex threat detection.

Cloud Firestore (firestore.googleapis.com): Our NoSQL database for storing agent findings and real-time logs.

Pub/Sub (pubsub.googleapis.com): Facilitates loosely coupled communication between the AI agent and other system components.


      4. Security & Identity
Workload Identity Federation: Enables the secure OIDC "Handshake" with GitHub Actions, removing the need for static JSON keys.

IAM API (iam.googleapis.com): Manages the "Least Privilege" permissions for the sentinel-bot service account.

Secret Manager (secretmanager.googleapis.com): Securely stores sensitive configuration data.
      

      5. Observability & Compliance
Cloud Logging: Audits all actions taken by the agent to ensure transparency.

Cloud Monitoring: Tracks performance and ensures the agent is running within defined parameters.
