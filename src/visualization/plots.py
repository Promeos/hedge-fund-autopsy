"""Matplotlib/seaborn chart functions for hedge fund analysis."""

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns


# ---------------------------------------------------------------------------
# Style defaults
# ---------------------------------------------------------------------------

COLORS = {
    'dark': '#2c3e50',
    'blue': '#2980b9',
    'light_blue': '#3498db',
    'red': '#e74c3c',
    'dark_red': '#c0392b',
    'green': '#27ae60',
    'light_green': '#2ecc71',
    'orange': '#f39c12',
    'light_orange': '#e67e22',
    'purple': '#8e44ad',
    'light_purple': '#9b59b6',
    'teal': '#1abc9c',
}

MARKET_EVENTS = {
    '2018-02-01': 'Volmageddon',
    '2020-03-01': 'COVID Crash',
    '2021-01-01': 'GameStop\nSqueeze',
    '2022-03-01': 'Fed Rate\nHikes Begin',
}


def setup_style():
    """Apply default plotting style."""
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['figure.figsize'] = (14, 6)
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def add_event_annotations(ax, ypos_frac=0.95):
    """Add vertical lines for key market events."""
    ylim = ax.get_ylim()
    ypos = ylim[0] + (ylim[1] - ylim[0]) * ypos_frac
    for date_str, label in MARKET_EVENTS.items():
        date = pd.Timestamp(date_str)
        try:
            ax.axvline(date, color='gray', linestyle='--', alpha=0.5, linewidth=0.8)
            ax.text(date, ypos, label, ha='center', va='top', fontsize=8,
                    color='gray', style='italic')
        except Exception:
            pass


def _save(fig, save_path):
    """Save figure if path is provided."""
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight', dpi=150)


# ---------------------------------------------------------------------------
# Chart functions
# ---------------------------------------------------------------------------

def plot_total_assets(df, save_path=None):
    """Total assets with QoQ growth bars (dual axis)."""
    fig, ax1 = plt.subplots(figsize=(14, 6))

    ax1.plot(df.index, df['Total assets'], color=COLORS['dark'], linewidth=2.5, label='Total Assets')
    ax1.fill_between(df.index, df['Total assets'], alpha=0.1, color=COLORS['dark'])
    ax1.set_ylabel('Total Assets ($B)', color=COLORS['dark'])

    ax2 = ax1.twinx()
    colors = [COLORS['green'] if x >= 0 else COLORS['red'] for x in df['total_assets_qoq'].fillna(0)]
    ax2.bar(df.index, df['total_assets_qoq'] * 100, width=60, alpha=0.4, color=colors, label='QoQ Growth %')
    ax2.set_ylabel('QoQ Growth (%)', color='#7f8c8d')
    ax2.axhline(0, color='gray', linewidth=0.5)

    add_event_annotations(ax1)
    ax1.set_title('Hedge Fund Industry — Total Assets & Quarterly Growth')
    fig.legend(loc='upper left', bbox_to_anchor=(0.12, 0.88))
    plt.tight_layout()
    _save(fig, save_path)
    plt.show()


def plot_asset_composition(df, save_path=None):
    """Stacked area chart of asset composition."""
    asset_cols = {
        'Corporate equities; asset': 'Corporate Equities',
        'Total debt securities; asset': 'Debt Securities',
        'Total loans; asset': 'Loans',
        'Security repurchase agreements; asset': 'Repo Agreements',
        'Miscellaneous assets; asset': 'Misc Assets',
    }
    df_plot = df.copy()
    df_plot['Cash & equivalents'] = (
        df_plot['Deposits; asset']
        + df_plot['Other cash and cash equivalents; asset']
        + df_plot['Money market fund shares; asset']
    )
    cols_to_stack = list(asset_cols.values()) + ['Cash & equivalents']
    rename_map = asset_cols.copy()
    df_plot = df_plot.rename(columns=rename_map)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

    # Absolute
    ax1.stackplot(df_plot.index, *[df_plot[c] for c in cols_to_stack],
                  labels=cols_to_stack, alpha=0.8)
    ax1.set_title('Asset Composition (Absolute, $B)')
    ax1.legend(loc='upper left', fontsize=9)
    add_event_annotations(ax1)

    # Proportional
    totals = df_plot[cols_to_stack].sum(axis=1)
    pct_data = df_plot[cols_to_stack].div(totals, axis=0) * 100
    ax2.stackplot(df_plot.index, *[pct_data[c] for c in cols_to_stack],
                  labels=cols_to_stack, alpha=0.8)
    ax2.set_title('Asset Composition (% of Total)')
    ax2.set_ylabel('%')
    add_event_annotations(ax2)

    plt.tight_layout()
    _save(fig, save_path)
    plt.show()


def plot_debt_securities(df, save_path=None):
    """Treasury vs corporate bond breakdown."""
    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(df.index, df['Treasury securities; asset'], linewidth=2,
            label='Treasury Securities', color=COLORS['blue'])
    ax.plot(df.index, df['Corporate and foreign bonds; asset'], linewidth=2,
            label='Corporate & Foreign Bonds', color=COLORS['red'])
    ax.fill_between(df.index, df['Treasury securities; asset'], alpha=0.1, color=COLORS['blue'])
    ax.fill_between(df.index, df['Corporate and foreign bonds; asset'], alpha=0.1, color=COLORS['red'])

    ax.set_title('Debt Securities Breakdown')
    ax.set_ylabel('$B')
    ax.legend()
    add_event_annotations(ax)
    plt.tight_layout()
    _save(fig, save_path)
    plt.show()


