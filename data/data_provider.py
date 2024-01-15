import datetime
from typing import List

import openmeteo_requests
import pandas as pd
import requests_cache
from alpaca.common.types import RawData
from alpaca.data import StockBarsRequest, StockQuotesRequest
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.models import QuoteSet
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import QueryOrderStatus
from alpaca.trading.requests import GetOrdersRequest
from numpy import void
from retry_requests import retry

from consts.consts import RunTypeParam, WeatherCoords
from core_script.class_alpaca_account import AlpacaAccount
from core_script.script_helpers import gen_preview_files
from data.data_classes import (DataProviderParams, DataProviderPayload,
                               OrderHistoryPayload)

"""
**********************************************************
Generates the price history of an asset 

Fields with an underscore prefix are raw data 
from the api e.g.
    - _ask_price    is from Alpaca
    - _tape         is from Alpaca
    - market_price  is derived

Nested data is of the type PriceHistoryPayload
**********************************************************
"""


async def gen_recent_live_stock_prices(
        acc: AlpacaAccount,
        target_symbol: str,
        period_start: datetime,
        period_end: datetime) -> pd.DataFrame:

    hist_data_client = StockHistoricalDataClient(*acc.get_api_keys())

    params_payload = StockQuotesRequest(
        symbol_or_symbols=target_symbol,
        start=period_start,
        end=period_end,  # TODO something weird going on w/ this param
        limit=10000,
        # timeframe=TimeFrame.Day,
        feed='sip',
        sort='asc',
    )

    hist_price_dataframe = hist_data_client.get_stock_quotes(params_payload)

    formatted_df = format_nested_stock_df(hist_price_dataframe, target_symbol)

    formatted_df = formatted_df.assign(market_price=(
        formatted_df['_bid_price'] + formatted_df['_ask_price']) / 2)

    return formatted_df


"""
**********************************************************
Generates the price history of an asset or list of assets
with open and closing prices based on an interval of time
**********************************************************
"""


async def gen_custom_period_stock_prices(
        acc: AlpacaAccount,
        target_symbol: str,
        period_start: datetime,
        period_end: datetime,
        period_interval: TimeFrame) -> pd.DataFrame:

    hist_data_client = StockHistoricalDataClient(*acc.get_api_keys())

    params_payload = StockBarsRequest(
        symbol_or_symbols=target_symbol,
        start=period_start,
        end=period_end,  # TODO something weird going on w/ this param
        limit=1000,
        timeframe=period_interval,
        feed='sip',
        sort='asc',
    )

    hist_price_dataframe = hist_data_client.get_stock_bars(params_payload)

    formatted_df = format_nested_stock_df(hist_price_dataframe, target_symbol)

    return formatted_df


"""
**********************************************************
Generates the Alpaca trading account closed/filled 
orders history

Data is of the type OrderHistoryPayload and then 
converted to dataframe
**********************************************************
"""


async def gen_orders_data(
        acc: AlpacaAccount,
        target_symbols: List[str],
        period_start: datetime,
        period_end: datetime,
        paper_trading: bool = True) -> pd.DataFrame:

    order_data_client = TradingClient(*acc.get_api_keys(), paper=paper_trading)

    params_payload = GetOrdersRequest(
        status=QueryOrderStatus.CLOSED,
        limit=500,  # 500 is max orders returned
        after=period_start,
        nested=True,
        until=period_end,  # TODO something weird going on w/ this param
        symbols=target_symbols
    )

    filled_orders: OrderHistoryPayload = order_data_client.get_orders(
        filter=params_payload)

    filled_orders_dataframe = pd.DataFrame(
        [{key: value for key, value in obj} for obj in filled_orders])

    formatted_df = format_raw_columns(filled_orders_dataframe)

    return formatted_df


