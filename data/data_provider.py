from typing import List
import pandas as pd
import json
import datetime
import asyncio

from consts.consts import WeatherCoords
from core_script.class_alpaca_account import AlpacaAccount
from data.data_classes import DataProviderParams, OrderHistoryPayload
from data.data_classes import DataProviderPayload

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data import StockQuotesRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus
from alpaca.trading.client import TradingClient

import openmeteo_requests
import requests_cache
from retry_requests import retry

"""
Generates the price history of an asset or list of assets

Returns a dict with 2 entries:
    - a dict w/ individual asset dataframes
    - a df with all asset data unioned together

Fields with an underscore prefix are raw data 
from the api e.g.
    - _ask_price    is from Alpaca
    - _tape         is from Alpaca
    - market_price  is derived

Nested data is of the type PriceHistoryPayload
"""


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
        end=period_end, ## TODO something weird going on w/ this param
        limit=100000,
        # timeframe=TimeFrame.Day,
        feed='sip',
        sort='asc',
    )

    hist_price_dataframe = hist_data_client.get_stock_quotes(params_payload)

    each_asset_df = {}
    all_assets_df = pd.DataFrame()

    for asset in hist_price_dataframe.data:
        asset_df = pd.DataFrame(
            [{key: value for key, value in obj} for obj in hist_price_dataframe.data[asset]])

        formatted_df = format_raw_columns(asset_df)

        formatted_df = formatted_df.assign(market_price=(
            formatted_df['_bid_price'] + formatted_df['_ask_price']) / 2)

        all_assets_df = pd.concat([all_assets_df, formatted_df], axis=1)
        each_asset_df[asset] = formatted_df

    final_data = {
        'price_history_by_asset': each_asset_df,
        'price_history_all': all_assets_df
    }

    return final_data


"""
Generates the Alpaca trading account closed/filled orders history

Data is of the type OrderHistoryPayload and then converted to dataframe
"""
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
        nested=True,
        until=period_end, ## TODO something weird going on w/ this param
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
        period_end: datetime,
):
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


def format_raw_columns (
        raw_data: pd.DataFrame
) -> pd.DataFrame:
    
    for col in raw_data.columns:
        raw_data.rename(columns={col: '_' + col}, inplace=True)

    return raw_data


"""
Generates all relevant data, with optional params on which data to get

Data is returned as individual dataframes as well as a TODO combined dataframe
indexed by time
"""
async def gen_data(
    acc: AlpacaAccount,
    params: DataProviderParams
) -> DataProviderPayload:

    nyc_lat, nyc_long = WeatherCoords.NY_WALL_STREET.value
    print(nyc_lat)
    print(nyc_long)
    print(params.period_start)
    print(params.period_end)

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
    weather_data = await gen_weather_data(
        latitude=nyc_lat,
        longitude=nyc_long,
        period_start=params.period_start,
        period_end=params.period_end
    )

    diff_data_sources = {
        'stock_data': stock_data,
        'orders_data': orders_data,
        'weather_data': weather_data
    }

    print(diff_data_sources)
    combined_data_sources = diff_data_sources  # TODO actually set this up lol

    final_data_payload = DataProviderPayload(
        params=params,
        diff_data_sources=diff_data_sources,
        combined_data_sources=combined_data_sources
    )

    return final_data_payload
