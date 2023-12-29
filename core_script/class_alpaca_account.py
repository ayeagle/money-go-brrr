from alpaca.trading.client import TradingClient
from decouple import config
from consts.consts import RunTypeParam

paper_api_key = config('PAPER_API_KEY_ID')
paper_secret_key = config('PAPER_API_SECRET_KEY')

real_api_key = config('API_KEY_ID')
real_secret_key = config('API_SECRET_KEY')


class AlpacaAccount:
    def __init__(self, run_type_param: RunTypeParam):
        self.run_type_param = run_type_param
        if (run_type_param == RunTypeParam.PROD or run_type_param == RunTypeParam.PROD_DANGEROUS):
            self.keys = (real_api_key, real_secret_key)        
            self._paper_trading = False
        else:
            self.keys = (paper_api_key, paper_secret_key)
            self._paper_trading = True

        self.client = TradingClient(*self.keys)
        self._account = self.client.get_account()

    # standard obj getters
    # no setters to avoid acc info corruption
    # there is no reason to modify acc info
    @property
    def account_blocked(self):
        return self._account.account_blocked

    @property
    def account_number(self):
        return self._account.account_number

    @property
    def buying_power(self):
        return float(self._account.buying_power)

    @property
    def cash(self):
        return float(self._account.cash)

    @property
    def created_at(self):
        return self._account.created_at

    @property
    def currency(self):
        return self._account.currency

    @property
    def crypto_status(self):
        return self._account.crypto_status

    @property
    def non_marginable_buying_power(self):
        return float(self._account.non_marginable_buying_power)

    @property
    def accrued_fees(self):
        return float(self._account.accrued_fees)

    @property
    def pending_transfer_in(self):
        return float(self._account.pending_transfer_in)

    @property
    def pending_transfer_out(self):
        return float(self._account.pending_transfer_out)

    @property
    def daytrade_count(self):
        return int(self._account.daytrade_count)

    @property
    def daytrading_buying_power(self):
        return float(self._account.daytrading_buying_power)

    @property
    def equity(self):
        return float(self._account.equity)

    @property
    def id(self):
        return self._account.id

    @property
    def initial_margin(self):
        return float(self._account.initial_margin)

    @property
    def last_equity(self):
        return float(self._account.last_equity)

    @property
    def last_maintenance_margin(self):
        return float(self._account.last_maintenance_margin)

    @property
    def long_market_value(self):
        return float(self._account.long_market_value)

    @property
    def maintenance_margin(self):
        return float(self._account.maintenance_margin)

    @property
    def multiplier(self):
        return int(self._account.multiplier)

    @property
    def pattern_day_trader(self):
        return self._account.pattern_day_trader

    @property
    def portfolio_value(self):
        return float(self._account.portfolio_value)

    @property
    def regt_buying_power(self):
        return float(self._account.regt_buying_power)

    @property
    def short_market_value(self):
        return float(self._account.short_market_value)

    @property
    def shorting_enabled(self):
        return self._account.shorting_enabled

    @property
    def sma(self):
        return float(self._account.sma)

    @property
    def status(self):
        return self._account.status

    @property
    def trade_suspended_by_user(self):
        return self._account.trade_suspended_by_user

    @property
    def trading_blocked(self):
        return self._account.trading_blocked

    @property
    def transfers_blocked(self):
        return self._account.transfers_blocked

    # custom helper functions

    @property
    def paper_trading(self):
        return self._paper_trading

    def get_api_keys(self):
        return self.keys

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
