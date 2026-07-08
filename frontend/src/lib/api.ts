const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001";

export async function fetchApi<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    cache: "no-store",
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json();
}

export async function uploadReport(file: File, companySymbol: string) {
  const form = new FormData();
  form.append("file", file);
  form.append("company_symbol", companySymbol);
  const res = await fetch(`${API_URL}/api/v1/reports/upload`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
  return res.json();
}

export const api = {
  health: () => fetchApi<{ status: string; version: string; environment: string }>("/health"),

  dashboard: (symbol = "AAPL") => fetchApi<DashboardSummary>(`/api/v1/dashboard/${symbol}`),

  company: (symbol: string) => fetchApi<CompanyProfile>(`/api/v1/companies/${symbol}`),
  financials: (symbol: string) => fetchApi<CompanyFinancials>(`/api/v1/companies/${symbol}/financials`),
  prices: (symbol: string, period = "1y") =>
    fetchApi<StockPrice[]>(`/api/v1/companies/${symbol}/prices?period=${period}`),
  news: (symbol: string) => fetchApi<NewsItem[]>(`/api/v1/companies/${symbol}/news`),

  ratios: (symbol: string) => fetchApi<RatioAnalysis>(`/api/v1/ratios/${symbol}`),

  forecast: (symbol: string, metric = "revenue", model = "xgboost") =>
    fetchApi<ForecastResult>(`/api/v1/forecast/${symbol}?metric=${metric}&model=${model}`),

  bankruptcy: (symbol: string) => fetchApi<BankruptcyRisk>(`/api/v1/risk/bankruptcy/${symbol}`),
  credit: (symbol: string) => fetchApi<CreditRisk>(`/api/v1/risk/credit/${symbol}`),

  dcf: (body: DCFInputs) =>
    fetchApi<DCFResult>("/api/v1/valuation/dcf", { method: "POST", body: JSON.stringify(body) }),

  sentiment: (symbol: string) => fetchApi<SentimentScore>(`/api/v1/sentiment/${symbol}`),

  optimizePortfolio: (body: PortfolioRequest) =>
    fetchApi<PortfolioResult>("/api/v1/portfolio/optimize", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  askAdvisor: (body: { question: string; symbol?: string }) =>
    fetchApi<AdvisorResponse>("/api/v1/advisor/ask", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  askReport: (reportId: number, question: string) =>
    fetchApi<ReportAnswer>(`/api/v1/reports/${reportId}/ask`, {
      method: "POST",
      body: JSON.stringify({ question }),
    }),
};

// Types
export interface CompanyProfile {
  symbol: string;
  name: string;
  sector?: string;
  industry?: string;
  market_cap?: number;
  current_price?: number;
  pe_ratio?: number;
  pb_ratio?: number;
}

export interface CompanyFinancials {
  symbol: string;
  income_statements: FinancialStatement[];
  balance_sheets: FinancialStatement[];
  cash_flows: FinancialStatement[];
}

export interface FinancialStatement {
  period: string;
  revenue?: number;
  net_income?: number;
  gross_profit?: number;
  total_assets?: number;
  total_debt?: number;
  free_cash_flow?: number;
}

export interface StockPrice {
  date: string;
  close: number;
  volume?: number;
}

export interface NewsItem {
  title: string;
  publisher?: string;
  link?: string;
}

export interface RatioAnalysis {
  symbol: string;
  categories: Array<{ name: string; metrics: Record<string, number | null> }>;
  history: Array<{ period: string; metrics: Record<string, number | null> }>;
}

export interface ForecastResult {
  symbol: string;
  metric: string;
  model: string;
  forecasts: Array<{ period: string; value: number; lower_bound?: number; upper_bound?: number }>;
  historical: Array<{ period: string; value: number }>;
  metrics: Record<string, number>;
}

export interface BankruptcyRisk {
  symbol: string;
  altman_z_score: number;
  zone: string;
  ml_probability: number;
  factors: Record<string, number>;
  shap_explanations: Array<{ feature: string; shap_value: number; direction: string }>;
}

export interface CreditRisk {
  symbol: string;
  predicted_rating: string;
  default_probability: number;
  confidence: number;
  shap_explanations: Array<{ feature: string; shap_value: number; direction: string }>;
}

export interface DCFInputs {
  symbol: string;
  revenue_growth: number;
  wacc: number;
  terminal_growth: number;
  projection_years?: number;
}

export interface DCFResult {
  symbol: string;
  enterprise_value: number;
  equity_value: number;
  fair_share_price: number;
  assumptions: Record<string, number>;
  comparables: Array<{ symbol: string; name: string; pe_ratio?: number; ev_ebitda?: number }>;
}

export interface SentimentScore {
  symbol: string;
  label: string;
  score: number;
  article_count: number;
  correlation_with_price?: number;
  articles: Array<{ title: string; label: string; score: number }>;
  timeline: Array<{ date: string; score: number; label: string }>;
}

export interface PortfolioRequest {
  total_value: number;
  risk_profile: string;
  currency?: string;
  symbols?: string[];
}

export interface PortfolioResult {
  total_value: number;
  risk_profile: string;
  expected_return: number;
  volatility: number;
  sharpe_ratio: number;
  allocations: Array<{ asset_class: string; symbol: string | null; weight: number; amount: number; expected_return?: number }>;
  efficient_frontier: Array<{ volatility: number; expected_return: number; sharpe_ratio: number }>;
}

export interface AdvisorResponse {
  question: string;
  symbol?: string;
  recommendation: string;
  summary: string;
  explanations: Array<{ feature: string; value: string; impact: string; shap_value: number | null }>;
  confidence: number;
}

export interface ReportAnswer {
  question: string;
  answer: string;
  sources: string[];
}

export interface DashboardSummary {
  symbol: string;
  company_name: string;
  current_price?: number;
  market_cap?: number;
  revenue_trend: Array<{ period: string; value: number }>;
  profit_trend: Array<{ period: string; value: number }>;
  cash_flow_trend: Array<{ period: string; value: number }>;
  ratio_summary: Record<string, number | null>;
  forecast_summary: Array<{ period: string; value: number }>;
  sentiment: SentimentScore;
  bankruptcy_probability: number;
  fair_share_price?: number;
  portfolio_sharpe?: number;
  recommendation: string;
}
