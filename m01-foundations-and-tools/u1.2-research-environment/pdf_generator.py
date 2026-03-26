"""
QSLab F1 — PDF Generator
Unit 1.2: Your Research Lab

Generates one PDF per step. Each PDF:
- Has a consistent QSL header
- Contains step data in clean tables
- Embeds the signal chart (step 3)
- Contains exploration prompts
- Opens automatically after saving
- Tells the student exactly where to find it
"""

import os
import subprocess
import platform
from datetime import datetime

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image
)
from reportlab.lib.enums import TA_CENTER

NAVY        = colors.HexColor("#0A1628")
BLUE        = colors.HexColor("#1565C0")
ORANGE      = colors.HexColor("#E65100")
GREEN_LIGHT = colors.HexColor("#C8E6C9")
GREY_LIGHT  = colors.HexColor("#F5F5F5")
WHITE       = colors.white
MID_GREY    = colors.HexColor("#888888")
BORDER_GREY = colors.HexColor("#DDDDDD")

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def _styles():
    return {
        "header_unit":  ParagraphStyle("hu",  fontSize=9,  textColor=MID_GREY, fontName="Helvetica", leading=12),
        "header_title": ParagraphStyle("ht",  fontSize=18, textColor=NAVY, fontName="Helvetica-Bold", leading=22),
        "header_sub":   ParagraphStyle("hs",  fontSize=10, textColor=BLUE, fontName="Helvetica", leading=14),
        "section":      ParagraphStyle("sec", fontSize=11, textColor=NAVY, fontName="Helvetica-Bold", leading=16, spaceBefore=12, spaceAfter=4),
        "body":         ParagraphStyle("bod", fontSize=9.5, textColor=NAVY, fontName="Helvetica", leading=14),
        "body_italic":  ParagraphStyle("bi",  fontSize=9.5, textColor=MID_GREY, fontName="Helvetica-Oblique", leading=14),
        "prompt_title": ParagraphStyle("pt",  fontSize=9,  textColor=ORANGE, fontName="Helvetica-Bold", leading=13),
        "prompt_body":  ParagraphStyle("pb",  fontSize=9,  textColor=NAVY, fontName="Helvetica", leading=13),
        "footer":       ParagraphStyle("ft",  fontSize=8,  textColor=MID_GREY, fontName="Helvetica", alignment=TA_CENTER),
    }


def _table_style():
    return TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),   NAVY),
        ("TEXTCOLOR",     (0,0), (-1,0),   WHITE),
        ("FONTNAME",      (0,0), (-1,0),   "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1),  9),
        ("FONTNAME",      (0,1), (-1,-1),  "Helvetica"),
        ("ROWBACKGROUNDS",(0,1), (-1,-1),  [WHITE, GREY_LIGHT]),
        ("TOPPADDING",    (0,0), (-1,-1),  6),
        ("BOTTOMPADDING", (0,0), (-1,-1),  6),
        ("LEFTPADDING",   (0,0), (-1,-1),  8),
        ("RIGHTPADDING",  (0,0), (-1,-1),  8),
        ("BOX",           (0,0), (-1,-1),  0.5, BORDER_GREY),
        ("LINEBELOW",     (0,0), (-1,0),   0.5, BORDER_GREY),
    ])


def _page_header(story, s, ticker, step_num, step_title, ma_period=None):
    period_str = f"  ·  {ma_period}-Day SMA" if ma_period else ""
    story.append(Paragraph(f"QSLab Foundation I  ·  Unit 1.2 — Your Research Lab  ·  {ticker}{period_str}", s["header_unit"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"Step {step_num} — {step_title}", s["header_title"]))
    story.append(Spacer(1, 2))
    story.append(Paragraph(datetime.now().strftime("Generated %B %d, %Y"), s["header_sub"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceAfter=10))


def _exploration_box(story, s, prompts):
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_GREY, spaceBefore=6, spaceAfter=6))
    story.append(Paragraph("What to explore next", s["prompt_title"]))
    story.append(Spacer(1, 4))
    for prompt in prompts:
        story.append(Paragraph(f"→  {prompt}", s["prompt_body"]))
        story.append(Spacer(1, 3))


def _footer(story, s, path):
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_GREY, spaceBefore=4, spaceAfter=4))
    story.append(Paragraph(f"Saved to: {path}", s["footer"]))


