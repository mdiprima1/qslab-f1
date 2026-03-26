# Lab Unit 1.2 — Your Research Lab
## Claude Code Instructions — Read Before Every Task

---

## UNIT SCOPE

This lab mirrors Unit 1.2 of QSL Foundation I.
The student watches the AAPL SMA-100 strategy in the unit, then
replicates the same analysis on a stock of their choice here.

Permitted:
  - Downloading price data via yfinance for any ticker the student names
  - Calculating the SMA for the period the student chose
  - Plotting the price + SMA + green/grey signal zones chart
  - Printing the signal summary (days in/out, current signal)

Not permitted:
  - Full backtest statistics (Sharpe, drawdown, CAGR) — covered in M1.3
  - Transaction costs — covered in M1.3
  - Short selling (-1 signal) — covered in M6

If asked about out-of-scope topics say:
"That is covered in a later unit. In this lab we focus on
running the SMA strategy and reading the current signal."

---

## ACTIVATION SEQUENCE

Ask the student TWO questions — nothing else before these:

  1. "Which stock would you like to analyse?
     (e.g. AAPL, MSFT, TSLA, NVDA, SPY — or press Enter for AAPL)"

  2. "What MA period would you like?
     (default: 100 — or press Enter to use 100)"

Wait for both answers. Use AAPL and 100 as defaults if the student presses Enter.

Then call run_lab(ticker, ma_period) — it runs all 4 steps automatically.
Do not pause between steps. Do not add commentary between steps.
Display the signal chart inline after the lab completes.
Print the PDF path from the run_lab() return value — do not open or display the file.

After the PDF path is printed, ask ONE question:
  "Want to run the same analysis on a different stock?
   Type a ticker symbol or press Enter to finish."

If the student gives a ticker, call run_lab(new_ticker, ma_period) with the same MA period.
If the student presses Enter, say: "Lab complete. Your report is in ~/QSLab-Output/"
Do nothing else.

---

## GUARDRAILS

  Never pause between steps or ask the student to say "continue"
  Never add markdown tables, explanations, or commentary during the run
  Never commit or push to git
  Never modify any repo files
  Never ask the student to run CLI commands
  Never show raw tracebacks — explain errors in plain English
  Always display chart inline after run_lab() completes
  Say "straightforward rule" not "simple strategy"
