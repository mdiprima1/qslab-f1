# QSLab F1-1.2 — Activation Prompt
# This is the ONLY thing the student pastes into Claude Code Desktop App.
# Claude Code handles everything else automatically.

---

You are setting up and running QSLab F1 — the hands-on research environment
for QSL Foundation I. The student has pasted this prompt. Do everything below
automatically. Do not ask the student to run any commands.

STEP 1 — Check if the repo exists locally

Check if ~/qslab-f1 exists and contains CLAUDE.md.

If it does NOT exist:
  - Clone it silently:
    git clone https://github.com/mdiprima1/qslab-f1.git ~/qslab-f1
  - Tell the student: "Downloading QSLab F1... done."

If it already exists:
  - Pull the latest version silently:
    cd ~/qslab-f1 && git pull
  - Tell the student: "QSLab F1 is up to date."

STEP 2 — Check Python dependencies

Check if these packages are installed: yfinance, pandas, matplotlib, reportlab, Pillow.
If any are missing, install them silently:
  pip install yfinance pandas matplotlib reportlab Pillow

Do not show the installation output to the student.
Tell the student: "Dependencies ready."

STEP 3 — Read the lab instructions

Read these three files:
1. ~/qslab-f1/CLAUDE.md — global rules
2. ~/qslab-f1/m01-foundations-and-tools/u1.2-intro-to-algo-trading/CLAUDE.md — unit scope and guardrails
3. ~/qslab-f1/m01-foundations-and-tools/u1.2-intro-to-algo-trading/lab_1_2.py — the lab script

STEP 4 — Welcome the student

After completing steps 1-3, say exactly this and nothing else:

"QSLab F1-1.2 is ready.

In this lab you will build the AAPL moving average strategy
from Unit 1.2 of your course — using real market data.

When you are ready to begin, say: Start QSLab F1-1.2"

Wait for the student. Do not start any analysis until they say "Start QSLab F1-1.2".
