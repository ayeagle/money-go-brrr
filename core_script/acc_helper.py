from alpaca.trading.client import TradingClient
from decouple import config

class AlpacaAccount:
    def __init__(self, api_key: str, secret_key: str):
        self.client = TradingClient(api_key, secret_key)
        self.account = self.client.get_account()

    # standard obj getters
    # no setters to avoid acc info corruption
    # there is no reason to modify acc info

    def get_account_blocked(self):
        return self.account.account_blocked

    def get_account_number(self):
        return self.account.account_number

    def get_buying_power(self):
        return float(self.account.buying_power)

    def get_cash(self):
        return float(self.account.cash)

    def get_created_at(self):
        return self.account.created_at

    def get_currency(self):
        return self.account.currency

    def get_crypto_status(self):
        return self.account.crypto_status

    def get_non_marginable_buying_power(self):
        return float(self.account.non_marginable_buying_power)

    def get_accrued_fees(self):
        return float(self.account.accrued_fees)

    def get_pending_transfer_in(self):
        return float(self.account.pending_transfer_in)

    def get_pending_transfer_out(self):
        return float(self.account.pending_transfer_out)

    def get_daytrade_count(self):
        return int(self.account.daytrade_count)

    def get_daytrading_buying_power(self):
        return float(self.account.daytrading_buying_power)

    def get_equity(self):
        return float(self.account.equity)

    def get_id(self):
        return self.account.id

    def get_initial_margin(self):
        return float(self.account.initial_margin)

    def get_last_equity(self):
        return float(self.account.last_equity)

    def get_last_maintenance_margin(self):
        return float(self.account.last_maintenance_margin)

    def get_long_market_value(self):
        return float(self.account.long_market_value)

    def get_maintenance_margin(self):
        return float(self.account.maintenance_margin)

    def get_multiplier(self):
        return int(self.account.multiplier)

    def get_pattern_day_trader(self):
        return self.account.pattern_day_trader

    def get_portfolio_value(self):
        return float(self.account.portfolio_value)

    def get_regt_buying_power(self):
        return float(self.account.regt_buying_power)

    def get_short_market_value(self):
        return float(self.account.short_market_value)

    def get_shorting_enabled(self):
        return self.account.shorting_enabled

    def get_sma(self):
        return float(self.account.sma)

    def get_status(self):
        return self.account.status

    def get_trade_suspended_by_user(self):
        return self.account.trade_suspended_by_user

    def get_trading_blocked(self):
        return self.account.trading_blocked

    def get_transfers_blocked(self):
        return self.account.transfers_blocked

    # custom helper functions

    def get_SAFE_cash_balance(self):
        return self.account.non_marginable_buying_power

    def can_trade(self):
        if not self.account.account_blocked:
            print("Cannot trade due to account being blocked")
            return False
        if self.account.status != "ACTIVE":
            print("Cannot trade due to account being inactive")
            return False
        if not self.account.trade_suspended_by_user:
            print("Cannot trade due to account being suspeneded by user")
            return False
        if not self.account.trading_blocked:
            print("Cannot trade due to trading being blocked on account")
            return False
        print("Can trade today")
        return True
