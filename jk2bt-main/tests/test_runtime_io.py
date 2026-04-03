"""
测试运行时 IO API - 增强版
补充更多边界情况、异常处理、辅助函数测试
"""

import pytest
import os
import tempfile
import threading
import time
from datetime import datetime
from pathlib import Path

from jk2bt.core.io import (
    record,
    send_message,
    read_file,
    write_file,
    get_record_data,
    get_messages,
    clear_runtime_data,
    set_runtime_dir,
    _get_runtime_dir,
    export_records_to_csv,
)


class TestRecordEnhanced:
    """测试 record API - 增强版"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_dir = tempfile.mkdtemp()
        set_runtime_dir(self.temp_dir)

    def teardown_method(self):
        clear_runtime_data()

    def test_record_empty_kwargs(self):
        """测试空参数"""
        record()
        data = get_record_data()
        assert len(data["default"]) == 1
        assert data["default"][0]["timestamp"]

    def test_record_multiple_calls_same_name(self):
        """测试多次调用同一个 name"""
        for i in range(10):
            record(name="series", value=i)
        data = get_record_data("series")
        assert len(data) == 10
        assert [d["value"] for d in data] == list(range(10))

    def test_record_different_data_types(self):
        """测试不同数据类型"""
        record(
            name="types",
            int_val=100,
            float_val=3.14159,
            str_val="hello",
            bool_val=True,
            none_val=None,
        )
        data = get_record_data("types")
        assert data[0]["int_val"] == 100
        assert data[0]["float_val"] == 3.14159
        assert data[0]["str_val"] == "hello"
        assert data[0]["bool_val"] is True
        assert data[0]["none_val"] is None

    def test_record_special_characters(self):
        """测试特殊字符"""
        record(name="special", msg="中文测试\n换行\t制表符")
        data = get_record_data("special")
        assert "中文测试" in data[0]["msg"]
        assert "\n" in data[0]["msg"]

    def test_record_unicode(self):
        """测试 Unicode 字符"""
        record(name="unicode", msg="日本語テスト🎉")
        data = get_record_data("unicode")
        assert "日本語テスト" in data[0]["msg"]

    def test_record_string_date(self):
        """测试字符串形式的日期"""
        record(name="strdate", date="2023-01-15", value=100)
        data = get_record_data("strdate")
        assert data[0]["date"] == "2023-01-15"

    def test_record_large_volume(self):
        """测试大量数据"""
        for i in range(100):
            record(name="large", idx=i, value=i * 1.5)
        data = get_record_data("large")
        assert len(data) == 100

    def test_record_get_nonexistent_name(self):
        """测试获取不存在的记录名"""
        data = get_record_data("nonexistent")
        assert data == []

    def test_record_multiple_names(self):
        """测试多个不同的记录名"""
        record(name="alpha", val=1.0)
        record(name="beta", val=2.0)
        record(name="gamma", val=3.0)

        all_data = get_record_data()
        assert "alpha" in all_data
        assert "beta" in all_data
        assert "gamma" in all_data
        assert len(all_data["alpha"]) == 1
        assert len(all_data["beta"]) == 1
        assert len(all_data["gamma"]) == 1

    def test_record_positional_args(self):
        """测试位置参数"""
        record(1, 2, 3, name="args")
        data = get_record_data("args")
        assert data[0]["arg_0"] == 1
        assert data[0]["arg_1"] == 2
        assert data[0]["arg_2"] == 3

    def test_record_csv_header_written_once(self):
        """测试 CSV header 只写入一次"""
        record(name="header_test", val=1)
        record(name="header_test", val=2)

        csv_path = Path(self.temp_dir) / "record_header_test.csv"
        with open(csv_path, "r") as f:
            lines = f.readlines()

        header_count = sum(1 for line in lines if "timestamp" in line)
        assert header_count == 1


class TestSendMessageEnhanced:
    """测试 send_message API - 增强版"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_dir = tempfile.mkdtemp()
        set_runtime_dir(self.temp_dir)

    def teardown_method(self):
        clear_runtime_data()

    def test_send_message_empty_title(self):
        """测试空标题"""
        send_message(title="", content="内容")
        messages = get_messages()
        assert messages[0]["title"] == ""

    def test_send_message_empty_content(self):
        """测试空内容"""
        send_message(title="标题", content="")
        messages = get_messages()
        assert messages[0]["content"] == ""

    def test_send_message_long_content(self):
        """测试长内容"""
        long_content = "A" * 10000
        send_message(title="长消息", content=long_content)
        messages = get_messages()
        assert len(messages[0]["content"]) == 10000

    def test_send_message_special_characters(self):
        """测试特殊字符"""
        send_message(title="特殊字符", content='测试\n换行\t制表符"双引号')
        messages = get_messages()
        assert "\n" in messages[0]["content"]
        assert "\t" in messages[0]["content"]

    def test_send_message_unicode(self):
        """测试 Unicode"""
        send_message(title="🎉庆祝", content="日本語テスト")
        messages = get_messages()
        assert "🎉" in messages[0]["title"]
        assert "日本語テスト" in messages[0]["content"]

    def test_send_message_multiple_calls(self):
        """测试多次调用"""
        for i in range(20):
            send_message(title=f"消息{i}", content=f"内容{i}")
        messages = get_messages()
        assert len(messages) == 20

    def test_send_message_multiple_channels(self):
        """测试多个渠道"""
        send_message(title="交易", content="买入", channel="trading")
        send_message(title="风控", content="警告", channel="risk")
        send_message(title="系统", content="启动", channel="system")

        messages = get_messages()
        channels = [m["channel"] for m in messages]
        assert "trading" in channels
        assert "risk" in channels
        assert "system" in channels

    def test_send_message_log_append(self):
        """测试日志追加"""
        send_message(title="消息1", content="内容1")
        send_message(title="消息2", content="内容2")

        log_path = Path(self.temp_dir) / "messages.log"
        with open(log_path, "r") as f:
            lines = f.readlines()

        assert len(lines) == 2


