import unittest

import numpy as np
import pandas as pd

from entry_overlay.factors import compute_15_ta_factors


class TestFactors(unittest.TestCase):
    def test_compute_15_ta_factors_shape_and_range(self):
        n = 300
        idx = pd.date_range("2026-01-01 09:30:00", periods=n, freq="min")
        close = 100 + np.cumsum(np.random.randn(n) * 0.1)
        bars = pd.DataFrame(
            {
                "open": close,
                "high": close + 0.2,
                "low": close - 0.2,
                "close": close,
                "volume": np.random.randint(100, 1000, n),
            },
            index=idx,
        )

        out = compute_15_ta_factors(bars)
        self.assertEqual(out.shape[1], 15)
        self.assertTrue(((out >= 0) & (out <= 1)).all().all())


if __name__ == "__main__":
    unittest.main()
