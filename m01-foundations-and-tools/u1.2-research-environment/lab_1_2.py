"""
QSLab F1 — Lab Unit 1.2
Your Research Lab: SMA Signal Explorer

Executed by Claude Code step by step.
Students do not run this directly.

Ticker: Student's choice (default: AAPL)
MA period: Student's choice (default: 100 — try 50 or 200)
Period: 20 years
Steps: 4 + rerun option
"""

import os
import warnings

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import yfinance as yf

from pdf_generator import (
    generate_step1_pdf,
    generate_step2_pdf,
    generate_step3_pdf,
    generate_step4_pdf,
    generate_rerun_pdf,
)

warnings.filterwarnings('ignore')

START_DATE   = "2005-01-01"
OUTPUT_DIR   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
NAVY         = "#0A1628"
BLUE_PRICE   = "#1565C0"
ORANGE_MA    = "#E65100"
GREEN_REGIME = "#C8E6C9"
GRAY_REGIME  = "#F0F0F0"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def step1_download_data(ticker: str = "AAPL") -> pd.DataFrame:
    """Download 20 years of daily close prices for the chosen ticker."""
    ticker = ticker.upper().strip()
    raw = yf.download(ticker, start=START_DATE, auto_adjust=True, progress=False)
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
    generate_step1_pdf(df, ticker)
    return df


def step2_calculate_sma(df: pd.DataFrame, ticker: str = "AAPL", ma_period: int = 100) -> pd.DataFrame:
    """Calculate SMA for the given period. Drops initial rows where SMA is undefined."""
    ticker = ticker.upper()
    col = f"SMA_{ma_period}"
    df = df.copy()
    df[col] = df["Close"].rolling(window=ma_period).mean().round(2)
    df = df.dropna()
    df["Position"] = df.apply(
        lambda r: "Above SMA ↑" if r["Close"] > r[col] else "Below SMA ↓", axis=1
    )

    print()
    print("=" * 60)
    print(f"  STEP 2 — {ma_period}-Day SMA Calculated")
    print("=" * 60)
    print(f"  MA period:     {ma_period} trading days")
    print(f"  Rows after:    {len(df):,}  (first {ma_period-1} rows dropped)")
    print()
    print(f"  {'Date':<14} {'Close':>10} {col:>12}  Position")
    print("  " + "-" * 55)
    for date, row in df.tail(8).iterrows():
        marker = "◀ TODAY" if date == df.index[-1] else ""
        print(f"  {date.strftime('%Y-%m-%d'):<14} ${row['Close']:>8.2f} ${row[col]:>10.2f}  {row['Position']}  {marker}")
    print()
    current = "ABOVE — signal +1 (in market)" if df["Close"].iloc[-1] > df[col].iloc[-1] else "BELOW — signal 0 (in cash)"
    print(f"  Current position:  {current}")
    print("=" * 60)
    print()
    generate_step2_pdf(df, ticker, ma_period)
    return df


def step3_plot_signal_chart(df: pd.DataFrame, ticker: str = "AAPL", ma_period: int = 100) -> str:
    """Plot price + SMA with green/grey signal zones. Saves to output/."""
    ticker = ticker.upper()
    col = f"SMA_{ma_period}"
    df = df.copy()
    df["Signal"] = (df["Close"] > df[col]).astype(int)

    fig, ax = plt.subplots(figsize=(18, 8))
    fig.patch.set_facecolor("white")

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

    ax.plot(df.index, df["Close"], color=BLUE_PRICE, linewidth=1.3, alpha=0.9, zorder=3)
    ax.plot(df.index, df[col], color=ORANGE_MA, linewidth=2.2, alpha=0.95, zorder=3)

    green_patch = mpatches.Patch(color=GREEN_REGIME, alpha=0.8, label="Signal +1 — In Market")
    grey_patch  = mpatches.Patch(color=GRAY_REGIME,  alpha=0.8, label="Signal 0 — Cash")
    ax.legend(handles=[
        plt.Line2D([0],[0], color=BLUE_PRICE, linewidth=1.5, label=f"{ticker} Close"),
        plt.Line2D([0],[0], color=ORANGE_MA,  linewidth=2.0, label=f"{ma_period}-Day SMA"),
        green_patch, grey_patch,
    ], fontsize=10, loc="upper left")

    ax.set_title(f"{ticker} — {ma_period}-Day SMA Signal Chart",
                 fontsize=15, fontweight="bold", color=NAVY, pad=14)
    ax.set_xlabel("Date", fontsize=12, color=NAVY)
    ax.set_ylabel("Price (USD)", fontsize=12, color=NAVY)
    ax.grid(True, alpha=0.20, linestyle="--")
    ax.tick_params(colors=NAVY, labelsize=10)
    for spine in ax.spines.values():
        spine.set_edgecolor("#DDDDDD")
    ax.text(0.99, 0.02, "QSL Foundation I — Lab 1.2",
            transform=ax.transAxes, fontsize=9, color="#AAAAAA", ha="right", va="bottom")

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, f"chart_signal_{ticker.lower()}_{ma_period}d.png")
    plt.savefig(path, dpi=220, bbox_inches="tight")
    plt.close()

    buy_days = int((df["Signal"] == 1).sum())
    pct = round(buy_days / len(df) * 100, 1)

    print()
    print("=" * 55)
    print(f"  STEP 3 — Signal Chart")
    print("=" * 55)
    print(f"  Chart saved: {path}")
    print()
    print(f"  Green zones (signal +1, in market): {pct}%")
    print(f"  Grey zones  (signal  0, in cash):   {round(100-pct,1)}%")
    print("=" * 55)
    print()
    generate_step3_pdf(path, ticker, ma_period, pct)
    return path


