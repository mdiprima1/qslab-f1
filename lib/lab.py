"""
QSL Lab Kit — lab.py
The shared spine of the Lab Kit journey: declare -> examine -> report.

It owns three things so the three skills agree with one another:
  1. Where the student's work is stored (lab/ under the repo root) and how a
     declaration and profile are read and written.
  2. THE ELEVEN QUESTIONS, in their fixed order, and how each one is resolved
     from a backtest today — or honestly marked "awaiting the Lab's full
     machinery" when today's small machinery cannot yet answer it.
  3. The personal readings (tax arm, drawdown comfort, capital, time) that
     turn measured numbers into a reading for one particular student.

Voice: calm, units always, dignity in failure. Dollar amounts before
percentages. This module does ANALYSIS ONLY on historical data — it is a
learning tool, not investment advice.
"""

import json
import os
import re
from datetime import datetime, timezone

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(_HERE, ".."))

LAB_DIR = os.path.join(REPO_ROOT, "lab")
DECLARATIONS_DIR = os.path.join(LAB_DIR, "declarations")
EXAMINATIONS_DIR = os.path.join(LAB_DIR, "examinations")
REPORTS_DIR = os.path.join(LAB_DIR, "reports")
PROFILE_PATH = os.path.join(LAB_DIR, "profile.json")
SERIAL_PATH = os.path.join(LAB_DIR, "serial.txt")

DISCLAIMER = "Educational output from historical data — not investment advice."
PENDING = "awaiting the Lab's full machinery"


# --------------------------------------------------------------------------
# Paths and small helpers
# --------------------------------------------------------------------------
def slugify(text: str) -> str:
    """Turn a strategy name into a safe filename slug."""
    text = (text or "strategy").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "strategy"


def _ensure_dirs() -> None:
    for path in (LAB_DIR, DECLARATIONS_DIR, EXAMINATIONS_DIR, REPORTS_DIR):
        os.makedirs(path, exist_ok=True)


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


# --------------------------------------------------------------------------
# Declarations and profile
# --------------------------------------------------------------------------
def save_declaration(declaration: dict) -> str:
    """Write a declaration to lab/declarations/<slug>.json. Returns the path."""
    _ensure_dirs()
    slug = declaration.get("slug") or slugify(declaration.get("name", "strategy"))
    declaration["slug"] = slug
    declaration.setdefault("created", _now_iso())
    path = os.path.join(DECLARATIONS_DIR, f"{slug}.json")
    with open(path, "w") as fh:
        json.dump(declaration, fh, indent=2)
    return path


def load_declaration(slug: str = None) -> dict:
    """
    Load a declaration by slug, or the most recently created one when no slug
    is given. Raises FileNotFoundError with a plain-English message if none.
    """
    if slug:
        path = os.path.join(DECLARATIONS_DIR, f"{slug}.json")
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"No declaration named '{slug}'. Run /qsl declare first."
            )
        with open(path) as fh:
            return json.load(fh)

    if not os.path.isdir(DECLARATIONS_DIR):
        raise FileNotFoundError("No strategy declared yet. Run /qsl declare first.")
    files = [f for f in os.listdir(DECLARATIONS_DIR) if f.endswith(".json")]
    if not files:
        raise FileNotFoundError("No strategy declared yet. Run /qsl declare first.")
    newest = max(files, key=lambda f: os.path.getmtime(os.path.join(DECLARATIONS_DIR, f)))
    with open(os.path.join(DECLARATIONS_DIR, newest)) as fh:
        return json.load(fh)


def save_profile(profile: dict) -> str:
    """Write the student profile once (reused across every strategy)."""
    _ensure_dirs()
    profile.setdefault("created", _now_iso())
    with open(PROFILE_PATH, "w") as fh:
        json.dump(profile, fh, indent=2)
    return PROFILE_PATH


def load_profile() -> dict:
    """Load the student profile, or return {} if it has not been set yet."""
    if not os.path.exists(PROFILE_PATH):
        return {}
    with open(PROFILE_PATH) as fh:
        return json.load(fh)


def profile_exists() -> bool:
    return os.path.exists(PROFILE_PATH)


# --------------------------------------------------------------------------
# Examinations
# --------------------------------------------------------------------------
def save_examination(exam: dict) -> str:
    """Persist an examination so the report can render it later."""
    _ensure_dirs()
    slug = exam.get("slug", "strategy")
    path = os.path.join(EXAMINATIONS_DIR, f"{slug}.json")
    with open(path, "w") as fh:
        json.dump(exam, fh, indent=2)
    return path


def load_examination(slug: str) -> dict:
    path = os.path.join(EXAMINATIONS_DIR, f"{slug}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"'{slug}' has not been examined yet. Run /qsl examine first."
        )
    with open(path) as fh:
        return json.load(fh)


