
import datetime as dt
from data.data_classes import DataProviderParams

data_param_presets: dict[str, DataProviderParams] = {
    'default': DataProviderParams(
        stock_tickers=["spy", "meta", "goog"],
        get_acc_trade_data=True,
        get_weather_data=True,
        period_start=dt.date.today() - dt.timedelta(days=365),
        period_end=dt.date.today() - dt.timedelta(days=1),
    ),
    'spy_only': DataProviderParams(
        stock_tickers=["spy"],
        get_acc_trade_data=True,
        get_weather_data=True,
        period_start=dt.date.today() - dt.timedelta(days=365),
        period_end=dt.date.today() - dt.timedelta(days=1),
    ),
    'spy_only_skip_extra': DataProviderParams(
        stock_tickers=["spy"],
        get_acc_trade_data=False,
        get_weather_data=False,
        period_start=dt.date.today() - dt.timedelta(days=365),
        period_end=dt.date.today() - dt.timedelta(days=1),    
    )
}
