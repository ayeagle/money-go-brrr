# import trading_calendars
# from trading_calendars import TradingCalendar, get_calendar, get_calendar_names
import pandas as pd
import numpy as np
import collections
import pandas_market_calendars as mcal
from acc_helper import AlpacaAccount
import asyncio

import pytz
import datetime


def is_trading_day() -> bool:
    nyse = mcal.get_calendar('NYSE')
    today = datetime.date.today()
    data = nyse.schedule(today, today)
    if data.empty:
        print("Not a valid trading day")
        return False
    else :
        print("Valid trading day")
        return True

async def main() -> int:
    if not is_trading_day() :
        return 1
    
    acc = AlpacaAccount()

    if not acc.can_trade() :
        return 1
    
    ## init get data for model

    ## run model

    ## check model for buy/no buy decision

    ## validate order makes sense

    ## exec order


    return 0


if __name__ == "__main__":
    asyncio.run(main())