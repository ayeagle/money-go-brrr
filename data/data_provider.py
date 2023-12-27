from typing import List
import pandas as pd
import json
import datetime
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data import StockQuotesRequest
from core_script.class_alpaca_account import AlpacaAccount
from data.class_data_provider_params import DataProviderParams
from data.class_data_provider_payload import DataProviderPayload
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus
from alpaca.trading.client import TradingClient


async def gen_stock_prices(
    acc: AlpacaAccount,
    target_symbols: List[str],
    period_start: datetime,
    period_end: datetime,
):

    hist_data_client = StockHistoricalDataClient(*acc.get_api_keys())

    params_payload = StockQuotesRequest(
        symbol_or_symbols=target_symbols,
        start=period_start,
        # end=period_end, TODO something weird going on w/ this param
        limit=5,
        # timeframe=TimeFrame.Day,
        feed='sip',
        sort='asc',
    )

    hist_data = hist_data_client.get_stock_quotes(params_payload).df

    formatted_data = None

    return formatted_data


async def gen_orders_data(
    acc: AlpacaAccount,
    target_symbols: List[str],
    period_start: datetime,
    period_end: datetime,
    paper_trading: bool = True,
):

    order_data_client = TradingClient(*acc.get_api_keys(), paper=paper_trading)

    params_payload = GetOrdersRequest(
        status=QueryOrderStatus.CLOSED,
        limit=500,  # 500 is max orders returned
        after=period_start,
        # until=period_end,  TODO something weird going on w/ this param
        symbols=target_symbols
    )

    filled_orders = order_data_client.get_orders(filter=params_payload)

    formatted_data = None

    return formatted_data


async def gen_data(
    acc: AlpacaAccount,
    params: DataProviderParams
) -> DataProviderPayload:

    stock_data = await gen_stock_prices(
        acc=acc,
        target_symbols=params.stock_tickers,
        period_start=params.period_start,
        period_end=params.period_end)
    orders_data = await gen_orders_data(
        acc=acc,
        target_symbols=params.stock_tickers,
        period_start=params.period_start,
        period_end=params.period_end,
        paper_trading=acc.paper_trading)

    diff_data_sources = {
        'stock_data': stock_data,
        'orders_data': orders_data
    }

    combined_data_sources = diff_data_sources  # TODO actually set this up lol

    final_data_payload = DataProviderPayload(
        params=params,
        diff_data_sources=diff_data_sources,
        combined_data_sources=combined_data_sources
    )

    return final_data_payload
