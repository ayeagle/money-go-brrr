from core_script.class_alpaca_account import AlpacaAccount
import asyncio
from decouple import config
from data.data_provider import gen_data
from data.data_classes import DataProviderParams
from core_script.script_helpers import convert_cli_args, is_trading_day


"""
If running for the first time, you will need to set up
env variables for alpaca api access. For paper trading
and testing it should look like:

    PAPER_API_ENDPOINT='paper-api.alpaca.markets'
    PAPER_API_KEY_ID='kjhasdkjahsdjkashdjkasdh'
    PAPER_API_SECRET_KEY='kkjhadsjkhasdkjhasdkjashd'

Run main script with:
    $ python3 script_controller.py

Will default run in "force test" mode to skip certain
Account checks that fail when paper trading
"""

## TODO MOVE THE API KEYS STUFF TO BE DETERMINED BY THE
## CLI ARGS!!!! DO IT!!!!

async def main() -> int:
    # TODO add richer test params
    test_param = convert_cli_args()


    print(test_param)
    if (test_param != "test"):
        if not is_trading_day():
            return 1

    acc = AlpacaAccount(api_key, secret_key, paper_trading)

    # if (test_param != "test"):
    #     if not acc.can_trade():
    #         return 1

    # need to define more specific params
    data_params = DataProviderParams()

    all_data = await gen_data(acc, data_params)

    # # Creating request object

    # init get data for model

    # run/create new model

    # backtest model for positive returns

    # check model for buy/no buy decision

    # validate order makes sense

    # exec order

    print("Successfully executed script -- bye bye")
    return 0


if __name__ == "__main__":
    api_key = config('PAPER_API_KEY_ID')
    secret_key = config('PAPER_API_SECRET_KEY')
    paper_trading = True ## TODO need to move these to a better scope determined by CLI args
    asyncio.run(main())
