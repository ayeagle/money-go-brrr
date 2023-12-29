import pandas_market_calendars as mcal
import sys
import datetime

not_ready_to_trade = True

help_message = '''
\033[92mCOMMANDS\033[0m

Modify the scripts execution behavior by adding params
after calling the script. No need to add flags, just the
word will do.

Available script commands:
... \033[92mtest\033[0m [default]  => runs script in paper trading, skipping certain account checks
... \033[92mfull_test       \033[0m=> runs script in paper trading, including account checks
... \033[92mprod            \033[0m=> runs script with real trading account
... \033[92mprod_dangerous  \033[0m=> runs script with real money and trading authorization
... \033[92mdownload        \033[0m=> runs script with paper creds and initials a download of the data
... \033[92mhelp            \033[0m=> shows help command
\033[0m
'''

commands = {
    'test': {
        'run_mode': 'Test',
        'trade_credentials': '\033[92mPaper Trading\033[0m',
        'can_trade': '\033[92mFalse\033[0m',
        'run_mode_descr' : 'Running without account checks'
    },
    'full_test': {
        'run_mode': 'Full Test',
        'trade_credentials': '\033[92mPaper Trading\033[0m',
        'can_trade': '\033[92mFalse\033[0m',
        'run_mode_descr' : 'Full test run'
    },
    'prod': {
        'run_mode': 'Prod',
        'trade_credentials': '\033[91mReal Money Trading\033[0m',
        'can_trade': '\033[92mFalse\033[0m',
        'run_mode_descr' : 'Running in prod without trading'
    },
    'prod_dangerous': {
        'run_mode': 'Prod DANGEROUS',
        'trade_credentials': '\033[91mReal Money Trading\033[0m',
        'can_trade': '\033[91mTrue\033[0m',
        'run_mode_descr' : 'Running prod with trading'
    },
    'download': {
        'run_mode': 'Download',
        'trade_credentials': '\033[92mPaper Trading\033[0m',
        'can_trade': '\033[92mFalse\033[0m',
        'run_mode_descr' : 'Full test run to download data'
    },
    'help': {
        'run_mode': 'Help',
        'trade_credentials': '\033[92mNone\033[0m',
        'can_trade': '\033[92mFalse\033[0m',
        'run_mode_descr' : help_message
    },
    'no_arg_found': {
        'run_mode': 'Test',
        'trade_credentials': '\033[92mPaper Trading\033[0m',
        'can_trade': '\033[92mFalse\033[0m',
        'run_mode_descr' : 'No argument was found, running in test mode without account checks'
    }
}


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

    command: str

    if(arg in commands):
        command = arg
        display_data = commands.get(arg)
    else: 
        command = 'test'
        display_data = commands.get('no_arg_found')
    print("\n*******************************************************************\n")
    print('Run Mode:    ' + display_data['run_mode'])
    print('Credentials: ' + display_data['trade_credentials'])
    print('Can Trade:   ' + display_data['can_trade'])
    print('Description: ' + display_data['run_mode_descr'])
    print("\n*******************************************************************\n")


    if(command == 'prod_dangerous' and not_ready_to_trade):
        print("\n\033[91m*******************************************************************")
        print("***                          WARNING                            ***")
        print("***              The script is NOT ready to trade               ***")
        print("***        Please do not use 'prod_dangerous' param yet         ***")
        print("*******************************************************************\n\033[0m")

        print('See other commands. Exiting script run...\n')
        print(help_message)
        sys.exit()


    return command