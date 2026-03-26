# QSLab F1 — PDF Layout Standard
## Version 1.0 — 2026-03-26

This file is read by Claude Code before generating any PDF.
Every QSLab PDF must follow this standard exactly.

---

## OUTPUT LOCATION

Always: ~/QSLab-Output/
Created automatically if it does not exist.
Never save inside the qslab-f1 repo.

---

## PAGE SETUP

Page size:    Letter (8.5 × 11 inches)
Margins:      0.75 inch all sides
Font family:  Helvetica only (Regular, Bold, Oblique)

---

## SECTION 1 — PAGE HEADER (every PDF, always first)

Three lines, top of page:

Line 1 — Eyebrow (8pt, grey #9E9E9E):
  "QSLab Foundation I  /  Unit [M.N] — [Unit Title]  /  [TICKER]  /  [N]-Day SMA"

Line 2 — Title (22pt, navy #0A1628, bold):
  "Step [N] — [Step Title]"

Line 3 — Datestamp (9pt, blue #1565C0):
  "Generated [Month DD, YYYY]"

Followed by: 2pt navy horizontal rule, 12pt space below

---

## SECTION 2 — SIGNAL BOX (steps 2, 4, rerun only)

A full-width coloured box immediately after the header.
Height: fixed at 50pt (14pt top padding, 14pt bottom padding, 15pt font).
Width: full text width.

Signal +1 (in market):
  Background: #E8F5E9 (light green)
  Border: 1.5pt navy
  Text: "Signal +1  —  Own the stock"
  Text colour: #1B5E20 (dark green), 15pt bold, centred

Signal 0 (in cash):
  Background: #F5F5F5 (light grey)
  Border: 1.5pt #E0E0E0 (grey)
  Text: "Signal 0  —  Hold cash"
  Text colour: #616161 (dark grey), 15pt bold, centred

Rule: never use special characters or symbols in the signal text.
Use plain ASCII only — "Signal +1" not "▶ Signal +1".

---

## SECTION 3 — DATA TABLES

Header row:
  Background: navy #0A1628
  Text: white, 9pt bold
  Padding: 6pt top and bottom, 9pt left and right

Data rows:
  Alternating white / #FAFAFA
  Text: navy, 9pt regular
  Padding: same as header
  Grid lines: 0.25pt #E0E0E0 between rows
  Outer border: 0.5pt #E0E0E0

Two-column tables (label / value):
  Column 1 width: 2.8 inch
  Column 2 width: 3.9 inch

Multi-column tables (3+ columns):
  Distribute widths evenly across 6.7 inch text width
  Left column (labels): 2.0–2.5 inch
  Remaining columns: equal share

---

## SECTION 4 — SECTION HEADERS

Within the body, section headers separate content blocks.

Style: 10pt bold, navy, 14pt leading
Space before: 14pt
Space after: 4pt

Example sections: "What this tells you" / "Last 8 trading days" /
"How to read this chart" / "What the difference tells you"

---

## SECTION 5 — BODY TEXT

Explanation paragraphs:
  Font: Helvetica 9.5pt, navy, 14pt leading

Limitation paragraph (always last in body, always present):
  Font: Helvetica Oblique 9pt, grey #616161, 13pt leading
  Prefix: "Limitation: "
  Always immediately below the relevant explanation

Spacing between paragraphs: 6pt

---

## SECTION 6 — CHART IMAGE (step 3 only)

Position: full text width, after the zone stats table
Size: 7.5 inch wide × 3.8 inch tall
Resolution: minimum 200 dpi source image
No border, no caption below the image

---

## SECTION 7 — EXPLORATION BOX (every PDF, always last before footer)

A bordered box with an orange accent. Appears at the bottom of every PDF.
Contains 2–3 follow-up prompts the student can copy into Claude Code.

Box structure:
  Header row: "What to explore next"
    Background: #FFF3E0 (light amber)
    Text: orange #E65100, 9pt bold
    Border: 0.5pt orange on all sides
  Prompt rows:
    Background: #FFFDE7 (very light yellow)
    Text: navy 9pt, 14pt leading, left indent 10pt
    Each prompt prefixed with Unicode right arrow →
  Padding: 7pt top/bottom, 10pt left/right

Rules:
  - 2 to 3 prompts per PDF — never more
  - Each prompt is a complete copyable question in plain English
  - Prompts are specific to the step and the student's actual ticker
  - No generic prompts — always reference [TICKER] and [MA_PERIOD]

---

## SECTION 8 — FORWARD HOOK (step 4 only)

A blue accent box above the exploration box.
Tells the student what comes next in the course.

Structure:
  Header row: "What comes next"
    Background: blue #1565C0
    Text: white, 9pt bold
  Body row:
    Background: #E3F2FD (light blue)
    Text: navy 9pt, 14pt leading, left indent 10pt
  Border: 0.5pt #E0E0E0

---

## SECTION 9 — FOOTER (every PDF, always last)

Thin 0.5pt grey rule above the footer text.
Text: "Saved to: [full path]"
Style: 7.5pt grey #9E9E9E, centred

---

## SPACING RULES

After header rule:          12pt before first content
Between major sections:     section header spaceBefore handles this (14pt)
Before exploration box:     12pt
Before footer rule:         10pt
Between table and next element: 10pt
Between body paragraphs:    6pt

---

## WHAT TO NEVER DO IN A PDF

- Never use special symbols, arrows, or emoji in signal boxes
  (renders as garbled characters in some PDF viewers)
- Never let the forward hook text get cut off — use KeepTogether
- Never save to a path inside the qslab-f1 repo
- Never produce a PDF under 2 pages for step 4
  (if content fits in 1 page the layout is too sparse)
- Never use font sizes below 7.5pt
- Never use more than 3 colours per section
- Never omit the limitation paragraph — it is required in every step

---

## NAMING CONVENTION

step1_data_[ticker].pdf
step2_sma_[ticker]_[N]d.pdf
step3_chart_[ticker]_[N]d.pdf
step4_signal_[ticker]_[N]d.pdf
step4_rerun_[ticker]_[N1]d_vs_[N2]d.pdf

All lowercase, underscores, no spaces.
