# TalentMatch AI

**AI-Powered Resume Screening & Candidate Matching System**

> ⚠️ **High-Risk AI System** — This system falls under EU AI Act Annex III, Category 4
> (Employment, workers management and access to self-employment). It is subject to
> conformity assessment, human oversight requirements, bias testing, and transparency
> obligations.

## Overview

TalentMatch AI automates the initial screening of job applications by matching
candidate resumes against job descriptions. It produces a compatibility score (0–100)
with an explanation of the key matching factors.

**This system is monitored by [Vigilens](https://github.com/vigilens/vigilens) for
continuous AI compliance across EU AI Act, NIST AI RMF, and SOC 2.**

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌───────────┐
│  Frontend    │────▶│  FastAPI      │────▶│  ML Model │
│  (Next.js)  │◀────│  Backend      │◀────│  (sklearn)│
└─────────────┘     └──────┬───────┘     └───────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ MLflow   │ │ Datadog  │ │ Vigilens │
        │ Tracking │ │ Monitor  │ │ Webhook  │
        └──────────┘ └──────────┘ └──────────┘
```

## Compliance Frameworks

| Framework | Coverage | Key Requirements |
|-----------|----------|-----------------|
| **EU AI Act** | High-Risk (Annex III, Cat. 4) | Conformity assessment, human oversight, bias testing, transparency, data governance |
| **NIST AI RMF** | All functions | Govern, Map, Measure, Manage — risk identification, fairness metrics, incident response |
| **SOC 2** | TSC applicable | Security (CC), Availability (A1), Processing Integrity (PI1), Confidentiality (C1) |

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

### Frontend

```bash
cd frontend
npm install
npm run dev   # → http://localhost:3001
```

### Train Model

```bash
cd backend
python -m app.ml.train
```

### Run Tests

```bash
cd backend
pytest tests/ -v
```

## Integrations with Vigilens

This system is designed to be monitored by Vigilens through all available integration channels:

- **GitHub** — Code repo monitoring (commits, PRs, code reviews)
- **GitLab** — ML pipeline repo (training code, model registry)
- **Jira** — Sprint board, bias-incident tickets, change management
- **Confluence** — Model cards, data governance policies, DPIA documentation
- **Datadog** — API monitoring, latency, error rates, model drift alerts
- **MLflow** — Training experiments, model versions, fairness metrics
- **Webhook** — CI/CD pipeline sends build + deploy events to Vigilens

## Project Structure

```
talentmatch-ai/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Settings & environment
│   │   ├── api/routes.py        # API endpoints
│   │   ├── models/screener.py   # ML model wrapper
│   │   ├── services/
│   │   │   ├── parser.py        # Resume text extraction
│   │   │   └── scorer.py        # Scoring + explanation logic
│   │   └── ml/
│   │       ├── train.py         # Training with MLflow
│   │       ├── evaluate.py      # Fairness evaluation
│   │       └── data/            # Sample training data
│   └── tests/
├── frontend/
│   └── src/app/                 # Next.js 14 App Router
├── docs/
│   ├── model_card.md            # Transparency (EU AI Act Art. 13)
│   ├── dpia.md                  # Data Protection Impact Assessment
│   ├── data_governance.md       # Data handling policies
│   ├── human_oversight.md       # Human-in-the-loop procedures
│   └── incident_response.md     # Bias incident response
├── monitoring/
│   └── datadog/monitors.yaml    # Datadog monitor definitions
└── .github/workflows/ci.yml     # CI + Vigilens webhook
```

## License

Proprietary — Internal Use Only
