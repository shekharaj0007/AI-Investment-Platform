# AI Financial Copilot

**An AI-powered platform for analyzing public companies, valuing businesses, forecasting financials, assessing risk, and answering investment questions using LLMs and machine learning.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Overview

AI Financial Copilot is a production-grade, open-source financial intelligence platform that combines:

- **Financial data pipelines** — income statements, balance sheets, cash flows, market data, news
- **Classical ML** — forecasting, bankruptcy prediction, credit risk, portfolio optimization
- **LLM + RAG** — annual report Q&A, investment advisor, report summaries
- **Explainable AI** — SHAP-backed explanations for every recommendation

Unlike typical student projects that stop at stock prediction or sentiment analysis, this platform demonstrates end-to-end understanding of financial analysis, machine learning, LLMs, and software engineering.

# 📸 Screenshots

## Executive Dashboard

![Executive Dashboard](assets/executive-dashboard.png)

---

## AI Financial Copilot Dashboard

![AI Financial Copilot Dashboard](assets/ai-financial-copilot-dashboard.png)

---

## Portfolio Manager

![Portfolio Manager](assets/portfolio-manager.png)

---

## Portfolio Optimizer

![Portfolio Optimizer](assets/portfolio-optimizer.png)

---

## AI Investment Advisor

![AI Investment Advisor](assets/ai-investment-advisor.png)

---

## AI Help Advisor

![AI Help Advisor](assets/ai-help-advisor.png)

---

## Annual Report Reader

![Annual Report Reader](assets/annual-report-reader.png)

---

## News Sentiment Analysis

![News Sentiment](assets/news-sentiment.png)

---

## Risk Models

![Risk Models](assets/risk-models.png)

---

## Revenue Forecasting

![Revenue Forecasting](assets/revenue-forecasting.png)

## Architecture

```
                           User
                             │
                   React / Next.js Dashboard
                             │
──────────────────────── API Layer ───────────────────────
                             │
        ┌───────────────┬──────────────┬──────────────┐
        │               │              │              │
 Financial Data     Annual Reports   News API     User Portfolio
        │               │              │              │
        └───────────────┴──────────────┴──────────────┘
                             │
                     Data Processing Layer
                             │
      Financial Ratios | Feature Engineering | NLP
                             │
────────────────── Machine Learning Layer ──────────────────
                             │
 Forecasting │ Risk │ Valuation │ Recommendation │ Sentiment
                             │
──────────────────── LLM + RAG Layer ───────────────────────
                             │
 PDF QA │ Financial Chatbot │ Report Summaries │ Insights
                             │
                     PostgreSQL / Vector DB
```

## Modules

| # | Module | Status |
|---|--------|--------|
| 1 | Financial Data Collection | 🚧 Scaffolded |
| 2 | AI Annual Report Reader | 🚧 Scaffolded |
| 3 | Financial Ratio Engine | 🚧 Scaffolded |
| 4 | Revenue Forecasting | 🚧 Scaffolded |
| 5 | Bankruptcy Prediction | 🚧 Scaffolded |
| 6 | Credit Risk Model | 🚧 Scaffolded |
| 7 | Valuation Engine (DCF + Comps) | 🚧 Scaffolded |
| 8 | News Sentiment | 🚧 Scaffolded |
| 9 | Portfolio Optimizer | 🚧 Scaffolded |
| 10 | AI Investment Advisor | 🚧 Scaffolded |
| 11 | Explainable AI (SHAP) | 🚧 Scaffolded |
| 12 | Executive Dashboard | 🚧 Scaffolded |

See [docs/ROADMAP.md](docs/ROADMAP.md) for the 8-week build plan.

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| Backend | Python, FastAPI, SQLAlchemy, Pydantic |
| ML/AI | scikit-learn, XGBoost, LightGBM, PyTorch, Hugging Face |
| LLM/RAG | LangChain, FAISS/ChromaDB, OpenAI-compatible models |
| Database | PostgreSQL, Redis, Vector DB |
| Frontend | React, Next.js 14, Tailwind CSS, Recharts |
| DevOps | Docker, GitHub Actions, Nginx |

## Quick Start

### Prerequisites

- **Python 3.11 or 3.12** (3.14+ lacks pandas/yfinance wheels — use Docker if on newer Python)
- Node.js 20+
- Docker & Docker Compose (recommended)

### 1. Clone and configure

```bash
git clone https://github.com/yourusername/ai-financial-copilot.git
cd ai-financial-copilot
cp .env.example .env
# Add your API keys to .env
```

### 2. Run with Docker (recommended)

```bash
docker compose up --build
```

- **Frontend:** http://localhost:3001
- **API docs:** http://localhost:8001/docs
- **Health check:** http://localhost:8001/health

### 3. Run locally (development)

**Backend:**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
ai-financial-copilot/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/v1/          # REST endpoints per module
│   │   ├── core/            # Config, database, security
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   ├── services/        # Business logic
│   │   └── ml/              # ML models & pipelines
│   └── tests/
├── frontend/                # Next.js dashboard
│   └── src/
│       ├── app/             # App router pages
│       └── components/      # UI components
├── docs/                    # Architecture & roadmap
├── data/                    # Local data & vector stores (gitignored)
└── docker-compose.yml
```

## API Overview

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/companies/{symbol}` | Company profile & financials |
| `GET /api/v1/ratios/{symbol}` | Computed financial ratios |
| `POST /api/v1/reports/upload` | Upload annual report PDF |
| `POST /api/v1/reports/{id}/ask` | RAG Q&A on a report |
| `GET /api/v1/forecast/{symbol}` | Revenue/income forecasts |
| `GET /api/v1/risk/bankruptcy/{symbol}` | Altman Z-score + ML probability |
| `GET /api/v1/risk/credit/{symbol}` | Credit rating prediction |
| `POST /api/v1/valuation/dcf` | DCF valuation |
| `GET /api/v1/sentiment/{symbol}` | News sentiment analysis |
| `POST /api/v1/portfolio/optimize` | MPT portfolio optimization |
| `POST /api/v1/advisor/ask` | AI investment advisor |

Full interactive docs at `/docs` when the backend is running.

## Contributing

Contributions welcome! See [docs/ROADMAP.md](docs/ROADMAP.md) for current priorities.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/module-3-ratios`)
3. Commit your changes
4. Open a Pull Request

## License

MIT License — see [LICENSE](LICENSE).

## Why This Project Stands Out

Most finance projects stop at one task. AI Financial Copilot demonstrates:

- **Real financial workflows** — DCF, credit analysis, portfolio theory, ratio analysis
- **Production engineering** — REST APIs, auth, CI/CD, Docker, tests
- **Modern AI stack** — RAG, FinBERT, SHAP explainability, time-series ML
- **Interview-ready depth** — explain *why* each module matters in business decisions

Built for AI/ML interviews, product roles, consulting cases, and MBA discussions.