def _open_pdf(path):
    try:
        if platform.system() == "Darwin":
            subprocess.run(["open", path], check=False)
        elif platform.system() == "Windows":
            os.startfile(path)
        else:
            subprocess.run(["xdg-open", path], check=False)
    except Exception:
        pass


def generate_step1_pdf(df: pd.DataFrame, ticker: str) -> str:
    ticker = ticker.upper()
    path = os.path.join(OUTPUT_DIR, f"step1_data_{ticker.lower()}.pdf")
    s = _styles()
    doc = SimpleDocTemplate(path, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.75*inch, bottomMargin=0.75*inch)
    story = []
    _page_header(story, s, ticker, 1, "Data Download")

    total_return = round((df["Close"].iloc[-1] / df["Close"].iloc[0] - 1) * 100, 1)
    data = [
        ["Field", "Value"],
        ["Ticker", ticker],
        ["Period", f"{df.index[0].strftime('%B %d, %Y')} — {df.index[-1].strftime('%B %d, %Y')}"],
        ["Trading days", f"{len(df):,}"],
        ["Start price", f"${df['Close'].iloc[0]:.2f}"],
        ["End price", f"${df['Close'].iloc[-1]:.2f}"],
        ["Total return", f"{total_return:+.1f}%"],
    ]
    t = Table(data, colWidths=[2.2*inch, 4.5*inch])
    t.setStyle(_table_style())
    story.append(t)
    story.append(Spacer(1, 10))

    story.append(Paragraph("What this tells you", s["section"]))
    story.append(Paragraph(
        f"This is {len(df):,} trading days of {ticker} price history — roughly 21 years "
        f"covering multiple full market cycles: the 2008 financial crisis, the long bull run "
        f"of the 2010s, the COVID crash in 2020, the 2022 bear market, and the recovery since.",
        s["body"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        f"The total return of {total_return:+.1f}% is the buy-and-hold baseline — "
        f"the number any strategy has to justify itself against.",
        s["body"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Limitation: total return alone tells you nothing about the risk taken to achieve it. "
        "The stock may have dropped 40% or more along the way.",
        s["body_italic"]))

    story.append(Paragraph("Last 8 trading days", s["section"]))
    rows = [["Date", "Close (USD)"]]
    for date, row in df.tail(8).iterrows():
        rows.append([date.strftime("%Y-%m-%d"), f"${row['Close']:.2f}"])
    t2 = Table(rows, colWidths=[2.5*inch, 2.5*inch])
    t2.setStyle(_table_style())
    story.append(t2)

    _exploration_box(story, s, [
        f"Ask: 'What would $100,000 invested in {ticker} in January 2005 be worth today if I held everything?'",
        f"Ask: 'Describe the biggest price drops for {ticker} over the last 20 years — what caused them?'",
    ])
    _footer(story, s, path)
    doc.build(story)
    print(f"\n  📄 Step 1 PDF → {path}")
    print(f"  Opening now...\n")
    _open_pdf(path)
    return path


def generate_step2_pdf(df: pd.DataFrame, ticker: str, ma_period: int) -> str:
    ticker = ticker.upper()
    col = f"SMA_{ma_period}"
    path = os.path.join(OUTPUT_DIR, f"step2_sma_{ticker.lower()}_{ma_period}d.pdf")
    s = _styles()
    doc = SimpleDocTemplate(path, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.75*inch, bottomMargin=0.75*inch)
    story = []
    _page_header(story, s, ticker, 2, f"{ma_period}-Day SMA Calculation", ma_period)

    current_close = round(float(df["Close"].iloc[-1]), 2)
    current_sma   = round(float(df[col].iloc[-1]), 2)
    is_above      = current_close > current_sma
    position_text = "Above SMA — Signal +1 (own the stock)" if is_above else "Below SMA — Signal 0 (hold cash)"
    bg = GREEN_LIGHT if is_above else colors.HexColor("#F0F0F0")

    pos_table = Table([["Current Position"], [position_text]], colWidths=[6.7*inch])
    pos_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 10),
        ("BACKGROUND",    (0,1), (-1,1), bg),
        ("FONTNAME",      (0,1), (-1,1), "Helvetica-Bold"),
        ("TEXTCOLOR",     (0,1), (-1,1), NAVY),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING",    (0,0), (-1,-1), 9),
        ("BOTTOMPADDING", (0,0), (-1,-1), 9),
        ("BOX",           (0,0), (-1,-1), 0.5, BORDER_GREY),
    ]))
    story.append(pos_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Last 8 trading days", s["section"]))
    rows = [["Date", "Close", f"SMA_{ma_period}", "Position"]]
    for date, row in df.tail(8).iterrows():
        marker = " ◀ Today" if date == df.index[-1] else ""
        pos_short = "Above ↑" if "Above" in row["Position"] else "Below ↓"
        rows.append([date.strftime("%Y-%m-%d"), f"${row['Close']:.2f}",
                     f"${row[col]:.2f}", f"{pos_short}{marker}"])
    t = Table(rows, colWidths=[1.8*inch, 1.4*inch, 1.6*inch, 1.9*inch])
    t.setStyle(_table_style())
    story.append(t)
    story.append(Spacer(1, 10))

    story.append(Paragraph("What this tells you", s["section"]))
    story.append(Paragraph(
        f"The {ma_period}-day SMA averages the last {ma_period} daily closing prices. "
        f"Each new day, the oldest drops off and today's is added. One bad day shifts it by "
        f"only 1/{ma_period}th — that smoothing filters noise and reveals the underlying trend.",
        s["body"]))
    story.append(Spacer(1, 5))
    story.append(Paragraph(
        "Limitation: the SMA is backward-looking. It reacts to price moves — it does not predict them.",
        s["body_italic"]))

    _exploration_box(story, s, [
        f"Ask: 'What would the current signal for {ticker} be with a 50-day SMA instead of {ma_period}-day?'",
        f"Ask: 'How many times has {ticker} crossed its {ma_period}-day SMA in the last 5 years?'",
    ])
    _footer(story, s, path)
    doc.build(story)
    print(f"\n  📄 Step 2 PDF → {path}")
    print(f"  Opening now...\n")
    _open_pdf(path)
    return path


def generate_step3_pdf(chart_path: str, ticker: str, ma_period: int, pct_in: float) -> str:
    ticker = ticker.upper()
    path = os.path.join(OUTPUT_DIR, f"step3_chart_{ticker.lower()}_{ma_period}d.pdf")
    s = _styles()
    doc = SimpleDocTemplate(path, pagesize=letter,
        leftMargin=0.5*inch, rightMargin=0.5*inch,
        topMargin=0.6*inch, bottomMargin=0.6*inch)
    story = []
    _page_header(story, s, ticker, 3, "Signal Zone Chart", ma_period)

    zone_data = [
        ["Zone", "Meaning", "% of Period"],
        ["Green", "Signal +1 — Strategy owned the stock", f"{pct_in:.1f}%"],
        ["Grey",  "Signal 0 — Strategy held cash",        f"{round(100-pct_in,1):.1f}%"],
    ]
    zt = Table(zone_data, colWidths=[1.0*inch, 4.5*inch, 1.2*inch])
    zt.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",   (0,0), (-1,0), WHITE),
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,-1), 9),
        ("FONTNAME",    (0,1), (-1,-1), "Helvetica"),
        ("BACKGROUND",  (0,1), (0,1),  GREEN_LIGHT),
        ("BACKGROUND",  (0,2), (0,2),  colors.HexColor("#F0F0F0")),
        ("TOPPADDING",  (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("BOX",         (0,0), (-1,-1), 0.5, BORDER_GREY),
        ("LINEBELOW",   (0,0), (-1,0),  0.5, BORDER_GREY),
    ]))
    story.append(zt)
    story.append(Spacer(1, 8))

    if os.path.exists(chart_path):
        story.append(Image(chart_path, width=7.5*inch, height=3.8*inch))
    story.append(Spacer(1, 8))

    story.append(Paragraph("How to read this chart", s["section"]))
    story.append(Paragraph(
        "Blue line = daily close price. Orange line = moving average. "
        "Green = strategy owned the stock. Grey = strategy held cash. "
        "Look at the grey zones — do any align with market events you recognise?",
        s["body"]))
    story.append(Spacer(1, 5))
    story.append(Paragraph(
        "Limitation: this chart shows hindsight. The zones look useful now because you can "
        "see what happened after. At the time each signal fired, the strategy did not know "
        "whether it was avoiding a crash or missing a rally.",
        s["body_italic"]))

    _exploration_box(story, s, [
        f"Identify one grey zone that was a good call (avoided a real crash). "
        f"Ask: 'What happened to {ticker} in [year] — was the signal correct?'",
        f"Ask: 'Which year had the most signal changes for {ticker}, and what was "
        f"happening in the market that year?'",
    ])
    _footer(story, s, path)
    doc.build(story)
    print(f"\n  📄 Step 3 PDF → {path}")
    print(f"  Opening now...\n")
    _open_pdf(path)
    return path


