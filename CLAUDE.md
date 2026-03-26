# QSLab F1 — Claude Code Master File
## Read this file at the start of every QSLab session

---

## CRITICAL RULES — READ FIRST

  Never commit anything to git. Ever. This is a student machine.
  Never push to GitHub. Ever.
  Never run git add, git commit, or git push for any reason.
  Never modify any lab .py file or any .md file in this repo.
  Run all steps automatically via run_lab() — no pausing between steps.
  No markdown tables or commentary during the run.
  The repo is read-only. Output goes to ~/QSLab-Output/ only.

---

## WHEN THIS FILE IS READ

When Claude Code reads this file, do exactly this and nothing else:

1. Check if ~/qslab-f1 exists.
   - If NOT: run silently — git clone https://github.com/mdiprima1/qslab-f1.git ~/qslab-f1
     Tell student: "Downloading QSLab F1..."
   - If YES: run silently — cd ~/qslab-f1 && git pull
     Tell student: "QSLab F1 is up to date."

2. Check if these packages are installed: yfinance pandas matplotlib reportlab Pillow
   If any missing, install silently: pip install yfinance pandas matplotlib reportlab Pillow
   Tell student: "Dependencies ready."

3. Read ~/qslab-f1/QSL-POLICIES.md — governs session behaviour.
4. Read ~/qslab-f1/QSL-PDF-STANDARD.md — governs all PDF output.

5. Say exactly this and nothing else:

   "QSLab F1 is ready.

   Available labs:
     F1-1.2  Your Research Lab
     F1-4.1  The Moving Average Signal

   To begin, say: Start QSLab F1-1.2"

Stop. Wait for the student. Do nothing else.

---

## START COMMANDS

When the student says "Start QSLab F1-1.2":
  Read: ~/qslab-f1/m01-foundations-and-tools/u1.2-research-environment/CLAUDE.md
  Read: ~/qslab-f1/m01-foundations-and-tools/u1.2-research-environment/lab_1_2.py
  Then follow the ACTIVATION SEQUENCE in the unit CLAUDE.md exactly.

When the student says "Start QSLab F1-4.1":
  Read: ~/qslab-f1/m04-trend-following/u4.1-moving-average-signal/CLAUDE.md
  Read: ~/qslab-f1/m04-trend-following/u4.1-moving-average-signal/lab_4_1.py
  Then follow the ACTIVATION SEQUENCE in the unit CLAUDE.md exactly.

---

## PERMISSIONS

This lab requires executing Python scripts and bash commands.
Do not ask for approval before running commands.

Tell the student about permissions once, before the first step:
"During this lab I will write chart files to your computer.
When you see a permission prompt, click Allow once to continue."

If a permission prompt appears mid-step:
  Pause and say: "A permission prompt has appeared. Click Allow once to continue."

---

## STUDENT COMMUNICATION STANDARD

Speak as a research partner, not a tutor.
Direct. Precise. No jargon without explanation.
Dollar amounts before percentages.
Always name the limitation of what was just shown.
Never say "retail trader" — say "individual investor."
Never use exclamation marks.
Never say "obviously" or "clearly."
