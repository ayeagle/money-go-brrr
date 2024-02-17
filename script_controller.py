import asyncio
from datetime import datetime


# maybe remove
import sys


from consts.consts import RunTypeParam, data_param_presets
from core_script.class_alpaca_account import AlpacaAccount
from core_script.cli_formatters import green
from core_script.script_helpers import (convert_cli_args, gen_preview_files,
                                        gen_prompt_confirm_data_params,
                                        is_trading_day, check_trade_readiness_param)
from data.data_classes import DataProviderParams
from data.data_provider import gen_data
from core_script.trading import exec_trade_decision
from trading_model.core_model import gen_run_core_model

"""
**********************************************************
If running for the first time, you will need to set up
env variables for alpaca api access. For paper trading
and testing it should look like:

    PAPER_API_ENDPOINT='paper-api.alpaca.markets'
    PAPER_API_KEY_ID='kjhasdkjahsdjkashdjkasdh'
    PAPER_API_SECRET_KEY='kkjhadsjkhasdkjhasdkjashd'

Run main script with:
    $ python3 script_controller.py {OPTIONAL_ARGS}

For list of run options:
    $ python3 script_controller.py help


Will default run in "test" mode to skip certain
Account checks that fail when paper trading
**********************************************************
"""


async def main(event_arg) -> int:

    check_trade_readiness_param()

    # TODO add richer test params
    run_type_param = convert_cli_args(event_arg)

    acc = AlpacaAccount(run_type_param)

    if (run_type_param in [
            RunTypeParam.FULL_TEST,
            RunTypeParam.PROD,
            RunTypeParam.PROD_DANGEROUS]):
        if not is_trading_day():
            return 1
        if not acc.can_trade():
            return 1

    # init get data for model

    # need to define more specific params passed maybe from CLI

    data_params = gen_prompt_confirm_data_params(
        acc, data_param_presets['default'])

    all_data = await gen_data(acc, data_params)

    if (acc.run_type_param == RunTypeParam.DOWNLOAD):
        ts = (datetime.now().strftime('%y_%m_%d'),
              datetime.now().strftime('%H:%M:%S'))
        gen_preview_files(
            data_params=data_params,
            data=all_data,
            should_download=True,
            ts=ts)
        print(green(
            'Data successfully downloaded. You can access it in the downloaded_data folder.'))
        return 0

    trade_decision_volume = await gen_run_core_model(data_params)

    await exec_trade_decision(acc, trade_decision_volume)

    # run/create new model

    # backtest model for positive returns

    # check model for buy/no buy decision

    # validate order makes sense

    # exec order

    print("Successfully executed script -- bye bye")
    return 0


if __name__ == "__main__":
    event_arg = None
    asyncio.run(main(event_arg))
