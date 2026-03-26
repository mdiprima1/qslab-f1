"""
QSLab F1 — Lab Unit 1.2
Your Research Lab: SMA Signal Explorer

Runs automatically from start to finish.
No pauses between steps.
One PDF at the end covering all results.

Ticker: Student's choice (default: AAPL)
MA period: Student's choice (default: 100)
Period: 20 years
"""

import os
import warnings

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import yfinance as yf

from pdf_generator import generate_session_pdf, OUTPUT_DIR

warnings.filterwarnings('ignore')

START_DATE   = "2005-01-01"
NAVY         = "#0A1628"
BLUE_PRICE   = "#1565C0"
ORANGE_MA    = "#E65100"
GREEN_REGIME = "#C8E6C9"
GRAY_REGIME  = "#F0F0F0"


def _progress(step: int, total: int, label: str):
    """Print a clean progress line between steps."""
    bar = "█" * step + "░" * (total - step)
    print(f"\n  [{bar}] Step {step}/{total} — {label}\n")


def step1_download_data(ticker: str = "AAPL") -> pd.DataFrame:
    ticker = ticker.upper().strip()
    raw = yf.download(ticker, start=START_DATE, auto_adjust=True, progress=False)
    df = raw[["Close"]].copy()
    df.index = pd.to_datetime(df.index)
    df.columns = ["Close"]
    df = df.dropna()
    df["Close"] = df["Close"].round(2)

    total_return = (df["Close"].iloc[-1] / df["Close"].iloc[0] - 1) * 100

    print(f"  Ticker:        {ticker}")
    print(f"  Trading days:  {len(df):,}")
    print(f"  From:          {df.index[0].strftime('%B %d, %Y')}")
    print(f"  To:            {df.index[-1].strftime('%B %d, %Y')}")
    print(f"  Start price:   ${df['Close'].iloc[0]:.2f}")
    print(f"  End price:     ${df['Close'].iloc[-1]:.2f}")
    print(f"  Total return:  {total_return:+.1f}%")

    return df


def step2_calculate_sma(df: pd.DataFrame, ticker: str, ma_period: int) -> pd.DataFrame:
    ticker = ticker.upper()
    col = f"SMA_{ma_period}"
    df = df.copy()
    df[col] = df["Close"].rolling(window=ma_period).mean().round(2)
    df = df.dropna()
    df["Position"] = df.apply(
        lambda r: "Above SMA" if r["Close"] > r[col] else "Below SMA", axis=1
    )

    current = "ABOVE — signal +1 (in market)" if df["Close"].iloc[-1] > df[col].iloc[-1] \
              else "BELOW — signal 0 (in cash)"
    print(f"  {ma_period}-day SMA calculated over {len(df):,} trading days")
    print(f"  Current position: {current}")

    return df


def step3_plot_signal_chart(df: pd.DataFrame, ticker: str, ma_period: int) -> str:
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
        ax.axvspan(dates[i], dates[min(j, len(dates)-1)],
                   color=color, alpha=0.55, linewidth=0)
        i = j

    ax.plot(df.index, df["Close"], color=BLUE_PRICE, linewidth=1.3, alpha=0.9, zorder=3)
    ax.plot(df.index, df[col],     color=ORANGE_MA,  linewidth=2.2, alpha=0.95, zorder=3)

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
    path = os.path.join(OUTPUT_DIR, f"chart_{ticker.lower()}_{ma_period}d.png")
    plt.savefig(path, dpi=220, bbox_inches="tight")
    plt.close()

    buy_days = int((df["Signal"] == 1).sum())
    pct = round(buy_days / len(df) * 100, 1)
    print(f"  Signal chart saved")
    print(f"  Green (in market): {pct}%  |  Grey (cash): {round(100-pct,1)}%")

    return path, pct


def step4_signal_summary(df: pd.DataFrame, ticker: str, ma_period: int) -> dict:
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
    signal_label   = "Signal +1 — Own the stock" if current_signal == 1 else "Signal 0 — Hold cash"

    print(f"  Days in market: {buy_days:,} ({pct_in}%)")
    print(f"  Days in cash:   {cash_days:,} ({round(100-pct_in,1)}%)")
    print(f"  Signal changes: {transitions}")
    print(f"  Current signal: {signal_label}")
    if current_signal == 1:
        print(f"  Flip to 0 if price falls ${abs(spread):.2f} (below ${current_sma:.2f})")
    else:
        print(f"  Flip to +1 if price rises ${abs(spread):.2f} (above ${current_sma:.2f})")

    return {
        "ticker": ticker, "ma_period": ma_period,
        "days_in_market": buy_days, "days_in_cash": cash_days,
        "pct_in_market": pct_in, "signal_changes": transitions,
        "current_signal": current_signal, "current_signal_label": signal_label,
        "current_close": current_close, "current_sma": current_sma, "spread": spread,
    }


def run_lab(ticker: str, ma_period: int):
    """Run all 4 steps automatically, then generate one PDF."""

    print()
    print("=" * 55)
    print(f"  QSLab F1-1.2 — Your Research Lab")
    print(f"  {ticker.upper()}  /  {ma_period}-Day SMA  /  20 years")
    print("=" * 55)

    _progress(1, 4, "Downloading data")
    df_raw = step1_download_data(ticker)

    _progress(2, 4, "Calculating SMA")
    df = step2_calculate_sma(df_raw, ticker, ma_period)

    _progress(3, 4, "Plotting signal chart")
    chart_path, pct_in = step3_plot_signal_chart(df, ticker, ma_period)

    _progress(4, 4, "Reading the signal")
    result = step4_signal_summary(df, ticker, ma_period)

    print()
    print("  " + "─" * 53)
    print("  All steps complete. Generating your research report...")
    print("  " + "─" * 53)

    # Collect all data for the single PDF
    total_return = round((df_raw["Close"].iloc[-1] / df_raw["Close"].iloc[0] - 1) * 100, 1)
    session_data = {
        "ticker": ticker.upper(),
        "ma_period": ma_period,
        "start_date": df_raw.index[0].strftime("%B %d, %Y"),
        "end_date": df_raw.index[-1].strftime("%B %d, %Y"),
        "trading_days": len(df_raw),
        "start_price": round(float(df_raw["Close"].iloc[0]), 2),
        "end_price": round(float(df_raw["Close"].iloc[-1]), 2),
        "total_return": total_return,
        "df_tail": df.tail(8),
        "chart_path": chart_path,
        "pct_in_market": pct_in,
        "signal_result": result,
    }

    pdf_path = generate_session_pdf(session_data)

    print()
    print("=" * 55)
    print(f"  Research report saved:")
    print(f"  {pdf_path}")
    print("=" * 55)
    print()
    print("  Want to run the same analysis on a different stock?")
    print("  Type a ticker symbol (e.g. MSFT, NVDA, TSLA, SPY)")
    print("  or press Enter to finish.")
    print()

    return session_data
