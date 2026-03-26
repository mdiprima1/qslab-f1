"""
QSLab F1 — Lab Unit 1.2
Your Research Lab: SMA Signal Explorer

Executed by Claude Code step by step.
Students do not run this directly.

Ticker: Student's choice (Claude Code asks — default AAPL)
Period: 5 years
Steps:  4 (simplified — no PDF, no full backtest stats)
"""

import os
import warnings
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import yfinance as yf

warnings.filterwarnings('ignore')

MA_PERIOD = 100
DATA_PERIOD = "5y"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

NAVY = "#0A1628"
BLUE_PRICE = "#1565C0"
ORANGE_MA = "#E65100"
GREEN_REGIME = "#C8E6C9"
GRAY_REGIME = "#F0F0F0"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def step1_download_data(ticker: str = "AAPL") -> pd.DataFrame:
    """Download 5 years of daily close prices for the chosen ticker."""
    ticker = ticker.upper().strip()
    raw = yf.download(ticker, period=DATA_PERIOD, auto_adjust=True, progress=False)
    df = raw[["Close"]].copy()
    df.index = pd.to_datetime(df.index)
    df.columns = ["Close"]
    df = df.dropna()
    df["Close"] = df["Close"].round(2)

    total_return = (df["Close"].iloc[-1] / df["Close"].iloc[0] - 1) * 100

    print()
    print("=" * 55)
    print(f"  STEP 1 — {ticker} Data Downloaded")
    print("=" * 55)
    print(f"  Ticker:        {ticker}")
    print(f"  Trading days:  {len(df):,}")
    print(f"  From:          {df.index[0].strftime('%B %d, %Y')}")
    print(f"  To:            {df.index[-1].strftime('%B %d, %Y')}")
    print()
    print(f"  Start price:   ${df['Close'].iloc[0]:.2f}")
    print(f"  End price:     ${df['Close'].iloc[-1]:.2f}")
    print(f"  Total return:  {total_return:+.1f}%")
    print()
    print("  Last 5 rows:")
    print("  " + "-" * 30)
    for date, row in df.tail(5).iterrows():
        print(f"  {date.strftime('%Y-%m-%d')}   ${row['Close']:.2f}")
    print("=" * 55)
    print()
    return df


