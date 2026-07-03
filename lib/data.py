"""
QSL Lab Kit — data.py
Fetch daily price bars from Yahoo Finance with a simple on-disk cache.

Beginner notes (read this once):
  - "Daily bars" just means one row of prices per trading day.
  - We ask Yahoo for AUTO-ADJUSTED prices. That means the numbers already
    account for dividends and stock splits, so the returns we compute later
    are honest.
  - The first time you ask for a ticker we download it and save a copy on
    your disk. The next time we read that copy, so it is fast and works even
    if the internet is slow.

This module does ANALYSIS ONLY. It never connects to a broker, never places
an order, never touches live money — not investment advice.

Pure Python + pandas + yfinance.
"""

import os
import time

import pandas as pd
import yfinance as yf


# Where the on-disk cache lives. One .csv file per ticker+period.
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cache")

# How long a cached file is considered "fresh" before we re-download (1 day).
CACHE_MAX_AGE_SECONDS = 24 * 60 * 60


class UnknownTickerError(Exception):
    """Raised when Yahoo returns no data for a ticker symbol."""
    pass


def _cache_path(ticker: str, years: int) -> str:
    """Build the file path for a ticker's cached data."""
    safe = ticker.upper().strip().replace("/", "_").replace("\\", "_")
    return os.path.join(CACHE_DIR, f"{safe}_{years}y.csv")


def _cache_is_fresh(path: str) -> bool:
    """True if a cache file exists and is younger than CACHE_MAX_AGE_SECONDS."""
    if not os.path.exists(path):
        return False
    age = time.time() - os.path.getmtime(path)
    return age < CACHE_MAX_AGE_SECONDS


def fetch_daily(ticker: str, years: int = 10, use_cache: bool = True) -> pd.DataFrame:
    """
    Return a DataFrame of daily bars for `ticker` over the last `years` years.

    Columns: Open, High, Low, Close, Volume  (Close is auto-adjusted).
    Index: dates (a pandas DatetimeIndex).

    If we have a fresh copy on disk we read that. Otherwise we download from
    Yahoo, save a copy, and return it.

    Raises UnknownTickerError with a plain-English message if the symbol is
    not recognised.
    """
    ticker = ticker.upper().strip()
    if not ticker:
        raise UnknownTickerError(
            "No ticker was given. Try a symbol like SPY, AAPL, or MSFT."
        )

    os.makedirs(CACHE_DIR, exist_ok=True)
    path = _cache_path(ticker, years)

    # 1. Try the on-disk cache first.
    if use_cache and _cache_is_fresh(path):
        try:
            df = pd.read_csv(path, index_col=0, parse_dates=True)
            if len(df) > 0:
                return df
        except Exception:
            # A corrupt cache file should never block us — just re-download.
            pass

    # 2. Download fresh data from Yahoo (auto-adjusted prices).
    period = f"{int(years)}y"
    raw = yf.download(
        ticker,
        period=period,
        auto_adjust=True,
        progress=False,
    )

    # yfinance returns an EMPTY frame for a symbol it does not recognise.
    if raw is None or len(raw) == 0:
        raise UnknownTickerError(
            f"'{ticker}' is not a symbol Yahoo Finance recognises. "
            f"Check the spelling and try a common one like SPY, AAPL, or MSFT."
        )

    # Newer yfinance can return multi-level columns for a single ticker.
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)

    df = raw.copy()
    df.index = pd.to_datetime(df.index)
    df = df.dropna()

    if len(df) == 0:
        raise UnknownTickerError(
            f"'{ticker}' returned no usable price history. "
            f"Try a common symbol like SPY, AAPL, or MSFT."
        )

    # 3. Save a copy for next time, then return.
    try:
        df.to_csv(path)
    except Exception:
        # Saving is a convenience, not a requirement. Never fail on it.
        pass

    return df


def close_series(ticker: str, years: int = 10, use_cache: bool = True) -> pd.Series:
    """
    Convenience helper: return just the auto-adjusted Close prices as a Series.

    This is what the metrics functions expect.
    """
    df = fetch_daily(ticker, years=years, use_cache=use_cache)
    return df["Close"].dropna()


if __name__ == "__main__":
    # Tiny manual smoke test: python3 lib/data.py SPY
    import sys

    sym = sys.argv[1] if len(sys.argv) > 1 else "SPY"
    try:
        prices = close_series(sym, years=10)
        print(f"{sym}: {len(prices)} daily bars")
        print(f"  first: {prices.index[0].date()}  ${prices.iloc[0]:,.2f}")
        print(f"  last:  {prices.index[-1].date()}  ${prices.iloc[-1]:,.2f}")
    except UnknownTickerError as err:
        print(f"Could not load data: {err}")
