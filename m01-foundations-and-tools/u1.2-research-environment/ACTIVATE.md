# QSLab F1-1.2 — Activation Prompt
## Copy this entire block and paste into a fresh Claude Code session

---

```
Please set up and start QSLab F1-1.2.

Step 1 — Get the files:
Check if ~/qslab-f1 exists. If not, clone it: git clone https://github.com/mdiprima1/qslab-f1.git ~/qslab-f1
If it exists, run: cd ~/qslab-f1 && git pull

Step 2 — Install packages:
pip install yfinance pandas matplotlib --quiet

Step 3 — Read these files IN THIS ORDER before doing anything else:
1. ~/qslab-f1/CLAUDE.md
2. ~/qslab-f1/QSL-POLICIES.md
3. ~/qslab-f1/m01-foundations-and-tools/u1.2-research-environment/CLAUDE.md
4. ~/qslab-f1/m01-foundations-and-tools/u1.2-research-environment/lab_1_2.py

Step 4 — Follow QSL-POLICIES.md exactly:
- Write the implementation plan and wait for my approval (Policy §1)
- After approval, print the session header (Policy §2)
- Warn me about permissions (Policy §3)
- Ask the two questions: which stock? what MA period?
- Run steps 1-4 one at a time, printing markdown tables after each step (Policy §4)
- Display charts inline at large size (Policy §4)
```

---

## FOR SLIDE 14

The above prompt is what appears on slide 14 as the copyable prompt.
It works from a cold session with no prior context.