async def gen_weather_data(
        latitude: float,
        longitude: float,
        period_start: datetime,
        period_end: datetime) -> pd.DataFrame:

    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": period_start,
        "end_date": period_end,
        "timezone": 'EST',
        'temperature_unit': 'fahrenheit',
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "apparent_temperature_max",
            "apparent_temperature_min"
        ]
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    dates = pd.date_range(
        start=pd.to_datetime(response.Daily().Time(), unit="s"),
        end=pd.to_datetime(response.Daily().TimeEnd(), unit="s"),
        freq=pd.Timedelta(seconds=response.Daily().Interval()),
        inclusive="right"
    ).strftime('%Y-%m-%d').tolist()

    temp_max = response.Daily().Variables(0).ValuesAsNumpy().tolist()
    temp_min = response.Daily().Variables(1).ValuesAsNumpy().tolist()
    feels_temp_max = response.Daily().Variables(2).ValuesAsNumpy().tolist()
    feels_temp_min = response.Daily().Variables(3).ValuesAsNumpy().tolist()

    weather_df = pd.DataFrame({
        "_latitude": response.Latitude(),
        "_longitude": response.Longitude(),
        '_date': dates,
        '_max_temp': temp_max,
        '_min_temp': temp_min,
        '_feels_max_temp': feels_temp_max,
        '_feels_min_temp': feels_temp_min
    })

    # location_data = {
    #     "latitude": response.Latitude(),
    #     "longitude": response.Longitude(),
    #     "elevation": response.Elevation(),
    #     "timezone": response.Timezone(),
    #     "model": response.Model(),
    #     "daily": response.Daily(),
    #     # "temperature_unit": response.temperature_unit(),
    #     "timezone_abbreviation": response.TimezoneAbbreviation(),
    #     "utc_offset_seconds": response.UtcOffsetSeconds(),
    #     "daily_data": {
    #         "date": pd.date_range(
    #             start=pd.to_datetime(response.Daily().Time(), unit="s"),
    #             end=pd.to_datetime(response.Daily().TimeEnd(), unit="s"),
    #             freq=pd.Timedelta(seconds=response.Daily().Interval()),
    #             inclusive="left"
    #         ).strftime('%Y-%m-%d').tolist(),  # Convert to string and then to list
    #         "temperature_2m_max": response.Daily().Variables(0).ValuesAsNumpy(),
    #         "temperature_2m_min": response.Daily().Variables(1).ValuesAsNumpy().tolist()

    #     }
    # }

    return weather_df


"""
**********************************************************
Dataframe formatters
**********************************************************
"""


def format_nested_stock_df(raw_data: QuoteSet | RawData, asset_key: str) -> pd.DataFrame:

    df = pd.DataFrame(
        [{key: value for key, value in obj} for obj in raw_data.data[asset_key]])

    formatted_df = format_raw_columns(df)

    return formatted_df


def format_raw_columns(raw_data: pd.DataFrame) -> pd.DataFrame:

    for col in raw_data.columns:
        raw_data.rename(columns={col: '_' + col}, inplace=True)

    return raw_data


"""
**********************************************************
Generates all relevant data, with optional params 
on which data to get

Data is returned as individual dataframes as well 
as a TODO combined dataframe indexed by time
**********************************************************
"""


async def gen_data(
    acc: AlpacaAccount,
    params: DataProviderParams
) -> DataProviderPayload:

    nyc_lat, nyc_long = WeatherCoords.NY_WALL_STREET.value

    diff_data_sources = {}
    diff_data_sources['recent_stock_feed_data'] = {}
    diff_data_sources['custom_period_stock_data'] = {}

    for stonk in params.stock_tickers:
        if (params.get_live_stock_data):
            new_data = await gen_recent_live_stock_prices(
                acc=acc,
                target_symbol=stonk,
                period_start=params.period_start,
                period_end=params.period_end)
            live_data_key = stonk + "_live"
            diff_data_sources['recent_stock_feed_data'][live_data_key] = new_data
        if (params.get_custom_period_stock_data):
            new_custom_data = await gen_custom_period_stock_prices(
                acc=acc,
                target_symbol=stonk,
                period_start=params.period_start,
                period_end=params.period_end,
                period_interval=params.custom_stock_data_period)
            custom_data_key = stonk + "_custom"
            diff_data_sources['custom_period_stock_data'][custom_data_key] = new_custom_data

    if (params.get_acc_trade_data):
        orders_data = await gen_orders_data(
            acc=acc,
            target_symbols=params.stock_tickers,
            period_start=params.period_start,
            period_end=params.period_end,
            paper_trading=acc.paper_trading)
        diff_data_sources['orders_data'] = orders_data

    if (params.get_weather_data):
        weather_data = await gen_weather_data(
            latitude=nyc_lat,
            longitude=nyc_long,
            period_start=params.period_start,
            period_end=params.period_end
        )
        diff_data_sources['weather_data'] = weather_data

    # print(diff_data_sources)
    # TODO actually set this up lol
    combined_data_sources = pd.DataFrame()

    final_data_payload = DataProviderPayload(
        params=params,
        diff_data_sources=diff_data_sources,
        combined_data_sources=combined_data_sources
    )

    if (acc.run_type_param != RunTypeParam.DOWNLOAD):
        gen_preview_files(
            data_params=params,
            data=final_data_payload)

    return final_data_payload
