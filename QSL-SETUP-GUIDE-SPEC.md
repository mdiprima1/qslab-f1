# QSL Setup Guide — Content Specification
## For PDF production (version 1.0)
## This file defines what goes in QSL-SETUP-GUIDE.pdf

The PDF lives at: github.com/mdiprima1/qslab-f1/blob/main/QSL-SETUP-GUIDE.pdf
It is updated independently of the course whenever UIs change.
Version number and date in footer of every page.

---

## SECTION 1 — Claude Desktop App Installation

**Purpose:** Student downloads and installs Claude Desktop on Mac or Windows.

Steps with screenshot for each:
1. Go to claude.ai/download
   Screenshot: the download page, highlighting the Mac / Windows download buttons
2. Run the installer
   Screenshot: macOS install drag-to-Applications / Windows setup wizard first screen
3. Open Claude Desktop App
   Screenshot: the Claude Desktop App icon in macOS Dock or Windows taskbar
4. Sign in with Anthropic account
   Screenshot: the sign-in screen
   Note: "If you do not have an account, click 'Sign up' — it is free."

---

## SECTION 2 — Claude Pro Subscription

**Purpose:** Student upgrades to Claude Pro to unlock Claude Code.

Steps with screenshot for each:
1. In the Claude Desktop App or at claude.ai, click your account name
   Screenshot: account menu location
2. Click "Upgrade to Pro"
   Screenshot: the upgrade prompt / billing page
3. Enter payment details — $20/month
   Screenshot: billing form (card fields only, no sensitive data)
4. Confirm subscription — Claude Pro is now active
   Screenshot: confirmation screen or Pro badge visible in UI
   Note: "Claude Code is included with Claude Pro. No additional cost."

---

## SECTION 3 — QSLab First Setup

**Purpose:** Student pastes the init prompt and confirms QSLab is ready.

Steps with screenshot for each:
1. Open Claude Desktop App — you should see a conversation window
   Screenshot: empty Claude Code conversation
2. Copy this prompt exactly (shown in a box):
   "I am starting the QSL Foundation I course. Please set up my research
   environment. Clone the QSLab repository from
   https://github.com/mdiprima1/qslab-f1.git, read the QSL Lab setup guide,
   the QSL Lab Requirements and the QSL Lab research policies. Then install
   Python if needed, install all required packages, and confirm everything is
   working by running a quick test."
3. Paste the prompt and press Enter
   Screenshot: the prompt pasted in the Claude Code input box
4. Wait approximately 30 seconds
   Screenshot: Claude Code showing "Downloading QSLab F1..."
5. Confirm success — Claude Code says:
   "QSLab F1 is ready.
   Available labs: F1-1.2 Your Research Environment
   To begin, say: Start QSLab F1-1.2"
   Screenshot: the success message

Troubleshooting:
- "Python not found" → Claude Code will install it automatically. Wait 60 seconds.
- "Permission denied" → On Mac: System Settings → Privacy → allow Claude Code.
  On Windows: run as administrator.
- "Network error" → Check internet connection. Try again.
- Still stuck → Ask Claude: "The QSLab setup failed with this error: [paste error]"

---

## SECTION 4 — QuantConnect Account Creation

**Purpose:** Student creates a free QuantConnect account.

Steps with screenshot for each:
1. Go to quantconnect.com
   Screenshot: the QuantConnect homepage, "Create Account" button highlighted
2. Click "Create Account" — enter email and password
   Screenshot: the sign-up form
3. Confirm your email address — check your inbox for the confirmation email
   Screenshot: the "check your email" page
4. Click the confirmation link in the email
   Screenshot: the email confirmation link (with email address blurred)
5. You are now on the Free tier
   Screenshot: the QuantConnect dashboard / Algorithm Lab landing page
   Note: "The Free tier includes full backtesting access at no cost.
   No credit card required."

---

## SECTION 5 — Cloning a Strategy in QuantConnect

**Purpose:** Student clones the AAPL SMA-100 strategy to their account.

Steps with screenshot for each:
1. Open the QSL clone link:
   quantconnect.cloud/backtest/f8e0ce6192ef8a9c2cb9d16cdb2adc55/
   Screenshot: the backtest results page
2. Sign in to your QuantConnect account if prompted
   Screenshot: sign-in prompt
3. Click the "Clone" button
   Screenshot: the Clone button location on the backtest page (circled/highlighted)
4. The strategy appears in your Algorithm Lab projects
   Screenshot: the project list with the cloned strategy visible
   Note: "You now have a copy of the strategy in your own account.
   You can view the code, run the backtest again, or modify it."

---

## PDF FORMATTING REQUIREMENTS

- Page size: A4 / Letter
- Cover page: QSL Foundation I logo, "QSL Setup Guide", version number, date
- Each section starts on a new page
- Screenshots: full-width, 2px border, rounded corners
- Step numbers: bold, large, clear
- Notes and troubleshooting: grey callout boxes
- Footer on every page: "QSL Foundation I — Setup Guide v[X.X] — quantstrategylab.com"
- Version history table on last page

---

## VERSION HISTORY

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-03-25 | Initial specification |

