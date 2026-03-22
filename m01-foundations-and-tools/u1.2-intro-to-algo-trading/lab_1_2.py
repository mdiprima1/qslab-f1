"""
QSLab F1 — Lab Unit 1.2
Introduction to Algorithmic Trading: AAPL 100-Day SMA Strategy

Executed by Claude Code step by step.
Students do not run this directly.
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

TICKER = "AAPL"
MA_PERIOD = 100
DATA_PERIOD = "10y"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
LOGO_PATH = os.path.join(ASSETS_DIR, "qsl_logo.png")

NAVY = "#0A1628"
GOLD = "#B8972A"
GREEN_REGIME = "#C8E6C9"
GRAY_REGIME = "#F0F0F0"
BLUE_PRICE = "#1565C0"
ORANGE_MA = "#E65100"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def step1_download_data():
    """Download AAPL daily close prices for 10 years."""
    raw = yf.download(TICKER, period=DATA_PERIOD, auto_adjust=True, progress=False)
    df = raw[["Close"]].copy()
    df.index = pd.to_datetime(df.index)
    df.columns = ["Close"]
    df = df.dropna()
    df["Close"] = df["Close"].round(2)

    print()
    print("=" * 55)
    print("  STEP 1 — AAPL Data Downloaded")
    print("=" * 55)
    print(f"  Ticker:        {TICKER}")
    print(f"  Trading days:  {len(df):,}")
    print(f"  From:          {df.index[0].strftime('%B %d, %Y')}")
    print(f"  To:            {df.index[-1].strftime('%B %d, %Y')}")
    print(f"  Start price:   ${df['Close'].iloc[0]:.2f}")
    print(f"  End price:     ${df['Close'].iloc[-1]:.2f}")
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


def step2_calculate_sma(df):
    """Add SMA-100 column. Drops first 99 rows where SMA is undefined."""
    df = df.copy()
    df["SMA_100"] = df["Close"].rolling(window=MA_PERIOD).mean().round(2)
    df = df.dropna()

    print()
    print("=" * 55)
    print("  STEP 2 — 100-Day SMA Calculated")
    print("=" * 55)
    print(f"  MA period:     {MA_PERIOD} trading days")
    print(f"  Rows after:    {len(df):,} (first 99 rows dropped)")
    print()
    print("  Latest 5 rows — Close + SMA_100:")
    print("  " + "-" * 44)
    print(f"  {'Date':<14} {'Close':>10} {'SMA_100':>10}")
    print("  " + "-" * 44)
    for date, row in df.tail(5).iterrows():
        diff = row['Close'] - row['SMA_100']
        flag = " (above)" if diff > 0 else " (below)"
        print(f"  {date.strftime('%Y-%m-%d'):<14} ${row['Close']:>8.2f} ${row['SMA_100']:>8.2f}{flag}")
    print("=" * 55)
    print()
    return df


def step3_plot_price_ma(df):
    """Plot AAPL close price and 100-day SMA. Saves to output/chart_price_ma.png."""
    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor("white")
    ax.plot(df.index, df["Close"], color=BLUE_PRICE, linewidth=1.0,
            label="AAPL Close Price", alpha=0.9)
    ax.plot(df.index, df["SMA_100"], color=ORANGE_MA, linewidth=1.8,
            label="100-Day SMA", alpha=0.95)
    ax.set_title("AAPL — Daily Close Price and 100-Day SMA",
                 fontsize=13, fontweight="bold", color=NAVY, pad=12)
    ax.set_xlabel("Date", fontsize=10, color=NAVY)
    ax.set_ylabel("Price (USD)", fontsize=10, color=NAVY)
    ax.legend(fontsize=10, loc="upper left")
    ax.grid(True, alpha=0.25, linestyle="--")
    ax.tick_params(colors=NAVY)
    for spine in ax.spines.values():
        spine.set_edgecolor("#DDDDDD")
    ax.text(0.99, 0.02, "QSL Foundation I — Lab 1.2",
            transform=ax.transAxes, fontsize=8, color="#AAAAAA",
            ha="right", va="bottom")
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "chart_price_ma.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    return path


def step4_generate_signals(df):
    """Apply SMA crossover rule: signal=1 (buy) when Close > SMA, else 0 (cash)."""
    df = df.copy()
    df["Signal"] = (df["Close"] > df["SMA_100"]).astype(int)

    buy_days = int(df["Signal"].sum())
    cash_days = len(df) - buy_days
    current = int(df["Signal"].iloc[-1])
    print()
    print("=" * 55)
    print("  STEP 4 — Strategy Rule")
    print("=" * 55)
    print("  Rule:")
    print("    Close > SMA_100  →  Signal +1  (own AAPL)")
    print("    Close <= SMA_100 →  Signal  0  (hold cash)")
    print()
    print(f"  Days with signal +1 (in market): {buy_days:,}")
    print(f"  Days with signal  0 (in cash):   {cash_days:,}")
    print(f"  Time in market: {buy_days/len(df)*100:.1f}%")
    print()
    label = "Signal +1 — Own AAPL" if current == 1 else "Signal 0 — Hold cash"
    print(f"  Current signal:  {label}")
    print()
    print("  Last 5 rows — Close, SMA, Signal:")
    print("  " + "-" * 50)
    print(f"  {'Date':<14} {'Close':>9} {'SMA_100':>9} {'Signal':>8}")
    print("  " + "-" * 50)
    for date, row in df.tail(5).iterrows():
        sig_label = "+1 buy" if row['Signal'] == 1 else " 0 cash"
        print(f"  {date.strftime('%Y-%m-%d'):<14} ${row['Close']:>7.2f} ${row['SMA_100']:>7.2f} {sig_label:>8}")
    print("=" * 55)
    print()
    return df


def step5_plot_regime(df):
    """Plot regime chart with green/gray background zones. Saves to output/chart_regime.png."""
    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor("white")
    dates = df.index
    signal = df["Signal"].values
    i = 0
    while i < len(dates):
        j = i
        while j < len(dates) and signal[j] == signal[i]:
            j += 1
        color = GREEN_REGIME if signal[i] == 1 else GRAY_REGIME
        ax.axvspan(dates[i], dates[min(j, len(dates) - 1)], color=color, alpha=0.6, linewidth=0)
        i = j
    ax.plot(df.index, df["Close"], color=BLUE_PRICE, linewidth=1.0,
            label="AAPL Close", alpha=0.9, zorder=3)
    ax.plot(df.index, df["SMA_100"], color=ORANGE_MA, linewidth=1.8,
            label="100-Day SMA", alpha=0.95, zorder=3)
    buy_patch = mpatches.Patch(color=GREEN_REGIME, alpha=0.8, label="Signal +1 — Own AAPL")
    cash_patch = mpatches.Patch(color=GRAY_REGIME, alpha=0.8, label="Signal 0 — Cash")
    ax.legend(handles=[
        plt.Line2D([0], [0], color=BLUE_PRICE, linewidth=1.5, label="AAPL Close"),
        plt.Line2D([0], [0], color=ORANGE_MA, linewidth=2.0, label="100-Day SMA"),
        buy_patch, cash_patch,
    ], fontsize=9, loc="upper left")
    ax.set_title("AAPL — SMA Crossover Strategy: Buy and Cash Regimes",
                 fontsize=13, fontweight="bold", color=NAVY, pad=12)
    ax.set_xlabel("Date", fontsize=10, color=NAVY)
    ax.set_ylabel("Price (USD)", fontsize=10, color=NAVY)
    ax.grid(True, alpha=0.20, linestyle="--")
    ax.tick_params(colors=NAVY)
    for spine in ax.spines.values():
        spine.set_edgecolor("#DDDDDD")
    ax.text(0.99, 0.02, "QSL Foundation I — Lab 1.2",
            transform=ax.transAxes, fontsize=8, color="#AAAAAA",
            ha="right", va="bottom")
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "chart_regime.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    return path


def step6_print_stats(stats):
    """Print the stats table directly to the conversation window."""
    print()
    print("=" * 55)
    print("  STEP 6 — Key Statistics")
    print("=" * 55)
    print(f"  Asset:              {stats['ticker']}")
    print(f"  MA period:          {stats['ma_period']} days")
    print(f"  Data range:         {stats['data_start']} to {stats['data_end']}")
    print()
    print(f"  Total trading days: {stats['total_trading_days']:,}")
    print(f"  Days in market:     {stats['days_in_market']:,} ({stats['pct_time_in_market']}%)")
    print(f"  Days in cash:       {stats['days_in_cash']:,} ({round(100 - stats['pct_time_in_market'], 1)}%)")
    print(f"  Regime changes:     {stats['regime_changes']}")
    print()
    print(f"  AAPL start price:   ${stats['start_price']}")
    print(f"  AAPL end price:     ${stats['end_price']}")
    print(f"  Buy-and-hold rtn:   {stats['buy_and_hold_return_pct']}%")
    print()
    print(f"  Latest close:       ${stats['latest_close']}")
    print(f"  Latest SMA-100:     ${stats['latest_sma_100']}")
    print(f"  Spread:             ${stats['price_vs_sma_spread']} ({stats['price_vs_sma_pct']}%)")
    print()
    print(f"  Current signal:     {stats['current_signal_label']}")
    print("=" * 55)
    print()


def step6_compute_stats(df):
    """Compute descriptive statistics for the strategy and dataset."""
    total_days = len(df)
    buy_days = int(df["Signal"].sum())
    cash_days = total_days - buy_days
    pct_in_market = round(buy_days / total_days * 100, 1)
    start_price = round(float(df["Close"].iloc[0]), 2)
    end_price = round(float(df["Close"].iloc[-1]), 2)
    bah_return = round((end_price - start_price) / start_price * 100, 1)
    transitions = int((df["Signal"].diff().abs() > 0).sum())
    current_signal = int(df["Signal"].iloc[-1])
    latest_close = round(float(df["Close"].iloc[-1]), 2)
    latest_sma = round(float(df["SMA_100"].iloc[-1]), 2)
    spread = round(latest_close - latest_sma, 2)
    spread_pct = round(spread / latest_sma * 100, 1)
    return {
        "ticker": TICKER,
        "ma_period": MA_PERIOD,
        "data_start": df.index[0].strftime("%Y-%m-%d"),
        "data_end": df.index[-1].strftime("%Y-%m-%d"),
        "total_trading_days": total_days,
        "days_in_market": buy_days,
        "days_in_cash": cash_days,
        "pct_time_in_market": pct_in_market,
        "regime_changes": transitions,
        "start_price": start_price,
        "end_price": end_price,
        "buy_and_hold_return_pct": bah_return,
        "latest_close": latest_close,
        "latest_sma_100": latest_sma,
        "price_vs_sma_spread": spread,
        "price_vs_sma_pct": spread_pct,
        "current_signal": current_signal,
        "current_signal_label": "Buy (own AAPL)" if current_signal == 1 else "Cash",
    }


def step6_print_stats(stats):
    """Print stats table to conversation in a readable format."""
    print()
    print("=" * 55)
    print("  STEP 6 — Strategy Statistics")
    print("=" * 55)
    print(f"  {'Metric':<36} {'Value':>14}")
    print("  " + "-" * 53)
    print(f"  {'Total trading days':<36} {stats['total_trading_days']:>14,}")
    print(f"  {'Days in market (signal +1)':<36} {str(stats['days_in_market']) + ' (' + str(stats['pct_time_in_market']) + '%)':>14}")
    print(f"  {'Days in cash (signal 0)':<36} {str(stats['days_in_cash']) + ' (' + str(round(100 - stats['pct_time_in_market'], 1)) + '%)':>14}")
    print(f"  {'Regime changes':<36} {stats['regime_changes']:>14,}")
    print(f"  {'AAPL price at start':<36} {'
    """Generate QSL-branded PDF research report. Saves to output/lab_1_2_report.pdf."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Image,
        Table, TableStyle, HRFlowable
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    pdf_path = os.path.join(OUTPUT_DIR, "lab_1_2_report.pdf")
    doc = SimpleDocTemplate(
        pdf_path, pagesize=letter,
        leftMargin=0.85 * inch, rightMargin=0.85 * inch,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch,
    )

    NAVY_RL = colors.HexColor("#0A1628")
    GOLD_RL = colors.HexColor("#B8972A")
    GRAY_RL = colors.HexColor("#F5F7FA")
    DGRAY_RL = colors.HexColor("#4A5568")
    GREEN_RL = colors.HexColor("#1A6B3C")

    styles = getSampleStyleSheet()
    WIDTH = letter[0] - 1.7 * inch

    h2 = ParagraphStyle("h2", parent=styles["Normal"], fontSize=13,
                         fontName="Helvetica-Bold", textColor=NAVY_RL,
                         spaceBefore=14, spaceAfter=4, leading=18)
    body = ParagraphStyle("body", parent=styles["Normal"], fontSize=10,
                           fontName="Helvetica", textColor=DGRAY_RL,
                           spaceAfter=6, leading=15)
    caption_s = ParagraphStyle("cap", parent=styles["Normal"], fontSize=8.5,
                                fontName="Helvetica-Oblique", textColor=DGRAY_RL,
                                spaceAfter=12, alignment=TA_CENTER)
    meta = ParagraphStyle("meta", parent=styles["Normal"], fontSize=9,
                           fontName="Helvetica", textColor=DGRAY_RL, leading=13)
    footer_s = ParagraphStyle("foot", parent=styles["Normal"], fontSize=8,
                               fontName="Helvetica",
                               textColor=colors.HexColor("#AAAAAA"),
                               alignment=TA_CENTER)

    story = []

    logo_img = Image(LOGO_PATH, width=1.6 * inch, height=0.6 * inch)
    title_p = Paragraph("<b>Lab Unit 1.2 — Introduction to Algorithmic Trading</b>",
                         ParagraphStyle("t", parent=styles["Normal"], fontSize=15,
                                        fontName="Helvetica-Bold", textColor=NAVY_RL,
                                        leading=20, alignment=TA_LEFT))
    sub_p = Paragraph("AAPL 100-Day Simple Moving Average Strategy",
                       ParagraphStyle("s", parent=styles["Normal"], fontSize=11,
                                      fontName="Helvetica", textColor=GOLD_RL,
                                      leading=16, alignment=TA_LEFT))
    ht = Table([[logo_img, [title_p, sub_p]]], colWidths=[1.8 * inch, WIDTH - 1.8 * inch])
    ht.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(ht)
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD_RL, spaceAfter=10))

    mt = Table([[
        Paragraph(f"<b>Asset:</b> {stats['ticker']}", meta),
        Paragraph(f"<b>MA Period:</b> {stats['ma_period']} days", meta),
        Paragraph(f"<b>Data:</b> {stats['data_start']} to {stats['data_end']}", meta),
        Paragraph(f"<b>Generated:</b> {datetime.today().strftime('%B %d, %Y')}", meta),
    ]], colWidths=[WIDTH / 4] * 4)
    mt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GRAY_RL),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(mt)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Mission", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    story.append(Paragraph(
        "This lab replicates the AAPL moving average strategy introduced in Unit 1.2 of "
        "QSL Foundation I. The objective is to observe how a single rule — price above or "
        "below a 100-day moving average — generates buy and cash signals on real market data. "
        "This is a first look at a trading algorithm. It is not a validated strategy. "
        "Validation is covered in later course modules.", body))

    story.append(Paragraph("Strategy Rule", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    rt = Table([
        [Paragraph("<b>Condition</b>", meta), Paragraph("<b>Signal</b>", meta), Paragraph("<b>Action</b>", meta)],
        [Paragraph("AAPL close > 100-day SMA", body),
         Paragraph("+1", ParagraphStyle("g", parent=styles["Normal"], fontSize=11,
                                         fontName="Helvetica-Bold", textColor=GREEN_RL)),
         Paragraph("Own AAPL", body)],
        [Paragraph("AAPL close <= 100-day SMA", body),
         Paragraph("0", ParagraphStyle("gr", parent=styles["Normal"], fontSize=11,
                                        fontName="Helvetica-Bold", textColor=DGRAY_RL)),
         Paragraph("Hold cash", body)],
    ], colWidths=[WIDTH * 0.5, WIDTH * 0.15, WIDTH * 0.35])
    rt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_RL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#E8F5EE")),
        ("BACKGROUND", (0, 2), (-1, 2), GRAY_RL),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(rt)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Price and Moving Average", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    story.append(Paragraph(
        "AAPL daily close price (blue) alongside the 100-day SMA (orange). "
        "The moving average smooths noise and reveals trend direction. "
        "It is backward-looking — it describes where price has been, not where it is going.", body))
    story.append(Image(chart_price_ma, width=WIDTH, height=WIDTH * 0.42))
    story.append(Paragraph("Figure 1. AAPL daily close and 100-day SMA. Data via Yahoo Finance.", caption_s))

    story.append(Paragraph("Regime Chart: Buy and Cash Zones", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    story.append(Paragraph(
        "Green zones: strategy is long AAPL (signal +1). "
        "Gray zones: strategy holds cash (signal 0). "
        "Background changes each time closing price crosses the 100-day average.", body))
    story.append(Image(chart_regime, width=WIDTH, height=WIDTH * 0.42))
    story.append(Paragraph("Figure 2. Regime zones. Green = long AAPL (+1). Gray = cash (0).", caption_s))

    story.append(Paragraph("Key Statistics", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    header_style = ParagraphStyle("th", parent=styles["Normal"], fontSize=9,
                                    fontName="Helvetica-Bold",
                                    textColor=colors.white, leading=13)
    data_rows = [
        ["Total trading days", str(stats["total_trading_days"])],
        ["Days in market (+1)", f"{stats['days_in_market']} ({stats['pct_time_in_market']}%)"],
        ["Days in cash (0)", f"{stats['days_in_cash']} ({round(100 - stats['pct_time_in_market'], 1)}%)"],
        ["Regime changes", str(stats["regime_changes"])],
        ["AAPL price — start", f"${stats['start_price']}"],
        ["AAPL price — end", f"${stats['end_price']}"],
        ["Buy-and-hold return", f"{stats['buy_and_hold_return_pct']}%"],
        ["Latest close vs SMA spread", f"${stats['price_vs_sma_spread']} ({stats['price_vs_sma_pct']}%)"],
        ["Current signal", stats["current_signal_label"]],
    ]
    sd = [[Paragraph("Metric", header_style), Paragraph("Value", header_style)]]
    for r in data_rows:
        sd.append([Paragraph(r[0], body), Paragraph(r[1], body)])
    st2 = Table(sd, colWidths=[WIDTH * 0.65, WIDTH * 0.35])
    ss = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_RL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    for i in range(1, len(sd)):
        ss.append(("BACKGROUND", (0, i), (-1, i), colors.white if i % 2 != 0 else GRAY_RL))
    st2.setStyle(TableStyle(ss))
    story.append(st2)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Honest Limitations", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    story.append(Paragraph(
        "The regime chart shows hindsight performance only. No transaction costs applied. "
        "No statistical testing performed. The 100-day period was not selected through "
        "any optimisation. Whether this rule has a genuine edge is covered in later modules.", body))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5,
                             color=colors.HexColor("#DDDDDD"), spaceAfter=6))
    story.append(Paragraph(
        f"QSL Foundation I — Lab Unit 1.2  |  "
        f"Generated {datetime.today().strftime('%B %d, %Y')}  |  quantstrategylab.com",
        footer_s))

    doc.build(story)
    return pdf_path
 + str(stats['start_price']):>14}")
    print(f"  {'AAPL price at end':<36} {'
    """Generate QSL-branded PDF research report. Saves to output/lab_1_2_report.pdf."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Image,
        Table, TableStyle, HRFlowable
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    pdf_path = os.path.join(OUTPUT_DIR, "lab_1_2_report.pdf")
    doc = SimpleDocTemplate(
        pdf_path, pagesize=letter,
        leftMargin=0.85 * inch, rightMargin=0.85 * inch,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch,
    )

    NAVY_RL = colors.HexColor("#0A1628")
    GOLD_RL = colors.HexColor("#B8972A")
    GRAY_RL = colors.HexColor("#F5F7FA")
    DGRAY_RL = colors.HexColor("#4A5568")
    GREEN_RL = colors.HexColor("#1A6B3C")

    styles = getSampleStyleSheet()
    WIDTH = letter[0] - 1.7 * inch

    h2 = ParagraphStyle("h2", parent=styles["Normal"], fontSize=13,
                         fontName="Helvetica-Bold", textColor=NAVY_RL,
                         spaceBefore=14, spaceAfter=4, leading=18)
    body = ParagraphStyle("body", parent=styles["Normal"], fontSize=10,
                           fontName="Helvetica", textColor=DGRAY_RL,
                           spaceAfter=6, leading=15)
    caption_s = ParagraphStyle("cap", parent=styles["Normal"], fontSize=8.5,
                                fontName="Helvetica-Oblique", textColor=DGRAY_RL,
                                spaceAfter=12, alignment=TA_CENTER)
    meta = ParagraphStyle("meta", parent=styles["Normal"], fontSize=9,
                           fontName="Helvetica", textColor=DGRAY_RL, leading=13)
    footer_s = ParagraphStyle("foot", parent=styles["Normal"], fontSize=8,
                               fontName="Helvetica",
                               textColor=colors.HexColor("#AAAAAA"),
                               alignment=TA_CENTER)

    story = []

    logo_img = Image(LOGO_PATH, width=1.6 * inch, height=0.6 * inch)
    title_p = Paragraph("<b>Lab Unit 1.2 — Introduction to Algorithmic Trading</b>",
                         ParagraphStyle("t", parent=styles["Normal"], fontSize=15,
                                        fontName="Helvetica-Bold", textColor=NAVY_RL,
                                        leading=20, alignment=TA_LEFT))
    sub_p = Paragraph("AAPL 100-Day Simple Moving Average Strategy",
                       ParagraphStyle("s", parent=styles["Normal"], fontSize=11,
                                      fontName="Helvetica", textColor=GOLD_RL,
                                      leading=16, alignment=TA_LEFT))
    ht = Table([[logo_img, [title_p, sub_p]]], colWidths=[1.8 * inch, WIDTH - 1.8 * inch])
    ht.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(ht)
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD_RL, spaceAfter=10))

    mt = Table([[
        Paragraph(f"<b>Asset:</b> {stats['ticker']}", meta),
        Paragraph(f"<b>MA Period:</b> {stats['ma_period']} days", meta),
        Paragraph(f"<b>Data:</b> {stats['data_start']} to {stats['data_end']}", meta),
        Paragraph(f"<b>Generated:</b> {datetime.today().strftime('%B %d, %Y')}", meta),
    ]], colWidths=[WIDTH / 4] * 4)
    mt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GRAY_RL),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(mt)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Mission", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    story.append(Paragraph(
        "This lab replicates the AAPL moving average strategy introduced in Unit 1.2 of "
        "QSL Foundation I. The objective is to observe how a single rule — price above or "
        "below a 100-day moving average — generates buy and cash signals on real market data. "
        "This is a first look at a trading algorithm. It is not a validated strategy. "
        "Validation is covered in later course modules.", body))

    story.append(Paragraph("Strategy Rule", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    rt = Table([
        [Paragraph("<b>Condition</b>", meta), Paragraph("<b>Signal</b>", meta), Paragraph("<b>Action</b>", meta)],
        [Paragraph("AAPL close > 100-day SMA", body),
         Paragraph("+1", ParagraphStyle("g", parent=styles["Normal"], fontSize=11,
                                         fontName="Helvetica-Bold", textColor=GREEN_RL)),
         Paragraph("Own AAPL", body)],
        [Paragraph("AAPL close <= 100-day SMA", body),
         Paragraph("0", ParagraphStyle("gr", parent=styles["Normal"], fontSize=11,
                                        fontName="Helvetica-Bold", textColor=DGRAY_RL)),
         Paragraph("Hold cash", body)],
    ], colWidths=[WIDTH * 0.5, WIDTH * 0.15, WIDTH * 0.35])
    rt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_RL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#E8F5EE")),
        ("BACKGROUND", (0, 2), (-1, 2), GRAY_RL),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(rt)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Price and Moving Average", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    story.append(Paragraph(
        "AAPL daily close price (blue) alongside the 100-day SMA (orange). "
        "The moving average smooths noise and reveals trend direction. "
        "It is backward-looking — it describes where price has been, not where it is going.", body))
    story.append(Image(chart_price_ma, width=WIDTH, height=WIDTH * 0.42))
    story.append(Paragraph("Figure 1. AAPL daily close and 100-day SMA. Data via Yahoo Finance.", caption_s))

    story.append(Paragraph("Regime Chart: Buy and Cash Zones", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    story.append(Paragraph(
        "Green zones: strategy is long AAPL (signal +1). "
        "Gray zones: strategy holds cash (signal 0). "
        "Background changes each time closing price crosses the 100-day average.", body))
    story.append(Image(chart_regime, width=WIDTH, height=WIDTH * 0.42))
    story.append(Paragraph("Figure 2. Regime zones. Green = long AAPL (+1). Gray = cash (0).", caption_s))

    story.append(Paragraph("Key Statistics", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    header_style = ParagraphStyle("th", parent=styles["Normal"], fontSize=9,
                                    fontName="Helvetica-Bold",
                                    textColor=colors.white, leading=13)
    data_rows = [
        ["Total trading days", str(stats["total_trading_days"])],
        ["Days in market (+1)", f"{stats['days_in_market']} ({stats['pct_time_in_market']}%)"],
        ["Days in cash (0)", f"{stats['days_in_cash']} ({round(100 - stats['pct_time_in_market'], 1)}%)"],
        ["Regime changes", str(stats["regime_changes"])],
        ["AAPL price — start", f"${stats['start_price']}"],
        ["AAPL price — end", f"${stats['end_price']}"],
        ["Buy-and-hold return", f"{stats['buy_and_hold_return_pct']}%"],
        ["Latest close vs SMA spread", f"${stats['price_vs_sma_spread']} ({stats['price_vs_sma_pct']}%)"],
        ["Current signal", stats["current_signal_label"]],
    ]
    sd = [[Paragraph("Metric", header_style), Paragraph("Value", header_style)]]
    for r in data_rows:
        sd.append([Paragraph(r[0], body), Paragraph(r[1], body)])
    st2 = Table(sd, colWidths=[WIDTH * 0.65, WIDTH * 0.35])
    ss = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_RL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    for i in range(1, len(sd)):
        ss.append(("BACKGROUND", (0, i), (-1, i), colors.white if i % 2 != 0 else GRAY_RL))
    st2.setStyle(TableStyle(ss))
    story.append(st2)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Honest Limitations", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    story.append(Paragraph(
        "The regime chart shows hindsight performance only. No transaction costs applied. "
        "No statistical testing performed. The 100-day period was not selected through "
        "any optimisation. Whether this rule has a genuine edge is covered in later modules.", body))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5,
                             color=colors.HexColor("#DDDDDD"), spaceAfter=6))
    story.append(Paragraph(
        f"QSL Foundation I — Lab Unit 1.2  |  "
        f"Generated {datetime.today().strftime('%B %d, %Y')}  |  quantstrategylab.com",
        footer_s))

    doc.build(story)
    return pdf_path
 + str(stats['end_price']):>14}")
    print(f"  {'Buy-and-hold return (full period)':<36} {str(stats['buy_and_hold_return_pct']) + '%':>14}")
    print(f"  {'Latest close vs SMA spread':<36} {'
    """Generate QSL-branded PDF research report. Saves to output/lab_1_2_report.pdf."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Image,
        Table, TableStyle, HRFlowable
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    pdf_path = os.path.join(OUTPUT_DIR, "lab_1_2_report.pdf")
    doc = SimpleDocTemplate(
        pdf_path, pagesize=letter,
        leftMargin=0.85 * inch, rightMargin=0.85 * inch,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch,
    )

    NAVY_RL = colors.HexColor("#0A1628")
    GOLD_RL = colors.HexColor("#B8972A")
    GRAY_RL = colors.HexColor("#F5F7FA")
    DGRAY_RL = colors.HexColor("#4A5568")
    GREEN_RL = colors.HexColor("#1A6B3C")

    styles = getSampleStyleSheet()
    WIDTH = letter[0] - 1.7 * inch

    h2 = ParagraphStyle("h2", parent=styles["Normal"], fontSize=13,
                         fontName="Helvetica-Bold", textColor=NAVY_RL,
                         spaceBefore=14, spaceAfter=4, leading=18)
    body = ParagraphStyle("body", parent=styles["Normal"], fontSize=10,
                           fontName="Helvetica", textColor=DGRAY_RL,
                           spaceAfter=6, leading=15)
    caption_s = ParagraphStyle("cap", parent=styles["Normal"], fontSize=8.5,
                                fontName="Helvetica-Oblique", textColor=DGRAY_RL,
                                spaceAfter=12, alignment=TA_CENTER)
    meta = ParagraphStyle("meta", parent=styles["Normal"], fontSize=9,
                           fontName="Helvetica", textColor=DGRAY_RL, leading=13)
    footer_s = ParagraphStyle("foot", parent=styles["Normal"], fontSize=8,
                               fontName="Helvetica",
                               textColor=colors.HexColor("#AAAAAA"),
                               alignment=TA_CENTER)

    story = []

    logo_img = Image(LOGO_PATH, width=1.6 * inch, height=0.6 * inch)
    title_p = Paragraph("<b>Lab Unit 1.2 — Introduction to Algorithmic Trading</b>",
                         ParagraphStyle("t", parent=styles["Normal"], fontSize=15,
                                        fontName="Helvetica-Bold", textColor=NAVY_RL,
                                        leading=20, alignment=TA_LEFT))
    sub_p = Paragraph("AAPL 100-Day Simple Moving Average Strategy",
                       ParagraphStyle("s", parent=styles["Normal"], fontSize=11,
                                      fontName="Helvetica", textColor=GOLD_RL,
                                      leading=16, alignment=TA_LEFT))
    ht = Table([[logo_img, [title_p, sub_p]]], colWidths=[1.8 * inch, WIDTH - 1.8 * inch])
    ht.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(ht)
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD_RL, spaceAfter=10))

    mt = Table([[
        Paragraph(f"<b>Asset:</b> {stats['ticker']}", meta),
        Paragraph(f"<b>MA Period:</b> {stats['ma_period']} days", meta),
        Paragraph(f"<b>Data:</b> {stats['data_start']} to {stats['data_end']}", meta),
        Paragraph(f"<b>Generated:</b> {datetime.today().strftime('%B %d, %Y')}", meta),
    ]], colWidths=[WIDTH / 4] * 4)
    mt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GRAY_RL),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(mt)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Mission", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    story.append(Paragraph(
        "This lab replicates the AAPL moving average strategy introduced in Unit 1.2 of "
        "QSL Foundation I. The objective is to observe how a single rule — price above or "
        "below a 100-day moving average — generates buy and cash signals on real market data. "
        "This is a first look at a trading algorithm. It is not a validated strategy. "
        "Validation is covered in later course modules.", body))

    story.append(Paragraph("Strategy Rule", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    rt = Table([
        [Paragraph("<b>Condition</b>", meta), Paragraph("<b>Signal</b>", meta), Paragraph("<b>Action</b>", meta)],
        [Paragraph("AAPL close > 100-day SMA", body),
         Paragraph("+1", ParagraphStyle("g", parent=styles["Normal"], fontSize=11,
                                         fontName="Helvetica-Bold", textColor=GREEN_RL)),
         Paragraph("Own AAPL", body)],
        [Paragraph("AAPL close <= 100-day SMA", body),
         Paragraph("0", ParagraphStyle("gr", parent=styles["Normal"], fontSize=11,
                                        fontName="Helvetica-Bold", textColor=DGRAY_RL)),
         Paragraph("Hold cash", body)],
    ], colWidths=[WIDTH * 0.5, WIDTH * 0.15, WIDTH * 0.35])
    rt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_RL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#E8F5EE")),
        ("BACKGROUND", (0, 2), (-1, 2), GRAY_RL),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(rt)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Price and Moving Average", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    story.append(Paragraph(
        "AAPL daily close price (blue) alongside the 100-day SMA (orange). "
        "The moving average smooths noise and reveals trend direction. "
        "It is backward-looking — it describes where price has been, not where it is going.", body))
    story.append(Image(chart_price_ma, width=WIDTH, height=WIDTH * 0.42))
    story.append(Paragraph("Figure 1. AAPL daily close and 100-day SMA. Data via Yahoo Finance.", caption_s))

    story.append(Paragraph("Regime Chart: Buy and Cash Zones", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    story.append(Paragraph(
        "Green zones: strategy is long AAPL (signal +1). "
        "Gray zones: strategy holds cash (signal 0). "
        "Background changes each time closing price crosses the 100-day average.", body))
    story.append(Image(chart_regime, width=WIDTH, height=WIDTH * 0.42))
    story.append(Paragraph("Figure 2. Regime zones. Green = long AAPL (+1). Gray = cash (0).", caption_s))

    story.append(Paragraph("Key Statistics", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    header_style = ParagraphStyle("th", parent=styles["Normal"], fontSize=9,
                                    fontName="Helvetica-Bold",
                                    textColor=colors.white, leading=13)
    data_rows = [
        ["Total trading days", str(stats["total_trading_days"])],
        ["Days in market (+1)", f"{stats['days_in_market']} ({stats['pct_time_in_market']}%)"],
        ["Days in cash (0)", f"{stats['days_in_cash']} ({round(100 - stats['pct_time_in_market'], 1)}%)"],
        ["Regime changes", str(stats["regime_changes"])],
        ["AAPL price — start", f"${stats['start_price']}"],
        ["AAPL price — end", f"${stats['end_price']}"],
        ["Buy-and-hold return", f"{stats['buy_and_hold_return_pct']}%"],
        ["Latest close vs SMA spread", f"${stats['price_vs_sma_spread']} ({stats['price_vs_sma_pct']}%)"],
        ["Current signal", stats["current_signal_label"]],
    ]
    sd = [[Paragraph("Metric", header_style), Paragraph("Value", header_style)]]
    for r in data_rows:
        sd.append([Paragraph(r[0], body), Paragraph(r[1], body)])
    st2 = Table(sd, colWidths=[WIDTH * 0.65, WIDTH * 0.35])
    ss = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_RL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    for i in range(1, len(sd)):
        ss.append(("BACKGROUND", (0, i), (-1, i), colors.white if i % 2 != 0 else GRAY_RL))
    st2.setStyle(TableStyle(ss))
    story.append(st2)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Honest Limitations", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    story.append(Paragraph(
        "The regime chart shows hindsight performance only. No transaction costs applied. "
        "No statistical testing performed. The 100-day period was not selected through "
        "any optimisation. Whether this rule has a genuine edge is covered in later modules.", body))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5,
                             color=colors.HexColor("#DDDDDD"), spaceAfter=6))
    story.append(Paragraph(
        f"QSL Foundation I — Lab Unit 1.2  |  "
        f"Generated {datetime.today().strftime('%B %d, %Y')}  |  quantstrategylab.com",
        footer_s))

    doc.build(story)
    return pdf_path
 + str(stats['price_vs_sma_spread']) + ' (' + str(stats['price_vs_sma_pct']) + '%)':>14}")
    print(f"  {'Current signal':<36} {stats['current_signal_label']:>14}")
    print("=" * 55)
    print()


