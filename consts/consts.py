from enum import Enum
import datetime as dt
from data.data_classes import DataProviderParams
from core_script.cli_formatters import red, green, yellow


class WeatherCoords(Enum):
    NY_WALL_STREET = (40.70618619744728, -74.00914109658291)

class RunTypeParam(Enum):
    TEST = 'test'
    FULL_TEST = 'full_test'
    PROD = 'prod'
    PROD_DANGEROUS = 'prod_dangerous'
    DOWNLOAD = 'download'
    

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


commands = {
    RunTypeParam.TEST.value: {
        'run_mode': 'Test [Default]',
        'run_type_param': RunTypeParam.TEST,
        'trade_credentials': green('Paper Trading'),
        'can_trade': green('False'),
        'run_mode_descr': 'Running without account checks'
    },
    RunTypeParam.FULL_TEST.value: {
        'run_mode': 'Full Test',
        'run_type_param': RunTypeParam.FULL_TEST,
        'trade_credentials': green('Paper Trading'),
        'can_trade': green('False'),
        'run_mode_descr': 'Full test run'
    },
    RunTypeParam.PROD.value: {
        'run_mode': 'Prod',
        'run_type_param': RunTypeParam.PROD,
        'trade_credentials': red('Real Money Trading'),
        'can_trade': green('False'),
        'run_mode_descr': 'Running in prod without trading'
    },
    RunTypeParam.PROD_DANGEROUS.value: {
        'run_mode': 'Prod DANGEROUS',
        'run_type_param': RunTypeParam.PROD_DANGEROUS,
        'trade_credentials': red('Real Money Trading'),
        'can_trade': red('True'),
        'run_mode_descr': 'Running prod with trading'
    },
    RunTypeParam.DOWNLOAD.value: {
        'run_mode': 'Download',
        'run_type_param': RunTypeParam.DOWNLOAD,
        'trade_credentials': green('Paper Trading'),
        'can_trade': green('False'),
        'run_mode_descr': 'Full test run to download data'
    },
    'help': {
        'run_mode': 'Help',
        'run_type_param': RunTypeParam.TEST,
        'trade_credentials': '\033[92mNone\033[0m',
        'can_trade': green('False'),
        'run_mode_descr':  f'''
{green('COMMANDS')}

Modify the scripts execution behavior by adding params
after calling the script. No need to add additional syntax, 
just the word will do.

Available script run modes:
... {green('test')} [default]   => runs script in paper trading, skipping certain account checks
... {green('full_test')}        => runs script in paper trading, including account checks
... {green('prod')}             => runs script with real trading account
... {green('prod_dangerous')}   => runs script with real money and trading authorization
... {green('download')}         => runs script with paper creds and initials a download of the data
... {green('help')}             => shows help command
\033[0m
'''
    },
    'no_arg_found': {
        'run_mode': 'No args [Default to Test]',
        'run_type_param': RunTypeParam.TEST,
        'trade_credentials': green('Paper Trading'),
        'can_trade': green('False'),
        'run_mode_descr': 'No argument was found, running in test mode without account checks'
    }
}
