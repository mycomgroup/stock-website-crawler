# -*- coding: utf-8 -*-
import json
import traceback
import base64
from datetime import datetime
import pandas as pd

# The JS script will replace these
_encoded_code = "{STRATEGY_CODE_BASE64}"
START_DATE = "{START_DATE}"
END_DATE = "{END_DATE}"
CAPITAL = {CAPITAL}

STRATEGY_CODE = base64.b64decode(_encoded_code).decode('utf-8')

# --- Mock Framework ---
class MockContext:
    def __init__(self, current_dt, portfolio_cash=100000.0):
        self.current_dt = current_dt
        self.portfolio = MockPortfolio(portfolio_cash)
        self.run_params = {"start_date": None, "end_date": None, "frequency": "daily", "benchmark": "000300.XSHG"}

class MockPortfolio:
    def __init__(self, cash=100000.0):
        self.available_cash = cash
        self.positions = {}
        self.total_value = cash

# Instead of Mocking all functions like order_target...
# If the strategy uses order_target... wait, if it uses order_value, get_price, etc, 
# Mocking all JoinQuant Trade APIs in a Notebook is ALOT of code. 

# WAIT! In JoinQuant Research/Notebook, there is NO built-in backtest? 
# If they don't have backtest, how do people backtest? Maybe there is a way to trigger backtest API but not from `jqresearch`.
