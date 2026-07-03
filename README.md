# QSLab F1 — Quantitative Strategy Lab: Foundation I
## Hands-On Research Environment for QSL Foundation I

QSLab F1 is the practical companion to QSL Foundation I. Each lab unit
mirrors a course unit and gives you a guided, prompt-driven research
experience using real market data.

You do not need to write code. You paste prompts. Claude Code does the work.

---

## Prerequisites

- Claude Desktop App (claude.ai/download)
- Claude Pro subscription ($20/month)
- Python 3.10+
- Git

## Setup (one time)

```bash
git clone https://github.com/mdiprima1/qslab-f1.git
cd qslab-f1
pip install yfinance pandas matplotlib reportlab Pillow
```

## How to Start a Lab

1. Open Claude Desktop App
2. Open the qslab-f1 folder as your project
3. Paste the contents of ACTIVATE.md into Claude Code
4. Say: **Start QSLab unit 1.2**
5. Follow the guided steps

Additional prompts are in PROMPTS_ADDITIONAL.md.

---

## QSL Lab Kit — Your First Two Commands

The Lab Kit powers the free mini-course **Quant Investing: First Steps**.
With two commands you compute real investment statistics on your own
machine, then watch a beautiful backtest fall apart.

- `/qsl toolkit TICKER` — fetch 10 years of a stock's history and print its
  yearly growth, its bumpiness, and its worst-ever drop, each explained in
  plain English. Defaults to `SPY` (the whole US market in one symbol).
- `/qsl overfit-demo` — build a strategy that looks perfect on old data,
  then watch it collapse on data it has never seen. The lesson: enough
  knobs fit any noise.

### Install in 3 steps (no terminal experience needed)

You only do this once. Copy each line, paste it, press Enter.

**Step 1 — download the Lab Kit.** Copy and paste this line, then Enter:

```bash
git clone https://github.com/mdiprima1/qslab-f1.git
```

**Step 2 — go into the folder.** Copy and paste this line, then Enter:

```bash
cd qslab-f1
```

**Step 3 — install the tools it needs.** Copy and paste this line, then
Enter, and wait for it to finish:

```bash
pip install yfinance pandas matplotlib reportlab Pillow
```

That is the whole install. Now open the `qslab-f1` folder in the Claude
Desktop App and type `/qsl toolkit SPY` to run your first command.

> Every Lab Kit output ends with the same reminder:
> *Educational output from historical data — not investment advice.*
> These commands do analysis only — they never connect to a broker, use
> live data, or place any order.

---

## Lab Units

| Lab | Course Unit | Topic |
|-----|-------------|-------|
| Lab 1.2 | Unit 1.2 | Introduction to Algorithmic Trading — AAPL SMA Strategy |

---

## Repo Naming Convention

  qslab-f1    Foundation I (this repo)
  qslab-f2    Foundation II (future)
  qslab-adv   Advanced (future)

*QSL Foundation I — Build real strategies. Based on evidence, not hope.*
