import asyncio
import sys
import math


from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, QueryOrderStatus, TimeInForce
from alpaca.trading.requests import GetOrdersRequest, MarketOrderRequest
from decouple import config
from consts.consts import ParamCanTrade, commands, trade_param_presets
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data import StockBarsRequest, StockQuotesRequest
import datetime as dt

from core_script.class_alpaca_account import AlpacaAccount


async def gen_last_stock_price(
        acc: AlpacaAccount,
        stonk: str) -> float:

    hist_data_client = StockHistoricalDataClient(*acc.get_api_keys())

    params_payload = StockQuotesRequest(
        symbol_or_symbols=stonk,
        limit=10,
        start=dt.date.today() - dt.timedelta(days=5),
        end=dt.date.today(),
        feed='sip',
        sort='desc',
    )

    recent_prices = hist_data_client.get_stock_quotes(params_payload)

    return recent_prices[stonk][0].ask_price


async def normalize_order_request_by_qty(
        acc: AlpacaAccount,
        order: MarketOrderRequest,
        volume: float) -> MarketOrderRequest:

    if (volume > 0):
        order.qty = volume
    else:
        order.qty = volume * -1
        order.side = OrderSide.SELL

    last_price = await gen_last_stock_price(acc, order.symbol)

    available_balance = acc.get_SAFE_cash_balance()

    # TODO also need to get account position in stonk
    current_position = 0

    # check if can buy that amount w/o margin
    if (order.side == OrderSide.BUY):
        if (order.qty * last_price > available_balance):
            print("Adjusting buy order to not exceed available funds")
            order.qty = (available_balance / last_price) * .9
    else:
        if (order.qty * last_price > current_position):
            print("Adjusting sell order to not exceed current positon")
            order.qty = (current_position / last_price) * .9

    return order


async def normalize_order_request_by_asset(
        client: TradingClient,
        order: MarketOrderRequest) -> MarketOrderRequest:

    asset = client.get_asset(order.symbol)

    # check if fractionable
    if (not asset.fractionable):
        if (order.side == OrderSide.BUY):
            order.qty = math.floor(order.qty)
        else:
            order.qty = math.ceil(order.qty)

    return order


async def exec_trade_decision(
        acc: AlpacaAccount,
        volume: float) -> int:

    keys = acc.get_api_keys()

    trading_client = TradingClient(
        api_key=keys[0],
        secret_key=keys[1],
        paper=acc.paper_trading)

    order: MarketOrderRequest = trade_param_presets['default']

    order = await normalize_order_request_by_qty(acc, order, volume)
    order = await normalize_order_request_by_asset(trading_client, order)

    can_exec_trade = commands[acc.run_type_param.value]['can_trade']

    if (can_exec_trade == ParamCanTrade.CAN_NOT_TRADE_ANY):
        print('Exiting script without committing trade based on run params.')
        sys.exit(0)

    # market_order = trading_client.submit_order(
    #     order_data=order
    # )

    # print(market_order)

    return 1


# print('client setup')

# # preparing market order
# market_order_data = MarketOrderRequest(
#     symbol="SPY",
#     qty=0.1,
#     side=OrderSide.BUY,
#     time_in_force=TimeInForce.DAY
# )
# print('order built')
# print(market_order_data)

# # Market order
# market_order = trading_client.submit_order(
#     order_data=market_order_data
# )
# print(market_order)
# print('order sent')

# # Get the last 100 closed orders
# get_orders_data = GetOrdersRequest(
#     # status=QueryOrderStatus.CLOSED,
#     limit=100,
#     nested=True  # show nested multi-leg orders
# )

# orders = trading_client.get_orders(filter=get_orders_data)
# # Process orders here
# print(orders)


# if __name__ == "__main__":
#     asyncio.run(main())

# trading_client = TradingClient('api-key', 'secret-key', paper=True)


# # for num in range(1, 3):
# print('client setup')

# # preparing market order
# market_order_data = MarketOrderRequest(
#     symbol="SPY",
#     qty=0.1,
#     side=OrderSide.BUY,
#     time_in_force=TimeInForce.DAY
# )
# print('order built')


# # Market order
# market_order = trading_client.submit_order(
#     order_data=market_order_data
# )
# print('order sent')

# # print(num)


# # Get the last 100 closed orders
# get_orders_data = GetOrdersRequest(
#     status=QueryOrderStatus.CLOSED,
#     limit=100,
#     nested=True  # show nested multi-leg orders
# )

# trading_client.get_orders(filter=get_orders_data)
