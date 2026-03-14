Fetch the latest data from all sources and update cached files.

## Steps
1. Run `python -m src.data.fetch` from the project root to execute all fetchers
2. Verify that the following files are updated in `data/raw/`:
   - `hedge_fund_balance_sheet_fred.csv` (FRED Z.1 balance sheet)
   - `vix_quarterly.csv` (VIX volatility)
   - `13f_all_holdings.csv` (SEC 13F aggregate)
   - `cftc_cot.csv` (CFTC Commitments of Traders)
3. Report which sources succeeded and which failed
4. Show the date range of each dataset

## Notes
- Requires `FRED_API_KEY` in `.env`
- SEC EDGAR and CFTC do not require API keys
- Rate limits apply; full refresh takes ~2 minutes
- Existing cached files will be loaded instead of re-fetched; delete them to force a refresh
