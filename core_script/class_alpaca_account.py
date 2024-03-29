import sys

from alpaca.trading.client import TradingClient
from decouple import config, UndefinedValueError

import consts.cli_messages as mess
from consts.consts import RunTypeParam
from core_script.cli_formatters import bold, formatWarningMessage, red


class AlpacaAccount:
    def __init__(self, run_type_param: RunTypeParam):
        self.run_type_param = run_type_param

        try:
            if (run_type_param in [RunTypeParam.PROD, RunTypeParam.PROD_DANGEROUS]):
                self.keys = (config('API_KEY_ID'), config('API_SECRET_KEY'))
                self._paper_trading = False
            else:
                self.keys = (config('PAPER_API_KEY_ID'),
                             config('PAPER_API_SECRET_KEY'))
                self._paper_trading = True
        except UndefinedValueError as e:
            missing_variable = str(e).split()[0]  # Extract the missing variable from the error message
            thing=f"""The required param ${missing_variable} 
                is missing in the .env file.\n"""

            formatWarningMessage(thing  + "\n" + mess.no_api_keys_message)
            sys.exit(0)

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
        return float(self._account.non_marginable_buying_power)

    def account_is_able_to_trade(self):
        if not self._account.account_blocked:
            print("Cannot trade due to account being blocked")
            return False
        if self._account.status != "ACTIVE":
            print("Cannot trade due to account being inactive")
            return False
        if not self._account.trade_suspended_by_user:
            print("Cannot trade due to account being suspeneded by user")
            return False
        if not self._account.trading_blocked:
            print("Cannot trade due to trading being blocked on account")
            return False
        print("Can trade today")
        return True
