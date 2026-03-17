Service Inventory: uiw-sentinel-agent
This document lists the Google Cloud Platform (GCP) services enabled for the Sentinel Agent project. Per the project requirements, we have identified the core IaaS components that underpin our PaaS/SaaS choices.

1. Core Infrastructure (IaaS)
While we utilize serverless tools, the following IaaS components are the foundation of our environment:

Compute Engine API (compute.googleapis.com): Provides the raw virtual machine resources used by Cloud Build and Cloud Run.

Virtual Private Cloud (VPC) & Networking: Managed via servicemanagement.googleapis.com and serviceusage.googleapis.com to ensure secure internal communication.

Cloud Storage (storage.googleapis.com): Provides object storage for project artifacts and long-term data persistence.

2. Serverless & Automation (PaaS)
Cloud Run (run.googleapis.com): Our primary compute platform for the AI agent logic.

Cloud Build (cloudbuild.googleapis.com): Handles the automated CI/CD pipeline from GitHub to GCP.

Artifact Registry (artifactregistry.googleapis.com): Stores the container images for our serverless deployments.

3. Data & AI Services
Cloud Natural Language API (language.googleapis.com): The "Brain" of the Sentinel Agent, used for sentiment analysis.

Cloud Firestore (firestore.googleapis.com): Our NoSQL database for storing agent findings and logs.

BigQuery (bigquery.googleapis.com): Enabled for large-scale data analysis and future reporting.

Pub/Sub (pubsub.googleapis.com): Facilitates loosely coupled communication between services.

4. Security & Identity
IAM API (iam.googleapis.com): Manages project permissions and the sentinel-bot identity.

Secret Manager (secretmanager.googleapis.com): Stores sensitive configuration data securely.

Workload Identity Federation: Enables the secure OIDC "Handshake" with GitHub Actions.

5. Observability (Operations Suite)
Cloud Logging (logging.googleapis.com): Centralized log management for auditing bot actions.

Cloud Monitoring (monitoring.googleapis.com): Performance tracking and health checks.
