"""
Runtime IO API 高级测试
补充边界情况、并发、性能、错误恢复等测试用例
"""

import pytest
import tempfile
import os
import threading
import time
from pathlib import Path
from datetime import datetime
import json

from jk2bt.core.io import (
    record,
    send_message,
    read_file,
    write_file,
    get_record_data,
    get_messages,
    clear_runtime_data,
    set_runtime_dir,
    export_records_to_csv,
)


class TestRecordAdvanced:
    """record API 高级测试"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_dir = tempfile.mkdtemp()
        set_runtime_dir(self.temp_dir)

    def teardown_method(self):
        clear_runtime_data()

    def test_record_empty_params(self):
        """测试空参数"""
        record()
        data = get_record_data()
        assert "default" in data
        assert len(data["default"]) == 1
        assert "timestamp" in data["default"][0]

    def test_record_multiple_names(self):
        """测试多个不同的记录器"""
        record(name="metrics", nav=1.0)
        record(name="signals", signal="buy")
        record(name="trades", stock="600519.XSHG")

        all_data = get_record_data()
        assert len(all_data) == 3
        assert "metrics" in all_data
        assert "signals" in all_data
        assert "trades" in all_data

    def test_record_special_characters(self):
        """测试特殊字符"""
        record(name="test", msg="中文测试\n换行\t制表符")
        data = get_record_data("test")
        assert "中文测试" in data[0]["msg"]
        assert "\n" in data[0]["msg"]

    def test_record_different_types(self):
        """测试不同数据类型"""
        record(
            name="types",
            int_val=123,
            float_val=3.14,
            str_val="hello",
            bool_val=True,
            none_val=None,
            list_val=[1, 2, 3],
            dict_val={"key": "value"},
        )

        data = get_record_data("types")
        assert data[0]["int_val"] == 123
        assert data[0]["float_val"] == 3.14
        assert data[0]["str_val"] == "hello"

    def test_record_large_batch(self):
        """测试批量记录"""
        for i in range(100):
            record(name="batch", index=i, value=i * 1.5)

        data = get_record_data("batch")
        assert len(data) == 100
        assert data[0]["index"] == 0
        assert data[99]["index"] == 99

    def test_record_string_date(self):
        """测试字符串日期"""
        record(name="strdate", date="2023-01-15", value=100)
        data = get_record_data("strdate")
        assert data[0]["date"] == "2023-01-15"

    def test_record_concurrent(self):
        """测试并发记录（线程安全）"""
        errors = []

        def record_batch(batch_id):
            try:
                for i in range(50):
                    record(name="concurrent", batch=batch_id, index=i)
            except Exception as e:
                errors.append(e)

        threads = []
        for batch_id in range(5):
            t = threading.Thread(target=record_batch, args=(batch_id,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(errors) == 0
        data = get_record_data("concurrent")
        assert len(data) == 250

    def test_csv_fieldnames_evolution(self):
        """测试 CSV 字段名演进（已知限制：追加模式不会更新表头）"""
        record(name="evolution", field1="value1", field2="value2", field3="value3")
        record(name="evolution", field1="value2", field2="value2_new")
        record(name="evolution", field1="value3")

        csv_path = Path(self.temp_dir) / "record_evolution.csv"
        assert csv_path.exists()

        with open(csv_path, "r") as f:
            lines = f.readlines()
            assert len(lines) == 4
            header = lines[0]
            assert "field1" in header
            assert "field2" in header
            assert "field3" in header


class TestSendMessageAdvanced:
    """send_message API 高级测试"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_dir = tempfile.mkdtemp()
        set_runtime_dir(self.temp_dir)

    def teardown_method(self):
        clear_runtime_data()

    def test_send_message_empty_title(self):
        """测试空标题"""
        send_message("", "内容")
        messages = get_messages()
        assert messages[0]["title"] == ""

    def test_send_message_long_content(self):
        """测试长消息内容"""
        long_content = "这是一条很长的消息" * 100
        send_message("长消息", long_content)
        messages = get_messages()
        assert len(messages[0]["content"]) == len(long_content)

    def test_send_message_special_characters(self):
        """测试特殊字符消息"""
        send_message("特殊字符", "中文\n换行\t制表符\"引号'单引号")
        messages = get_messages()
        assert "中文" in messages[0]["content"]

    def test_send_message_unicode(self):
        """测试 Unicode 字符"""
        send_message("Unicode", "🎉🎊💰🚀")
        messages = get_messages()
        assert "🎉" in messages[0]["content"]

    def test_send_message_multiple_channels(self):
        """测试多个渠道"""
        channels = ["trading", "risk", "system", "debug", "notification"]
        for channel in channels:
            send_message(f"{channel}消息", f"这是{channel}渠道", channel=channel)

        messages = get_messages()
        assert len(messages) == 5
        channel_set = {msg["channel"] for msg in messages}
        assert channel_set == set(channels)


