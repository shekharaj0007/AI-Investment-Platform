# AI Financial Copilot — 8-Week Build Roadmap

Production-grade open-source build plan. Each week delivers shippable, demo-ready functionality.

## Phase 0: Foundation (Week 1) ✅

**Goal:** Runnable monorepo with CI, Docker, and API skeleton.

- [x] Project structure (backend + frontend + docs)
- [x] FastAPI with module routers and Pydantic schemas
- [x] Docker Compose (PostgreSQL, Redis, backend, frontend)
- [x] Next.js dashboard shell
- [x] GitHub Actions CI
- [ ] Database migrations (Alembic)
- [ ] Authentication (JWT)

**Demo:** Health check, portfolio optimizer, advisor stub via API + dashboard.

---

## Phase 1: Data Layer (Week 2)

**Goal:** Real financial data flowing into the system.

### Module 1 — Financial Data Collection
- [ ] Unified data adapter interface (Alpha Vantage, FMP, Yahoo Finance)
- [ ] Cache layer with Redis
- [ ] Store normalized financials in PostgreSQL
- [ ] Stock price history endpoints
- [ ] Earnings call transcript ingestion (FMP)

**Demo:** Search `AAPL` → see income statement, balance sheet, cash flow, price chart.

---

## Phase 2: Analytics Core (Week 3)

**Goal:** Classical financial analysis working on real data.

### Module 3 — Financial Ratio Engine
- [ ] Full ratio suite (profitability, liquidity, leverage, efficiency, valuation)
- [ ] Historical ratio time series
- [ ] Peer comparison (sector benchmarks)

### Module 7 — Valuation Engine (Part 1)
- [ ] DCF with editable assumptions
- [ ] Comparable company analysis (EV/EBITDA, P/E)

**Demo:** Ratio dashboard + DCF calculator for any public company.

---

## Phase 3: Machine Learning (Weeks 4–5)

**Goal:** Trained models with evaluation metrics.

### Module 4 — Revenue Forecasting
- [ ] Feature engineering pipeline (lag features, rolling stats)
- [ ] XGBoost + LightGBM baselines
- [ ] LSTM / TFT (stretch goal)
- [ ] RMSE, MAE, MAPE evaluation

### Module 5 — Bankruptcy Prediction
- [ ] Altman Z-score (production-ready)
- [ ] Random Forest / XGBoost on fundamentals
- [ ] Probability output with confidence intervals

### Module 6 — Credit Risk Model
- [ ] Rating classification (AAA → BB)
- [ ] Default probability regression

**Demo:** Forecast chart + risk score card with model metrics.

---

## Phase 4: LLM + RAG (Week 6)

**Goal:** Document intelligence and conversational finance.

### Module 2 — AI Annual Report Reader
- [ ] PDF parsing (pypdf + OCR fallback)
- [ ] Structured extraction (revenue, debt, risks, MD&A, ESG)
- [ ] LangChain + ChromaDB vector store
- [ ] RAG Q&A ("Why did gross margin fall?")

### Module 10 — AI Investment Advisor
- [ ] Tool-calling agent (ratios, forecast, sentiment, valuation)
- [ ] Grounded responses with citations

**Demo:** Upload Tesla 10-K → ask comparative questions → get sourced answers.

---

## Phase 5: Sentiment & Portfolio (Week 7)

**Goal:** Market intelligence and allocation.

### Module 8 — News Sentiment
- [ ] News aggregation (NewsAPI / FMP)
- [ ] FinBERT inference
- [ ] Sentiment vs. price correlation

### Module 9 — Portfolio Optimizer
- [ ] Modern Portfolio Theory (efficient frontier)
- [ ] Sharpe ratio optimization
- [ ] Multi-asset support (stocks, ETFs, gold, bonds)

**Demo:** Sentiment timeline + ₹10L portfolio recommendation.

---

## Phase 6: Polish & Launch (Week 8)

**Goal:** Production-ready open-source release.

### Module 11 — Explainable AI
- [ ] SHAP values for all ML predictions
- [ ] Feature contribution cards in UI

### Module 12 — Executive Dashboard
- [ ] Revenue / profit / cash flow charts
- [ ] Ratio history, forecasts, sentiment timeline
- [ ] Portfolio allocation pie chart
- [ ] Risk score + valuation summary

### DevOps
- [ ] Full test coverage (>80% backend)
- [ ] E2E tests (Playwright)
- [ ] AWS/Azure deployment guide
- [ ] Nginx reverse proxy config
- [ ] Contributing guide + issue templates

**Demo:** Full end-to-end walkthrough suitable for portfolio / interviews.

---

## Priority Order (if time-constrained)

1. **Must-have:** Modules 1, 3, 7, 10, 12
2. **Strong differentiators:** Modules 2, 4, 5, 11
3. **Nice-to-have:** Modules 6, 8, 9

## Success Metrics

| Metric | Target |
|--------|--------|
| API endpoints | 25+ |
| Test coverage | >80% |
| Docker one-command start | ✅ |
| Demo companies supported | 50+ |
| Report Q&A accuracy | Subjective, sourced answers |
| Forecast MAPE | <15% on holdout |

## Next Step

Start **Phase 1** — wire Yahoo Finance + FMP into Module 1 with PostgreSQL persistence.
