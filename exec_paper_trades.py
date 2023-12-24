from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus
from decouple import config
import asyncio



api_key = config('PAPER_API_KEY_ID')
secret_key = config('PAPER_API_SECRET_KEY')
print(api_key)
print(secret_key)

trading_client = TradingClient(api_key, secret_key, paper=True)


# async def main():


print('client setup')

# preparing market order
market_order_data = MarketOrderRequest(
    symbol="SPY",
    qty=0.1,
    side=OrderSide.BUY,
    time_in_force=TimeInForce.DAY
)
print('order built')
print(market_order_data)

# Market order
market_order = trading_client.submit_order(
    order_data=market_order_data
)
print(market_order)
print('order sent')

# Get the last 100 closed orders
get_orders_data = GetOrdersRequest(
    # status=QueryOrderStatus.CLOSED,
    limit=100,
    nested=True  # show nested multi-leg orders
)

orders = trading_client.get_orders(filter=get_orders_data)
# Process orders here
print(orders)


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
