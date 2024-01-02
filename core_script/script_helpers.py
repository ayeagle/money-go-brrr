from numpy import void
import pandas as pd
import pandas_market_calendars as mcal
import sys
from datetime import datetime
from core_script.class_alpaca_account import AlpacaAccount
from consts.consts import RunTypeParam
from decouple import config
from typing import Union


from data.data_classes import DataProviderPayload

ready_to_trade = config('READY_TO_TRADE') == 'True'


def is_trading_day() -> bool:
    nyse = mcal.get_calendar('NYSE')
    today = datetime.date.today()
    data = nyse.schedule(today, today)
    if data.empty:
        print('Not a valid trading day')
        return False
    else:
        print('Valid trading day')
        return True


def convert_cli_args() -> list:
    args = sys.argv[1:]
    if args and len(args) > 0:
        primary_arg = args[0].lower()
    else:
        primary_arg = ''
    run_param = handle_special_commands(primary_arg)
    return run_param


def gen_download_files(
        data: Union[DataProviderPayload, dict],
        ts: tuple) -> void:

    if isinstance(data, DataProviderPayload):
        exec_df_download(data.combined_data_sources,
                         'combine_data_sources', ts)
        gen_download_files(data.diff_data_sources, ts)
    else:
        for key in data.keys():
            val = data[key]
            if isinstance(val, pd.DataFrame):
                print(f"\nDataFrame at key '{key}':")
                print(val.head())
                exec_df_download(val, key, ts)
            elif isinstance(val, dict):
                gen_download_files(val, ts)


def exec_df_download(
        data: pd.DataFrame,
        file_name: str,
        timestamp: tuple) -> void:
    data.to_csv(
        f'downloaded_data/{timestamp[0]}_{file_name}_{timestamp[1]}.csv', index=False)


def handle_special_commands(arg: str) -> RunTypeParam:

    if (arg in commands):
        command_data = commands.get(arg)
        print_run_mode_summary([arg])
    else:
        command_data = commands.get('no_arg_found')
        print_run_mode_summary(['no_arg_found'])

    if (command_data['run_type_param'] == RunTypeParam.PROD_DANGEROUS and not ready_to_trade):
        print(not_ready_warning_message)
        print_run_mode_summary(commands.keys())
        print(not_ready_warning_message)
        sys.exit()
    elif (command_data['run_type_param'] == RunTypeParam.TEST and arg == 'help'):
        print_run_mode_summary(commands.keys())
        sys.exit()

    return command_data['run_type_param']


def print_run_mode_summary(items: list) -> void:
    if (len(items) > 1):
        print(help_message)
        print('See more detail about run modes below...\n')

    print("\n*******************************************************************\n")
    for key in items:
        if (key == 'help'):
            continue
        command_data = commands[key]
        print('Run Mode:    \u001b[44;1m\033[92m' +
              command_data['run_mode']+' \u001b[0m')
        print('Script flag:     ' + "'" +
              command_data['run_type_param'].value + "'")
        print('Credentials:     ' + command_data['trade_credentials'])
        print('Can Trade:       ' + command_data['can_trade'])
        print('Description:     ' + command_data['run_mode_descr'])
        print("\n*******************************************************************\n")


def red(text: str) -> str:
    return f'\033[91m{text}\033[0m'


def green(text: str) -> str:
    return f'\033[92m{text}\033[0m'


not_ready_warning_message = red('''
\n*******************************************************************
***                          WARNING                            ***
***              The script is NOT ready to trade               ***
***        Please do not use 'prod_dangerous' param yet         ***
*******************************************************************
''')

help_message = f'''
{green('COMMANDS')}

Modify the scripts execution behavior by adding params
after calling the script. No need to add flags, just the
word will do.

Available script run modes:
... {green('test')} [default]   => runs script in paper trading, skipping certain account checks
... {green('full_test')}        => runs script in paper trading, including account checks
... {green('prod')}             => runs script with real trading account
... {green('prod_dangerous')}   => runs script with real money and trading authorization
... {green('download')}         => runs script with paper creds and initials a download of the data
... {green('help')}             => shows help command
\033[0m
'''


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
        'run_mode_descr': help_message
    },
    'no_arg_found': {
        'run_mode': 'No args [Default to Test]',
        'run_type_param': RunTypeParam.TEST,
        'trade_credentials': green('Paper Trading'),
        'can_trade': green('False'),
        'run_mode_descr': 'No argument was found, running in test mode without account checks'
    }
}