class TestReadFileEnhanced:
    """测试 read_file API - 增强版"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_dir = tempfile.mkdtemp()
        set_runtime_dir(self.temp_dir)

    def teardown_method(self):
        clear_runtime_data()

    def test_read_empty_file(self):
        """测试空文件"""
        write_file("empty.txt", "")
        content = read_file("empty.txt")
        assert content == ""

    def test_read_large_file(self):
        """测试大文件"""
        large_content = "X" * 100000
        write_file("large.txt", large_content)
        content = read_file("large.txt")
        assert len(content) == 100000

    def test_read_file_with_path_spaces(self):
        """测试路径包含空格"""
        write_file("path with spaces/file.txt", "内容")
        content = read_file("path with spaces/file.txt")
        assert content == "内容"

    def test_read_deep_nested_path(self):
        """测试深层嵌套路径"""
        write_file("a/b/c/d/e/file.txt", "深层文件")
        content = read_file("a/b/c/d/e/file.txt")
        assert content == "深层文件"

    def test_read_chinese_filename(self):
        """测试中文文件名"""
        write_file("中文文件.txt", "中文内容")
        content = read_file("中文文件.txt")
        assert content == "中文内容"

    def test_read_unicode_filename(self):
        """测试 Unicode 文件名"""
        write_file("🎉test.txt", "unicode filename")
        content = read_file("🎉test.txt")
        assert content == "unicode filename"

    def test_read_file_multiple_times(self):
        """测试多次读取同一文件"""
        write_file("repeat.txt", "内容")
        for _ in range(10):
            content = read_file("repeat.txt")
            assert content == "内容"

    def test_read_binary_empty(self):
        """测试二进制空文件"""
        write_file("empty.bin", b"", mode="wb")
        content = read_file("empty.bin", mode="rb")
        assert content == b""

    def test_read_binary_large(self):
        """测试二进制大文件"""
        large_binary = bytes(range(256)) * 1000
        write_file("large.bin", large_binary, mode="wb")
        content = read_file("large.bin", mode="rb")
        assert len(content) == 256 * 1000


class TestWriteFileEnhanced:
    """测试 write_file API - 增强版"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_dir = tempfile.mkdtemp()
        set_runtime_dir(self.temp_dir)

    def teardown_method(self):
        clear_runtime_data()

    def test_write_empty_content(self):
        """测试空内容"""
        write_file("empty.txt", "")
        content = read_file("empty.txt")
        assert content == ""

    def test_write_large_content(self):
        """测试大内容"""
        large = "Y" * 100000
        write_file("large.txt", large)
        content = read_file("large.txt")
        assert len(content) == 100000

    def test_write_path_with_spaces(self):
        """测试路径包含空格"""
        write_file("dir with spaces/file name.txt", "内容")
        path = Path(self.temp_dir) / "dir with spaces" / "file name.txt"
        assert path.exists()

    def test_write_chinese_path(self):
        """测试中文路径"""
        write_file("中文目录/中文文件.txt", "中文内容")
        path = Path(self.temp_dir) / "中文目录" / "中文文件.txt"
        assert path.exists()

    def test_write_deep_nested_path(self):
        """测试深层路径"""
        write_file("level1/level2/level3/level4/file.txt", "deep")
        path = (
            Path(self.temp_dir) / "level1" / "level2" / "level3" / "level4" / "file.txt"
        )
        assert path.exists()

    def test_write_overwrite(self):
        """测试覆盖写入"""
        write_file("overwrite.txt", "第一次")
        write_file("overwrite.txt", "第二次")
        content = read_file("overwrite.txt")
        assert content == "第二次"

    def test_write_binary_append(self):
        """测试二进制追加"""
        write_file("bin_append.bin", b"\x00\x01", mode="wb")
        write_file("bin_append.bin", b"\x02\x03", mode="ab")
        content = read_file("bin_append.bin", mode="rb")
        assert content == b"\x00\x01\x02\x03"

    def test_write_multiple_files(self):
        """测试写入多个文件"""
        for i in range(20):
            write_file(f"file_{i}.txt", f"内容{i}")

        for i in range(20):
            content = read_file(f"file_{i}.txt")
            assert content == f"内容{i}"


