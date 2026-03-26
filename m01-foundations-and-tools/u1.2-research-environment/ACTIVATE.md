# QSLab F1-1.2 — Student Activation
## Copy the prompt below and paste into a fresh Claude Code session

---

```
Please set up and start QSLab F1-1.2.

Check if ~/qslab-f1 exists:
  If not: git clone https://github.com/mdiprima1/qslab-f1.git ~/qslab-f1
  If yes: cd ~/qslab-f1 && git pull

Then read ~/qslab-f1/CLAUDE.md and follow it exactly.
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
