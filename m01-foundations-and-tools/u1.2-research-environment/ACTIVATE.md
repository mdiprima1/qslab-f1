# QSLab F1-1.2 — Student Activation
## Copy the prompt below and paste into a fresh Claude Code session

---

```
Please set up and start QSLab F1-1.2.

Step 1 — Get the files:
Check if ~/qslab-f1 exists. If not, clone it:
  git clone https://github.com/mdiprima1/qslab-f1.git ~/qslab-f1
If it exists, run:
  cd ~/qslab-f1 && git pull

Step 2 — Install packages:
  pip install yfinance pandas matplotlib reportlab Pillow --quiet

Step 3 — Read these files IN THIS ORDER before doing anything else:
  1. ~/qslab-f1/CLAUDE.md
  2. ~/qslab-f1/QSL-POLICIES.md
  3. ~/qslab-f1/QSL-PDF-STANDARD.md
  4. ~/qslab-f1/m01-foundations-and-tools/u1.2-research-environment/CLAUDE.md
  5. ~/qslab-f1/m01-foundations-and-tools/u1.2-research-environment/lab_1_2.py

Step 4 — Start the lab:
Ask me which stock to analyse and what MA period.
Then call run_lab(ticker, ma_period) and let it run automatically.
Display the signal chart inline when done.
Print the PDF path from the run_lab() return value — do not open or display the file.
Then ask if I want to run the analysis on a different stock.
```

---

## What happens

1. You are asked two questions: which stock? what MA period?
2. All four steps run automatically — no pausing
3. A progress bar shows between steps
4. One research report PDF opens when complete
5. You are offered to run the same analysis on a different stock

## Output location

Your research report saves to: `~/QSLab-Output/`
Filename: `research_[TICKER]_[N]d_[date].pdf`