# --------------------------------------------------------------------------
# Serial counter (a local, monotonic Lab Report number)
# --------------------------------------------------------------------------
def next_serial() -> int:
    """Read, increment, and persist the local Lab Report serial counter."""
    _ensure_dirs()
    current = 0
    if os.path.exists(SERIAL_PATH):
        try:
            with open(SERIAL_PATH) as fh:
                current = int((fh.read() or "0").strip())
        except (ValueError, OSError):
            current = 0
    nxt = current + 1
    with open(SERIAL_PATH, "w") as fh:
        fh.write(str(nxt))
    return nxt


# --------------------------------------------------------------------------
# THE ELEVEN QUESTIONS — fixed order
# --------------------------------------------------------------------------
# Each question has a stable id, the plain question, and a resolver. A resolver
# returns (status, reading) where status is "answered" or "pending". Pending
# questions render honestly as PENDING — the Lab does not pretend to know.
QUESTION_ORDER = [
    "makes_money",
    "growth_rate",
    "bumpiness",
    "worst_fall",
    "reward_for_risk",
    "beats_buy_hold",
    "survives_unseen",
    "dry_spells",
    "survives_costs",
    "robust_to_knobs",
    "holds_across_markets",
]

QUESTION_TEXT = {
    "makes_money": "Does the strategy make money at all?",
    "growth_rate": "How fast does it grow, per year?",
    "bumpiness": "How bumpy is the ride?",
    "worst_fall": "What is the worst fall it ever suffered?",
    "reward_for_risk": "Is the reward worth the risk taken?",
    "beats_buy_hold": "Does it beat simply buying and holding?",
    "survives_unseen": "Does the edge survive on data it never saw?",
    "dry_spells": "How long are the dry spells?",
    "survives_costs": "Does it still work once real trading costs are paid?",
    "robust_to_knobs": "Is it robust to small changes in its settings?",
    "holds_across_markets": "Does it hold up across other markets and eras?",
}


def _pct(x: float) -> str:
    return f"{x * 100:.1f}%"


def resolve_questions(bt: dict) -> list:
    """
    Resolve the eleven questions IN THE FIXED ORDER from a backtest result
    dict (see lib/backtest.run_backtest). Returns a list of dicts:
        {id, question, status, reading}
    status is "answered" (one-line evidence) or "pending" (awaiting machinery).
    """
    s = bt["strategy"]
    h = bt["buy_hold"]
    results = []

    def add(qid, status, reading):
        results.append({
            "id": qid,
            "question": QUESTION_TEXT[qid],
            "status": status,
            "reading": reading,
        })

    # 1. Does it make money at all?
    tr = s["total_return"]
    if tr > 0:
        add("makes_money", "answered",
            f"Yes — $1 became ${1 + tr:,.2f} over {bt['years']:.0f} years "
            f"({_pct(tr)} total).")
    else:
        add("makes_money", "answered",
            f"No — $1 ended at ${1 + tr:,.2f} over {bt['years']:.0f} years "
            f"({_pct(tr)} total). It lost ground, and that is worth knowing.")

    # 2. Growth rate (CAGR).
    add("growth_rate", "answered",
        f"About {_pct(s['cagr'])} per year — the smooth pace behind a bumpy ride.")

    # 3. Bumpiness (volatility).
    add("bumpiness", "answered",
        f"Annualized volatility of {_pct(s['volatility'])}. That is risk, not loss.")

    # 4. Worst fall (max drawdown).
    dd = abs(s["max_drawdown"])
    add("worst_fall", "answered",
        f"At its worst, {_pct(-dd)} was gone from a previous high — the deepest "
        f"hole you would have had to sit in.")

    # 5. Reward for risk (CAGR / volatility).
    vol = s["volatility"]
    if vol > 1e-9:
        ratio = s["cagr"] / vol
        add("reward_for_risk", "answered",
            f"About {ratio:.2f} units of yearly growth for each unit of "
            f"bumpiness. Higher is steadier; below ~0.5 is a rough ride.")
    else:
        add("reward_for_risk", "answered",
            "The ride was essentially flat, so reward-for-risk cannot be read.")

    # 6. Beats buy-and-hold?
    edge = s["total_return"] - h["total_return"]
    if edge >= 0:
        add("beats_buy_hold", "answered",
            f"Yes, by {_pct(edge)} total against buy-and-hold "
            f"(${1 + h['total_return']:,.2f} the plain way).")
    else:
        add("beats_buy_hold", "answered",
            f"No — buy-and-hold ended {_pct(-edge)} higher. Plain holding won "
            f"this window, and that is an honest result.")

    # 7. Survives on unseen data (in-sample vs out-of-sample split).
    is_r = bt["in_sample_return"]
    oos_r = bt["out_of_sample_return"]
    if is_r > 0 and oos_r > 0:
        add("survives_unseen", "answered",
            f"It held: {_pct(is_r)} on the first half, {_pct(oos_r)} on the "
            f"unseen second half. The edge did not vanish.")
    elif is_r > 0 >= oos_r:
        add("survives_unseen", "answered",
            f"It faded: {_pct(is_r)} on the first half but {_pct(oos_r)} on the "
            f"unseen second half. Treat the shine with caution.")
    else:
        add("survives_unseen", "answered",
            f"First half {_pct(is_r)}, unseen second half {_pct(oos_r)}. "
            f"No durable edge showed across the split.")

    # 8. Dry spells (longest time underwater).
    days = bt["longest_underwater_days"]
    add("dry_spells", "answered",
        f"The longest dry spell lasted about {days:,} days "
        f"(~{days / 365.25:.1f} years) below a prior high. That is the "
        f"patience it demands.")

    # 9-11. Beyond today's small machinery — named honestly, never faked.
    add("survives_costs", "pending",
        f"Trading costs and slippage are not modelled yet — {PENDING}.")
    add("robust_to_knobs", "pending",
        f"Parameter-sensitivity sweeps are not built yet — {PENDING}.")
    add("holds_across_markets", "pending",
        f"Cross-market and cross-era testing is not built yet — {PENDING}.")

    return results


