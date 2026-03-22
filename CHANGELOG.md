# QSLab F1 — Changelog

---

## v0.1 Beta — March 22, 2026

First working prototype. Lab 1.2 tested end-to-end.

### What works
- Full 7-step guided lab sequence on AAPL 100-day SMA strategy
- All step output displayed inline in Claude Code conversation
- Charts at 16x7 200dpi displayed inline after each plot step
- QSL-branded PDF report generated and opened automatically
- PDF stats table header bug fixed
- Syntax error in lab_1_2.py fixed (duplicate function removed)
- Strict no-commit guardrails in root CLAUDE.md

### Known issues
- Student must manually set Claude Code to Auto mode to avoid approval prompts
  (partial fix: .claude/settings.json added to pre-approve safe commands)
- Charts may not persist in conversation history on scroll
  (partial fix: text summary printed alongside each chart)

### Student setup
1. Claude Desktop App + Claude Pro subscription
2. Paste: "Set up QSLab F1 from https://github.com/mdiprima1/qslab-f1.git"
3. Type: "Initiate QSLab F1"
4. Type: "Start QSLab F1-1.2"

### Lab units available
- Lab 1.2 — Introduction to Algorithmic Trading (AAPL SMA-100)

### V0.2 roadmap
- bypassPermissionsModeAccept in settings.json (eliminate approval prompts fully)
- Lab 1.1, 2.1, 2.2, 2.3, 2.4
- Course website integration
- QSLab section added to content guide template in course-builder-v2