def step7_generate_pdf(stats, chart_price_ma, chart_regime):
    """Generate QSL-branded PDF research report. Saves to output/lab_1_2_report.pdf."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Image,
        Table, TableStyle, HRFlowable
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    pdf_path = os.path.join(OUTPUT_DIR, "lab_1_2_report.pdf")
    doc = SimpleDocTemplate(
        pdf_path, pagesize=letter,
        leftMargin=0.85 * inch, rightMargin=0.85 * inch,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch,
    )

    NAVY_RL = colors.HexColor("#0A1628")
    GOLD_RL = colors.HexColor("#B8972A")
    GRAY_RL = colors.HexColor("#F5F7FA")
    DGRAY_RL = colors.HexColor("#4A5568")
    GREEN_RL = colors.HexColor("#1A6B3C")

    styles = getSampleStyleSheet()
    WIDTH = letter[0] - 1.7 * inch

    h2 = ParagraphStyle("h2", parent=styles["Normal"], fontSize=13,
                         fontName="Helvetica-Bold", textColor=NAVY_RL,
                         spaceBefore=14, spaceAfter=4, leading=18)
    body = ParagraphStyle("body", parent=styles["Normal"], fontSize=10,
                           fontName="Helvetica", textColor=DGRAY_RL,
                           spaceAfter=6, leading=15)
    caption_s = ParagraphStyle("cap", parent=styles["Normal"], fontSize=8.5,
                                fontName="Helvetica-Oblique", textColor=DGRAY_RL,
                                spaceAfter=12, alignment=TA_CENTER)
    meta = ParagraphStyle("meta", parent=styles["Normal"], fontSize=9,
                           fontName="Helvetica", textColor=DGRAY_RL, leading=13)
    footer_s = ParagraphStyle("foot", parent=styles["Normal"], fontSize=8,
                               fontName="Helvetica",
                               textColor=colors.HexColor("#AAAAAA"),
                               alignment=TA_CENTER)

    story = []

    logo_img = Image(LOGO_PATH, width=1.6 * inch, height=0.6 * inch)
    title_p = Paragraph("<b>Lab Unit 1.2 — Introduction to Algorithmic Trading</b>",
                         ParagraphStyle("t", parent=styles["Normal"], fontSize=15,
                                        fontName="Helvetica-Bold", textColor=NAVY_RL,
                                        leading=20, alignment=TA_LEFT))
    sub_p = Paragraph("AAPL 100-Day Simple Moving Average Strategy",
                       ParagraphStyle("s", parent=styles["Normal"], fontSize=11,
                                      fontName="Helvetica", textColor=GOLD_RL,
                                      leading=16, alignment=TA_LEFT))
    ht = Table([[logo_img, [title_p, sub_p]]], colWidths=[1.8 * inch, WIDTH - 1.8 * inch])
    ht.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(ht)
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD_RL, spaceAfter=10))

    mt = Table([[
        Paragraph(f"<b>Asset:</b> {stats['ticker']}", meta),
        Paragraph(f"<b>MA Period:</b> {stats['ma_period']} days", meta),
        Paragraph(f"<b>Data:</b> {stats['data_start']} to {stats['data_end']}", meta),
        Paragraph(f"<b>Generated:</b> {datetime.today().strftime('%B %d, %Y')}", meta),
    ]], colWidths=[WIDTH / 4] * 4)
    mt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GRAY_RL),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(mt)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Mission", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    story.append(Paragraph(
        "This lab replicates the AAPL moving average strategy introduced in Unit 1.2 of "
        "QSL Foundation I. The objective is to observe how a single rule — price above or "
        "below a 100-day moving average — generates buy and cash signals on real market data. "
        "This is a first look at a trading algorithm. It is not a validated strategy. "
        "Validation is covered in later course modules.", body))

    story.append(Paragraph("Strategy Rule", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    rt = Table([
        [Paragraph("<b>Condition</b>", meta), Paragraph("<b>Signal</b>", meta), Paragraph("<b>Action</b>", meta)],
        [Paragraph("AAPL close > 100-day SMA", body),
         Paragraph("+1", ParagraphStyle("g", parent=styles["Normal"], fontSize=11,
                                         fontName="Helvetica-Bold", textColor=GREEN_RL)),
         Paragraph("Own AAPL", body)],
        [Paragraph("AAPL close <= 100-day SMA", body),
         Paragraph("0", ParagraphStyle("gr", parent=styles["Normal"], fontSize=11,
                                        fontName="Helvetica-Bold", textColor=DGRAY_RL)),
         Paragraph("Hold cash", body)],
    ], colWidths=[WIDTH * 0.5, WIDTH * 0.15, WIDTH * 0.35])
    rt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_RL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#E8F5EE")),
        ("BACKGROUND", (0, 2), (-1, 2), GRAY_RL),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(rt)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Price and Moving Average", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    story.append(Paragraph(
        "AAPL daily close price (blue) alongside the 100-day SMA (orange). "
        "The moving average smooths noise and reveals trend direction. "
        "It is backward-looking — it describes where price has been, not where it is going.", body))
    story.append(Image(chart_price_ma, width=WIDTH, height=WIDTH * 0.42))
    story.append(Paragraph("Figure 1. AAPL daily close and 100-day SMA. Data via Yahoo Finance.", caption_s))

    story.append(Paragraph("Regime Chart: Buy and Cash Zones", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    story.append(Paragraph(
        "Green zones: strategy is long AAPL (signal +1). "
        "Gray zones: strategy holds cash (signal 0). "
        "Background changes each time closing price crosses the 100-day average.", body))
    story.append(Image(chart_regime, width=WIDTH, height=WIDTH * 0.42))
    story.append(Paragraph("Figure 2. Regime zones. Green = long AAPL (+1). Gray = cash (0).", caption_s))

    story.append(Paragraph("Key Statistics", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    header_style = ParagraphStyle("th", parent=styles["Normal"], fontSize=9,
                                    fontName="Helvetica-Bold",
                                    textColor=colors.white, leading=13)
    data_rows = [
        ["Total trading days", str(stats["total_trading_days"])],
        ["Days in market (+1)", f"{stats['days_in_market']} ({stats['pct_time_in_market']}%)"],
        ["Days in cash (0)", f"{stats['days_in_cash']} ({round(100 - stats['pct_time_in_market'], 1)}%)"],
        ["Regime changes", str(stats["regime_changes"])],
        ["AAPL price — start", f"${stats['start_price']}"],
        ["AAPL price — end", f"${stats['end_price']}"],
        ["Buy-and-hold return", f"{stats['buy_and_hold_return_pct']}%"],
        ["Latest close vs SMA spread", f"${stats['price_vs_sma_spread']} ({stats['price_vs_sma_pct']}%)"],
        ["Current signal", stats["current_signal_label"]],
    ]
    sd = [[Paragraph("Metric", header_style), Paragraph("Value", header_style)]]
    for r in data_rows:
        sd.append([Paragraph(r[0], body), Paragraph(r[1], body)])
    st2 = Table(sd, colWidths=[WIDTH * 0.65, WIDTH * 0.35])
    ss = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_RL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    for i in range(1, len(sd)):
        ss.append(("BACKGROUND", (0, i), (-1, i), colors.white if i % 2 != 0 else GRAY_RL))
    st2.setStyle(TableStyle(ss))
    story.append(st2)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Honest Limitations", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD_RL, spaceAfter=8))
    story.append(Paragraph(
        "The regime chart shows hindsight performance only. No transaction costs applied. "
        "No statistical testing performed. The 100-day period was not selected through "
        "any optimisation. Whether this rule has a genuine edge is covered in later modules.", body))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5,
                             color=colors.HexColor("#DDDDDD"), spaceAfter=6))
    story.append(Paragraph(
        f"QSL Foundation I — Lab Unit 1.2  |  "
        f"Generated {datetime.today().strftime('%B %d, %Y')}  |  quantstrategylab.com",
        footer_s))

    doc.build(story)
    return pdf_path
