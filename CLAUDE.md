# CLAUDE.md

## Project Identity
This repository is a reusable template for projects focused on:
- Google Cloud solutions
- Data engineering
- RAG / agentic systems
- Dynamic web applications
- Data governance with Dataplex and Purview
- Secure CI/CD

## Operating Principles
- Be practical, structured, and delivery-oriented.
- Prefer small, safe, reversible changes.
- Explain trade-offs when more than one valid solution exists.
- Keep technical internal instructions in English.
- Keep business-facing deliverables in Spanish unless explicitly requested otherwise.

## Approved Languages
- Python
- SQL
- TypeScript
- JavaScript
- Bash
- YAML
- Terraform
- Dockerfile
- Markdown
- Mermaid
- HTML
- CSS

## Preferred Stack
### Google Cloud
- BigQuery
- Cloud Storage
- Cloud Run
- Pub/Sub
- Secret Manager
- Artifact Registry
- Cloud Build
- Workflows
- Vertex AI
- IAM
- VPC

### Engineering
- FastAPI for Python APIs
- React / Next.js for front-end applications
- Dataform for BigQuery-first transformation workflows
- Terraform for infrastructure
- GitHub Actions for repository CI
- Cloud Build for GCP-native build/deploy
- Docker for service packaging

## Git Workflow
Use lightweight gitflow:
- main = stable
- develop = integration
- feature/* = new work
- fix/* = bug fixes
- hotfix/* = urgent fixes

Never push directly to main.

## Security Guardrails
- Never deploy to production without explicit approval.
- Never run terraform apply without explicit approval.
- Never delete cloud resources without explicit approval.
- Never commit real secrets.
- Never store credentials in files.
- Always use Secret Manager for runtime secrets when possible.
- Always verify target environment before any deployment or infra action.
- Treat IAM, networking, Terraform, Docker, Cloud Build, and GitHub workflow files as high-risk.

## Autonomy Rules
Claude may:
- propose solutions
- edit and create files
- prepare pull requests
- run local quality checks with approval
- execute shell commands with approval
- build or run containers when needed
- deploy to dev with approval

Claude must ask before:
- running tests
- running shell commands
- deploying anywhere
- touching infrastructure
- changing workflows or security-sensitive files

Claude must not do without approval:
- production deployment
- terraform apply
- deleting cloud resources
- writing secrets
- direct push to main

## Quality Gates
Before suggesting merge-ready work, ensure:
- format
- lint
- type checks where applicable
- unit tests
- dependency and security scan
- IaC scan when Terraform or Docker exists
- docs updated if behavior changes
- ADR written if architecture changes

## Standard Deliverables
Keep these updated whenever relevant:
- README.md
- docs/architecture/system-overview.md
- docs/diagrams/architecture.mmd
- docs/delivery/backlog.md
- docs/delivery/handoff.md
- docs/delivery/qa-checklist.md
- docs/runbooks/local-development.md
- docs/runbooks/deployment.md
- .env.example

## Domain Guidance
### Data Engineering
- Document source, grain, transformations, and business rules.
- Prefer simple layered architecture.
- Prefer BigQuery-native patterns when suitable.
- Use Dataform unless complexity clearly requires something else.

### RAG / Agentic Systems
- Separate ingestion, retrieval, prompting, tools, and orchestration.
- Keep evaluation explicit.
- Document grounding strategy and limitations.
- Prefer MVP-first architecture.

### Web Applications
- Prefer secure containerized deployment.
- Separate frontend and backend responsibilities.
- Always document local development and deployment.

### Governance
- Support glossary, lineage, ownership, classification, and data quality artifacts.
- Use Dataplex for GCP-oriented governance.
- Use Purview references for Microsoft-centric governance scenarios.

## Documentation Rules
- Technical docs: concise, precise, implementation-ready.
- Business docs: clear, structured, executive-friendly.
- Diagrams must be simple and readable.
- Prefer Mermaid for architecture and flow diagrams.

## High-Risk Paths
- infra/
- .github/workflows/
- cloudbuild/
- Dockerfile
- .claude/
- .vscode/

## Working Pattern
For any medium or large task:
1. Plan
2. Implement smallest safe increment
3. Validate
4. Document
5. Summarize status and next step