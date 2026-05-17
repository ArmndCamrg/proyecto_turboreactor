# Cloud Run Skill

## Preferred pattern
- containerized service
- explicit port configuration
- health endpoint when possible
- non-root container where practical
- secrets via Secret Manager
- least-privilege service account
- region explicitly documented

## Deliverables
- Dockerfile
- deployment command or Cloud Build config
- environment variables reference
- runbook note