def step4_signal_summary(df: pd.DataFrame, ticker: str = "AAPL", ma_period: int = 100) -> dict:
    """Print the current signal and summary statistics."""
    ticker = ticker.upper()
    col = f"SMA_{ma_period}"
    df = df.copy()
    df["Signal"] = (df["Close"] > df[col]).astype(int)

    buy_days    = int((df["Signal"] == 1).sum())
    cash_days   = int((df["Signal"] == 0).sum())
    pct_in      = round(buy_days / len(df) * 100, 1)
    transitions = int((df["Signal"].diff().abs() > 0).sum())

    current_signal = int(df["Signal"].iloc[-1])
    current_close  = round(float(df["Close"].iloc[-1]), 2)
    current_sma    = round(float(df[col].iloc[-1]), 2)
    spread         = round(current_close - current_sma, 2)
    spread_pct     = round(spread / current_sma * 100, 1)

    signal_label = "Signal +1 — Own the stock" if current_signal == 1 else "Signal 0 — Hold cash"
    spread_label = f"${abs(spread):.2f} ({abs(spread_pct):.1f}%) {'above' if spread > 0 else 'below'} SMA"

    print()
    print("=" * 55)
    print(f"  STEP 4 — Signal Summary for {ticker}")
    print("=" * 55)
    print(f"  Days in market (+1):  {buy_days:,} ({pct_in}%)")
    print(f"  Days in cash   ( 0):  {cash_days:,} ({round(100-pct_in,1)}%)")
    print(f"  Signal changes:       {transitions}")
    print()
    print(f"  Today's close:  ${current_close}")
    print(f"  {ma_period}-day SMA:    ${current_sma}")
    print(f"  Spread:         {spread_label}")
    print()
    print(f"  ▶  Current signal:  {signal_label}")
    print()
    if current_signal == 1:
        print(f"  Signal flips to 0 if {ticker} falls ${abs(spread):.2f} or more (below ${current_sma:.2f})")
    else:
        print(f"  Signal flips to +1 if {ticker} rises ${abs(spread):.2f} or more (above ${current_sma:.2f})")
    print("=" * 55)
    print()

    result = {
        "ticker": ticker, "ma_period": ma_period,
        "days_in_market": buy_days, "days_in_cash": cash_days,
        "pct_in_market": pct_in, "signal_changes": transitions,
        "current_signal": current_signal, "current_signal_label": signal_label,
        "current_close": current_close, "current_sma": current_sma, "spread": spread,
    }
    generate_step4_pdf(result, ticker, ma_period)
    return result


def rerun_prompt(df_raw: pd.DataFrame, ticker: str, original_period: int, original_transitions: int):
    """Offer the student a rerun with a different MA period."""
    print()
    print("  " + "─" * 53)
    print("  Want to see how the chart changes with a different period?")
    print(f"  You just used a {original_period}-day SMA.")
    print("  Try 50 (more signals) or 200 (fewer signals).")
    print()
    print("  Type a new MA period and press Enter, or press Enter to finish:")
    print("  " + "─" * 53)


def run_rerun(df_raw: pd.DataFrame, ticker: str, new_period: int,
              original_period: int, original_transitions: int):
    """Rerun steps 2-4 with a new MA period and generate comparison PDF."""
    # Run new period
    df2 = step2_calculate_sma(df_raw, ticker=ticker, ma_period=new_period)
    step3_plot_signal_chart(df2, ticker=ticker, ma_period=new_period)
    result_new = step4_signal_summary(df2, ticker=ticker, ma_period=new_period)

    # Rebuild original period result for comparison PDF
    col_orig = f"SMA_{original_period}"
    df_orig = df_raw.copy()
    df_orig[col_orig] = df_orig["Close"].rolling(window=original_period).mean().round(2)
    df_orig = df_orig.dropna()
    df_orig["Signal"] = (df_orig["Close"] > df_orig[col_orig]).astype(int)

    buy_orig = int((df_orig["Signal"] == 1).sum())
    result_orig = {
        "ticker": ticker.upper(), "ma_period": original_period,
        "days_in_market": buy_orig, "days_in_cash": len(df_orig) - buy_orig,
        "pct_in_market": round(buy_orig / len(df_orig) * 100, 1),
        "signal_changes": original_transitions,
        "current_signal": int(df_orig["Signal"].iloc[-1]),
        "current_signal_label": "Signal +1 — Own the stock" if df_orig["Signal"].iloc[-1] == 1 else "Signal 0 — Hold cash",
        "current_close": round(float(df_orig["Close"].iloc[-1]), 2),
        "current_sma": round(float(df_orig[col_orig].iloc[-1]), 2),
        "spread": round(float(df_orig["Close"].iloc[-1]) - float(df_orig[col_orig].iloc[-1]), 2),
    }

    new_transitions = result_new["signal_changes"]
    print()
    print("  " + "─" * 53)
    print(f"  {original_period}-day SMA: {original_transitions} signal changes")
    print(f"  {new_period}-day SMA: {new_transitions} signal changes")
    print("  Same stock. Different rule. Different result.")
    print("  " + "─" * 53)
    print()
    generate_rerun_pdf(result_orig, result_new, ticker, original_period, new_period)


def print_closing():
    """Print the closing message and Unit 1.3 forward hook."""
    print("  You have run a moving average strategy on real data.")
    print("  The next unit shows how to validate whether it would have made money")
    print("  properly — with real costs and professional data.")
    print()
    print("  When you are ready, type:  Start QSLab F1-1.3")
    print()
