# Hedge Fund Industry Analysis

A data science report analyzing the U.S. hedge fund industry through balance sheet trends, leverage dynamics, and the meme stock era (2012-2025).

## Overview

This project pulls data from multiple public sources to build a comprehensive picture of how the hedge fund industry is structured, how it evolved over the past decade, and what the data reveals about key market events like COVID-19 and the GameStop short squeeze.

## Data Sources

| Source | Description | File |
|--------|-------------|------|
| **Federal Reserve Z.1** | Aggregate hedge fund balance sheet (Table B.101.f) — 29 quarterly series via FRED API | `hedge_fund_balance_sheet_fred.csv` |
| **SEC EDGAR 13F** | Institutional holdings for 8 major hedge funds (Citadel, Bridgewater, Renaissance, Point72, Two Sigma, D.E. Shaw, Millennium, AQR) | `13f_*.csv` |
| **CFTC COT** | Leveraged fund positioning in equity index futures (S&P 500, NASDAQ, etc.) | `cftc_cot.csv` |
| **CBOE VIX** | Market volatility index aggregated to quarterly statistics via FRED | `vix_quarterly.csv` |

## Key Analyses

- **Balance sheet composition** — what hedge funds hold (equities, debt, derivatives, loans) and how allocations shift over time
- **Leverage trends** — liability structure, leverage ratios, and borrowing patterns (domestic vs. foreign, prime brokerage vs. secured/unsecured)
- **Derivative exposure** — long derivative values relative to total assets, including the Q1 2018 "Volmageddon" spike
- **GameStop deep dive** — before/after comparison of industry metrics around the Jan 2021 short squeeze
- **13F holdings** — what major hedge funds actually held during the GameStop window
- **CFTC positioning** — net long/short positioning of leveraged funds in equity futures
- **VIX correlation** — relationship between market volatility and hedge fund leverage
- **Statistical analysis** — time series decomposition, rolling correlations, structural break detection (CUSUM)

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Add your FRED API key to .env
echo "FRED_API_KEY=your_key_here" > .env
```

Get a free FRED API key at https://fred.stlouisfed.org/docs/api/api_key.html

## Usage

Open and run `hedge_fund_analysis.ipynb`. The notebook:

1. Fetches all data from FRED, SEC EDGAR, and CFTC (with local caching — subsequent runs are fast)
2. Computes derived metrics (leverage ratio, allocation percentages, growth rates)
3. Generates 12+ visualizations with key event annotations
4. Produces a statistical analysis and automated summary of findings

## Project Structure

```
.
├── hedge_fund_analysis.ipynb   # Main analysis notebook
├── data/                       # Cached datasets (auto-generated on first run)
├── src/
│   └── prepare.py              # Data preparation utilities
├── .env                        # FRED API key (not committed)
└── requirements.txt            # Python dependencies
```

## Tech Stack

Python, Pandas, NumPy, Matplotlib, Seaborn, fredapi, statsmodels, Requests
