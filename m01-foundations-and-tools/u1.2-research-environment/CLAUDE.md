# Lab Unit 1.2 — Your Research Lab
## Claude Code Instructions — Read Before Every Task

---

## UNIT SCOPE

This lab mirrors Unit 1.2 of QSL Foundation I.
The student watches the AAPL SMA-100 strategy in the unit, then
replicates the same analysis on a stock of their choice here.

Permitted:
  - Downloading price data via yfinance for any ticker the student names
  - Calculating the 100-day SMA
  - Plotting the price + SMA + green/grey signal zones chart
  - Printing the signal summary (days in/out, current signal)

Not permitted:
  - Full backtest statistics (Sharpe, drawdown, CAGR) — covered in M1.3
  - PDF report — covered in M4.1
  - Transaction costs — covered in M1.3
  - Short selling (-1 signal) — covered in M6
  - Any MA period other than what the student chose (or default 100)
    (the rerun prompt after step 4 offers a second period)

If asked about out-of-scope topics say:
"That is covered in a later unit. In this lab we focus on
running the 100-day SMA strategy and reading the current signal."

---

## REQUIRED PACKAGES

  yfinance, pandas, matplotlib

Install if missing: pip install yfinance pandas matplotlib

---

## DATA PARAMETERS

  Ticker:     Student's choice — Claude Code asks them
              Default to AAPL if student does not specify
  MA period:  Student's choice — default 100, try 50 or 200
  Period:     20 years (from 2005-01-01)
  Signal:     Close > SMA_{period} → signal = +1 (in market)
              Close ≤ SMA_{period} → signal =  0 (in cash)

---

## OUTPUT FILES

  output/chart_signal_{ticker}.png  — signal zone chart

Never commit output/.

---

## ACTIVATION SEQUENCE

When student says "Start QSLab F1-1.2":

  First, ask the student TWO questions:

  1. "Which stock would you like to analyse?
     Type a ticker symbol (e.g. AAPL, MSFT, TSLA, NVDA, SPY)
     or press Enter to use AAPL."

  2. "What MA period? (default: 100 — try 50 or 200)"

  Wait for their answers. Store ticker and ma_period.
  If they press Enter or give no value, use AAPL and 100.

  Then execute steps 1–4 in order.
  Run one step at a time. Wait for student to say "continue" or "next".
  Paste full terminal output after every step.

  Step 1 — Run step1_download_data(ticker) in lab_1_2.py
    Paste complete output.
    Then print a markdown table in the chat (per QSL-POLICIES.md §4):
    | Field | Value |
    Ticker, Period, Trading days, Start price, End price, Total return.
    Explain: what the date range means, what the total return tells them.

  Step 2 — Run step2_calculate_sma(df, ma_period) in lab_1_2.py
    Paste complete output.
    Then print last 8 rows as a markdown table in the chat (per QSL-POLICIES.md §4):
    | Date | Close | SMA_{period} | Position |
    Explain: why the SMA moves slowly, what Above/Below means for the signal.

  Step 3 — Run step3_plot_signal_chart(df, ticker, ma_period) in lab_1_2.py
    Display the chart inline immediately after saving.
    Chart must be large — minimum figsize=(18, 8), dpi=200.
    Chart must remain visible in the chat after step 4 runs.
    Paste the printed summary.
    Explain: what the green and grey zones show, name one real-world event
    visible in the chart if possible (e.g. 2022 bear market, March 2020).

  Step 4 — Run step4_signal_summary(df, ticker, ma_period) in lab_1_2.py
    Paste complete output.
    Then print a markdown summary table in the chat (per QSL-POLICIES.md §4):
    | Metric | Value |
    Days in market, Days in cash, Signal changes, Current signal,
    Current close, Current SMA, Points to flip.
    Explain the signal flip line in plain English.

  After Step 4 — Run rerun_prompt(df_raw, ticker, ma_period, transitions)
    Show the rerun offer. If student enters a new period:
    Run run_rerun(df_raw, ticker, new_period, ma_period, transitions)
    Then run print_closing().
    If student presses Enter with no input, run print_closing() directly.

---

## GUARDRAILS

  Never commit or push to git
  Never modify any repo files
  Never ask the student to run CLI commands
  Never show raw tracebacks — explain errors in plain English
  Never skip or combine steps
  Always display chart inline immediately after saving
  Always name the honest limitation after each explanation
  Say "straightforward rule" not "simple strategy"
