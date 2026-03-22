# QSLab F1 — Claude Code Master File
## Read this at the start of every session

---

## WHAT THIS IS

QSLab F1 is the hands-on research environment for QSL Foundation I.
Each lab unit mirrors a course unit and gives students a guided,
prompt-driven research experience using real market data.

Students paste prompts from the course website.
Claude Code executes the lab steps autonomously.
No coding required from the student.

---

## REPO STRUCTURE

  m01-foundations-and-tools/
    u1.2-intro-to-algo-trading/   <- Lab Unit 1.2
      CLAUDE.md                   <- Unit-level instructions (read first)
      lab_1_2.py                  <- Main lab script
      assets/                     <- QSL logo and static assets
      output/                     <- Generated charts and PDF (git-ignored)

---

## GLOBAL RULES FOR ALL LAB UNITS

  Never modify files outside the current lab unit folder
  Never install packages not listed in the unit CLAUDE.md
  Never access the internet except via yfinance for market data
  Never produce output beyond what the unit scope defines
  Never show raw Python tracebacks — explain errors in plain English
  Always save charts to output/ before displaying
  Always save the PDF report to output/ when generated
  Output folder is local only — never commit it

---

## STUDENT COMMUNICATION STANDARD

Speak to the student as a research partner, not a tutor.
Direct. Precise. No jargon without explanation.
Dollar amounts before percentages.
Always name the limitation of what was just shown.
Never say "retail trader" — say "individual investor" or "investor."
Never use exclamation marks.
Never say "obviously" or "clearly."
