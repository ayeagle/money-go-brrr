from core_script.class_alpaca_account import AlpacaAccount
import asyncio
from decouple import config
from data.data_provider import data_provider
from data.class_data_provider_params import DataProviderParams
from core_script.script_helpers import handle_cli_args, is_trading_day

from consts.data_type_enums import DataSourceFormat


api_key = config('PAPER_API_KEY_ID')
secret_key = config('PAPER_API_SECRET_KEY')


async def main() -> int:
    test_param = handle_cli_args()

    print("this is the test param")
    print(test_param)

    if (test_param != "force test"):
        if not is_trading_day():
            return 1

    acc = AlpacaAccount(api_key, secret_key)

    if (test_param != "force test"):
        if not acc.can_trade():
            return 1

    data_params = DataProviderParams()

    all_data = data_provider(acc, data_params)


    print(all_data)

    # Creating request object

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
