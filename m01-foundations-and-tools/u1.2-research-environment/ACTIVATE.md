# QSLab F1-1.2 — Student Activation Prompt
## Copy this entire block and paste it into a new Claude Code session

---

## COPY FROM HERE ↓

Please do the following in order. Do not skip any step.

**Step 1 — Get the lab files**

Check if the folder ~/qslab-f1 exists on this computer.

If it does NOT exist:
  Run: git clone https://github.com/mdiprima1/qslab-f1.git ~/qslab-f1
  Tell me: "Lab files downloaded."

If it already exists:
  Run: cd ~/qslab-f1 && git pull
  Tell me: "Lab files are up to date."

**Step 2 — Install required packages**

Run: pip install yfinance pandas matplotlib --quiet
Tell me: "Packages ready."

**Step 3 — Read the lab instructions**

Read this file: ~/qslab-f1/CLAUDE.md
Then read: ~/qslab-f1/m01-foundations-and-tools/u1.2-research-environment/CLAUDE.md
Then read: ~/qslab-f1/m01-foundations-and-tools/u1.2-research-environment/lab_1_2.py

**Step 4 — Start the lab**

Follow the ACTIVATION SEQUENCE in the unit CLAUDE.md exactly.
Ask me the two questions (which stock, which MA period), then run steps 1-4 one at a time.

## COPY TO HERE ↑

---

## FOR THE SLIDE PROMPT (what appears on the unit slide)

The slide shows a single copyable prompt:

```
Please set up and start QSLab F1-1.2. Check if ~/qslab-f1 exists — if not, clone it from github.com/mdiprima1/qslab-f1. If yes, run git pull. Then install yfinance, pandas, and matplotlib if needed. Then read ~/qslab-f1/CLAUDE.md and ~/qslab-f1/m01-foundations-and-tools/u1.2-research-environment/CLAUDE.md and follow the activation sequence.
```

This is one prompt, pasted once, works from a cold session.
