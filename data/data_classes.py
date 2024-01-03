from datetime import date, datetime, timedelta
from typing import Union, List, Optional
import pandas as pd
import datetime as dt

class DataProviderParams:
    def __init__(
            self,
            stock_tickers: list[str] = ["spy","meta","goog"],
            get_acc_trade_data: bool = True,
            get_weather_data: bool = True,
            period_start: datetime = None,
            period_end: datetime = None,
    ):
        self._stock_tickers = stock_tickers
        self._get_acc_trade_data = get_acc_trade_data
        self._get_weather_data = get_weather_data
        self._period_end = period_end or dt.date.today() - dt.timedelta(days=1)
        self._period_start = period_start or self._period_end - dt.timedelta(days=365)
        
    @property
    def stock_tickers(self):
        return self._stock_tickers

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
