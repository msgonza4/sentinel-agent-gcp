System Architecture: The Sentinel Agent
Project: Cloud Computing Spring 2026
Authors: Mia Gonzalez & Terrel Elliot

1. High-Level Flow Diagram
	This diagram illustrates our Loosely Coupled architecture. Each service communicates via API, ensuring that a failure in one component does not crash the entire system.

2. Component Breakdown (The Building Blocks)
	A. Source Control & Trigger (GitHub)
Role: The "Source of Truth."
Function: When a "Live-Fire" test sample is pushed to the repository, a webhook triggers the CI/CD pipeline. This removes the need for human interaction to start the analysis.

B. Orchestration (GitHub Actions)
Role: The Automation Engine.
Function: It builds the container image and deploys it to Google Cloud. This fulfills the CI/CD requirement for modern cloud architecture.

C. Compute Layer (Google Cloud Run)
Role: The "Agent" Brain (Serverless).
Function: We chose Cloud Run because it is Stateless. It wakes up only when a request is received, analyzes the data, and shuts down, keeping our project within the Free Tier.

D. Intelligence Layer (Vertex AI / Natural Language API)
Role: Shared Services / AI Reasoning.
Function: The Agent sends raw text to this API. The API returns a Sentiment Score ($\text{Score} \in [-1, 1]$) and identifies key entities (like "Gift Cards" or "QR Codes").

E. Storage Layer (Firestore)
Role: NoSQL Database (Block/Object Hybrid).
Function: We utilize the Vertex-to-Firestore flow. The Agent acts as a bridge; it only writes to the database after the AI has validated the threat level. This ensures the database remains clean of "junk" data.


3. Architecture Principles Applied
	Loosely Coupled: If the Firestore database is undergoing maintenance, the Cloud Run agent can still receive and process data from GitHub, caching results or logging errors without crashing the front-end.
Observability: Every step in this flow generates a log entry in Google Cloud Logging, allowing us to trace a "Live-Fire" sample from the moment it leaves GitHub until it hits the database.