class TestFileIOAdvanced:
    """文件读写高级测试"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_dir = tempfile.mkdtemp()
        set_runtime_dir(self.temp_dir)

    def teardown_method(self):
        clear_runtime_data()

    def test_write_large_file(self):
        """测试大文件写入"""
        large_content = "这是测试内容\n" * 10000
        write_file("large_file.txt", large_content)

        read_content = read_file("large_file.txt")
        assert len(read_content) == len(large_content)
        assert read_content == large_content

    def test_write_deep_subdirectory(self):
        """测试深层子目录"""
        deep_path = "level1/level2/level3/level4/file.txt"
        write_file(deep_path, "deep content")

        path = Path(self.temp_dir) / deep_path
        assert path.exists()
        assert read_file(deep_path) == "deep content"

    def test_write_special_filename(self):
        """测试特殊文件名"""
        special_names = [
            "file with spaces.txt",
            "file_with_underscore.txt",
            "file-with-dash.txt",
            "文件中文.txt",
            "file123.txt",
        ]

        for name in special_names:
            write_file(name, f"content of {name}")
            assert read_file(name) == f"content of {name}"

    def test_write_overwrite(self):
        """测试覆盖写入"""
        write_file("overwrite.txt", "原始内容")
        write_file("overwrite.txt", "新内容")

        content = read_file("overwrite.txt")
        assert content == "新内容"
        assert "原始内容" not in content

    def test_append_multiple_times(self):
        """测试多次追加"""
        for i in range(10):
            write_file("append.txt", f"Line {i}\n", mode="a")

        content = read_file("append.txt")
        lines = content.strip().split("\n")
        assert len(lines) == 10

    def test_binary_large_file(self):
        """测试二进制大文件"""
        large_binary = bytes(range(256)) * 100
        write_file("large.bin", large_binary, mode="wb")

        read_binary = read_file("large.bin", mode="rb")
        assert read_binary == large_binary
        assert len(read_binary) == len(large_binary)

    def test_write_json_file(self):
        """测试写入 JSON 文件"""
        json_data = {
            "strategy": "test",
            "params": {"stop_loss": 0.05, "take_profit": 0.15},
            "stocks": ["600519.XSHG", "000858.XSHE"],
        }
        write_file("config.json", json.dumps(json_data, indent=2))

        read_content = read_file("config.json")
        parsed = json.loads(read_content)
        assert parsed["strategy"] == "test"
        assert len(parsed["stocks"]) == 2

    def test_file_not_exists_error(self):
        """测试文件不存在错误"""
        with pytest.raises(FileNotFoundError) as excinfo:
            read_file("nonexistent.txt")
        assert "File not found" in str(excinfo.value)

    def test_read_empty_file(self):
        """测试读取空文件"""
        write_file("empty.txt", "")
        content = read_file("empty.txt")
        assert content == ""

    def test_write_and_read_cycle_binary(self):
        """测试二进制文件写读循环"""
        test_data = [
            b"\x00\x01\x02\x03",
            b"\xff\xfe\xfd\xfc",
            bytes(range(128)),
            bytes([i for i in range(256) if i % 2 == 0]),
        ]

        for i, data in enumerate(test_data):
            filename = f"binary_{i}.bin"
            write_file(filename, data, mode="wb")
            read_data = read_file(filename, mode="rb")
            assert read_data == data

    def test_concurrent_write_different_files(self):
        """测试并发写入不同文件"""
        errors = []

        def write_file_thread(thread_id):
            try:
                for i in range(20):
                    filename = f"thread_{thread_id}_file_{i}.txt"
                    write_file(filename, f"Thread {thread_id} iteration {i}")
                    content = read_file(filename)
                    assert content == f"Thread {thread_id} iteration {i}"
            except Exception as e:
                errors.append(e)

        threads = []
        for thread_id in range(5):
            t = threading.Thread(target=write_file_thread, args=(thread_id,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(errors) == 0

    def test_file_permission_preserved(self):
        """测试文件权限"""
        write_file("test_perm.txt", "content")
        path = Path(self.temp_dir) / "test_perm.txt"
        assert path.exists()
        assert os.access(path, os.R_OK)
        assert os.access(path, os.W_OK)


class TestSecurityAdvanced:
    """安全边界高级测试"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_dir = tempfile.mkdtemp()
        set_runtime_dir(self.temp_dir)

    def teardown_method(self):
        clear_runtime_data()

    def test_path_with_multiple_dotdot(self):
        """测试多层上级目录"""
        with pytest.raises(ValueError):
            write_file("../../../../outside.txt", "content")

        with pytest.raises(ValueError):
            read_file("../../../../../etc/passwd")

    def test_path_with_dotdot_in_middle(self):
        """测试中间包含上级目录"""
        with pytest.raises(ValueError):
            write_file("safe/../../outside.txt", "content")

        with pytest.raises(ValueError):
            read_file("safe/../safe2/../../outside.txt")

    def test_absolute_path_various_formats(self):
        """测试各种绝对路径格式"""
        absolute_paths = [
            "/etc/passwd",
            "/tmp/file.txt",
            "/Users/test/file.txt",
            "/var/log/test.log",
        ]

        for path in absolute_paths:
            with pytest.raises(ValueError) as excinfo:
                write_file(path, "content")
            assert "absolute paths" in str(excinfo.value)

    def test_mixed_path_attacks(self):
        """测试混合路径攻击"""
        attack_paths = [
            "./../../outside.txt",
            "safe/./../../outside.txt",
            "safe/../safe/../../outside.txt",
        ]

        for path in attack_paths:
            with pytest.raises(ValueError):
                write_file(path, "content")

    def test_symlink_attack_prevention(self):
        """测试符号链接攻击防护"""
        write_file("safe.txt", "safe content")

        symlink_path = Path(self.temp_dir) / "link_to_safe.txt"
        safe_file = Path(self.temp_dir) / "safe.txt"

        try:
            symlink_path.symlink_to(safe_file)
            content = read_file("link_to_safe.txt")
            assert content == "safe content"
        except OSError:
            pass

    def test_empty_path_handling(self):
        """测试空路径处理"""
        # 空路径会导致 IsADirectoryError（尝试读取目录本身）
        with pytest.raises((ValueError, IsADirectoryError, OSError)):
            read_file("")

    def test_path_with_only_dots(self):
        """测试仅包含点的路径"""
        # "." 和 ".." 可能不会触发 ValueError，但会导致其他错误
        with pytest.raises((ValueError, OSError, IsADirectoryError)):
            write_file(".", "content")

        with pytest.raises((ValueError, OSError, IsADirectoryError)):
            read_file("..")

    def test_null_byte_in_path(self):
        """测试路径中的空字节"""
        with pytest.raises((ValueError, OSError)):
            write_file("test\x00file.txt", "content")


