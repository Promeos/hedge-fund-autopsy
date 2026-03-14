# Hedge Fund Industry Analysis

Balance Sheet Trends, Leverage, and the Meme Stock Era (2012-2025)

Analysis of domestic hedge fund balance sheets using Federal Reserve Z.1 data (Table B.101.f), enriched with SEC 13F filings, CFTC Commitments of Traders positioning, and CBOE VIX volatility data. The narrative covers post-GFC recovery, leverage buildup, COVID shock, meme stock squeeze, and aftermath.

## Directory Structure

```
financial_data/
├── CLAUDE.md                    # This file — project guide
├── .claude/
│   ├── settings.local.json      # Claude Code permissions
│   ├── agents/                  # Specialized agent definitions
│   │   ├── data-engineer.md     # Data pipeline agent
│   │   ├── analyst.md           # Financial analysis agent
│   │   ├── visualizer.md        # Charting agent
│   │   ├── report-writer.md     # Report generation agent
│   │   ├── data-quality.md      # Data validation agent
│   │   ├── statistician.md      # Advanced statistical analysis agent
│   │   ├── regulatory-expert.md # SEC/regulatory domain agent
│   │   └── scenario-analyst.md  # Stress testing & scenario agent
│   └── commands/                # Slash commands
│       ├── refresh-data.md      # /refresh-data — fetch all data sources
│       ├── run-analysis.md      # /run-analysis — end-to-end pipeline
│       ├── validate-data.md     # /validate-data — data quality sweep
│       ├── generate-report.md   # /generate-report — produce formatted reports
│       └── stress-test.md       # /stress-test — run scenario analysis
├── .env                         # API keys (never commit)
├── requirements.txt             # Python dependencies
├── data/
│   ├── raw/                     # Original untransformed data (cached API responses)
│   ├── processed/               # Cleaned, merged, derived datasets
│   └── .gitignore
├── notebooks/
│   └── hedge_fund_analysis.ipynb  # Primary analysis notebook
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── fetch.py             # FRED, SEC EDGAR, CFTC, VIX data fetchers
│   │   └── prepare.py           # Data cleaning and transformation
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── metrics.py           # Derived metrics and statistical computations
│   └── visualization/
│       ├── __init__.py
│       └── plots.py             # matplotlib/seaborn chart functions
├── tests/                       # Test suite
└── outputs/
    ├── figures/                 # Saved chart PNGs
    └── reports/                 # Generated reports
```

## Tech Stack

- **Python 3.10+**
- Core: `pandas`, `numpy`
- Visualization: `matplotlib`, `seaborn`
- Data access: `requests`, `fredapi`
- Configuration: `python-dotenv`
- Standard library: `os`, `json`, `time`, `datetime`, `warnings`, `xml.etree.ElementTree`, `io.StringIO`

## Data Sources

### 1. FRED API — Federal Reserve Z.1 Financial Accounts
- **Table B.101.f**: Balance Sheet of Domestic Hedge Funds
- 30 series covering assets, liabilities, net assets, derivatives
- Series IDs: `BOGZ1FL62*Q` (quarterly)
- Also: `VIXCLS` for daily VIX data
- Requires `FRED_API_KEY` in `.env`
- Rate limit: 0.2s between requests

### 2. SEC EDGAR — 13F-HR Filings
- 8 major hedge funds: Citadel, Bridgewater, Renaissance, Point72, Two Sigma, D.E. Shaw, Millennium, AQR
- Focus window: Q4 2020 - Q1 2021 (GameStop event)
- Requires `User-Agent` header
- Rate limit: 0.15s between requests

### 3. CFTC — Commitments of Traders
- Traders in Financial Futures (TFF) report
- Equity index futures: S&P 500, DJIA, NASDAQ, Russell
- Leveraged fund long/short/spreading positions

### 4. CBOE VIX — Volatility Index
- Fetched via FRED (VIXCLS series)
- Aggregated from daily to quarterly (mean, max, min, end, std)

## Key Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the notebook
jupyter notebook notebooks/hedge_fund_analysis.ipynb

# Fetch/refresh all data
python -m src.data.fetch

