# Architecture

## System Overview

AI Financial Copilot follows a layered architecture separating data ingestion, analytics, ML inference, and LLM reasoning.

```
┌─────────────────────────────────────────────────────────────┐
│                     Presentation Layer                       │
│              Next.js 14 · Tailwind · Recharts                │
└─────────────────────────────┬───────────────────────────────┘
                              │ REST / JSON
┌─────────────────────────────▼───────────────────────────────┐
│                       API Layer (FastAPI)                    │
│  /companies  /ratios  /forecast  /risk  /valuation           │
│  /sentiment  /portfolio  /advisor  /reports                  │
└─────────────────────────────┬───────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌─────────────────┐   ┌─────────────────┐
│   Services    │   │   ML Pipeline   │   │   RAG Pipeline  │
│  (business    │   │  XGBoost · LSTM │   │ LangChain ·     │
│   logic)      │   │  FinBERT · SHAP │   │ ChromaDB · LLM  │
└───────┬───────┘   └────────┬────────┘   └────────┬────────┘
        │                    │                     │
        └────────────────────┼─────────────────────┘
                             ▼
              ┌──────────────────────────────┐
              │         Data Layer            │
              │  PostgreSQL · Redis · Chroma  │
              └──────────────────────────────┘
                             ▲
              ┌──────────────┴───────────────┐
              │      External APIs          │
              │  Yahoo · FMP · Alpha Vantage │
              │  Polygon · News · OpenAI     │
              └──────────────────────────────┘
```

## Backend Structure

```
backend/app/
├── api/v1/           # Thin HTTP handlers — validate, delegate, respond
├── core/             # Config, database session, auth (future)
├── models/           # SQLAlchemy ORM entities
├── schemas/          # Pydantic request/response contracts
├── services/         # Business logic — one service per module
└── ml/               # Model training, inference, feature stores (future)
```

**Design principles:**
- **Services are stateless** — all state in PostgreSQL/Redis/vector DB
- **Schemas define contracts** — frontend and tests depend on stable API shapes
- **ML models loaded lazily** — heavy models (FinBERT, TFT) init on first request
- **RAG is isolated** — report reader owns chunking, embedding, retrieval

## Data Flow Examples

### Company Analysis Request

```
User → GET /api/v1/companies/AAPL/financials
     → FinancialDataService.get_financials()
     → yfinance (cache miss) → Redis (cache hit on repeat)
     → Normalize to FinancialStatement schema
     → JSON response
```

### Investment Advisor

```
User → POST /api/v1/advisor/ask {"question": "Should I buy INFY?", "symbol": "INFY"}
     → AdvisorService orchestrates:
         ├── RatioEngine.compute_ratios()
         ├── ForecastingService.forecast()
         ├── RiskService.bankruptcy_risk()
         ├── SentimentService.analyze()
         └── ValuationService.dcf()
     → Aggregate into AdvisorResponse with SHAP explanations
     → JSON response
```

### Annual Report Q&A

```
User → POST /api/v1/reports/upload (PDF)
     → ReportReaderService:
         ├── Extract text (pypdf / OCR)
         ├── Structured field extraction
         ├── Chunk → embed → store in ChromaDB
     → report_id

User → POST /api/v1/reports/{id}/ask {"question": "..."}
     → Retrieve relevant chunks (similarity search)
     → LLM generation with context
     → Answer + source citations
```

## Database Schema (Initial)

| Table | Purpose |
|-------|---------|
| `companies` | Symbol, name, sector, market cap |
| `annual_reports` | Uploaded PDFs, extraction summary, vector collection ID |
| `portfolios` | User portfolio configurations and allocations |
| `financial_statements` | (Phase 1) Normalized quarterly/annual data |
| `forecasts` | (Phase 3) Stored model predictions |
| `news_articles` | (Phase 5) Headlines + sentiment scores |

## Frontend Structure

```
frontend/src/
├── app/
│   ├── page.tsx              # Executive dashboard (Module 12)
│   ├── company/[symbol]/     # Company deep-dive
│   ├── reports/              # PDF upload + Q&A
│   ├── portfolio/            # Optimizer UI
│   └── advisor/              # Chat interface
├── components/
│   ├── charts/               # Recharts wrappers
│   ├── layout/               # Sidebar, header
│   └── ui/                   # Cards, badges, forms
└── lib/
    └── api.ts                # Typed API client
```

## Security (Planned)

- JWT authentication for user-specific portfolios
- API key rotation for external data providers
- Rate limiting via Redis
- PDF upload size limits and virus scanning (production)

## Deployment

```
Internet → Nginx (TLS termination, static assets)
              ├── /api/* → FastAPI (Gunicorn + Uvicorn workers)
              └── /*     → Next.js (SSR + static)
                         PostgreSQL (RDS)
                         Redis (ElastiCache)
                         ChromaDB (persistent volume)
```

See `docker-compose.yml` for local development parity.
