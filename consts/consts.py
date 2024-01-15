import datetime as dt
from enum import Enum

from alpaca.data.timeframe import TimeFrame

import consts.cli_messages as mess
from core_script.cli_formatters import green, red, yellow
from data.data_classes import DataProviderParams
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce, OrderClass


class WeatherCoords(Enum):
    NY_WALL_STREET = (40.70618619744728, -74.00914109658291)


class RunTypeParam(Enum):
    TEST = 'test'
    FULL_TEST = 'full_test'
    TRADE_TEST = 'trade_test'
    PROD = 'prod'
    PROD_DANGEROUS = 'prod_dangerous'
    DOWNLOAD = 'download'


class ParamTradeCredentials(Enum):
    PAPER_TRADING = 'paper_trading'
    REAL_MONEY_TRADING = 'real_money_trading'
    NONE = 'none'


class ParamCanTrade(Enum):
    CAN_TRADE_PAPER = 'can_trade_paper'
    CAN_TRADE_REAL_MONEY = 'can_trade_real_money'
    CAN_NOT_TRADE_ANY = 'can_not_trade_any'


'''
**********************************************************
Run time modes, do not edit
**********************************************************
'''

commands = {
    RunTypeParam.TEST.value: {
        'run_mode': 'Test [Default]',
        'run_type_param': RunTypeParam.TEST,
        'trade_credentials': ParamTradeCredentials.PAPER_TRADING,
        'can_trade': ParamCanTrade.CAN_NOT_TRADE_ANY,
        'run_mode_descr': 'Running without account checks'
    },
    RunTypeParam.FULL_TEST.value: {
        'run_mode': 'Full Test',
        'run_type_param': RunTypeParam.FULL_TEST,
        'trade_credentials': ParamTradeCredentials.PAPER_TRADING,
        'can_trade': ParamCanTrade.CAN_NOT_TRADE_ANY,
        'run_mode_descr': 'Full test run'
    },
    RunTypeParam.TRADE_TEST.value: {
        'run_mode': 'Trade Test',
        'run_type_param': RunTypeParam.TRADE_TEST,
        'trade_credentials': ParamTradeCredentials.PAPER_TRADING,
        'can_trade': ParamCanTrade.CAN_TRADE_PAPER,
        'run_mode_descr': 'Runs test run with trading, skipping account checks'
    },
    RunTypeParam.PROD.value: {
        'run_mode': 'Prod',
        'run_type_param': RunTypeParam.PROD,
        'trade_credentials': ParamTradeCredentials.REAL_MONEY_TRADING,
        'can_trade': ParamCanTrade.CAN_NOT_TRADE_ANY,
        'run_mode_descr': 'Running in prod without trading'
    },
    RunTypeParam.PROD_DANGEROUS.value: {
        'run_mode': 'Prod DANGEROUS',
        'run_type_param': RunTypeParam.PROD_DANGEROUS,
        'trade_credentials': ParamTradeCredentials.REAL_MONEY_TRADING,
        'can_trade': ParamCanTrade.CAN_TRADE_REAL_MONEY,
        'run_mode_descr': 'Running prod with trading'
    },
    RunTypeParam.DOWNLOAD.value: {
        'run_mode': 'Download',
        'run_type_param': RunTypeParam.DOWNLOAD,
        'trade_credentials': ParamTradeCredentials.PAPER_TRADING,
        'can_trade': ParamCanTrade.CAN_NOT_TRADE_ANY,
        'run_mode_descr': 'Full test run to download data'
    },
    'help': {
        'run_mode': 'Help',
        'run_type_param': RunTypeParam.TEST,
        'trade_credentials': ParamTradeCredentials.NONE,
        'can_trade': ParamCanTrade.CAN_NOT_TRADE_ANY,
        'run_mode_descr':  mess.help_message
    },
    'no_arg_found': {
        'run_mode': 'No args [Default to Test]',
        'run_type_param': RunTypeParam.TEST,
        'trade_credentials': ParamTradeCredentials.PAPER_TRADING,
        'can_trade': ParamCanTrade.CAN_NOT_TRADE_ANY,
        'run_mode_descr': 'No argument was found, running in test mode without account checks'
    }
}


'''
**********************************************************
Data param presets that can be used during test and
prod runs. See data/data_classes ==> DataProviderParams
for more info on these params.

These are primarily for testing purposes and downloading,
in actual prod executions only one param will be run.
**********************************************************
'''


data_param_presets: dict[str, DataProviderParams] = {
    'default': DataProviderParams(
        stock_tickers=["SPY", "META", "GOOG"],
        get_live_stock_data=True,
        get_custom_period_stock_data=True,
        custom_stock_data_period=TimeFrame.Day,
        get_acc_trade_data=True,
        get_weather_data=True,
        period_start=dt.date.today() - dt.timedelta(days=365),
        period_end=dt.date.today() - dt.timedelta(days=1),
        show_data_previews=True,
        show_data_info=True,
    ),
    'spy_only': DataProviderParams(
        stock_tickers=["SPY"],
        get_live_stock_data=True,
        get_custom_period_stock_data=True,
        custom_stock_data_period=TimeFrame.Day,
        get_acc_trade_data=True,
        get_weather_data=True,
        period_start=dt.date.today() - dt.timedelta(days=365),
        period_end=dt.date.today() - dt.timedelta(days=1),
        show_data_previews=True,
        show_data_info=True,
    ),
    'spy_only_skip_extra': DataProviderParams(
        stock_tickers=["SPY"],
        get_live_stock_data=True,
        get_custom_period_stock_data=True,
        custom_stock_data_period=TimeFrame.Day,
        get_acc_trade_data=False,
        get_weather_data=False,
        period_start=dt.date.today() - dt.timedelta(days=365),
        period_end=dt.date.today() - dt.timedelta(days=1),
        show_data_previews=True,
        show_data_info=True,
    ),
    'no_data': DataProviderParams(
        stock_tickers=["SPY"],
        get_live_stock_data=False,
        get_custom_period_stock_data=True,
        custom_stock_data_period=TimeFrame.Week,
        get_acc_trade_data=False,
        get_weather_data=False,
        period_start=dt.date.today() - dt.timedelta(days=365),
        period_end=dt.date.today() - dt.timedelta(days=1),
        show_data_previews=True,
        show_data_info=True,
    ),
}


trade_param_presets: dict[str, MarketOrderRequest] = {
    'default': MarketOrderRequest(
        symbol='SPY',
        qty=.01,
        side=OrderSide.BUY,
        type=OrderType.MARKET,
        time_in_force=TimeInForce.DAY,
        # notional = 1 Does NOT work while using qty
        # extended_hours= float idrk
        # client_order_id= str doesn't apply to single user bot
        # order_class = OrderClass doesn't apply
        # take_profit= TakeProfitRequest don't think this matters
        # stop_loss   =  StopLossRequest doesn't apply
    )
}
