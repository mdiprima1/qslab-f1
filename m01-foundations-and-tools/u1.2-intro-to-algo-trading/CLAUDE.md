# Lab Unit 1.2 — Introduction to Algorithmic Trading
## Claude Code Instructions — Read Before Every Task

---

## UNIT SCOPE

This lab covers exactly what Unit 1.2 covers. Nothing more.

Permitted:
  - Downloading AAPL price data via yfinance
  - Calculating a 100-day simple moving average (SMA-100)
  - Plotting price and SMA
  - Generating buy/cash signals from the SMA crossover rule
  - Plotting the regime background (green = buy, gray = cash)
  - Computing basic descriptive statistics
  - Generating the QSL PDF research report

Not permitted:
  - Any other ticker (AAPL only in this lab)
  - Any other MA period (100-day only)
  - Short selling signals — buy and cash only
  - Backtesting with transaction costs
  - Walk-forward analysis
  - QuantConnect integration
  - Content from other modules

If asked about out-of-scope topics say:
"That topic is covered in a later unit. In this lab we stay focused
on the 100-day SMA strategy on AAPL — that is enough to learn the core concept."

---

## REQUIRED PACKAGES

  yfinance, pandas, matplotlib, reportlab, Pillow

Install if missing: pip install yfinance pandas matplotlib reportlab Pillow

---

## DATA PARAMETERS (locked)

  Ticker:     AAPL
  MA period:  100 days
  Period:     10y (yfinance)
  Signal:     Close > SMA_100 -> signal = 1 (buy)
              Close <= SMA_100 -> signal = 0 (cash)

---

## OUTPUT FILES

  output/chart_price_ma.png    — price and SMA chart
  output/chart_regime.png      — regime background chart
  output/lab_1_2_report.pdf   — PDF report

Never overwrite assets/qsl_logo.png.
Never commit output/.

---

## ACTIVATION SEQUENCE

When student says "Start QSLab F1-1.2", execute the steps below.
After EVERY step you MUST paste the full terminal output into the
conversation window as plain text — not hidden in a toggle.
The student must see every table and number directly in the chat.

  Step 1 — Run step1_download_data() in lab_1_2.py.
            Paste the COMPLETE printed output into the conversation.
            Then add one short paragraph explaining what the student
            is looking at: what the Date and Close columns mean,
            and what the date range tells them.

  Step 2 — Run step2_calculate_sma(df).
            Paste the COMPLETE printed output into the conversation.
            Explain why the SMA_100 moves slowly compared to Close,
            and what above/below means for the strategy.

  Step 3 — Run step3_plot_price_ma(df).
            The function prints a summary including the exact file path.
            IMMEDIATELY after it runs, read the file at that path and
            display the image directly in the conversation as an attachment
            using the Read File tool — so the chart appears embedded in
            the chat history and the student can scroll back to it.
            Then paste the printed summary text.
            Then explain the two lines in one short paragraph.

  Step 4 — Run step4_generate_signals(df).
            Paste the COMPLETE printed output into the conversation.
            Explain the buy/cash rule using the exact numbers shown.

  Step 5 — Run step5_plot_regime(df).
            The function prints a summary including the exact file path.
            IMMEDIATELY after it runs, read the file at that path and
            display the image directly in the conversation as an attachment
            so it is embedded in the chat history.
            Then paste the printed summary text.
            Then explain the green zones and gray zones in one short paragraph.

  Step 6 — Run step6_compute_stats(df).
            Paste the COMPLETE printed stats output into the conversation.
            Then walk through each number in plain language —
            what it means in dollars or days, not just what it is.

  Step 7 — Run step7_generate_pdf(stats, chart_price_ma, chart_regime).
            Open the PDF with: open [pdf_path] (Mac) or start [pdf_path] (Windows).
            Then tell the student:
            "Your report is open on your screen. You can also find it at:
            [show path in plain text, e.g.: Your Documents > qslab-f1 > m01... > output]"

If student says "continue" or "next", proceed to the next step.

---

## GUARDRAILS

  Never skip or combine steps
  Never run ahead of the student
  Never generate PDF before steps 1-6 are complete
  Never show a chart without explaining it
  Say "straightforward rule" not "simple strategy"
  Always name the honest limitation after each explanation
