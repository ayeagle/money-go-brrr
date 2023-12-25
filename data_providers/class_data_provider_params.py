import datetime
from enums.data_type_enums import DataSourceFormat
from typing import Union, List


class DataProviderParams:
    def __init__(
            self,
            stock_tickers: List[str] = ["spy"],
            get_acc_trade_data: bool = False,
            get_weather_data: bool = False,
            period_start: datetime = None,
            period_end: datetime = None,
            data_format: DataSourceFormat = DataSourceFormat.PYDICT
    ):
        self._stock_tickers = stock_tickers
        self._get_acc_trade_data = get_acc_trade_data
        self._get_weather_data = get_weather_data
        self._period_start = period_start or datetime.date.today() - datetime.timedelta(days=1)
        self._period_end = period_end or self.period_start - datetime.timedelta(days=365 * 2)
        self._data_format = data_format
        
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

    @property
    def data_format(self):
        return self._data_format