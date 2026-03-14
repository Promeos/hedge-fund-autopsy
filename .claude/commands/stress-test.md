Run stress test scenarios against the latest quarter of hedge fund data.

## Steps

1. Load data and compute derived metrics
2. Extract latest quarter values for: total assets, total liabilities, net assets, leverage ratio, equity allocation, derivative exposure

3. Run the following scenarios:

   **Scenario 1: Equity Market Drawdown (-20%)**
   - Corporate equities decline 20%
   - Other assets unchanged
   - Liabilities decline 5% (partial deleveraging)
   - Compute stressed leverage ratio

   **Scenario 2: COVID-Style Shock (replay 2020-Q1 dynamics)**
   - Apply the actual QoQ changes observed in 2020-Q1 to current positions
   - Report stressed metrics vs current

   **Scenario 3: Interest Rate Shock (+200bp)**
   - Estimate Treasury securities value decline (duration ~ 5 years → ~10% loss)
   - Increase unsecured borrowing cost
   - Compute impact on net assets

   **Scenario 4: Prime Brokerage Pullback (-25%)**
   - Reduce prime brokerage lending by 25%
   - Shift to other secured/unsecured funding
   - Assess leverage and funding mix impact

4. Compute risk metrics on historical data:
   - VaR (95%) and CVaR (95%) on quarterly net asset changes
   - Maximum drawdown with date and recovery quarters
   - Worst 3 quarters by net asset change

5. Print a structured stress test report and save to `outputs/reports/stress_test.txt`

## Notes
- State all assumptions clearly
- Compare stressed values to historical extremes
- Include recovery estimates based on historical recovery speeds