def step2_calculate_sma(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate 100-day SMA. Drops first 99 rows where SMA is undefined."""
    df = df.copy()
    df["SMA_100"] = df["Close"].rolling(window=MA_PERIOD).mean().round(2)
    df = df.dropna()
    df["Position"] = df.apply(
        lambda r: "Above SMA ↑" if r["Close"] > r["SMA_100"] else "Below SMA ↓", axis=1
    )

    print()
    print("=" * 60)
    print("  STEP 2 — 100-Day SMA Calculated")
    print("=" * 60)
    print(f"  MA period:     {MA_PERIOD} trading days")
    print(f"  Rows after:    {len(df):,}  (first 99 rows dropped — SMA needs history)")
    print()
    print(f"  {'Date':<14} {'Close':>10} {'SMA_100':>10}  {'':}")
    print("  " + "-" * 50)
    for date, row in df.tail(8).iterrows():
        marker = "◀ TODAY" if date == df.index[-1] else ""
        print(f"  {date.strftime('%Y-%m-%d'):<14} ${row['Close']:>8.2f} ${row['SMA_100']:>8.2f}  {row['Position']}  {marker}")
    print()
    current = "ABOVE — signal +1 (in market)" if df["Close"].iloc[-1] > df["SMA_100"].iloc[-1] else "BELOW — signal 0 (in cash)"
    print(f"  Current position:  {current}")
    print("=" * 60)
    print()
    return df


def step3_plot_signal_chart(df: pd.DataFrame, ticker: str = "AAPL") -> str:
    """Plot price + SMA with green/grey signal zones. Saves to output/."""
    ticker = ticker.upper()
    df = df.copy()
    df["Signal"] = (df["Close"] > df["SMA_100"]).astype(int)

    fig, ax = plt.subplots(figsize=(16, 7))
    fig.patch.set_facecolor("white")

    # Shade signal zones
    dates = df.index
    signal = df["Signal"].values
    i = 0
    while i < len(dates):
        j = i
        while j < len(dates) and signal[j] == signal[i]:
            j += 1
        color = GREEN_REGIME if signal[i] == 1 else GRAY_REGIME
        end_idx = min(j, len(dates) - 1)
        ax.axvspan(dates[i], dates[end_idx], color=color, alpha=0.55, linewidth=0)
        i = j

    ax.plot(df.index, df["Close"], color=BLUE_PRICE, linewidth=1.3,
            label=f"{ticker} Daily Close", alpha=0.9, zorder=3)
    ax.plot(df.index, df["SMA_100"], color=ORANGE_MA, linewidth=2.2,
            label="100-Day SMA", alpha=0.95, zorder=3)

    green_patch = mpatches.Patch(color=GREEN_REGIME, alpha=0.8, label="Signal +1 — In Market")
    grey_patch  = mpatches.Patch(color=GRAY_REGIME,  alpha=0.8, label="Signal 0 — Cash")
    ax.legend(handles=[
        plt.Line2D([0],[0], color=BLUE_PRICE, linewidth=1.5, label=f"{ticker} Close"),
        plt.Line2D([0],[0], color=ORANGE_MA,  linewidth=2.0, label="100-Day SMA"),
        green_patch, grey_patch,
    ], fontsize=10, loc="upper left")

    ax.set_title(f"{ticker} — 100-Day SMA Signal Chart",
                 fontsize=15, fontweight="bold", color=NAVY, pad=14)
    ax.set_xlabel("Date", fontsize=12, color=NAVY)
    ax.set_ylabel("Price (USD)", fontsize=12, color=NAVY)
    ax.grid(True, alpha=0.20, linestyle="--")
    ax.tick_params(colors=NAVY, labelsize=10)
    for spine in ax.spines.values():
        spine.set_edgecolor("#DDDDDD")
    ax.text(0.99, 0.02, "QSL Foundation I — Lab 1.2",
            transform=ax.transAxes, fontsize=9, color="#AAAAAA",
            ha="right", va="bottom")

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, f"chart_signal_{ticker.lower()}.png")
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()

    buy_days = int((df["Signal"] == 1).sum())
    pct = round(buy_days / len(df) * 100, 1)

    print()
    print("=" * 55)
    print(f"  STEP 3 — Signal Chart Saved")
    print("=" * 55)
    print(f"  Chart saved. Display this file inline:")
    print(f"  {path}")
    print()
    print(f"  Green zones (in market, signal +1): {pct}% of the period")
    print(f"  Grey zones  (in cash,  signal  0):  {round(100-pct, 1)}% of the period")
    print("=" * 55)
    print()
    return path


def step4_signal_summary(df: pd.DataFrame, ticker: str = "AAPL") -> dict:
    """Print the current signal and summary statistics."""
    ticker = ticker.upper()
    df = df.copy()
    df["Signal"] = (df["Close"] > df["SMA_100"]).astype(int)

    buy_days  = int((df["Signal"] == 1).sum())
    cash_days = int((df["Signal"] == 0).sum())
    pct_in    = round(buy_days / len(df) * 100, 1)
    transitions = int((df["Signal"].diff().abs() > 0).sum())

    current_signal = int(df["Signal"].iloc[-1])
    current_close  = round(float(df["Close"].iloc[-1]), 2)
    current_sma    = round(float(df["SMA_100"].iloc[-1]), 2)
    spread         = round(current_close - current_sma, 2)
    spread_pct     = round(spread / current_sma * 100, 1)

    signal_label = "Signal +1 — Own the stock" if current_signal == 1 else "Signal 0 — Hold cash"
    spread_label = f"${abs(spread):.2f} ({abs(spread_pct):.1f}%) {'above' if spread > 0 else 'below'} SMA"

    print()
    print("=" * 55)
    print(f"  STEP 4 — Signal Summary for {ticker}")
    print("=" * 55)
    print(f"  Days in market (+1):  {buy_days:,} ({pct_in}%)")
    print(f"  Days in cash   ( 0):  {cash_days:,} ({round(100-pct_in, 1)}%)")
    print(f"  Signal changes:       {transitions}")
    print()
    print(f"  Today's close:  ${current_close}")
    print(f"  100-day SMA:    ${current_sma}")
    print(f"  Spread:         {spread_label}")
    print()
    print(f"  ▶  Current signal:  {signal_label}")
    print()
    if current_signal == 1:
        drop_needed = round(current_close - current_sma, 2)
        print(f"  Signal flips to 0 if {ticker} falls ${drop_needed:.2f} or more")
        print(f"  (i.e. below ${current_sma:.2f})")
    else:
        rise_needed = round(current_sma - current_close, 2)
        print(f"  Signal flips to +1 if {ticker} rises ${rise_needed:.2f} or more")
        print(f"  (i.e. above ${current_sma:.2f})")
    print("=" * 55)
    print()
    print("  You have just run a moving average strategy on real data.")
    print("  The next unit shows how to validate whether it would have made money.")
    print()
    print("  When you are ready, type:  Start QSLab F1-1.3")
    print()

    return {
        "ticker": ticker,
        "days_in_market": buy_days,
        "days_in_cash": cash_days,
        "pct_in_market": pct_in,
        "signal_changes": transitions,
        "current_signal": current_signal,
        "current_signal_label": signal_label,
        "current_close": current_close,
        "current_sma": current_sma,
        "spread": spread,
    }