# --------------------------------------------------------------------------
# Personal readings — the second half of the Lab Report
# --------------------------------------------------------------------------
ACCOUNT_TYPE_LABEL = {
    "taxable": "Taxable brokerage",
    "traditional_ira": "Traditional IRA / 401(k)",
    "roth_ira": "Roth IRA",
}

SIZE_BAND_LABEL = {
    "under_10k": "under $10,000",
    "10k_100k": "$10,000 – $100,000",
    "100k_1m": "$100,000 – $1,000,000",
    "over_1m": "over $1,000,000",
}

SIZE_BAND_MIDPOINT = {
    "under_10k": 5_000,
    "10k_100k": 55_000,
    "100k_1m": 550_000,
    "over_1m": 1_500_000,
}


def personal_readings(profile: dict, bt: dict) -> list:
    """
    Turn measured numbers into readings for one particular student. Returns a
    list of {title, reading} cards. Every reading names its limit and keeps
    dignity in failure — a mismatch is information, not a verdict on the person.
    """
    cards = []
    if not profile:
        cards.append({
            "title": "Profile not set",
            "reading": "No profile was found, so the personal section is blank. "
                       "Run /qsl declare to answer the four profile prompts once.",
        })
        return cards

    s = bt["strategy"]
    cagr = s["cagr"]
    worst = abs(s["max_drawdown"])

    # 1. Tax arm — what the growth looks like after the student's bracket, and
    #    whether the account type shelters it.
    acct = profile.get("account_type", "taxable")
    bracket = float(profile.get("tax_bracket", 0.0) or 0.0)
    acct_label = ACCOUNT_TYPE_LABEL.get(acct, "Taxable brokerage")
    if acct in ("roth_ira", "traditional_ira"):
        cards.append({
            "title": "The tax arm",
            "reading": f"Held in a {acct_label}, this year's gains are sheltered "
                       f"from tax as they compound. A pre-tax {_pct(cagr)} stays "
                       f"{_pct(cagr)} inside the account.",
        })
    else:
        after = cagr * (1 - bracket)
        cards.append({
            "title": "The tax arm",
            "reading": f"In a {acct_label} at roughly a {_pct(bracket)} bracket, a "
                       f"pre-tax {_pct(cagr)} per year reads closer to {_pct(after)} "
                       f"after tax on gains. A rough guide, not a tax filing.",
        })

    # 2. Drawdown comfort vs the measured worst fall.
    comfort = profile.get("drawdown_comfort")
    if comfort is not None:
        comfort = float(comfort)
        if worst <= comfort:
            cards.append({
                "title": "Drawdown comfort",
                "reading": f"You said you could sit through about a {_pct(comfort)} "
                           f"fall. The worst this strategy showed was {_pct(worst)} "
                           f"— inside your comfort. Paper comfort is easier than the "
                           f"real thing, so hold that lightly.",
            })
        else:
            gap = worst - comfort
            cards.append({
                "title": "Drawdown comfort",
                "reading": f"You said about a {_pct(comfort)} fall is your limit, but "
                           f"the worst here reached {_pct(worst)} — {_pct(gap)} deeper "
                           f"than you signed up for. That mismatch is the most useful "
                           f"line in this report: it is the point you would likely "
                           f"have sold at a loss.",
            })

    # 3. Capital check — what the growth means in dollars at the account size.
    band = profile.get("account_size_band")
    if band in SIZE_BAND_MIDPOINT:
        mid = SIZE_BAND_MIDPOINT[band]
        grown = mid * ((1 + cagr) ** 10)
        cards.append({
            "title": "Capital check",
            "reading": f"At a typical {SIZE_BAND_LABEL[band]} account (say ${mid:,.0f}), "
                       f"ten years at {_pct(cagr)} would trace toward ${grown:,.0f} "
                       f"before tax and costs — a projection of the past, not a promise.",
        })

    # 4. Time check — the patience the dry spells demand.
    days = bt["longest_underwater_days"]
    cards.append({
        "title": "Time check",
        "reading": f"The longest stretch underwater was about {days / 365.25:.1f} "
                   f"years. Ask yourself honestly whether you would keep going that "
                   f"long with no new high in sight.",
    })

    return cards
