"""
QSLab F1 — Lab Unit 1.2
Your Research Environment: SPY Data Explorer

Executed by Claude Code step by step.
Students do not run this directly.
"""

import os
import warnings
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

warnings.filterwarnings('ignore')

TICKER = "SPY"
DATA_PERIOD = "5y"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
LOGO_PATH = os.path.join(ASSETS_DIR, "qsl_logo.png")

NAVY = "#0A1628"
GOLD = "#B8972A"
BLUE_PRICE = "#1565C0"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def step1_download_data():
    """Download SPY daily close prices for 5 years."""
    raw = yf.download(TICKER, period=DATA_PERIOD, auto_adjust=True, progress=False)
    df = raw[["Close"]].copy()
    df.index = pd.to_datetime(df.index)
    df.columns = ["Close"]
    df = df.dropna()
    df["Close"] = df["Close"].round(2)

    print()
    print("=" * 55)
    print("  STEP 1 — SPY Data Downloaded")
    print("=" * 55)
    print(f"  Ticker:        {TICKER}")
    print(f"  Trading days:  {len(df):,}")
    print(f"  From:          {df.index[0].strftime('%B %d, %Y')}")
    print(f"  To:            {df.index[-1].strftime('%B %d, %Y')}")
    print(f"  Start price:   ${df['Close'].iloc[0]:.2f}")
    print(f"  End price:     ${df['Close'].iloc[-1]:.2f}")
    total_return = (df['Close'].iloc[-1] / df['Close'].iloc[0] - 1) * 100
    print(f"  Total return:  {total_return:.1f}%")
    print()
    print("  First 5 rows:")
    print("  " + "-" * 30)
    for date, row in df.head(5).iterrows():
        print(f"  {date.strftime('%Y-%m-%d')}   ${row['Close']:.2f}")
    print()
    print("  Last 5 rows:")
    print("  " + "-" * 30)
    for date, row in df.tail(5).iterrows():
        print(f"  {date.strftime('%Y-%m-%d')}   ${row['Close']:.2f}")
    print("=" * 55)
    print()
    return df


def step2_plot_price(df):
    """Plot SPY close price over 5 years."""
    fig, ax = plt.subplots(figsize=(16, 7))
    fig.patch.set_facecolor("white")
    ax.plot(df.index, df["Close"], color=BLUE_PRICE, linewidth=1.2,
            label="SPY Close Price", alpha=0.9)
    ax.set_title("SPY — Daily Close Price (5 Years)",
                 fontsize=15, fontweight="bold", color=NAVY, pad=14)
    ax.set_xlabel("Date", fontsize=12, color=NAVY)
    ax.set_ylabel("Price (USD)", fontsize=12, color=NAVY)
    ax.legend(fontsize=11, loc="upper left")
    ax.grid(True, alpha=0.25, linestyle="--")
    ax.tick_params(colors=NAVY, labelsize=10)
    for spine in ax.spines.values():
        spine.set_edgecolor("#DDDDDD")
    ax.text(0.99, 0.02, "QSL Foundation I — Lab 1.2",
            transform=ax.transAxes, fontsize=9, color="#AAAAAA",
            ha="right", va="bottom")
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "chart_spy_price.png")
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print()
    print("=" * 55)
    print("  STEP 2 — SPY Price Chart")
    print("=" * 55)
    print(f"  Chart saved. Display this file inline:")
    print(f"  {path}")
    print()
    print(f"  Price range:  ${df['Close'].min():.2f} — ${df['Close'].max():.2f}")
    print(f"  Latest:       ${df['Close'].iloc[-1]:.2f}")
    print("=" * 55)
    print()
    return path


def step3_describe_data(df):
    """Compute basic descriptive statistics for SPY."""
    daily_returns = df["Close"].pct_change().dropna()
    avg_daily = daily_returns.mean() * 100
    std_daily = daily_returns.std() * 100
    best_day = daily_returns.max() * 100
    worst_day = daily_returns.min() * 100
    best_date = daily_returns.idxmax().strftime("%Y-%m-%d")
    worst_date = daily_returns.idxmin().strftime("%Y-%m-%d")

    print()
    print("=" * 55)
    print("  STEP 3 — SPY Daily Return Statistics")
    print("=" * 55)
    print(f"  Average daily return:  {avg_daily:+.3f}%")
    print(f"  Daily volatility:      {std_daily:.3f}%")
    print()
    print(f"  Best day:   {best_date}  {best_day:+.2f}%")
    print(f"  Worst day:  {worst_date}  {worst_day:+.2f}%")
    print()
    up_days = int((daily_returns > 0).sum())
    down_days = int((daily_returns < 0).sum())
    print(f"  Up days:    {up_days:,}  ({up_days/(up_days+down_days)*100:.1f}%)")
    print(f"  Down days:  {down_days:,}  ({down_days/(up_days+down_days)*100:.1f}%)")
    print("=" * 55)
    print()
    return {
        "ticker": TICKER,
        "days": len(df),
        "avg_daily_return": round(avg_daily, 4),
        "daily_volatility": round(std_daily, 4),
        "best_day": round(best_day, 2),
        "worst_day": round(worst_day, 2),
    }