class TestAuxiliaryFunctions:
    """测试辅助函数"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_dir = tempfile.mkdtemp()
        set_runtime_dir(self.temp_dir)

    def teardown_method(self):
        clear_runtime_data()

    def test_get_runtime_dir(self):
        """测试获取运行时目录"""
        dir_path = _get_runtime_dir()
        # macOS 上 /var 是 /private/var 的符号链接，需要 resolve
        assert dir_path.resolve() == Path(self.temp_dir).resolve()
        assert dir_path.exists()

    def test_set_runtime_dir(self):
        """测试设置运行时目录"""
        new_dir = tempfile.mkdtemp()
        set_runtime_dir(new_dir)

        write_file("test.txt", "内容")
        assert Path(new_dir).joinpath("test.txt").exists()

    def test_clear_runtime_data(self):
        """测试清空数据"""
        record(name="test", val=1)
        send_message(title="test")

        assert len(get_record_data()) > 0
        assert len(get_messages()) > 0

        clear_runtime_data()

        assert len(get_record_data()) == 0
        assert len(get_messages()) == 0

    def test_export_records_to_csv(self):
        """测试导出记录"""
        record(name="export1", val=1)
        record(name="export2", val=2)

        export_dir = tempfile.mkdtemp()
        exported = export_records_to_csv(export_dir)

        assert "export1" in exported
        assert "export2" in exported
        assert Path(exported["export1"]).exists()
        assert Path(exported["export2"]).exists()

    def test_export_empty_records(self):
        """测试导出空记录"""
        export_dir = tempfile.mkdtemp()
        exported = export_records_to_csv(export_dir)
        assert exported == {}


class TestConcurrency:
    """测试并发场景"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_dir = tempfile.mkdtemp()
        set_runtime_dir(self.temp_dir)

    def teardown_method(self):
        clear_runtime_data()

    def test_record_concurrent(self):
        """测试并发 record"""

        def worker(i):
            for j in range(50):
                record(name="concurrent", thread=i, count=j)

        threads = []
        for i in range(5):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        data = get_record_data("concurrent")
        assert len(data) == 250  # 5 threads * 50 records

    def test_send_message_concurrent(self):
        """测试并发 send_message"""

        def worker(i):
            for j in range(30):
                send_message(title=f"T{i}", content=f"M{j}")

        threads = []
        for i in range(3):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        messages = get_messages()
        assert len(messages) == 90  # 3 threads * 30 messages

    def test_write_file_concurrent_different_files(self):
        """测试并发写入不同文件"""

        def worker(i):
            write_file(f"thread_{i}.txt", f"content from thread {i}")

        threads = []
        for i in range(10):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        for i in range(10):
            content = read_file(f"thread_{i}.txt")
            assert f"thread {i}" in content


