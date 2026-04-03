import unittest
import io
import sys
import pandas as pd

from jk2bt.core.strategy_base import (
    JQLogAdapter,
    log,
)


class TestLogAdapter(unittest.TestCase):
    def test_log_info(self):
        adapter = JQLogAdapter()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        adapter.info("test message")
        sys.stdout = sys.__stdout__
        self.assertIn("test message", captured_output.getvalue())

    def test_log_info_multiple_args(self):
        adapter = JQLogAdapter()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        adapter.info("buy", "600519.XSHG", 100)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("buy", output)
        self.assertIn("600519.XSHG", output)
        self.assertIn("100", output)

    def test_log_warn(self):
        adapter = JQLogAdapter()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        adapter.warn("warning message")
        sys.stdout = sys.__stdout__
        self.assertIn("[WARN]", captured_output.getvalue())

    def test_log_error(self):
        adapter = JQLogAdapter()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        adapter.error("error message")
        sys.stdout = sys.__stdout__
        self.assertIn("[ERROR]", captured_output.getvalue())

    def test_set_level(self):
        adapter = JQLogAdapter()
        adapter.set_level("order", "error")
        self.assertEqual(adapter._log_levels["order"], "error")

    def test_dataframe_format(self):
        adapter = JQLogAdapter()
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        captured_output = io.StringIO()
        sys.stdout = captured_output
        adapter.info("DataFrame:", df)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("DataFrame:", output)
        self.assertTrue(output.count("\n") >= 2)

    def test_series_format(self):
        adapter = JQLogAdapter()
        s = pd.Series([1, 2, 3], name="test")
        captured_output = io.StringIO()
        sys.stdout = captured_output
        adapter.info("Series:", s)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Series:", output)

    def test_kwargs(self):
        adapter = JQLogAdapter()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        adapter.info("message", key="value")
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("key=value", output)

    def test_global_log(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        log.info("global log test")
        sys.stdout = sys.__stdout__
        self.assertIn("global log test", captured_output.getvalue())


if __name__ == "__main__":
    unittest.main()