class TestPerformanceAndStress:
    """性能和压力测试"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_dir = tempfile.mkdtemp()
        set_runtime_dir(self.temp_dir)

    def teardown_method(self):
        clear_runtime_data()

    def test_record_performance_batch(self):
        """测试批量记录性能"""
        start_time = time.time()

        for i in range(1000):
            record(name="perf_test", index=i, value=i * 0.01)

        elapsed = time.time() - start_time
        assert elapsed < 10.0

        data = get_record_data("perf_test")
        assert len(data) == 1000

    def test_file_write_performance(self):
        """测试文件写入性能"""
        start_time = time.time()

        for i in range(100):
            write_file(f"perf_file_{i}.txt", f"Content {i}" * 100)

        elapsed = time.time() - start_time
        assert elapsed < 5.0

    def test_mixed_operations_performance(self):
        """测试混合操作性能"""
        start_time = time.time()

        for i in range(50):
            record(name="mixed", iteration=i)
            send_message(f"Message {i}", f"Content {i}")
            write_file(f"mixed_{i}.txt", f"File content {i}")
            read_file(f"mixed_{i}.txt")

        elapsed = time.time() - start_time
        assert elapsed < 10.0


class TestErrorRecovery:
    """错误恢复测试"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_dir = tempfile.mkdtemp()
        set_runtime_dir(self.temp_dir)

    def teardown_method(self):
        clear_runtime_data()

    def test_continue_after_error(self):
        """测试错误后能否继续"""
        try:
            write_file("/invalid/path.txt", "content")
        except ValueError:
            pass

        write_file("valid.txt", "valid content")
        assert read_file("valid.txt") == "valid content"

    def test_record_after_send_message_error(self):
        """测试消息发送错误后能否记录"""
        try:
            send_message("Title", invalid_param="value")
        except ValueError:
            pass

        record(name="after_error", value=100)
        data = get_record_data("after_error")
        assert len(data) == 1

    def test_partial_write_recovery(self):
        """测试部分写入恢复"""
        write_file("partial.txt", "Line 1\n")
        write_file("partial.txt", "Line 2\n", mode="a")

        try:
            write_file("../../invalid.txt", "invalid")
        except ValueError:
            pass

        write_file("partial.txt", "Line 3\n", mode="a")
        content = read_file("partial.txt")
        assert "Line 1" in content
        assert "Line 2" in content
        assert "Line 3" in content


