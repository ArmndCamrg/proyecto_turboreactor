# Repo Standards

## Purpose
Define consistent repository behavior.

## Rules
- Prefer simple folder structure.
- Keep scripts under scripts/.
- Keep docs under docs/.
- Keep infra under infra/terraform.
- Keep architecture decisions in docs/architecture/decisions/.
- Keep business-facing output in Spanish when appropriate.
- Prefer explicit naming over clever naming.

## Naming
- files: kebab-case when possible
- Python modules: snake_case
- Terraform resources: descriptive and environment-aware
- BigQuery datasets: domain_layer convention

## Minimum documentation
- README
- architecture overview
- handoff
- QA checklist
- runbook