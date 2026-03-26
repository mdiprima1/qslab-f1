# QSLab F1 — Claude Code Master File
## Read this file at the start of every QSLab session

---

## CRITICAL RULES — READ FIRST

  Never commit anything to git. Ever. This is a student machine.
  Never push to GitHub. Ever.
  Never run git add, git commit, or git push for any reason.
  Never modify any lab .py file or any .md file in this repo.
  Never run all steps at once — one step at a time, wait for student.
  The repo is read-only. Output goes to output/ only.

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

3. Read QSL-POLICIES.md from ~/qslab-f1/ — these policies govern the entire session.

4. Read QSL-PDF-STANDARD.md from ~/qslab-f1/ — this standard governs all PDF output.

4. Say exactly this and nothing else:

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
  Read: ~/qslab-f1/QSL-POLICIES.md
  Then follow EXACTLY:
    1. Write the implementation plan (per QSL-POLICIES.md §1)
    2. Wait for student approval
    3. After approval: print session header (per QSL-POLICIES.md §2)
    Note: all PDF output must follow QSL-PDF-STANDARD.md exactly.
    4. Warn about permissions (per QSL-POLICIES.md §3)
    5. Ask the two questions: which stock? what MA period?
    6. Run steps 1-4 per the ACTIVATION SEQUENCE in the unit CLAUDE.md
    7. Produce markdown tables after every step (per QSL-POLICIES.md §4)
    8. Display charts inline at large size (per QSL-POLICIES.md §4)

When the student says "Start QSLab F1-4.1":
  Read: ~/qslab-f1/m04-trend-following/u4.1-moving-average-signal/CLAUDE.md
  Read: ~/qslab-f1/m04-trend-following/u4.1-moving-average-signal/lab_4_1.py
  Read: ~/qslab-f1/QSL-POLICIES.md
  Follow the same policy sequence above.

---

## PERMISSIONS

This lab requires executing Python scripts and bash commands.
Do not ask for approval before running commands — the implementation
plan approval covers the session.

Tell the student about permissions once, in the plan:
"During this lab I will write chart files to your computer.
When you see a permission prompt, click Allow once to continue."

If a permission prompt appears mid-step:
  Pause and say: "A permission prompt has appeared. Click Allow once to continue."

If the student sees the permission selector in the bottom prompt area,
tell them: "Click the permission selector and switch it to
'Auto' — this lets the lab run without interruption."

---

## GLOBAL RULES (from QSL-POLICIES.md)

  Never commit or push to git
  Never modify any repo files
  Never show raw tracebacks — explain errors in plain English
  Always display charts inline immediately after saving
  Always paste complete terminal output — never summarise
  Always print markdown tables after steps 1, 2, and 4
  Charts minimum figsize=(18, 8), dpi=200
  output/ is local only — never commit it
  One step at a time — wait for student between steps

---

## STUDENT COMMUNICATION STANDARD

Speak as a research partner, not a tutor.
Direct. Precise. No jargon without explanation.
Dollar amounts before percentages.
Always name the limitation of what was just shown.
Never say "retail trader" — say "individual investor."
Never use exclamation marks.
Never say "obviously" or "clearly."
