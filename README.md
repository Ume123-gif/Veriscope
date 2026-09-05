# VERISCOPE

**An autonomous transaction verification and fraud intelligence platform.**

Veriscope ingests a transaction, runs it through a multi-model risk pipeline — a supervised classifier, an unsupervised anomaly detector, and a graph-based ring detector — combines the three into a single explainable risk score, and returns a deterministic **ALLOW / REVIEW / HOLD / BLOCK** decision with a SHAP-backed justification.

🔗 **Live demo:** [veriscope-gamma.vercel.app](https://veriscope-gamma.vercel.app)

🔗 **API:** [veriscope-pu8m.onrender.com](https://veriscope-pu8m.onrender.com) — try [`/health`](https://veriscope-pu8m.onrender.com/health) or [`/metrics`](https://veriscope-pu8m.onrender.com/metrics)

> The API runs on Render's free tier, which spins the service down after **15 minutes** of no incoming traffic. The first request after that idle window triggers a cold start — expect up to ~30–60s before it responds while the service (and its ML dependencies) boot back up.

---

## Table of Contents

- [Problem](#problem)
- [Solution](#solution)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [ML Pipeline](#ml-pipeline)
- [Graph Intelligence](#graph-intelligence)
- [Risk Agent](#risk-agent)
- [Decision Engine](#decision-engine)
- [Audit Trail](#audit-trail)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Running Locally](#running-locally)
- [Deployment](#deployment)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)

---

## Problem

Fraud rarely shows up as a single suspicious transaction — it appears as a **pattern**.

Examples include:

- An account transacting at unusually high velocity.
- A transaction amount that deviates significantly from an account's history.
- Multiple accounts sharing the same device, IP, or card fingerprint.
- Apparently normal transactions that are actually part of a coordinated fraud ring.

Point solutions that rely on a single classifier or static rules can miss fraud that exists across multiple signals.

---

## Solution

Veriscope evaluates every transaction through three independent risk signals:

1. **Supervised Risk** — XGBoost analyzes engineered behavioral and transaction features to predict fraud risk.
2. **Behavioral Anomaly** — Isolation Forest identifies transactions that deviate from normal behavioral patterns without relying directly on fraud labels.
3. **Network Risk** — NetworkX builds an account relationship graph using shared devices, IPs, and card fingerprints, while Louvain community detection identifies suspicious account communities.

A **Risk Agent** combines these signals into a composite risk score.

A deterministic **Decision Engine** then converts the score into:

```text
ALLOW / REVIEW / HOLD / BLOCK
```

Every decision is explained using **SHAP feature attributions** and persisted to **PostgreSQL** for auditability.

---

## Key Features

- **Multi-signal risk scoring** — combines supervised ML, behavioral anomaly detection, and graph intelligence.
- **XGBoost fraud detection** — primary supervised fraud classifier.
- **Behavioral anomaly detection** — detects unusual transaction behavior using Isolation Forest.
- **Fraud-ring detection** — identifies suspicious account communities using shared entities and Louvain community detection.
- **SHAP explainability** — shows the features that contributed most to the model's decision.
- **Deterministic decisioning** — converts the composite risk score into ALLOW / REVIEW / HOLD / BLOCK.
- **Risk Agent orchestration** — coordinates the complete transaction risk pipeline.
- **PostgreSQL persistence** — stores transaction, risk-analysis, and audit information.
- **Investigation History** — a dedicated tab that lists recent risk decisions pulled live from `/audit-trail`.
- **React investigation console** — allows analysts to search and investigate transactions through a dedicated dashboard.

---

## Live Deployment

| Component | Platform | URL |
|---|---|---|
| Frontend | Vercel | [veriscope-gamma.vercel.app](https://veriscope-gamma.vercel.app) |
| Backend API | Render (free tier) | [veriscope-pu8m.onrender.com](https://veriscope-pu8m.onrender.com) |
| Database | Neon (serverless Postgres, free tier) | — |

Search any `transaction_id` present in `Data/features.csv` in the live demo to see a full risk breakdown end-to-end, or switch to the **Investigation History** tab to see recently analyzed transactions pulled from the audit log.

---

## System Architecture

```mermaid
flowchart TD

    subgraph DATA["Offline Data Layer"]
        DG["data_generator.py<br/>Synthetic accounts / transactions / fraud rings"]
        RAW[("CSV Dataset")]
        FE["feature_engineering.py<br/>Velocity / deviation / sharing features"]
        FEATURES[("features.csv")]

        DG --> RAW
        RAW --> FE
        FE --> FEATURES
    end

    subgraph API["FastAPI Backend"]
        EP1["GET /health"]
        EP2["GET /metrics"]
        EP3["GET /audit-trail"]
        EP4["GET /transactions/{id}/risk"]

        AGENT["Risk Agent"]

        XGB["XGBoost"]
        ISO["Isolation Forest"]
        GRAPH["NetworkX + Louvain"]
        SHAP["SHAP"]

        SCORE["Composite Risk Score"]
        DECISION["Decision Engine"]

        EP4 --> AGENT

        AGENT --> XGB
        AGENT --> ISO
        AGENT --> GRAPH
        AGENT --> SHAP

        XGB --> SCORE
        ISO --> SCORE
        GRAPH --> SCORE

        SCORE --> DECISION
    end

    subgraph DB["Persistence Layer"]
        POSTGRES[("PostgreSQL")]
        TRANSACTIONS["Transactions"]
        ANALYSES["Risk Analyses"]
        AUDIT["Audit Logs"]

        POSTGRES --> TRANSACTIONS
        POSTGRES --> ANALYSES
        POSTGRES --> AUDIT
    end

    subgraph UI["React Investigation Console"]
        SEARCH["Transaction Search"]
        RESULTS["Risk Investigation"]
        HISTORY["Investigation History"]

        SEARCH --> RESULTS
        SEARCH --> EP4
        EP3 --> HISTORY
    end

    FEATURES --> XGB
    FEATURES --> ISO
    FEATURES --> GRAPH

    DECISION --> RESULTS
    DECISION --> ANALYSES
    DECISION --> AUDIT
    AUDIT --> EP3
```

---

## ML Pipeline

The models operate on engineered transaction and behavioral features including:

- Transaction velocity over recent time windows
- Amount deviation from account history
- Device-sharing behavior
- IP-sharing behavior
- Card-fingerprint sharing
- Account age
- Refund behavior
- Time-of-day characteristics

### Models

| Model | Role | Status |
|---|---|---|
| **XGBoost** | Primary supervised fraud classifier | Live |
| **Isolation Forest** | Behavioral anomaly detector | Live |
| **SHAP TreeExplainer** | Model explainability | Live |
| **Random Forest** | Baseline model comparison | Offline |

### XGBoost

The primary supervised model uses `XGBClassifier`.

Current configuration:

```text
n_estimators = 300
max_depth = 5
learning_rate = 0.05
```

The model provides the primary supervised fraud-risk signal. It is retrained in-memory on each request rather than loaded from a persisted artifact (see [Limitations](#limitations)).

### Isolation Forest

Isolation Forest provides an independent behavioral signal by identifying transactions that differ from the normal transaction population.

### SHAP

SHAP's `TreeExplainer` identifies the features that contribute most strongly to the XGBoost prediction.

The highest-impact features are returned as human-readable explanations in the investigation dashboard.

---

## Graph Intelligence

Graph analysis is implemented using **NetworkX** — not a graph neural network.

Each account is represented as a graph node.

Relationships are created when accounts share:

- Device identifiers
- IP addresses
- Card fingerprints

The resulting graph is partitioned using **Louvain community detection**.

Communities are evaluated using:

- Graph density
- Relative edge count
- Community size

The resulting `graph_ring_score` is assigned to accounts within suspicious communities and incorporated into the Risk Agent.

This allows Veriscope to detect coordinated fraud where individual transactions may appear relatively normal but their surrounding network reveals suspicious relationships.

The graph and its Louvain partition are recomputed from scratch on every risk lookup — there is no caching or incremental update.

---

## Risk Agent

`risk_agent.py` orchestrates the complete transaction analysis pipeline.

The composite risk score is:

```python
risk_score = (
    xgb_score * 0.50
    + anomaly_score * 0.20
    + graph_score * 0.30
)
```

### Risk Levels

| Risk Score | Risk Level |
|---:|---|
| ≥ 0.75 | **HIGH** |
| ≥ 0.50 | **MEDIUM** |
| < 0.50 | **LOW** |

---

## Decision Engine

`decision_engine.py` converts the composite risk score into a deterministic operational decision.

| Risk Score | Decision |
|---:|---|
| ≥ 0.85 | **BLOCK** |
| ≥ 0.70 | **HOLD** |
| ≥ 0.50 | **REVIEW** |
| < 0.50 | **ALLOW** |

The final decision is deterministic and auditable rather than being another black-box model.

---

## Audit Trail

Every call to `/transactions/{id}/risk` writes a `RiskAnalysis` row and an `AuditLog` row to PostgreSQL.

### Transactions

- Transaction ID
- Account ID
- Transaction amount
- Transaction timestamp

### Risk Analyses

- XGBoost score
- Behavioral anomaly score
- Graph score
- Composite risk score
- Risk level
- Decision
- Community ID
- SHAP explanations

### Audit Logs

- Transaction ID
- Action
- Decision
- Risk score
- Timestamp

`GET /audit-trail` returns the most recent `AuditLog` entries (default limit 20), and the React frontend's **Investigation History** tab (`AuditTrail.jsx`) fetches and renders this list live.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI |
| Language | Python |
| Supervised ML | XGBoost |
| Baseline ML | scikit-learn Random Forest |
| Anomaly Detection | Isolation Forest |
| Explainability | SHAP |
| Graph Intelligence | NetworkX |
| Community Detection | Louvain |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database Hosting | Neon |
| Data Generation | Faker, NumPy, pandas |
| Frontend | React 18 |
| Build Tool | Vite |
| Styling | Tailwind CSS |
| Icons | lucide-react |
| Hosting | Render (backend), Vercel (frontend) |

---

## Project Structure

```text
Veriscope/
│
├── veriscope_backend/
│   ├── api/
│   │   └── main.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   └── seed.py
│   │
│   ├── graph/
│   │   └── ring_detection.py
│   │
│   ├── ml/
│   │   ├── xgboost_model.py
│   │   ├── random_forest.py
│   │   ├── isolation_forest.py
│   │   └── explainability.py
│   │
│   ├── Data/
│   │   ├── accounts.csv
│   │   ├── transactions.csv
│   │   ├── features.csv
│   │   ├── fraud_rings.csv
│   │   └── ground_truth.csv
│   │
│   ├── data_generator.py
│   ├── feature_engineering.py
│   ├── risk_agent.py
│   ├── decision_engine.py
│   ├── requirements.txt
│   └── .env.example
│
└── veriscope_frontend/
    └── src/
        ├── components/
        │   ├── Navbar.jsx
        │   ├── SearchBar.jsx
        │   ├── DecisionBanner.jsx
        │   ├── RiskScores.jsx
        │   ├── ShapExplanation.jsx
        │   ├── NetworkIntelligence.jsx
        │   ├── AuditTrail.jsx
        │   ├── OverviewStats.jsx
        │   └── States.jsx
        ├── services/
        └── utils/
```

---

## Installation

### Backend

```bash
cd veriscope_backend
pip install -r requirements.txt
```

### Frontend

```bash
cd veriscope_frontend
npm install
```

---

## Environment Variables

### Backend

Create:

```text
veriscope_backend/.env
```

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require
```

The connection string can point to a local PostgreSQL instance or a hosted PostgreSQL provider such as Neon.

**Never commit `.env` to Git.**

A template is provided in `veriscope_backend/.env.example`.

### Frontend

Create:

```text
veriscope_frontend/.env
```

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

For production, replace this with the deployed FastAPI backend URL.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Service health check |
| `GET` | `/metrics` | Dataset-level platform metrics |
| `GET` | `/audit-trail` | Most recent risk decisions from the audit log (default limit 20) |
| `GET` | `/transactions/{transaction_id}/risk` | Full transaction risk analysis |

### `/health`

```http
GET /health
```

Example:

```json
{
  "status": "healthy",
  "service": "Veriscope"
}
```

### `/metrics`

Returns:

- Total transactions
- Fraud cases
- Fraud-ring cases
- Behavioral anomalies
- Normal transactions

### `/transactions/{transaction_id}/risk`

Runs the complete risk pipeline:

```text
XGBoost
   ↓
SHAP
   ↓
Isolation Forest
   ↓
Graph Intelligence
   ↓
Risk Agent
   ↓
Decision Engine
```

The endpoint returns the complete risk breakdown and persists the analysis. Unknown transaction IDs return `404 Not Found`.

### `/audit-trail`

Returns the most recent `AuditLog` rows written by risk analyses, ordered newest-first.

---

## Running Locally

To try Veriscope without any setup, use the [live demo](#live-deployment) instead. To run it on your own machine:

### 1. Generate synthetic data

```bash
cd veriscope_backend
python data_generator.py
```

### 2. Generate engineered features

```bash
python feature_engineering.py
```

### 3. Configure PostgreSQL

Set `DATABASE_URL` in `veriscope_backend/.env`.

### 4. Seed the database

```bash
python -m database.seed
```

### 5. Start the backend

Run from `veriscope_backend/` so the `database`, `ml`, and `graph` packages resolve correctly:

```bash
uvicorn api.main:app --reload
```

The API will run at `http://127.0.0.1:8000`.

### 6. Start the frontend

In another terminal:

```bash
cd veriscope_frontend
npm run dev
```

Open the Vite URL displayed in the terminal, search for a transaction ID from `Data/features.csv` to run an investigation, or switch to **Investigation History** to see recent decisions.

---

## Deployment

The production deployment architecture is:

```text
┌──────────────────────┐
│       Vercel          │
│   React Frontend      │
└──────────┬─────────────┘
           │
           ▼
┌──────────────────────┐
│       Render           │
│    FastAPI Backend     │
└──────────┬─────────────┘
           │
           ▼
┌──────────────────────┐
│        Neon             │
│     PostgreSQL          │
└──────────────────────┘
```

### Backend — Render

```text
Root Directory:  veriscope_backend
Build Command:   pip install -r requirements.txt
Start Command:   uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

Set:

```env
DATABASE_URL=<Neon PostgreSQL connection string>
```

### Frontend — Vercel

```text
Root Directory: veriscope_frontend
```

Set:

```env
VITE_API_BASE_URL=https://<your-render-backend>.onrender.com
```

The frontend then communicates with the deployed FastAPI backend.

---

## Limitations

- **No model persistence.** XGBoost and Isolation Forest are currently trained in-memory rather than loaded from persisted model artifacts.
- **Training and inference are not separated.** Models are retrained during risk analysis.
- **Graph recomputation.** The account graph and Louvain communities are recomputed for every risk lookup rather than being incrementally maintained.
- **Synthetic data.** The current dataset is generated using Faker and has not been evaluated against real payment-platform data.
- **Random Forest is offline.** It currently serves as a baseline comparison rather than part of the live Risk Agent.
- **No authentication.** The API does not currently implement authentication or role-based authorization.
- **No comprehensive automated testing or CI/CD pipeline.**
- **Static topology preview.** The frontend's network panel represents graph intelligence through a dashboard visualization rather than rendering the complete underlying NetworkX graph.
- **Free-tier hosting.** The Render backend spins down after 15 minutes of inactivity, causing a cold-start delay of roughly 30–60s on the first request afterward, and the Neon database is on a free/serverless tier — not sized for sustained production load.

---

## Future Improvements

- Persist trained models and separate training from inference.
- Add model versioning and monitoring.
- Cache or incrementally update graph communities.
- Introduce real-time transaction streaming.
- Add authentication, RBAC, and API rate limiting.
- Add automated unit, integration, and end-to-end tests.
- Add CI/CD with GitHub Actions.
- Add model drift monitoring.
- Render live account/entity graphs with actual nodes and edges.
- Integrate real or privacy-preserving transaction datasets.
- Add analyst feedback loops for continuous model improvement.

---

## Project Status

**End-to-end prototype completed and deployed.**

```text
Synthetic Data
      ↓
Feature Engineering
      ↓
XGBoost ─────────────┐
                      │
Isolation Forest ─────┼──→ Risk Agent
                      │
Graph Intelligence ───┘
      ↓
SHAP Explainability
      ↓
Composite Risk Score
      ↓
Decision Engine
      ↓
ALLOW / REVIEW / HOLD / BLOCK
      ↓
PostgreSQL Audit Trail
      ↓
React Investigation Console
```

Veriscope demonstrates how machine learning, behavioral analytics, graph intelligence, explainable AI, and deterministic decisioning can work together in an end-to-end transaction fraud investigation platform.
