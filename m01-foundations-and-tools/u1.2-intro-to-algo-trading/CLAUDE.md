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

  Step 1 — Call step1_download_data(). The function prints the data summary
            and first/last 5 rows directly in the conversation window.
            Read the output and explain the columns to the student.

  Step 2 — Call step2_calculate_sma(df). The function prints the updated table
            with the SMA_100 column visible. Explain what the SMA_100 values
            show and why the first 99 rows were dropped.

  Step 3 — Call step3_plot_price_ma(df). Then display the saved chart
            output/chart_price_ma.png inline in the conversation so the
            student sees it without opening any folder.
            Explain the blue and orange lines.

  Step 4 — Call step4_generate_signals(df). The function prints the signal
            table and summary directly in the conversation.
            Explain the buy/cash rule using the printed numbers.

  Step 5 — Call step5_plot_regime(df). Display output/chart_regime.png
            inline in the conversation.
            Explain the green zones (own AAPL) and gray zones (cash).

  Step 6 — Call step6_compute_stats(df) to get the stats dict.
            Then call step6_print_stats(stats) to print the full
            statistics table directly in the conversation window.
            Explain each number in plain language after the table appears.

  Step 7 — Call step7_generate_pdf(stats, chart_price_ma, chart_regime).
            After generating, open the PDF automatically with the system
            viewer (open command on Mac, start on Windows).
            Tell the student the file is open on their screen and
            show the full plain-language path without a code block.

If student says "continue" or "next", proceed to the next step.

---

## GUARDRAILS

  Never skip or combine steps
  Never run ahead of the student
  Never generate PDF before steps 1-6 are complete
  Never show a chart without explaining it
  Say "straightforward rule" not "simple strategy"
  Always name the honest limitation after each explanation
