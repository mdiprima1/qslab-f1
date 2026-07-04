"""
QSL Lab Kit — backtest.py
A simple, honest backtest of moving-average / momentum-style rules on the
daily auto-adjusted prices returned by lib/data.py.

This is the small machinery the Lab uses today. It is deliberately plain:
each day the strategy is either fully IN the market (its return follows the
price) or fully in cash (zero return). No leverage, no shorting, no costs
modelled yet — the honest limits are named, never hidden.

This module does ANALYSIS ONLY on historical data. It is a learning tool —
not investment advice.
"""

import numpy as np
import pandas as pd

from lib.metrics import (
    cagr,
    annual_volatility,
    max_drawdown,
    TRADING_DAYS_PER_YEAR,
)


def signal_from_rule(prices: pd.Series, rule: dict) -> pd.Series:
    """
    Turn a declared buy rule into a daily in-market signal (1.0 = hold the
    market, 0.0 = sit in cash), computed only from information available the
    day before (we shift by one day so there is no look-ahead cheating).

    Supported rule kinds:
      - "ma_cross":  in market when the fast moving average is above the slow
                     moving average. Params: fast, slow.
      - "momentum":  in market when the trailing return over `lookback`
                     trading days is positive. Param: lookback.
      - "buy_hold":  always in the market (the honest baseline).
    """
    prices = pd.Series(prices).dropna()
    kind = (rule or {}).get("kind", "buy_hold")

    if kind == "ma_cross":
        fast = max(1, int(rule.get("fast", 50)))
        slow = max(fast + 1, int(rule.get("slow", 200)))
        fast_ma = prices.rolling(fast).mean()
        slow_ma = prices.rolling(slow).mean()
        raw = (fast_ma > slow_ma).astype(float)
    elif kind == "momentum":
        lookback = max(1, int(rule.get("lookback", 126)))
        trailing = prices / prices.shift(lookback) - 1.0
        raw = (trailing > 0).astype(float)
    else:  # buy_hold and any unknown kind fall back to the honest baseline
        raw = pd.Series(1.0, index=prices.index)

    # Act on yesterday's signal — you cannot trade on a price you have not
    # seen yet. This one shift is what keeps the backtest honest.
    return raw.shift(1).fillna(0.0)


def run_backtest(prices: pd.Series, rule: dict) -> dict:
    """
    Run the declared rule against `prices` and return a dictionary of results
    the Lab can read: the strategy's equity curve, the buy-and-hold baseline,
    headline metrics for both, an in-sample / out-of-sample split, and the
    longest stretch the strategy spent underwater (below a previous high).
    """
    prices = pd.Series(prices).dropna()
    daily_ret = prices.pct_change().fillna(0.0)

    signal = signal_from_rule(prices, rule)
    strat_ret = signal * daily_ret

    strat_equity = (1.0 + strat_ret).cumprod()
    hold_equity = (1.0 + daily_ret).cumprod()

    # Longest time underwater, in calendar days, for the strategy.
    underwater_days = _longest_underwater_days(strat_equity)

    # In-sample / out-of-sample split: does the edge survive on unseen data?
    half = len(prices) // 2
    is_total = float(strat_equity.iloc[half - 1] / strat_equity.iloc[0] - 1.0) if half > 1 else 0.0
    oos_total = float(strat_equity.iloc[-1] / strat_equity.iloc[half] - 1.0) if half >= 1 and half < len(strat_equity) else 0.0

    # How often the rule flips in or out of the market (a cadence proxy).
    flips = int((signal.diff().abs() > 0).sum())
    years = max((prices.index[-1] - prices.index[0]).days / 365.25, 1e-9)
    flips_per_year = flips / years

    strat = {
        "cagr": cagr_from_equity(strat_equity),
        "volatility": float(strat_ret.std() * np.sqrt(TRADING_DAYS_PER_YEAR)),
        "max_drawdown": max_drawdown(strat_equity),
        "total_return": float(strat_equity.iloc[-1] - 1.0),
    }
    hold = {
        "cagr": cagr(prices),
        "volatility": annual_volatility(prices),
        "max_drawdown": max_drawdown(prices),
        "total_return": float(hold_equity.iloc[-1] - 1.0),
    }

    return {
        "start": prices.index[0].date().isoformat(),
        "end": prices.index[-1].date().isoformat(),
        "n_days": int(len(prices)),
        "years": float(years),
        "strategy": strat,
        "buy_hold": hold,
        "in_sample_return": is_total,
        "out_of_sample_return": oos_total,
        "longest_underwater_days": int(underwater_days),
        "flips_per_year": float(flips_per_year),
        "time_in_market": float(signal.mean()),
    }


def cagr_from_equity(equity: pd.Series) -> float:
    """CAGR computed from an equity curve (which starts near 1.0)."""
    equity = pd.Series(equity).dropna()
    if len(equity) < 2:
        return 0.0
    days = (equity.index[-1] - equity.index[0]).days
    years = days / 365.25
    if years <= 0 or equity.iloc[0] <= 0 or equity.iloc[-1] <= 0:
        return 0.0
    return float((equity.iloc[-1] / equity.iloc[0]) ** (1.0 / years) - 1.0)


def _longest_underwater_days(equity: pd.Series) -> int:
    """
    The longest calendar-day stretch the equity curve spent below a previous
    high. This is the "how long were the dry spells" measure — the patience a
    strategy actually demands.
    """
    equity = pd.Series(equity).dropna()
    if len(equity) < 2:
        return 0
    peak = equity.cummax()
    underwater = equity < peak
    longest = 0
    start = None
    for date, wet in underwater.items():
        if wet and start is None:
            start = date
        elif not wet and start is not None:
            longest = max(longest, (date - start).days)
            start = None
    if start is not None:
        longest = max(longest, (equity.index[-1] - start).days)
    return longest
