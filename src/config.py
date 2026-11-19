"""
config.py
---------
Central place for every setting the project uses.
Change values here instead of hunting through the code.
"""

from pathlib import Path

# ---------- Folder paths (built relative to this file, so it works on any PC) ----------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"   # processed CSV files
IMAGES_DIR = BASE_DIR / "images"     # saved charts (PNG)
REPORTS_DIR = BASE_DIR / "reports"   # text / markdown reports

# ---------- Default analysis settings ----------
DEFAULT_TICKER = "AAPL"
DEFAULT_START = "2023-01-01"
DEFAULT_END = "2024-12-31"

# Moving-average windows (in trading days)
SHORT_WINDOW = 20    # ~1 month
LONG_WINDOW = 50     # ~2.5 months
TREND_WINDOW = 200   # ~1 year (long-term trend)

# Rolling volatility window (trading days)
VOLATILITY_WINDOW = 20

# Approx. number of trading days in a year (used to annualise numbers)
TRADING_DAYS = 252

# Annual risk-free rate used in the Sharpe ratio (4% = 0.04)
RISK_FREE_RATE = 0.04


def ensure_folders() -> None:
    """Create output folders if they don't exist yet."""
    for folder in (DATA_DIR, OUTPUTS_DIR, IMAGES_DIR, REPORTS_DIR):
        folder.mkdir(parents=True, exist_ok=True)
