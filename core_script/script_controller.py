import pandas as pd
import numpy as np
# import collections
import pandas_market_calendars as mcal
from acc_helper import AlpacaAccount
import asyncio
from decouple import config
import sys
import json
import datetime
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data import StockQuotesRequest
from enum import Enum


class DataFormat(Enum):
    PYDICT = 'pydict'
    JSON = 'json'
    DATAFRAME = 'dataframe'


api_key = config('PAPER_API_KEY_ID')
secret_key = config('PAPER_API_SECRET_KEY')


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


def stock_price_provider(
    target_symbol: str,
    format: DataFormat = DataFormat.PYDICT
):

    hist_data_client = StockHistoricalDataClient(api_key, secret_key)

    today = datetime.date.today()
    two_years_ago = today - datetime.timedelta(days=365 * 2)
    limit = 10000 
    order = "asc"

    data_params = StockQuotesRequest(
        symbol_or_symbols=target_symbol,
        start=two_years_ago,
        end=today,
        limit=limit,
        sort=order
    )
    hist_data = hist_data_client.get_stock_quotes(data_params)

    formatted_data = None

    if (format == DataFormat.PYDICT):
        formatted_data = hist_data
    elif (format == DataFormat.JSON):
        formatted_data = json.dumps(hist_data)
    elif (format == DataFormat.DATAFRAME):
        formatted_data = pd.DataFrame(hist_data[target_symbol])

    return formatted_data


async def main() -> int:
    test_param = handle_cli_args()

    print("this is the test param")
    print(test_param)

    if (test_param != "force test"):
        if not is_trading_day():
            return 1

    acc = AlpacaAccount(api_key, secret_key)

    if (test_param != "force test"):
        if not acc.can_trade():
            return 1

    prices = stock_price_provider('SPY', DataFormat.DATAFRAME)

    print(prices)

    # Creating request object

    # init get data for model

    # run/create new model

    # backtest model for positive returns

    # check model for buy/no buy decision

    # validate order makes sense

    # exec order

    print("Successfully executed script -- bye bye")
    return 0


if __name__ == "__main__":
    asyncio.run(main())