# Run tests
pytest tests/
```

## Coding Conventions

- All monetary values are in **billions USD** (FRED Z.1 returns millions; divide by 1000)
- **Quarterly frequency** for all time series alignment (quarter-end dates)
- **Cache first**: Always check for cached CSV in `data/raw/` before making API calls
- Rate limits: 0.2s sleep for FRED, 0.15s for SEC EDGAR
- Date parsing: `pd.to_datetime`; numeric conversion: `pd.to_numeric(errors='coerce')`
- Missing values: `fillna(0)` for balance sheet items
- Plotting style: `seaborn-v0_8-whitegrid`, figure size `(14, 6)`, DPI 100, font size 12
- Market event annotations on all time series charts via `add_event_annotations()`

## Security

- `.env` contains `FRED_API_KEY` — **never commit this file**
- SEC EDGAR `User-Agent` header should use a real contact email for production use
- No other credentials stored; CFTC and VIX data are publicly available

## Agents

| Agent | File | Purpose |
|-------|------|---------|
| Data Engineer | `.claude/agents/data-engineer.md` | FRED, SEC EDGAR, CFTC, VIX data pipelines; caching; rate limiting |
| Financial Analyst | `.claude/agents/analyst.md` | Derived metrics, leverage trends, allocation analysis, market event impact |
| Visualizer | `.claude/agents/visualizer.md` | matplotlib/seaborn charts; style guide; event annotations; 8 chart functions |
| Report Writer | `.claude/agents/report-writer.md` | Executive summaries, HTML reports, CSV exports to `outputs/reports/` |
| Data Quality | `.claude/agents/data-quality.md` | Schema validation, range checks, temporal continuity, cross-source reconciliation |
| Statistician | `.claude/agents/statistician.md` | ARIMA, Granger causality, regime detection, VaR/CVaR, event studies |
| Regulatory Expert | `.claude/agents/regulatory-expert.md` | SEC filing interpretation, regulatory timeline, 13F limitations, compliance context |
| Scenario Analyst | `.claude/agents/scenario-analyst.md` | Stress tests, sensitivity analysis, drawdown modeling, Monte Carlo simulation |

## Slash Commands

| Command | File | Purpose |
|---------|------|---------|
| `/refresh-data` | `.claude/commands/refresh-data.md` | Fetch latest data from all 4 sources |
| `/run-analysis` | `.claude/commands/run-analysis.md` | End-to-end: load data → compute metrics → generate charts → summary stats |
| `/validate-data` | `.claude/commands/validate-data.md` | Full data quality sweep with PASS/WARN/FAIL report |
| `/generate-report` | `.claude/commands/generate-report.md` | Produce executive summary, charts, and CSV exports |
| `/stress-test` | `.claude/commands/stress-test.md` | Run 4 stress scenarios + VaR/drawdown analysis |

## Derived Metrics Reference

| Metric | Formula |
|--------|---------|
| `leverage_ratio` | Total liabilities / Total net assets |
| `cash_to_assets` | (Deposits + Other cash + MMF shares) / Total assets |
| `equity_pct` | Corporate equities / Total assets |
| `debt_securities_pct` | Total debt securities / Total assets |
| `derivative_to_assets` | Derivatives (long value) / Total assets |
| `loans_to_assets` | Total loans (asset) / Total assets |
| `prime_brokerage_pct` | Prime brokerage borrowing / Total loans (liability) |
| `other_secured_pct` | Other secured borrowing / Total loans (liability) |
| `unsecured_pct` | Unsecured borrowing / Total loans (liability) |
| `domestic_borrowing` | Sum of domestic repo + prime brokerage + other secured |
| `foreign_borrowing` | Sum of foreign repo + prime brokerage + other secured |
| `foreign_borrowing_share` | Foreign / (Domestic + Foreign) |
| `total_assets_qoq` | Total assets quarter-over-quarter % change |
| `total_assets_yoy` | Total assets year-over-year % change |
| `net_assets_qoq` | Net assets quarter-over-quarter % change |
| `liabilities_qoq` | Total liabilities quarter-over-quarter % change |
| `leverage_change` | Leverage ratio quarter-over-quarter difference |
