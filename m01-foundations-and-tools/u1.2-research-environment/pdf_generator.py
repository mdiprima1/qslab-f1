"""
QSLab F1 — PDF Generator v3.0
Unit 1.2: Your Research Lab

Layout standard: ~/qslab-f1/QSL-PDF-STANDARD.md

One PDF per session. Called once at the end of run_lab().
Contains all four step results in sequence.
Saves to ~/QSLab-Output/. Opens automatically.
"""

import os
import subprocess
import platform
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_CENTER

# ── Colours ───────────────────────────────────────────────────────────────────
NAVY        = colors.HexColor("#0A1628")
BLUE        = colors.HexColor("#1565C0")
ORANGE      = colors.HexColor("#E65100")
GREEN_FILL  = colors.HexColor("#1B5E20")
GREEN_BG    = colors.HexColor("#E8F5E9")
GREY_BG     = colors.HexColor("#F5F5F5")
GREY_DARK   = colors.HexColor("#616161")
WHITE       = colors.white
MID_GREY    = colors.HexColor("#9E9E9E")
BORDER      = colors.HexColor("#E0E0E0")
BLUE_LIGHT  = colors.HexColor("#E3F2FD")
TABLE_ALT   = colors.HexColor("#FAFAFA")
AMBER_BG    = colors.HexColor("#FFF8E1")
AMBER_DARK  = colors.HexColor("#FFF3E0")


def _get_output_dir() -> str:
    d = os.path.expanduser("~/QSLab-Output")
    os.makedirs(d, exist_ok=True)
    return d


OUTPUT_DIR = _get_output_dir()


# ── Styles ────────────────────────────────────────────────────────────────────
def _styles():
    return {
        "eyebrow":     ParagraphStyle("ey", fontSize=8,   textColor=MID_GREY,    fontName="Helvetica",       leading=11),
        "title":       ParagraphStyle("ti", fontSize=22,  textColor=NAVY,        fontName="Helvetica-Bold",  leading=26, spaceBefore=4),
        "datestamp":   ParagraphStyle("ds", fontSize=9,   textColor=BLUE,        fontName="Helvetica",       leading=12, spaceBefore=2),
        "step_head":   ParagraphStyle("sh", fontSize=13,  textColor=NAVY,        fontName="Helvetica-Bold",  leading=18, spaceBefore=16, spaceAfter=4),
        "section":     ParagraphStyle("sc", fontSize=10,  textColor=NAVY,        fontName="Helvetica-Bold",  leading=14, spaceBefore=10, spaceAfter=3),
        "body":        ParagraphStyle("bo", fontSize=9.5, textColor=NAVY,        fontName="Helvetica",       leading=14),
        "limitation":  ParagraphStyle("li", fontSize=9,   textColor=GREY_DARK,   fontName="Helvetica-Oblique", leading=13, spaceBefore=5),
        "signal_in":   ParagraphStyle("si", fontSize=15,  textColor=GREEN_FILL,  fontName="Helvetica-Bold",  leading=20, alignment=TA_CENTER),
        "signal_out":  ParagraphStyle("so", fontSize=15,  textColor=GREY_DARK,   fontName="Helvetica-Bold",  leading=20, alignment=TA_CENTER),
        "footer":      ParagraphStyle("fo", fontSize=7.5, textColor=MID_GREY,    fontName="Helvetica",       alignment=TA_CENTER),
    }


def _table_style():
    return TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),   NAVY),
        ("TEXTCOLOR",     (0,0), (-1,0),   WHITE),
        ("FONTNAME",      (0,0), (-1,0),   "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1),  9),
        ("FONTNAME",      (0,1), (-1,-1),  "Helvetica"),
        ("ROWBACKGROUNDS",(0,1), (-1,-1),  [WHITE, TABLE_ALT]),
        ("TOPPADDING",    (0,0), (-1,-1),  6),
        ("BOTTOMPADDING", (0,0), (-1,-1),  6),
        ("LEFTPADDING",   (0,0), (-1,-1),  9),
        ("RIGHTPADDING",  (0,0), (-1,-1),  9),
        ("BOX",           (0,0), (-1,-1),  0.5, BORDER),
        ("LINEBELOW",     (0,0), (-1,0),   0.5, BORDER),
        ("GRID",          (0,1), (-1,-1),  0.25, BORDER),
    ])


