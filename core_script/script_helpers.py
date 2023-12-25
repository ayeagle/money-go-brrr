import pandas_market_calendars as mcal
import sys
import datetime


def is_trading_day() -> bool:
    nyse = mcal.get_calendar('NYSE')
    today = datetime.date.today()
    data = nyse.schedule(today, today)
    if data.empty:
        print("Not a valid trading day")
        return False
    else:
        print("Valid trading day")
        return True


def handle_cli_args() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return "force test"