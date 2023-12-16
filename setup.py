from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from decouple import config

api_key = config('PAPER_API_KEY_ID')
secret_key = config('PAPER_API_SECRET_KEY')

print("yay the script is running")
print(api_key)
print(secret_key)

trading_client = TradingClient(api_key, secret_key)


# Get our account information.
account = trading_client.get_account()

# Check if our account is restricted from trading.
if account.trading_blocked:
    print('Account is currently restricted from trading.')

# Check how much money we can use to open new positions.
print('${} is available as buying power.'.format(account.buying_power))

