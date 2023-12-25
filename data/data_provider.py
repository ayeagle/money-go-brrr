from typing import List
import pandas as pd
import json
import datetime
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data import StockQuotesRequest
from core_script.class_alpaca_account import AlpacaAccount
from data.class_data_provider_params import DataProviderParams
from data.class_data_provider_payload import DataProviderPayload
from consts.data_type_enums import DataSourceFormat
from alpaca.data.timeframe import TimeFrame


def stock_price_provider(
    acc: AlpacaAccount,
    target_symbol: List[str],
    period_start: datetime,
    period_end: datetime,
    format: DataSourceFormat = DataSourceFormat.PYDICT
):

    hist_data_client = StockHistoricalDataClient(*acc.get_api_keys())

    params_payload = StockQuotesRequest(
        symbol_or_symbols=target_symbol,
        start=period_start,
        # end=period_end, TODO something weird going on w/ this param
        limit=10000,
        # timeframe=TimeFrame.Day,
        feed='sip',
        sort='asc',
    )

    hist_data = hist_data_client.get_stock_quotes(params_payload)

    formatted_data = None

    if (format == DataSourceFormat.PYDICT):
        formatted_data = hist_data
    elif (format == DataSourceFormat.JSON):
        formatted_data = json.dumps(hist_data)
    elif (format == DataSourceFormat.DATAFRAME):
        formatted_data = pd.DataFrame(hist_data[target_symbol])

    return formatted_data


def data_provider(
    acc: AlpacaAccount,
    params: DataProviderParams
) -> DataProviderPayload:

    stock_data = stock_price_provider(
        acc=acc,
        target_symbol=params.stock_tickers,
        period_start=params.period_start,
        period_end=params.period_end,
        format=params.data_format
    )
    diff_data_sources = {
        'stock_data': stock_data
    }

    combined_data_sources = diff_data_sources  # TODO actually set this up lol

    final_data_payload = DataProviderPayload(
        params=params,
        diff_data_sources=diff_data_sources,
        combined_data_sources=combined_data_sources
    )

    # if(params.get_acc_trade_data):
    # get data

    return final_data_payload
