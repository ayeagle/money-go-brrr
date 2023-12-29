import pandas_market_calendars as mcal
import sys
import datetime
from consts.consts import RunTypeParam
from decouple import config

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

    

def handle_special_commands(arg: str):

    if(arg in commands):
        command_data = commands.get(arg)
        print_run_mode_summary([arg])
    else: 
        command_data = commands.get('no_arg_found')
        print_run_mode_summary(['no_arg_found'])

    if(command_data['run_type_param'] == RunTypeParam.PROD_DANGEROUS and not ready_to_trade):
        print(not_ready_warning_message)
        print_run_mode_summary(commands.keys())
        print(not_ready_warning_message)
        sys.exit()
    elif(command_data['run_type_param']  == RunTypeParam.TEST and arg == 'help'):
        print_run_mode_summary(commands.keys())
        sys.exit()

    return command_data['run_type_param']


def print_run_mode_summary(items: list):
        
        if(len(items) > 1):
            print(help_message)
            print('See more detail about run modes below...\n')

        print("\n*******************************************************************\n")
        for key in items:
            if(key == 'help' or key == 'no_arg_found'): continue
            command_data = commands[key]
            print('Run Mode:    \u001b[44;1m\033[92m' + command_data['run_mode']+' \u001b[0m')
            print('Script flag:     ' + "'"+command_data['run_type_param'].value +"'")
            print('Credentials:     ' + command_data['trade_credentials'])
            print('Can Trade:       ' + command_data['can_trade'])
            print('Description:     ' + command_data['run_mode_descr'])
            print("\n*******************************************************************\n")



not_ready_warning_message = '''
\n\033[91m*******************************************************************
***                          WARNING                            ***
***              The script is NOT ready to trade               ***
***        Please do not use 'prod_dangerous' param yet         ***
*******************************************************************\n\033[0m
'''

help_message = '''
\033[92mCOMMANDS\033[0m

Modify the scripts execution behavior by adding params
after calling the script. No need to add flags, just the
word will do.

Available script run modes:
... \033[92mtest\033[0m [default]  => runs script in paper trading, skipping certain account checks
... \033[92mfull_test       \033[0m=> runs script in paper trading, including account checks
... \033[92mprod            \033[0m=> runs script with real trading account
... \033[92mprod_dangerous  \033[0m=> runs script with real money and trading authorization
... \033[92mdownload        \033[0m=> runs script with paper creds and initials a download of the data
... \033[92mhelp            \033[0m=> shows help command
\033[0m
'''

commands = {
    RunTypeParam.TEST.value: {
        'run_mode': 'Test',
        'run_type_param': RunTypeParam.TEST,
        'trade_credentials': '\033[92mPaper Trading\033[0m',
        'can_trade': '\033[92mFalse\033[0m',
        'run_mode_descr' : 'Running without account checks'
    },
    RunTypeParam.FULL_TEST.value: {
        'run_mode': 'Full Test',
        'run_type_param': RunTypeParam.FULL_TEST,
        'trade_credentials': '\033[92mPaper Trading\033[0m',
        'can_trade': '\033[92mFalse\033[0m',
        'run_mode_descr' : 'Full test run'
    },
    RunTypeParam.PROD.value: {
        'run_mode': 'Prod',
        'run_type_param': RunTypeParam.PROD,
        'trade_credentials': '\033[91mReal Money Trading\033[0m',
        'can_trade': '\033[92mFalse\033[0m',
        'run_mode_descr' : 'Running in prod without trading'
    },
    RunTypeParam.PROD_DANGEROUS.value: {
        'run_mode': 'Prod DANGEROUS',
        'run_type_param': RunTypeParam.PROD_DANGEROUS,
        'trade_credentials': '\033[91mReal Money Trading\033[0m',
        'can_trade': '\033[91mTrue\033[0m',
        'run_mode_descr' : 'Running prod with trading'
    },
    RunTypeParam.DOWNLOAD.value: {
        'run_mode': 'Download',
        'run_type_param': RunTypeParam.DOWNLOAD,
        'trade_credentials': '\033[92mPaper Trading\033[0m',
        'can_trade': '\033[92mFalse\033[0m',
        'run_mode_descr' : 'Full test run to download data'
    },
    'help': {
        'run_mode': 'Help',
        'run_type_param': RunTypeParam.TEST,
        'trade_credentials': '\033[92mNone\033[0m',
        'can_trade': '\033[92mFalse\033[0m',
        'run_mode_descr' : help_message
    },
    'no_arg_found': {
        'run_mode': 'Test',
        'run_type_param': RunTypeParam.TEST,
        'trade_credentials': '\033[92mPaper Trading\033[0m',
        'can_trade': '\033[92mFalse\033[0m',
        'run_mode_descr' : 'No argument was found, running in test mode without account checks'
    }
}
