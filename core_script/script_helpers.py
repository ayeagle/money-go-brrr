import sys
from datetime import datetime
from typing import Union

import pandas as pd
import pandas_market_calendars as mcal
from decouple import config
from numpy import void

import consts.cli_messages as mess
from consts.consts import RunTypeParam, commands, data_param_presets
from core_script.class_alpaca_account import AlpacaAccount
from core_script.cli_formatters import (blue_back, bold, emphasize, green, red,
                                        yellow)
from data.data_classes import DataProviderParams, DataProviderPayload

ready_to_trade = config('READY_TO_TRADE') == 'True'

'''
**********************************************************
General functions
**********************************************************
'''


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


'''
**********************************************************
Data provider params CLI edit functions
**********************************************************
'''


def gen_prompt_confirm_data_params(
        acc: AlpacaAccount,
        params: DataProviderParams) -> DataProviderParams:

    final_params = params

    if (acc.run_type_param == RunTypeParam.DOWNLOAD):
        print('Default params currently...')
        print_params(params)
        final_params = confirm_edit_params(params)

    print("Running with following data params:")
    print_params(final_params)

    return final_params


def print_params(params: DataProviderParams) -> void:
    params_dict = vars(params)
    for key, value in params_dict.items():
        key = key + ' :'
        print(f"{key:25}{green(value)}")


def confirm_edit_params(params) -> bool:
    input_str = input("\nDo you want to override with new params? (Y/N)")
    ans = input_str.lower()

    if (ans == 'n'):
        return params
    elif (ans == 'y'):
        return gen_set_new_params()
    else:
        print(red('\nInvalid response, use Y or N'))
        return confirm_edit_params(params)


def gen_set_new_params() -> DataProviderParams:
    print("\nAvailable data param presets")
    for key in data_param_presets.keys():
        params_dict = vars(data_param_presets[key])
        print(f'\nData Param Preset: {green(key)}')
        for key, value in params_dict.items():
            key = key + ' :'
            print(f"    {key:<25}{value}")
    print(yellow("\nDon't see what you need? Add a new param preset in consts/consts => data_param_presets"))

    ans = input(
        "\nEnter the key string for the preset you'd like to use:")

    while (ans not in data_param_presets):
        print(yellow("\nKey doesn't exist, try again..."))
        ans = input(
            "\nEnter the key string for the preset you'd like to use:")

    return data_param_presets[ans]


'''
**********************************************************
Data preview and download functions
**********************************************************
'''


def gen_preview_files(
        data: Union[DataProviderPayload, dict],
        parent: str = 'DataProviderPayload',
        should_download: bool = False,
        ts: tuple = (0, 0)) -> void:

    if isinstance(data, DataProviderPayload):
        if (should_download):
            exec_df_download(data.combined_data_sources,
                             'combine_data_sources', ts)
        gen_preview_files(data.diff_data_sources,
                          'diff_data_sources', should_download, ts)
    else:
        for key in data.keys():
            val = data[key]
            if isinstance(val, pd.DataFrame):
                preview_data(val, parent, key)
                if (should_download):
                    exec_df_download(val, key, ts)
            elif isinstance(val, dict):
                gen_preview_files(val, key, should_download, ts)


def preview_data(data: pd.DataFrame, parent: str, key: str) -> void:
    print(emphasize(f"\nFolder '{parent}' \nKey '{key}':"))
    print(green("DataFrame preview"))
    print(data.head())
    print(green("DataFrame info"))
    data.info()


def exec_df_download(
        data: pd.DataFrame,
        file_name: str,
        timestamp: tuple) -> void:
    data.to_csv(
        f'downloaded_data/{timestamp[0]}_{file_name}_{timestamp[1]}.csv', index=False)


'''
**********************************************************
CLI runtime parameter parsing functions
**********************************************************
'''


def convert_cli_args() -> list:
    args = sys.argv[1:]
    if args and len(args) > 0:
        primary_arg = args[0].lower()
    else:
        primary_arg = ''
    run_param = handle_special_commands(primary_arg)
    return run_param


def handle_special_commands(arg: str) -> RunTypeParam:

    if (arg in commands):
        command_data = commands.get(arg)
        print_run_mode_summary([arg])
    else:
        command_data = commands.get('no_arg_found')
        print_run_mode_summary(['no_arg_found'])

    if (command_data['run_type_param'] == RunTypeParam.PROD_DANGEROUS and not ready_to_trade):
        print(mess.not_ready_warning_message)
        print_run_mode_summary(commands.keys())
        print(mess.not_ready_warning_message)
        sys.exit()
    elif (command_data['run_type_param'] == RunTypeParam.TEST and arg == 'help'):
        print_run_mode_summary(commands.keys())
        sys.exit()

    return command_data['run_type_param']


def print_run_mode_summary(items: list) -> void:
    if (len(items) > 1):
        print(commands.get('help')['run_mode_descr'])
        print('See more detail about run modes below...\n')

    print(mess.hl)
    for key in items:
        if (key == 'help'):
            continue
        command_data = commands[key]
        print('Run Mode:    ' + emphasize(command_data['run_mode']))
        print('Script flag:     ' + "'" +
              command_data['run_type_param'].value + "'")
        print('Credentials:     ' + command_data['trade_credentials'])
        print('Can Trade:       ' + command_data['can_trade'])
        print('Description:     ' + command_data['run_mode_descr'])
        print(mess.hl)
