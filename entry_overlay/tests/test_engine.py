import unittest

import numpy as np
import pandas as pd

from entry_overlay.engine import EntryMode, EntryOverlayConfig, EntryOverlayEngine


class TestEngine(unittest.TestCase):
    def setUp(self):
        n = 280
        idx = pd.date_range("2026-01-01 09:30:00", periods=n, freq="min")
        close = 100 + np.cumsum(np.random.randn(n) * 0.05)
        self.bars = pd.DataFrame(
            {
                "open": close,
                "high": close + 0.1,
                "low": close - 0.1,
                "close": close,
                "volume": np.random.randint(100, 1000, n),
            },
            index=idx,
        )

    def test_rank_filter_mode_returns_boolean_by_threshold(self):
        conf = EntryOverlayConfig(mode=EntryMode.RANK_FILTER, min_score_to_buy=0.99)
        decision = EntryOverlayEngine(conf).decide(self.bars)
        self.assertFalse(decision.should_buy)

    def test_timing_only_always_buy(self):
        conf = EntryOverlayConfig(mode=EntryMode.TIMING_ONLY, min_score_to_buy=0.99)
        decision = EntryOverlayEngine(conf).decide(self.bars)
        self.assertTrue(decision.should_buy)
        self.assertGreaterEqual(len(decision.best_times), 1)


if __name__ == "__main__":
    unittest.main()