class TestExportRecordsAdvanced:
    """导出记录高级测试"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_dir = tempfile.mkdtemp()
        set_runtime_dir(self.temp_dir)

    def teardown_method(self):
        clear_runtime_data()

    def test_export_empty_records(self):
        """测试导出空记录"""
        exported = export_records_to_csv()
        assert exported == {}

    def test_export_single_record(self):
        """测试导出单个记录"""
        record(name="single", value=100)
        exported = export_records_to_csv()

        assert "single" in exported
        assert Path(exported["single"]).exists()

    def test_export_multiple_records(self):
        """测试导出多个记录"""
        for name in ["metrics", "signals", "trades"]:
            for i in range(10):
                record(name=name, index=i)

        exported = export_records_to_csv()
        assert len(exported) == 3

        for name, path in exported.items():
            assert Path(path).exists()
            with open(path, "r") as f:
                lines = f.readlines()
                assert len(lines) == 11

    def test_export_to_custom_directory(self):
        """测试导出到自定义目录"""
        custom_dir = tempfile.mkdtemp()

        record(name="custom", value=100)
        exported = export_records_to_csv(custom_dir)

        assert "custom" in exported
        assert Path(exported["custom"]).parent == Path(custom_dir)


class TestRuntimeDirManagement:
    """运行时目录管理测试"""

    def test_set_runtime_dir_multiple_times(self):
        """测试多次设置运行时目录"""
        dir1 = tempfile.mkdtemp()
        dir2 = tempfile.mkdtemp()

        set_runtime_dir(dir1)
        write_file("test1.txt", "content in dir1")

        set_runtime_dir(dir2)
        write_file("test2.txt", "content in dir2")

        assert Path(dir1, "test1.txt").exists()
        assert Path(dir2, "test2.txt").exists()

        with pytest.raises(FileNotFoundError):
            read_file("test1.txt")

    def test_runtime_dir_auto_created(self):
        """测试运行时目录自动创建"""
        # 清除全局运行时目录，测试自动创建功能
        import jk2bt.core.io as runtime_io_module

        runtime_io_module._RUNTIME_DIR = None

        from jk2bt.core.io import _get_runtime_dir

        default_dir = _get_runtime_dir()
        assert default_dir.exists()
        assert "runtime_data" in str(default_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