def _signal_box(s, is_in: bool):
    text  = "Signal +1  —  Own the stock" if is_in else "Signal 0  —  Hold cash"
    style = s["signal_in"] if is_in else s["signal_out"]
    bg    = GREEN_BG if is_in else GREY_BG
    box   = Table([[Paragraph(text, style)]], colWidths=[6.8*inch])
    box.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("BOX",           (0,0), (-1,-1), 1.5 if is_in else 0.5, NAVY if is_in else BORDER),
        ("TOPPADDING",    (0,0), (-1,-1), 14),
        ("BOTTOMPADDING", (0,0), (-1,-1), 14),
    ]))
    return box


def _open(path):
    try:
        if platform.system() == "Darwin":
            subprocess.run(["open", path], check=False)
        elif platform.system() == "Windows":
            os.startfile(path)
        else:
            subprocess.run(["xdg-open", path], check=False)
    except Exception:
        pass


# ── Main function ─────────────────────────────────────────────────────────────
def generate_session_pdf(data: dict) -> str:
    """
    Generate one PDF covering all four steps of the lab session.

    data keys:
      ticker, ma_period, start_date, end_date, trading_days,
      start_price, end_price, total_return,
      df_tail (DataFrame — last 8 rows with Close, SMA_N, Position),
      chart_path, pct_in_market, signal_result (dict from step4)
    """
    ticker     = data["ticker"].upper()
    ma_period  = data["ma_period"]
    result     = data["signal_result"]
    col        = f"SMA_{ma_period}"

    filename   = f"research_{ticker.lower()}_{ma_period}d_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    path       = os.path.join(OUTPUT_DIR, filename)
    s          = _styles()

    doc = SimpleDocTemplate(path, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.75*inch, bottomMargin=0.75*inch)
    story = []

    # ── Cover header ──────────────────────────────────────────────────────────
    story.append(Paragraph(
        f"QSLab Foundation I  /  Unit 1.2 — Your Research Lab",
        s["eyebrow"]))
    story.append(Paragraph(
        f"{ticker}  /  {ma_period}-Day SMA  /  Research Report",
        s["title"]))
    story.append(Paragraph(
        datetime.now().strftime("Generated %B %d, %Y"), s["datestamp"]))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY, spaceAfter=14))

    # ── Step 1 — Data ─────────────────────────────────────────────────────────
    story.append(Paragraph("Step 1 — Data Download", s["step_head"]))
    data_rows = [
        ["Field", "Value"],
        ["Ticker", ticker],
        ["Period", f"{data['start_date']} — {data['end_date']}"],
        ["Trading days", f"{data['trading_days']:,}"],
        ["Start price", f"${data['start_price']:.2f}"],
        ["End price", f"${data['end_price']:.2f}"],
        ["Total return", f"{data['total_return']:+.1f}%"],
    ]
    t = Table(data_rows, colWidths=[2.2*inch, 4.5*inch])
    t.setStyle(_table_style())
    story.append(t)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        f"This is {data['trading_days']:,} trading days of {ticker} history — roughly 21 years "
        f"covering the 2008 financial crisis, the COVID crash in 2020, the 2022 bear market, "
        f"and the recovery since.",
        s["body"]))
    story.append(Paragraph(
        "Limitation: total return alone tells you nothing about the risk taken to achieve it.",
        s["limitation"]))

    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER,
        spaceBefore=12, spaceAfter=4))

    # ── Step 2 — SMA ──────────────────────────────────────────────────────────
    story.append(Paragraph(f"Step 2 — {ma_period}-Day SMA", s["step_head"]))

    # Current position box
    is_in = result["current_signal"] == 1
    story.append(KeepTogether([_signal_box(s, is_in)]))
    story.append(Spacer(1, 8))

    # Last 8 rows table
    story.append(Paragraph("Last 8 trading days", s["section"]))
    sma_rows = [["Date", "Close", f"SMA {ma_period}d", "Position"]]
    for date, row in data["df_tail"].iterrows():
        marker = " Today" if date == data["df_tail"].index[-1] else ""
        pos = "Above" if "Above" in str(row.get("Position","")) else "Below"
        sma_rows.append([
            date.strftime("%Y-%m-%d"),
            f"${row['Close']:.2f}",
            f"${row[col]:.2f}" if col in row else "—",
            f"{pos}{marker}",
        ])
    t2 = Table(sma_rows, colWidths=[1.8*inch, 1.4*inch, 1.6*inch, 1.9*inch])
    t2.setStyle(_table_style())
    story.append(t2)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        f"The {ma_period}-day SMA averages the last {ma_period} daily prices. "
        f"One bad day shifts it by only 1/{ma_period}th — that smoothing reveals the underlying trend.",
        s["body"]))
    story.append(Paragraph(
        "Limitation: the SMA is backward-looking. It reacts to price moves — it does not predict them.",
        s["limitation"]))

    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER,
        spaceBefore=12, spaceAfter=4))

    # ── Step 3 — Chart ────────────────────────────────────────────────────────
    story.append(Paragraph("Step 3 — Signal Zone Chart", s["step_head"]))

    zone_rows = [
        ["Zone", "Meaning", "% of Period"],
        ["Green", f"Signal +1 — Strategy owned {ticker}", f"{data['pct_in_market']:.1f}%"],
        ["Grey",  "Signal 0 — Strategy held cash",         f"{round(100-data['pct_in_market'],1):.1f}%"],
    ]
    zt = Table(zone_rows, colWidths=[0.9*inch, 4.4*inch, 1.4*inch])
    zt.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",   (0,0), (-1,0), WHITE),
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,-1), 9),
        ("FONTNAME",    (0,1), (-1,-1), "Helvetica"),
        ("BACKGROUND",  (0,1), (0,1),  GREEN_BG),
        ("BACKGROUND",  (0,2), (0,2),  GREY_BG),
        ("TOPPADDING",  (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 9),
        ("BOX",         (0,0), (-1,-1), 0.5, BORDER),
        ("LINEBELOW",   (0,0), (-1,0),  0.5, BORDER),
        ("GRID",        (0,1), (-1,-1), 0.25, BORDER),
    ]))
    story.append(zt)
    story.append(Spacer(1, 8))

    if data.get("chart_path") and os.path.exists(data["chart_path"]):
        story.append(Image(data["chart_path"], width=7.0*inch, height=3.5*inch))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Green background: strategy owned the stock. "
        "Grey background: strategy held cash. "
        "Look at the grey zones — do any align with market events you recognise?",
        s["body"]))
    story.append(Paragraph(
        "Limitation: this chart shows hindsight. At the time each signal fired, "
        "the strategy did not know whether it was avoiding a crash or missing a rally.",
        s["limitation"]))

    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER,
        spaceBefore=12, spaceAfter=4))

    # ── Step 4 — Return Comparison ─────────────────────────────────────────────
    story.append(Paragraph("Step 4 — Return Comparison", s["step_head"]))

    strat_cagr = data["strat_cagr"]
    bah_cagr   = data["bah_cagr"]

    return_rows = [
        ["", "Return per year"],
        ["Strategy (SMA rule)", f"{strat_cagr:.1f}%"],
        [f"Buy-and-hold ({ticker})", f"{bah_cagr:.1f}%"],
    ]
    rt = Table(return_rows, colWidths=[3.5*inch, 3.2*inch])
    rt.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 10),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("BOX",           (0,0), (-1,-1), 0.5, BORDER),
        ("LINEBELOW",     (0,0), (-1,0),  0.5, BORDER),
        ("GRID",          (0,1), (-1,-1), 0.25, BORDER),
    ]))
    story.append(rt)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        f"Both figures are annualised returns over the full 20-year period. "
        f"The strategy owned {ticker} only when price was above the {ma_period}-day SMA — "
        f"holding cash otherwise. Buy-and-hold owned it continuously.",
        s["body"]))
    story.append(Paragraph(
        "Limitation: return alone does not tell you whether the strategy was worth using. "
        "Risk, drawdown, and costs matter. We cover those in the modules ahead.",
        s["limitation"]))

    # ── Footer ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER,
        spaceBefore=4, spaceAfter=4))
    story.append(Paragraph(f"Saved to: {path}", s["footer"]))

    doc.build(story)

    print(f"\n  Research report: {path}")
    _open(path)
    return path
