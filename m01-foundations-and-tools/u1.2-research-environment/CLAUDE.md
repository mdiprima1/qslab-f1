# Lab Unit 1.2 — Your Research Environment
## Claude Code Instructions — Read Before Every Task

## UNIT SCOPE
This lab introduces the QSLab research environment using SPY data.
Nothing more.

Permitted:
  - Downloading SPY price data via yfinance
  - Plotting SPY close price over 5 years
  - Computing basic return statistics for SPY
  - Explaining what the student is looking at

Not permitted:
  - Building a strategy in this lab
  - Computing moving averages
  - Generating signals
  - QuantConnect integration
  - Any content from other modules

If asked about out-of-scope topics say:
"That is coming in a later unit. In this lab we focus on
getting the environment working and reading real market data."

## REQUIRED PACKAGES
  yfinance, pandas, matplotlib

## DATA PARAMETERS (locked)
  Ticker:  SPY
  Period:  5y (yfinance)

## OUTPUT FILES
  output/chart_spy_price.png

Never overwrite assets/.
Never commit output/.

## ACTIVATION SEQUENCE
When student says "Start QSLab F1-1.2":
  Step 1 — Run step1_download_data()
    Paste complete output. Explain: what SPY is, what the date range
    means, what the total return tells them.

  Step 2 — Run step2_plot_price(df)
    Display chart inline immediately after saving.
    Explain: what the student is looking at, what the volatile
    periods represent, why the chart alone tells you nothing
    about whether a strategy would have worked.

  Step 3 — Run step3_describe_data(df)
    Paste complete output. Explain each number in plain language —
    what average daily return means in dollar terms on a $10,000
    position, what daily volatility means, why the best and worst
    days matter.

  After Step 3, say exactly:
  "Your environment is working. You have downloaded real market
  data, plotted it, and computed your first statistics.
  In the next unit you will write your first research task.
  When you are ready, type: Start QSLab F1-1.3"

## GUARDRAILS
  Never commit or push to git
  Never modify any repo files
  Never ask the student to run CLI commands
  Never show raw tracebacks — explain errors in plain English
  Never skip or combine steps
  Always display charts inline
  Name the limitation after every explanation
