"""Tests for src.analysis.cross_source."""

import pandas as pd

from src.analysis.cross_source import (
    align_quarterly,
)
from src.analysis.cross_source import (
    test_h7_concentration_correlation as run_h7_concentration_correlation,
)


def test_align_quarterly_uses_deduped_rates_notional_clearing():
    """DTCC alignment should dedupe rows and preserve rates-specific clearing."""
    dtcc = pd.DataFrame(
        {
            "date": pd.to_datetime(
                [
                    "2025-03-28",
                    "2025-03-31",
                    "2025-03-31",
                    "2025-03-31",
                ]
            ),
            "asset_class": ["RATES", "RATES", "RATES", "FOREX"],
            "total_notional_bn": [100.0, 200.0, 220.0, 300.0],
            "cleared_notional_bn": [60.0, 140.0, 176.0, 30.0],
            "cleared_pct": [0.70, 0.72, 0.73, 0.10],
        }
    )

    aligned = align_quarterly({"dtcc": dtcc})

    assert "dtcc_rates_cleared_notional_pct" in aligned.columns
    assert "dtcc_forex_cleared_notional_pct" in aligned.columns
    assert aligned.loc[pd.Timestamp("2025-03-31"), "dtcc_rates_cleared_notional_pct"] == 0.8
    assert aligned.loc[pd.Timestamp("2025-03-31"), "dtcc_forex_cleared_notional_pct"] == 0.1


def test_h7_accepts_value_thousands_and_report_period(monkeypatch, tmp_path):
    """H7 should work with the repo's 13F schema, not require legacy columns."""
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()

    # 12 funds per quarter so top-10 share < 1.0 and varies across quarters.
    # Funds K and L grow from small to large, shifting the top-10 concentration.
    funds = [f"Fund {c}" for c in "ABCDEFGHIJKL"]
    rows = []
    # Q1: K=10, L=10 are tiny → top-10 share high
    q1_vals = [500, 400, 300, 200, 150, 120, 100, 80, 60, 50, 10, 10]
    # Q2: K=50, L=50 growing
    q2_vals = [450, 380, 280, 200, 150, 120, 100, 80, 60, 50, 50, 50]
    # Q3: K=100, L=100
    q3_vals = [400, 350, 260, 200, 150, 120, 100, 80, 60, 50, 100, 100]
    # Q4: K=200, L=200 → top-10 share drops as bottom 2 are now in top-10
    q4_vals = [350, 300, 250, 200, 150, 120, 100, 80, 60, 50, 200, 200]
    for q, vals in [("2024Q1", q1_vals), ("2024Q2", q2_vals), ("2024Q3", q3_vals), ("2024Q4", q4_vals)]:
        for fund, val in zip(funds, vals):
            rows.append({"fund": fund, "report_period": q, "value_thousands": val})
    holdings = pd.DataFrame(rows)
    holdings.to_csv(raw_dir / "13f_all_holdings.csv", index=False)

    monkeypatch.setattr("src.analysis.cross_source.RAW", str(raw_dir))

    form_pf_concentration = pd.DataFrame(
        {
            "top_n": ["Top 10"] * 4,
            "quarter": ["2024Q1", "2024Q2", "2024Q3", "2024Q4"],
            "nav_share": [0.10, 0.20, 0.30, 0.40],
        }
    )

    result = run_h7_concentration_correlation(
        {
            "form_pf_concentration": form_pf_concentration,
        }
    )

    assert result["result"] in {"PASS", "FAIL"}
    assert "lacks required columns" not in result["interpretation"]
    assert "lacks fund column" not in result["interpretation"]
