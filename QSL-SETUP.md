# QSL Lab Setup Guide
## QSLab F1 — Foundation I Research Environment

This guide is read by Claude Code during QSLab initialisation.
It defines what a correct setup looks like.

## What a correct setup includes
  - Python 3.10 or later installed
  - Git installed
  - qslab-f1 repo cloned to ~/qslab-f1
  - All required packages installed (see QSL-REQUIREMENTS.txt)
  - output/ directory writable in each unit folder

## Verification steps Claude Code runs
  1. python3 --version  (must be 3.10+)
  2. python3 -c "import yfinance, pandas, matplotlib, reportlab, Pillow"
     (all must import without error)
  3. python3 -c "import yfinance; d = yfinance.download('SPY', period='5d', progress=False); print('OK' if len(d) > 0 else 'FAIL')"
     (must print OK)

## What to do if verification fails
  - Python missing: install from python.org
  - Package missing: pip install [package]
  - Import error: pip install --upgrade [package]
  - Data download fails: check internet connection

## What Claude Code must never do during setup
  - Never ask the student to run CLI commands manually
  - Never show raw tracebacks
  - Explain all errors in plain English
  - Complete setup silently — only speak when done or when an
    error requires student action