def generate_step4_pdf(result: dict, ticker: str, ma_period: int) -> str:
    ticker = ticker.upper()
    path = os.path.join(OUTPUT_DIR, f"step4_signal_{ticker.lower()}_{ma_period}d.pdf")
    s = _styles()
    doc = SimpleDocTemplate(path, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.75*inch, bottomMargin=0.75*inch)
    story = []
    _page_header(story, s, ticker, 4, "Signal Summary", ma_period)

    is_in = result["current_signal"] == 1
    bg = GREEN_LIGHT if is_in else colors.HexColor("#F0F0F0")
    signal_text = "▶  Signal +1 — Own the stock" if is_in else "▶  Signal 0 — Hold cash"
    sig_t = Table([["Current Signal"], [signal_text]], colWidths=[6.7*inch])
    sig_t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 10),
        ("BACKGROUND",    (0,1), (-1,1), bg),
        ("FONTNAME",      (0,1), (-1,1), "Helvetica-Bold"),
        ("TEXTCOLOR",     (0,1), (-1,1), NAVY),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("BOX",           (0,0), (-1,-1), 0.5, BORDER_GREY),
    ]))
    story.append(sig_t)
    story.append(Spacer(1, 10))

    spread = result["spread"]
    spread_abs = abs(spread)
    spread_pct = round(spread_abs / result["current_sma"] * 100, 1)
    direction = "above" if spread > 0 else "below"
    flip_dir = "fall" if is_in else "rise"
    flip_to  = "0 (cash)" if is_in else "+1 (in market)"

    summary = [
        ["Metric", "Value"],
        ["Ticker", ticker],
        ["MA Period", f"{ma_period}-day SMA"],
        ["Days in market (+1)", f"{result['days_in_market']:,} ({result['pct_in_market']}%)"],
        ["Days in cash (0)", f"{result['days_in_cash']:,} ({round(100-result['pct_in_market'],1)}%)"],
        ["Signal changes", str(result["signal_changes"])],
        ["Today's close", f"${result['current_close']:.2f}"],
        [f"{ma_period}-day SMA", f"${result['current_sma']:.2f}"],
        ["Spread", f"${spread_abs:.2f} ({spread_pct:.1f}%) {direction} SMA"],
        ["Flip distance", f"Price must {flip_dir} ${spread_abs:.2f} → signal becomes {flip_to}"],
    ]
    t = Table(summary, colWidths=[2.8*inch, 3.9*inch])
    t.setStyle(_table_style())
    story.append(t)
    story.append(Spacer(1, 10))

    story.append(Paragraph("What this tells you", s["section"]))
    story.append(Paragraph(
        f"The flip distance tells you exactly how far {ticker} would need to move before "
        f"the strategy changes position. A large flip distance means the signal is stable. "
        f"A small one means it could change soon.",
        s["body"]))
    story.append(Spacer(1, 5))
    story.append(Paragraph(
        "You have completed the research loop: question → data → analysis → result. "
        "The result is a live signal on a stock you chose. It is a data point, not advice.",
        s["body"]))
    story.append(Spacer(1, 5))
    story.append(Paragraph(
        "Limitation: this signal tells you what one rule says about one stock. "
        "It does not tell you whether the rule is good or whether the signal will be correct.",
        s["body_italic"]))

    # Forward hook
    story.append(Spacer(1, 8))
    hook = Table(
        [["What comes next"],
         ["Unit 1.3 — Your First Backtest: take this exact strategy to a professional platform "
          "and find out whether it would have made money — with real transaction costs, "
          "institutional data, and a proper performance dashboard."]],
        colWidths=[6.7*inch])
    hook.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), BLUE),
        ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 9),
        ("BACKGROUND",    (0,1), (-1,1), colors.HexColor("#E8F0FE")),
        ("FONTNAME",      (0,1), (-1,1), "Helvetica"),
        ("TEXTCOLOR",     (0,1), (-1,1), NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("BOX",           (0,0), (-1,-1), 0.5, BORDER_GREY),
    ]))
    story.append(hook)

    _exploration_box(story, s, [
        f"Ask: 'What would need to happen for the {ticker} signal to flip? How far must "
        f"the price move from today?'",
        f"Ask: 'I ran the {ma_period}-day SMA on {ticker}. Which specific periods drove the "
        f"most return — and which look like the strategy made the wrong call?'",
        f"Ask: 'Compare {ma_period}-day vs 200-day SMA on {ticker}. Which has fewer signal changes?'",
    ])
    _footer(story, s, path)
    doc.build(story)
    print(f"\n  📄 Step 4 PDF → {path}")
    print(f"  Opening now...\n")
    _open_pdf(path)
    return path


