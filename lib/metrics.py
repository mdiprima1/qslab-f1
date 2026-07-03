"""
QSL Lab Kit — metrics.py
Three plain-English investment statistics, written to be read by beginners.

Every function takes a pandas Series of daily prices (auto-adjusted Close)
and returns one number. The docstrings explain the idea in words first and
the formula second.

This module does ANALYSIS ONLY on historical data. It is a learning tool —
not investment advice.
"""

import numpy as np
import pandas as pd


# There are roughly 252 trading days in a year (markets are closed on
# weekends and holidays). We use this to turn daily numbers into yearly ones.
TRADING_DAYS_PER_YEAR = 252


def cagr(prices: pd.Series) -> float:
    """
    CAGR = Compound Annual Growth Rate.

    Plain English: "If this investment had grown by the SAME smooth percentage
    every year, what would that yearly percentage be?" It answers the question
    "how fast did my money grow, per year, on average?"

    A CAGR of 0.10 means 10% per year.

    How it is computed:
      1. Total growth = final price / starting price.
      2. Figure out how many years passed.
      3. Take the "per-year" root of the total growth and subtract 1.

    Returns a decimal (0.10 = 10% a year). Returns 0.0 if there is not enough
    data or the numbers make growth impossible to define.
    """
    prices = pd.Series(prices).dropna()
    if len(prices) < 2:
        return 0.0

    start_price = float(prices.iloc[0])
    end_price = float(prices.iloc[-1])
    if start_price <= 0 or end_price <= 0:
        return 0.0

    # Number of years between the first and last day.
    days = (prices.index[-1] - prices.index[0]).days
    years = days / 365.25
    if years <= 0:
        return 0.0

    total_growth = end_price / start_price
    return total_growth ** (1.0 / years) - 1.0


def annual_volatility(prices: pd.Series) -> float:
    """
    Annualized volatility = how bumpy the ride was, expressed per year.

    Plain English: volatility measures how much the daily returns jump around.
    A calm, steady investment has LOW volatility. A wild one that swings up and
    down a lot has HIGH volatility. It is a measure of risk, not of loss.

    A volatility of 0.18 means about 18% — a typical figure for the US stock
    market as a whole.

    How it is computed:
      1. Turn prices into daily percentage changes (returns).
      2. Take the standard deviation of those daily returns (their typical
         wiggle).
      3. Scale it up to a year by multiplying by the square root of 252
         (the number of trading days in a year).

    Returns a decimal (0.18 = 18%). Returns 0.0 if there is not enough data.
    """
    prices = pd.Series(prices).dropna()
    if len(prices) < 2:
        return 0.0

    daily_returns = prices.pct_change().dropna()
    if len(daily_returns) < 2:
        return 0.0

    daily_std = float(daily_returns.std())
    return daily_std * np.sqrt(TRADING_DAYS_PER_YEAR)


def max_drawdown(prices: pd.Series) -> float:
    """
    Maximum drawdown = the worst peak-to-valley drop the account ever suffered.

    Plain English: imagine watching the value of your investment day by day.
    At some point it hit an all-time high. Then it fell. The biggest fall from
    a previous high, before it recovered, is the maximum drawdown. It answers
    the gut question: "what is the worst it ever felt to hold this?"

    A max drawdown of -0.55 means the investment once lost 55% of its value
    from its peak — more than half the account was gone at the worst point.

    How it is computed:
      1. Track the running highest price seen so far (the "peak").
      2. For each day, measure how far below that peak we are, as a percentage.
      3. The most negative of those numbers is the maximum drawdown.

    Returns a decimal, always <= 0 (-0.55 = a 55% drop). Returns 0.0 if there
    is not enough data.
    """
    prices = pd.Series(prices).dropna()
    if len(prices) < 2:
        return 0.0

    running_peak = prices.cummax()
    drawdowns = prices / running_peak - 1.0
    return float(drawdowns.min())


def summary(prices: pd.Series) -> dict:
    """
    Return all three metrics in one dictionary, for convenience.

    Keys: 'cagr', 'annual_volatility', 'max_drawdown' (all decimals).
    """
    return {
        "cagr": cagr(prices),
        "annual_volatility": annual_volatility(prices),
        "max_drawdown": max_drawdown(prices),
    }


if __name__ == "__main__":
    # Tiny manual smoke test using a fake, made-up price path.
    idx = pd.date_range("2015-01-01", periods=252 * 10, freq="B")
    # A gently rising line with some noise, just to exercise the math.
    rng = np.random.default_rng(0)
    steps = rng.normal(0.0003, 0.01, size=len(idx))
    fake = pd.Series(100 * np.exp(np.cumsum(steps)), index=idx)

    s = summary(fake)
    print(f"CAGR:              {s['cagr'] * 100:6.2f}% per year")
    print(f"Annual volatility: {s['annual_volatility'] * 100:6.2f}%")
    print(f"Max drawdown:      {s['max_drawdown'] * 100:6.2f}%")
