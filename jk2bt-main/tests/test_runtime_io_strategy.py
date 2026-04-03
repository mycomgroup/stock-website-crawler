"""
测试 runtime IO 在策略运行器中的集成
"""

import pytest
import tempfile
import os
from pathlib import Path

from jk2bt.core.io import (
    record,
    send_message,
    read_file,
    write_file,
    set_runtime_dir,
    clear_runtime_data,
    get_record_data,
    get_messages,
)


class TestRuntimeIOInStrategy:
    """测试 runtime IO 在策略场景中的使用"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_dir = tempfile.mkdtemp()
        set_runtime_dir(self.temp_dir)

    def teardown_method(self):
        clear_runtime_data()

    def test_strategy_can_record_signals(self):
        record(name="signals", signal="buy", stock="600519.XSHG", price=100.5)
        record(name="signals", signal="sell", stock="600519.XSHG", price=102.0)

        data = get_record_data("signals")
        assert len(data) == 2
        assert data[0]["signal"] == "buy"
        assert data[1]["signal"] == "sell"

        csv_path = Path(self.temp_dir) / "record_signals.csv"
        assert csv_path.exists()
        with open(csv_path) as f:
            content = f.read()
            assert "buy" in content
            assert "sell" in content

    def test_strategy_can_send_notifications(self):
        send_message("风险警告", "仓位超过限制", channel="risk_management")
        send_message("交易完成", "买入成功", channel="trading_log")

        messages = get_messages()
        assert len(messages) == 2
        assert messages[0]["channel"] == "risk_management"
        assert messages[1]["channel"] == "trading_log"

        msg_log = Path(self.temp_dir) / "messages.log"
        assert msg_log.exists()

    def test_strategy_can_write_and_read_config(self):
        config = {
            "strategy_name": "test_strategy",
            "max_position": 0.8,
            "stop_loss": 0.05,
        }
        config_str = str(config)
        write_file("strategy_config.txt", config_str)

        read_content = read_file("strategy_config.txt")
        assert "strategy_name" in read_content
        assert "max_position" in read_content

    def test_strategy_can_log_trades(self):
        trade_log = "2023-01-01: BUY 600519.XSHG 100@100.5\n"
        write_file("trades.txt", trade_log)

        trade_log2 = "2023-01-02: SELL 600519.XSHG 100@102.0\n"
        write_file("trades.txt", trade_log2, mode="a")

        content = read_file("trades.txt")
        assert "BUY" in content
        assert "SELL" in content

    def test_runtime_dir_defaults_to_repo(self):
        from jk2bt.core.io import (
            _get_runtime_dir,
            _RUNTIME_DIR,
        )
        import src.runtime_io as runtime_io_module

        original_runtime_dir = runtime_io_module._RUNTIME_DIR
        runtime_io_module._RUNTIME_DIR = None

        try:
            default_dir = _get_runtime_dir()
            assert "runtime_data" in str(default_dir)

            repo_root = Path(__file__).parent.parent.parent
            assert str(default_dir).startswith(str(repo_root))
        finally:
            runtime_io_module._RUNTIME_DIR = original_runtime_dir

    def test_invalid_path_rejected_in_strategy_context(self):
        with pytest.raises(ValueError) as excinfo:
            write_file("/etc/outside.txt", "invalid")
        assert "absolute paths" in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            read_file("../../outside.txt")
        assert "parent directory" in str(excinfo.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