def generate_rerun_pdf(result_orig: dict, result_new: dict,
                       ticker: str, orig_period: int, new_period: int) -> str:
    ticker = ticker.upper()
    path = os.path.join(OUTPUT_DIR, f"step4_rerun_{ticker.lower()}_{orig_period}d_vs_{new_period}d.pdf")
    s = _styles()
    doc = SimpleDocTemplate(path, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.75*inch, bottomMargin=0.75*inch)
    story = []
    _page_header(story, s, ticker, 4, f"Rerun — {orig_period}-Day vs {new_period}-Day SMA")

    story.append(Paragraph("Same stock. Different rule. Different result.", s["section"]))
    story.append(Spacer(1, 6))

    comp = [
        ["Metric", f"{orig_period}-Day SMA", f"{new_period}-Day SMA"],
        ["Days in market", f"{result_orig['days_in_market']:,} ({result_orig['pct_in_market']}%)",
                           f"{result_new['days_in_market']:,} ({result_new['pct_in_market']}%)"],
        ["Days in cash",   f"{result_orig['days_in_cash']:,}", f"{result_new['days_in_cash']:,}"],
        ["Signal changes", str(result_orig["signal_changes"]), str(result_new["signal_changes"])],
        ["Current close",  f"${result_orig['current_close']:.2f}", f"${result_new['current_close']:.2f}"],
        ["Current SMA",    f"${result_orig['current_sma']:.2f}",   f"${result_new['current_sma']:.2f}"],
        ["Current signal", result_orig["current_signal_label"],    result_new["current_signal_label"]],
    ]
    ct = Table(comp, colWidths=[2.2*inch, 2.2*inch, 2.3*inch])
    ct.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 9),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, GREY_LIGHT]),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("BOX",           (0,0), (-1,-1), 0.5, BORDER_GREY),
        ("LINEBELOW",     (0,0), (-1,0),  0.5, BORDER_GREY),
        ("LINEBEFORE",    (1,0), (2,-1),  0.5, BORDER_GREY),
    ]))
    story.append(ct)
    story.append(Spacer(1, 10))

    faster = min(orig_period, new_period)
    slower = max(orig_period, new_period)
    faster_res = result_orig if orig_period == faster else result_new
    slower_res = result_orig if orig_period == slower else result_new

    story.append(Paragraph("What the difference tells you", s["section"]))
    story.append(Paragraph(
        f"The {faster}-day SMA reacts faster — {faster_res['signal_changes']} signal changes "
        f"versus {slower_res['signal_changes']} for the {slower}-day SMA. More signal changes "
        f"means more trades, more costs, and more false signals in choppy markets.",
        s["body"]))
    story.append(Spacer(1, 5))
    story.append(Paragraph(
        f"The {slower}-day SMA is slower and smoother — it holds positions longer. "
        f"Neither is better. They are different tradeoffs that require testing before "
        f"drawing any conclusion.",
        s["body"]))
    story.append(Spacer(1, 5))
    story.append(Paragraph(
        "This is the core insight of Unit 1.2: systematic research is not about finding "
        "one right answer. It is about asking precise questions and reading what the data says.",
        s["body_italic"]))

    _exploration_box(story, s, [
        f"Ask: 'If I used a {faster}-day SMA on {ticker}, which year had the most false signals?'",
        f"Ask: 'Compare {faster}-day and {slower}-day SMA on {ticker} — which had higher CAGR?'",
    ])
    _footer(story, s, path)
    doc.build(story)
    print(f"\n  📄 Rerun PDF → {path}")
    print(f"  Opening now...\n")
    _open_pdf(path)
    return path
