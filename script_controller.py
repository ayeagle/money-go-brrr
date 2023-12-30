from consts.consts import RunTypeParam
from core_script.class_alpaca_account import AlpacaAccount
import asyncio
from data.data_provider import gen_data
from data.data_classes import DataProviderParams
from core_script.script_helpers import convert_cli_args, gen_download_files, is_trading_day


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
    run_type_param = convert_cli_args()


    print(run_type_param)
    # if (run_type_param != "test"):
    #     if not is_trading_day():
    #         return 1

    # return 1
    acc = AlpacaAccount(run_type_param)


    # if (test_param != "test"):
    #     if not acc.can_trade():
    #         return 1

    # need to define more specific params
    data_params = DataProviderParams()

    all_data = await gen_data(acc, data_params)

    if(acc.run_type_param == RunTypeParam.DOWNLOAD):
        gen_download_files(acc, all_data)



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
    asyncio.run(main())
