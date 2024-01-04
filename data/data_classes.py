import datetime as dt
from datetime import date, datetime, timedelta
from typing import List, Optional, Union

import pandas as pd
from alpaca.data.timeframe import TimeFrame


class DataProviderParams:
    def __init__(
            self,
            stock_tickers: list[str] = ["SPY"],
            get_live_stock_data: bool = True,
            get_custom_period_stock_data: bool = True,
            custom_stock_data_period: TimeFrame = TimeFrame.Day,
            get_acc_trade_data: bool = True,
            get_weather_data: bool = True,
            period_start: datetime = dt.date.today() - dt.timedelta(days=1),
            period_end: datetime = dt.date.today() - dt.timedelta(days=365),
            show_data_previews=True,
            show_data_info=True,
    ):
        self._stock_tickers = stock_tickers
        self._get_live_stock_data = get_live_stock_data
        self._get_custom_period_stock_data = get_custom_period_stock_data
        self._custom_stock_data_period = custom_stock_data_period
        self._custom_stock_data_period
        self._get_acc_trade_data = get_acc_trade_data
        self._get_weather_data = get_weather_data
        self._period_end = period_end
        self._period_start = period_start
        self._show_data_previews = show_data_previews
        self._show_data_info = show_data_info

    @property
    def stock_tickers(self):
        return self._stock_tickers

    @property
    def get_live_stock_data(self):
        return self._get_live_stock_data

    @property
    def get_custom_period_stock_data(self):
        return self._get_custom_period_stock_data

    @property
    def custom_stock_data_period(self):
        return self._custom_stock_data_period

    @property
    def get_acc_trade_data(self):
        return self._get_acc_trade_data

    @property
    def get_weather_data(self):
        return self._get_weather_data

    @property
    def period_start(self):
        return self._period_start

    @property
    def period_end(self):
        return self._period_end

    @property
    def show_data_previews(self):
        return self._show_data_previews

    @property
    def show_data_info(self):
        return self._show_data_info


class DataProviderPayload:
    def __init__(
            self,
            params: DataProviderParams,
            diff_data_sources: dict,
            combined_data_sources: pd.DataFrame
    ):
        self._params = params
        self._diff_data_sources = diff_data_sources
        self._combined_data_sources = combined_data_sources

    @property
    def params(self):
        return self._params

    @property
    def diff_data_sources(self):
        return self._diff_data_sources

    @property
    def combined_data_sources(self):
        return self._combined_data_sources


"""
Type enforcement/documentation for get_orders method
"""


class OrderHistoryPayload:
    asset_class: str
    asset_id: str
    canceled_at: Optional[datetime]
    client_order_id: str
    created_at: datetime
    expired_at: Optional[datetime]
    extended_hours: bool
    failed_at: Optional[datetime]
    filled_at: datetime
    filled_avg_price: float
    filled_qty: float
    hwm: Optional[float]
    id: str
    legs: Optional[str]
    limit_price: Optional[float]
    notional: Optional[float]
    order_class: str
    order_type: str
    qty: float
    replaced_at: Optional[datetime]
    replaced_by: Optional[str]
    replaces: Optional[str]
    side: str
    status: str
    stop_price: Optional[float]
    submitted_at: datetime
    symbol: str
    time_in_force: str
    trail_percent: Optional[float]
    trail_price: Optional[float]
    type: str
    updated_at: datetime


class PriceHistoryPayload:
    ask_exchange: str
    ask_price: float
    ask_size: float
    bid_exchange: str
    bid_price: float
    bid_size: float
    conditions: List[str]
    symbol: str
    tape: str
    timestamp: datetime