class TestPathInjectionEnhanced:
    """测试路径注入攻击 - 增强版"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_dir = tempfile.mkdtemp()
        set_runtime_dir(self.temp_dir)

    def teardown_method(self):
        clear_runtime_data()

    def test_path_with_hidden_dotdot(self):
        """测试隐藏的 .. 路径"""
        with pytest.raises(ValueError):
            read_file("normal/../../escape.txt")

        with pytest.raises(ValueError):
            write_file("normal/../escape.txt", "content")

    def test_path_with_encoded_dotdot(self):
        """测试编码的 .. 路径"""
        # %2e%2e 是 .. 的 URL 编码，但在这里直接测试
        with pytest.raises(ValueError):
            read_file("..%2e/secrets.txt")

    def test_path_with_backslash(self):
        """测试反斜杠路径（Windows 风格）"""
        # 在 macOS/Linux 上，反斜杠会被当作文件名的一部分
        write_file("test\\file.txt", "content")
        content = read_file("test\\file.txt")
        assert content == "content"

    def test_path_with_null_byte(self):
        """测试空字节注入"""
        with pytest.raises((ValueError, OSError)):
            read_file("test\x00.txt")

    def test_empty_path(self):
        """测试空路径"""
        # 空路径会尝试读取 runtime_dir 本身（目录）
        with pytest.raises((ValueError, IsADirectoryError, FileNotFoundError)):
            read_file("")

    def test_path_starting_with_slash(self):
        """测试以斜杠开头的路径"""
        with pytest.raises(ValueError):
            read_file("/tmp/test.txt")


class TestSymlinkEscape:
    """测试符号链接逃逸"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_dir = tempfile.mkdtemp()
        set_runtime_dir(self.temp_dir)

    def teardown_method(self):
        clear_runtime_data()

    def test_symlink_escape(self):
        """测试符号链接逃逸"""
        external_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
        external_file.write("external secret")
        external_file.close()

        symlink_path = None
        try:
            symlink_path = Path(self.temp_dir) / "link"
            symlink_path.symlink_to(external_file.name)

            with pytest.raises(ValueError):
                read_file("link")
        finally:
            if symlink_path and symlink_path.exists():
                symlink_path.unlink()
            os.unlink(external_file.name)


