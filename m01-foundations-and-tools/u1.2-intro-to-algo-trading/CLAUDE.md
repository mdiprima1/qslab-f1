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

When student says "Start QSLab F1-1.2", run lab_1_2.py step by step.
Pause after each step. Explain before moving on.

  Step 1 — Download data, show dataframe, explain columns
  Step 2 — Calculate SMA-100, show amended dataframe, explain
  Step 3 — Plot price and SMA, explain what to look for
  Step 4 — Explain the strategy rule in plain English
  Step 5 — Generate signals, plot regime chart, explain zones
  Step 6 — Compute stats, display, explain each number
  Step 7 — Generate PDF report, confirm saved to output/

If student says "continue" or "next", proceed to the next step.

---

## GUARDRAILS

  Never skip or combine steps
  Never run ahead of the student
  Never generate PDF before steps 1-6 are complete
  Never show a chart without explaining it
  Say "straightforward rule" not "simple strategy"
  Always name the honest limitation after each explanation
