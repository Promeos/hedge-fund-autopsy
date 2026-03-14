Execute the full analysis pipeline end-to-end.

## Steps
1. Ensure data is available in `data/raw/` — if not, run `/refresh-data` first
2. Load the hedge fund balance sheet data from `data/raw/hedge_fund_balance_sheet_fred.csv` (or the original `data/raw/hedge_fund_balance_sheet.csv`)
3. Run data preparation using `src.data.prepare.prep_financial_report()`
4. Compute derived metrics using `src.analysis.metrics.compute_derived_metrics()`
5. Save the processed dataset to `data/processed/hedge_fund_analysis.csv`
6. Generate all standard visualizations using functions from `src.visualization.plots` and save to `outputs/figures/`:
   - `total_assets.png`
   - `asset_composition.png`
   - `debt_securities.png`
   - `liability_structure.png`
   - `balance_sheet_overview.png`
   - `derivative_exposure.png`
   - `borrowing_patterns.png`
   - `correlation_heatmap.png`
7. Output summary statistics for key metrics (leverage ratio, asset growth CAGR, allocation percentages)
8. Report any data quality issues (missing quarters, outliers, NaN values)

## Expected Outputs
- Processed dataset: `data/processed/hedge_fund_analysis.csv`
- 8 standard charts in `outputs/figures/`
- Summary statistics printed to console