class TestErrorMessages:
    """测试错误消息质量"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_dir = tempfile.mkdtemp()
        set_runtime_dir(self.temp_dir)

    def teardown_method(self):
        clear_runtime_data()

    def test_read_file_error_message_clear(self):
        """测试读取文件错误消息清晰"""
        with pytest.raises(FileNotFoundError) as excinfo:
            read_file("nonexistent.txt")

        error_msg = str(excinfo.value)
        assert "File not found" in error_msg
        assert "nonexistent.txt" in error_msg

    def test_write_file_mode_error_message(self):
        """测试写入模式错误消息"""
        with pytest.raises(ValueError) as excinfo:
            write_file("test.txt", "content", mode="invalid")

        error_msg = str(excinfo.value)
        assert "'w', 'a', 'wb', or 'ab'" in error_msg
        assert "'invalid'" in error_msg

    def test_send_message_param_error_message(self):
        """测试 send_message 参数错误消息"""
        with pytest.raises(ValueError) as excinfo:
            send_message("title", invalid_param="value")

        error_msg = str(excinfo.value)
        assert "invalid_param" in error_msg

    def test_absolute_path_error_message(self):
        """测试绝对路径错误消息"""
        with pytest.raises(ValueError) as excinfo:
            read_file("/absolute/path.txt")

        error_msg = str(excinfo.value)
        assert "absolute paths" in error_msg

    def test_parent_dir_error_message(self):
        """测试上级目录错误消息"""
        with pytest.raises(ValueError) as excinfo:
            write_file("../parent.txt", "content")

        error_msg = str(excinfo.value)
        assert "parent directory" in error_msg


class TestRealWorldScenarios:
    """测试真实使用场景"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_dir = tempfile.mkdtemp()
        set_runtime_dir(self.temp_dir)

    def teardown_method(self):
        clear_runtime_data()

    def test_strategy_signal_recording(self):
        """模拟策略信号记录"""
        signals = [
            {"date": "2023-01-01", "signal": "buy", "price": 100.0},
            {"date": "2023-01-02", "signal": "hold", "price": 101.5},
            {"date": "2023-01-03", "signal": "sell", "price": 105.0},
        ]

        for sig in signals:
            record(name="signals", **sig)

        data = get_record_data("signals")
        assert len(data) == 3
        assert data[0]["signal"] == "buy"
        assert data[2]["signal"] == "sell"

    def test_strategy_config_write_read(self):
        """模拟策略配置写入读取"""
        config = """
{
    "strategy_name": "momentum",
    "params": {
        "lookback": 20,
        "threshold": 0.02
    }
}
"""
        write_file("config/strategy_config.json", config)
        read_config = read_file("config/strategy_config.json")
        assert "momentum" in read_config
        assert "lookback" in read_config

    def test_trade_log_append(self):
        """模拟交易日志追加"""
        trades = [
            "2023-01-01 09:30:00 BUY 600519.XSHG 100@100.5",
            "2023-01-01 10:00:00 SELL 600519.XSHG 100@101.0",
            "2023-01-02 09:35:00 BUY 000858.XSHE 200@50.0",
        ]

        for trade in trades:
            write_file("logs/trades.log", trade + "\n", mode="a")

        log_content = read_file("logs/trades.log")
        lines = log_content.strip().split("\n")  # strip() 移除末尾换行
        assert len(lines) == 3
        assert "600519.XSHG" in log_content

    def test_risk_alert_messages(self):
        """模拟风控消息"""
        alerts = [
            ("仓位警告", "总仓位达到 85%", "risk"),
            ("止损触发", "个股触及止损线", "trading"),
            ("系统通知", "数据更新完成", "system"),
        ]

        for title, content, channel in alerts:
            send_message(title=title, content=content, channel=channel)

        messages = get_messages()
        assert len(messages) == 3

        risk_msgs = [m for m in messages if m["channel"] == "risk"]
        assert len(risk_msgs) == 1

    def test_daily_report_generation(self):
        """模拟日报生成"""
        for i in range(5):
            record(
                name="daily_report",
                date=datetime(2023, 1, i + 1),
                nav=1000 + i * 10,
                pnl=i * 10,
                drawdown=-i * 0.5,
            )

        exported = export_records_to_csv()
        assert "daily_report" in exported

        csv_content = read_file(Path(exported["daily_report"]).name)
        assert "nav" in csv_content
        assert "pnl" in csv_content


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
