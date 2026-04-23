import unittest

import numpy as np
import pandas as pd

from entry_overlay.data_sources import PandasAdapter
from entry_overlay.engine import EntryMode
from entry_overlay.offline import grid_search_params, run_event_backtest


class TestOffline(unittest.TestCase):
    def setUp(self):
        n = 900
        idx = pd.date_range("2026-01-05 09:30:00", periods=n, freq="min")
        close = 100 + np.cumsum(np.random.randn(n) * 0.03)
        self.bars = pd.DataFrame(
            {
                "code": ["000001.XSHE"] * n,
                "time": idx,
                "open": close,
                "high": close + 0.1,
                "low": close - 0.1,
                "close": close,
                "volume": np.random.randint(100, 1000, n),
            }
        )
        self.events = pd.DataFrame(
            {
                "code": ["000001.XSHE", "000001.XSHE"],
                "signal_time": [idx[30], idx[500]],
                "must_buy": [False, True],
            }
        )

    def test_run_event_backtest(self):
        rep = run_event_backtest(PandasAdapter(self.bars), self.events)
        self.assertGreaterEqual(rep.trade_count, 1)
        self.assertIn("ret", rep.summary.columns)

    def test_grid_search_params(self):
        res = grid_search_params(
            PandasAdapter(self.bars),
            self.events,
            profile_list=("general", "trend"),
            threshold_list=(0.55, 0.6),
            mode=EntryMode.RANK_FILTER,
        )
        self.assertFalse(res.empty)
        self.assertIn("sharpe_like", res.columns)


if __name__ == "__main__":
    unittest.main()
