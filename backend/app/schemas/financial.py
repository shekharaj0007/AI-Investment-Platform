from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str


class StockPricePoint(BaseModel):
    date: str
    open: float | None = None
    high: float | None = None
    low: float | None = None
    close: float
    volume: float | None = None


class NewsItem(BaseModel):
    title: str
    publisher: str | None = None
    link: str | None = None
    published: str | None = None


class CompanyProfile(BaseModel):
    symbol: str
    name: str
    sector: str | None = None
    industry: str | None = None
    market_cap: float | None = None
    currency: str = "USD"
    current_price: float | None = None
    pe_ratio: float | None = None
    pb_ratio: float | None = None
    dividend_yield: float | None = None
    fifty_two_week_high: float | None = None
    fifty_two_week_low: float | None = None


class FinancialStatement(BaseModel):
    period: str
    revenue: float | None = None
    gross_profit: float | None = None
    net_income: float | None = None
    ebit: float | None = None
    total_assets: float | None = None
    total_debt: float | None = None
    total_equity: float | None = None
    current_assets: float | None = None
    current_liabilities: float | None = None
    inventory: float | None = None
    operating_cash_flow: float | None = None
    free_cash_flow: float | None = None
    eps: float | None = None


class CompanyFinancials(BaseModel):
    symbol: str
    income_statements: list[FinancialStatement] = []
    balance_sheets: list[FinancialStatement] = []
    cash_flows: list[FinancialStatement] = []


class CompanyDataBundle(BaseModel):
    profile: CompanyProfile
    financials: CompanyFinancials
    stock_prices: list[StockPricePoint] = []
    news: list[NewsItem] = []


class RatioCategory(BaseModel):
    name: str
    metrics: dict[str, float | None]


class RatioHistoryPoint(BaseModel):
    period: str
    metrics: dict[str, float | None]


class RatioAnalysis(BaseModel):
    symbol: str
    as_of: str
    categories: list[RatioCategory]
    history: list[RatioHistoryPoint] = []


class ForecastPoint(BaseModel):
    period: str
    value: float
    lower_bound: float | None = None
    upper_bound: float | None = None


class ForecastResult(BaseModel):
    symbol: str
    metric: str
    model: str
    forecasts: list[ForecastPoint]
    historical: list[ForecastPoint] = []
    metrics: dict[str, float] = Field(default_factory=dict)


class BankruptcyRisk(BaseModel):
    symbol: str
    altman_z_score: float
    zone: str
    ml_probability: float
    model: str
    factors: dict[str, float] = {}
    shap_explanations: list[dict[str, float | str]] = []


class CreditRisk(BaseModel):
    symbol: str
    predicted_rating: str
    default_probability: float
    confidence: float
    feature_contributions: dict[str, float] = {}
    shap_explanations: list[dict[str, float | str]] = []


class DCFInputs(BaseModel):
    symbol: str
    revenue_growth: float = Field(..., ge=-0.5, le=1.0)
    wacc: float = Field(..., ge=0.01, le=0.30)
    terminal_growth: float = Field(..., ge=0.0, le=0.06)
    projection_years: int = Field(default=5, ge=3, le=10)
    free_cash_flow: float | None = None


class ComparableCompany(BaseModel):
    symbol: str
    name: str
    pe_ratio: float | None = None
    ev_ebitda: float | None = None
    market_cap: float | None = None


class DCFResult(BaseModel):
    symbol: str
    enterprise_value: float
    equity_value: float
    fair_share_price: float
    assumptions: dict[str, float]
    sensitivity: dict[str, float] = {}
    comparables: list[ComparableCompany] = []


class SentimentArticle(BaseModel):
    title: str
    label: str
    score: float
    published: str | None = None


class SentimentScore(BaseModel):
    symbol: str
    label: str
    score: float
    article_count: int
    correlation_with_price: float | None = None
    articles: list[SentimentArticle] = []
    timeline: list[dict[str, float | str]] = []


class PortfolioRequest(BaseModel):
    total_value: float = Field(..., gt=0)
    risk_profile: str = Field(..., pattern="^(conservative|moderate|aggressive)$")
    currency: str = "INR"
    symbols: list[str] | None = None


class AssetAllocation(BaseModel):
    asset_class: str
    symbol: str | None = None
    weight: float
    amount: float
    expected_return: float | None = None


class EfficientFrontierPoint(BaseModel):
    volatility: float
    expected_return: float
    sharpe_ratio: float


class PortfolioResult(BaseModel):
    total_value: float
    risk_profile: str
    expected_return: float
    volatility: float
    sharpe_ratio: float
    allocations: list[AssetAllocation]
    efficient_frontier: list[EfficientFrontierPoint] = []


class AdvisorRequest(BaseModel):
    question: str
    symbol: str | None = None


class FeatureExplanation(BaseModel):
    feature: str
    value: str
    impact: str
    shap_value: float | None = None


class AdvisorResponse(BaseModel):
    question: str
    symbol: str | None = None
    recommendation: str
    summary: str
    explanations: list[FeatureExplanation]
    confidence: float


class ReportUploadResponse(BaseModel):
    report_id: int
    filename: str
    company_symbol: str
    extracted_fields: dict[str, str]


class ReportQuestionRequest(BaseModel):
    question: str


class ReportAnswer(BaseModel):
    question: str
    answer: str
    sources: list[str] = []


class DashboardSummary(BaseModel):
    symbol: str
    company_name: str
    current_price: float | None
    market_cap: float | None
    revenue_trend: list[dict[str, float | str]]
    profit_trend: list[dict[str, float | str]]
    cash_flow_trend: list[dict[str, float | str]]
    ratio_summary: dict[str, float | None]
    forecast_summary: list[ForecastPoint]
    sentiment: SentimentScore
    bankruptcy_probability: float
    fair_share_price: float | None
    portfolio_sharpe: float | None
    recommendation: str