def plot_liability_structure(df, save_path=None):
    """Stacked liability composition + leverage ratio."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), height_ratios=[2, 1], sharex=True)

    liab_data = pd.DataFrame({
        'Repo Agreements': df['Total security repurchase agreements; liability'],
        'Prime Brokerage': df['Loans, total secured borrowing via prime brokerage; liability'],
        'Other Secured': df['Loans, total other secured borrowing; liability'],
        'Unsecured': df['Loans, total unsecured borrowing; liability'],
    })

    ax1.stackplot(df.index, *[liab_data[c] for c in liab_data.columns],
                  labels=liab_data.columns, alpha=0.8)
    ax1.set_title('Liability Structure')
    ax1.set_ylabel('$B')
    ax1.legend(loc='upper left')
    add_event_annotations(ax1)

    ax2.plot(df.index, df['leverage_ratio'], linewidth=2.5, color=COLORS['dark_red'])
    ax2.axhline(df['leverage_ratio'].mean(), color='gray', linestyle='--', alpha=0.5,
                label=f"Mean: {df['leverage_ratio'].mean():.2f}x")
    ax2.set_ylabel('Leverage Ratio (x)')
    ax2.legend()

    plt.tight_layout()
    _save(fig, save_path)
    plt.show()


def plot_balance_sheet_overview(df, save_path=None):
    """Three-line overlay — assets, liabilities, net assets."""
    fig, ax = plt.subplots(figsize=(14, 7))

    ax.plot(df.index, df['Total assets'], linewidth=2.5, label='Total Assets', color=COLORS['dark'])
    ax.plot(df.index, df['Total liabilities'], linewidth=2.5, label='Total Liabilities', color=COLORS['red'])
    ax.plot(df.index, df['Total net assets'], linewidth=2.5, label='Net Assets', color=COLORS['green'])

    ax.fill_between(df.index, df['Total liabilities'], df['Total assets'], alpha=0.05, color=COLORS['dark'])
    ax.fill_between(df.index, 0, df['Total net assets'], alpha=0.05, color=COLORS['green'])

    ax.set_title('Balance Sheet Overview — Assets vs Liabilities vs Net Assets')
    ax.set_ylabel('$B')
    ax.legend()
    add_event_annotations(ax)
    plt.tight_layout()
    _save(fig, save_path)
    plt.show()


def plot_derivative_exposure(df, save_path=None):
    """Derivative exposure with ratio to total assets."""
    fig, ax1 = plt.subplots(figsize=(14, 6))

    ax1.plot(df.index, df['Derivatives (long value)'], linewidth=2.5,
             color=COLORS['purple'], label='Derivatives (Long Value)')
    ax1.fill_between(df.index, df['Derivatives (long value)'], alpha=0.15, color=COLORS['purple'])
    ax1.set_ylabel('Derivatives ($B)', color=COLORS['purple'])

    ax2 = ax1.twinx()
    ax2.plot(df.index, df['derivative_to_assets'] * 100, linewidth=1.5,
             color=COLORS['light_orange'], linestyle='--', label='Derivatives / Total Assets (%)')
    ax2.set_ylabel('% of Total Assets', color=COLORS['light_orange'])

    add_event_annotations(ax1)
    ax1.set_title('Derivative Exposure')
    fig.legend(loc='upper left', bbox_to_anchor=(0.12, 0.88))
    plt.tight_layout()
    _save(fig, save_path)
    plt.show()


def plot_borrowing_patterns(df, save_path=None):
    """Domestic vs foreign borrowing side-by-side."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    ax1.plot(df.index, df['domestic_borrowing'], linewidth=2, label='Domestic', color=COLORS['blue'])
    ax1.plot(df.index, df['foreign_borrowing'], linewidth=2, label='Foreign', color=COLORS['red'])
    ax1.fill_between(df.index, df['domestic_borrowing'], alpha=0.1, color=COLORS['blue'])
    ax1.fill_between(df.index, df['foreign_borrowing'], alpha=0.1, color=COLORS['red'])
    ax1.set_title('Borrowing by Source (Absolute)')
    ax1.set_ylabel('$B')
    ax1.legend()
    add_event_annotations(ax1)

    ax2.plot(df.index, df['foreign_borrowing_share'] * 100, linewidth=2, color=COLORS['red'])
    ax2.fill_between(df.index, df['foreign_borrowing_share'] * 100, alpha=0.1, color=COLORS['red'])
    ax2.set_title('Foreign Borrowing Share (%)')
    ax2.set_ylabel('%')
    add_event_annotations(ax2)

    plt.tight_layout()
    _save(fig, save_path)
    plt.show()


def plot_correlation_heatmap(df, cols=None, save_path=None):
    """Correlation matrix heatmap of balance sheet components."""
    if cols is None:
        cols = ['Total assets', 'Total liabilities', 'Total net assets',
                'Corporate equities; asset', 'Total debt securities; asset',
                'Total loans; asset', 'Derivatives (long value)',
                'Security repurchase agreements; asset']

    available = [c for c in cols if c in df.columns]
    short_labels = [c.split(';')[0].replace('Total ', '') for c in available]

    fig, ax = plt.subplots(figsize=(10, 8))
    corr = df[available].corr()
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
                xticklabels=short_labels, yticklabels=short_labels, ax=ax)
    ax.set_title('Balance Sheet Component Correlations')
    plt.tight_layout()
    _save(fig, save_path)
    plt.show()
