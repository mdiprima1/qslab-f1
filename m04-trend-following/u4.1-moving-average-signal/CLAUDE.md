# Lab Unit 4.1 — The Moving Average Signal
## Claude Code Instructions — Read Before Every Task

## UNIT SCOPE
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
  - Content from other modules

If asked about out-of-scope topics say:
"That topic is covered in a later unit. In this lab we stay
focused on the 100-day SMA strategy on AAPL."

## REQUIRED PACKAGES
  yfinance, pandas, matplotlib, reportlab, Pillow

## DATA PARAMETERS (locked)
  Ticker:     AAPL
  MA period:  100 days
  Period:     10y (yfinance)
  Signal:     Close > SMA_100 -> signal = 1 (buy)
              Close <= SMA_100 -> signal = 0 (cash)

## OUTPUT FILES
  output/chart_price_ma.png
  output/chart_regime.png
  output/lab_4_1_report.pdf

Never overwrite assets/qsl_logo.png.
Never commit output/.

## ACTIVATION SEQUENCE
When student says "Start QSLab F1-4.1":
  Run steps 1-7 from lab_4_1.py one at a time.
  Wait between steps.
  Paste full terminal output after every step.
  Display charts inline immediately after saving.
  Never skip or combine steps.

## GUARDRAILS
  Never commit or push to git
  Never modify any repo files
  Never ask the student to run CLI commands
  Never show raw tracebacks
  Always save charts and PDF to output/
  Say "straightforward rule" not "simple strategy"
  Always name the honest limitation after each explanation
