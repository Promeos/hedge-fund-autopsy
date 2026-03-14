Generate formatted analysis reports from the current data.

## Steps

1. Load data from `data/raw/hedge_fund_balance_sheet_fred.csv`
2. Compute derived metrics using `src.analysis.metrics.compute_derived_metrics()`
3. Generate all standard charts using `src.visualization.plots` with `save_path` set to `outputs/figures/`:
   - `outputs/figures/total_assets.png`
   - `outputs/figures/asset_composition.png`
   - `outputs/figures/debt_securities.png`
   - `outputs/figures/liability_structure.png`
   - `outputs/figures/balance_sheet_overview.png`
   - `outputs/figures/derivative_exposure.png`
   - `outputs/figures/borrowing_patterns.png`
   - `outputs/figures/correlation_heatmap.png`

4. Compute summary statistics:
   - CAGR of total assets over full period
   - Leverage ratio: mean, peak (with date), trough (with date)
   - Latest quarter metrics: leverage, equity allocation, cash-to-assets, derivative exposure
   - Before/after comparisons for COVID and GameStop events

5. Generate **Executive Summary** (`outputs/reports/executive_summary.md`):
   - Title, data period, generation timestamp
   - 3-5 key findings with supporting numbers
   - Table of latest quarter metrics
   - References to chart files

6. Generate **Summary Statistics CSV** (`outputs/reports/summary_statistics.csv`):
   - One row per quarter with key metrics
   - Suitable for import into Excel/Sheets

7. Save processed dataset to `data/processed/hedge_fund_analysis.csv`

## Notes
- Charts must be generated before the report (report references chart file paths)
- Include a "Data Sources" section citing FRED, SEC EDGAR, CFTC, CBOE VIX
- Add generation timestamp to all outputs
- Flag any data quality issues encountered during generation