from core_script.class_alpaca_account import AlpacaAccount
import asyncio
from decouple import config
from data.data_provider import gen_data
from data.class_data_provider_params import DataProviderParams
from core_script.script_helpers import handle_cli_args, is_trading_day

from consts.data_type_enums import DataSourceFormat


async def main() -> int:
    # TODO add richer test params
    test_param = handle_cli_args()

    if (test_param != "force test"):
        if not is_trading_day():
            return 1

    acc = AlpacaAccount(api_key, secret_key, paper_trading)

    if (test_param != "force test"):
        if not acc.can_trade():
            return 1

    # need to define more specific params
    data_params = DataProviderParams()

    all_data = await gen_data(acc, data_params)

    # print(all_data)
    # print('STOCK DATA')
    # print(all_data.diff_data_sources['stock_data'])
    # # print('orders DATA')
    # # print(all_data.diff_data_sources['orders_data'])

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
    paper_trading = True
    asyncio.run(main())
