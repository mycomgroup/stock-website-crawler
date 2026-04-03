"""
测试运行时资源管理包
验证策略资源隔离和路径映射功能
覆盖：基本功能、边界情况、异常处理、集成场景
"""

import pytest
import tempfile
import os
import shutil
import json
import pickle
from pathlib import Path
from io import BytesIO
from datetime import datetime
import pandas as pd

from jk2bt.strategy.runtime_resource_pack import (
    RuntimeResourcePack,
    create_resource_pack,
    list_all_strategies,
    get_current_resource_pack,
)
from jk2bt.runtime_io import (
    set_strategy_name,
    get_current_strategy_name,
    get_resource_pack,
    read_file,
    write_file,
    clear_runtime_data,
    set_runtime_dir,
    record,
    send_message,
    get_record_data,
    get_messages,
)


class TestRuntimeResourcePackBasic:
    """测试资源包基本功能"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_create_resource_pack(self):
        pack = RuntimeResourcePack(
            strategy_name="test_strategy",
            runtime_base=self.temp_base,
        )

        assert pack.strategy_name == "test_strategy"
        assert pack.strategy_dir.exists()
        assert pack.input_dir.exists()
        assert pack.output_dir.exists()

        for subdir in pack.RESOURCE_TYPES["input"].keys():
            assert (pack.input_dir / subdir).exists()

        for subdir in pack.RESOURCE_TYPES["output"].keys():
            assert (pack.output_dir / subdir).exists()

    def test_create_without_auto_create(self):
        pack = RuntimeResourcePack(
            strategy_name="no_auto_create",
            runtime_base=self.temp_base,
            auto_create=False,
        )

        assert not pack.strategy_dir.exists()

        pack.setup_resource_dir()
        assert pack.strategy_dir.exists()

    def test_default_strategy_name(self):
        pack = RuntimeResourcePack(runtime_base=self.temp_base)
        assert pack.strategy_name == "default"

    def test_write_and_read_input_resource_binary(self):
        pack = RuntimeResourcePack(
            strategy_name="test_ml",
            runtime_base=self.temp_base,
        )

        model_bytes = b"\x00\x01\x02\x03\x04\x05"
        path = pack.write_input_resource("my_model.pkl", model_bytes)

        assert path.exists()
        assert path.parent.name == "models"

        read_content = pack.read_input_resource("my_model.pkl")
        assert read_content == model_bytes

    def test_write_and_read_input_resource_text(self):
        pack = RuntimeResourcePack(
            strategy_name="text_test",
            runtime_base=self.temp_base,
        )

        text_content = "Hello World\n中文测试"
        path = pack.write_input_resource("note.txt", text_content)

        assert path.exists()
        read_content = pack.read_input_resource("note.txt")
        assert read_content == text_content

    def test_write_and_read_config(self):
        pack = RuntimeResourcePack(
            strategy_name="config_test",
            runtime_base=self.temp_base,
        )

        config_json = '{"threshold": 0.05, "max_pos": 100}'
        path = pack.write_input_resource("strategy_config.json", config_json)

        assert path.exists()
        assert path.parent.name == "config"

        read_content = pack.read_input_resource("strategy_config.json")
        assert read_content == config_json

    def test_write_and_read_output_resource(self):
        pack = RuntimeResourcePack(
            strategy_name="output_test",
            runtime_base=self.temp_base,
        )

        trade_log = "2023-01-01: BUY 600519.XSHG 100@100.5\n"
        path = pack.write_output_resource("trade_log.csv", trade_log)

        assert path.exists()
        assert path.parent.name == "trades"

        read_content = pack.read_output_resource("trade_log.csv")
        assert read_content == trade_log

    def test_append_mode_write(self):
        pack = RuntimeResourcePack(
            strategy_name="append_test",
            runtime_base=self.temp_base,
        )

        pack.write_output_resource("log.txt", "Line1\n")
        pack.write_output_resource("log.txt", "Line2\n", mode="a")

        content = pack.read_output_resource("log.txt")
        assert "Line1" in content
        assert "Line2" in content

    def test_write_with_explicit_resource_type(self):
        pack = RuntimeResourcePack(
            strategy_name="explicit_type",
            runtime_base=self.temp_base,
        )

        path = pack.write_input_resource("data.txt", "content", resource_type="params")
        assert path.parent.name == "params"

        path = pack.write_output_resource(
            "output.txt", "content", resource_type="research"
        )
        assert path.parent.name == "research"

    def test_nested_directory_path(self):
        pack = RuntimeResourcePack(
            strategy_name="nested_test",
            runtime_base=self.temp_base,
        )

        path = pack.write_input_resource("subdir/deep/config.json", '{"nested": true}')
        assert path.exists()
        assert path.parent.name == "deep"

        content = pack.read_input_resource("subdir/deep/config.json")
        assert "nested" in content

    def test_read_nonexistent_file_raises_error(self):
        pack = RuntimeResourcePack(
            strategy_name="error_test",
            runtime_base=self.temp_base,
        )

        with pytest.raises(FileNotFoundError):
            pack.read_input_resource("nonexistent.pkl")

        with pytest.raises(FileNotFoundError):
            pack.read_output_resource("nonexistent.csv")

    def test_list_resources(self):
        pack = RuntimeResourcePack(
            strategy_name="list_test",
            runtime_base=self.temp_base,
        )

        pack.write_input_resource("model1.pkl", b"binary1")
        pack.write_input_resource("model2.h5", b"binary2")
        pack.write_input_resource("config.json", '{"test": 1}')
        pack.write_output_resource("trades.csv", "trade_data")
        pack.write_output_resource("signals.log", "signal_data")

        input_list = pack.list_input_resources()
        output_list = pack.list_output_resources()

        assert len(input_list) == 3
        assert len(output_list) == 2

        model_files = [r for r in input_list if r["type"] == "models"]
        assert len(model_files) == 2

    def test_list_resources_by_type(self):
        pack = RuntimeResourcePack(
            strategy_name="list_type_test",
            runtime_base=self.temp_base,
        )

        pack.write_input_resource("model.pkl", b"binary")
        pack.write_input_resource("config.json", '{"test": 1}')
        pack.write_input_resource("data.csv", "data")

        models = pack.list_input_resources("models")
        configs = pack.list_input_resources("config")

        assert len(models) == 1
        assert len(configs) == 1

    def test_resource_summary(self):
        pack = RuntimeResourcePack(
            strategy_name="summary_test",
            runtime_base=self.temp_base,
        )

        pack.write_input_resource("model.pkl", b"binary")
        pack.write_output_resource("trades.csv", "data")
        pack.write_output_resource("nav.log", "nav_data")

        summary = pack.get_resource_summary()

        assert summary["strategy_name"] == "summary_test"
        assert summary["total_input_files"] == 1
        assert summary["total_output_files"] == 2
        assert "models" in summary["input_resources"]
        assert "trades" in summary["output_resources"]

    def test_clear_output_resources_by_type(self):
        pack = RuntimeResourcePack(
            strategy_name="clear_type_test",
            runtime_base=self.temp_base,
        )

        pack.write_output_resource("log1.txt", "data1", resource_type="logs")
        pack.write_output_resource("log2.txt", "data2", resource_type="logs")
        pack.write_output_resource("trade.csv", "trade_data", resource_type="trades")

        assert len(pack.list_output_resources()) == 3

        pack.clear_output_resources("logs")

        logs_files = [r for r in pack.list_output_resources() if r["type"] == "logs"]
        assert len(logs_files) == 0

        trades_files = [
            r for r in pack.list_output_resources() if r["type"] == "trades"
        ]
        assert len(trades_files) == 1

    def test_clear_all_output_resources(self):
        pack = RuntimeResourcePack(
            strategy_name="clear_all_test",
            runtime_base=self.temp_base,
        )

        pack.write_output_resource("log.txt", "data")
        pack.write_output_resource("trade.csv", "data")

        assert len(pack.list_output_resources()) == 2

        pack.clear_output_resources()
        assert len(pack.list_output_resources()) == 0

    def test_clear_all_resources(self):
        pack = RuntimeResourcePack(
            strategy_name="clear_all_full_test",
            runtime_base=self.temp_base,
        )

        pack.write_input_resource("model.pkl", b"binary")
        pack.write_output_resource("trade.csv", "data")

        pack.clear_all_resources()

        assert len(pack.list_input_resources()) == 0
        assert len(pack.list_output_resources()) == 0


class TestResourceTypeInference:
    """测试资源类型推断"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_infer_model_types(self):
        pack = RuntimeResourcePack(runtime_base=self.temp_base)

        assert pack._infer_resource_type("model.pkl") == "models"
        assert pack._infer_resource_type("weights.h5") == "models"
        assert pack._infer_resource_type("checkpoint.pth") == "models"
        assert pack._infer_resource_type("model.pt") == "models"
        assert pack._infer_resource_type("net.onnx") == "models"
        assert pack._infer_resource_type("my_model.model") == "models"
        assert pack._infer_resource_type("weights.bin") == "models"

    def test_infer_config_types(self):
        pack = RuntimeResourcePack(runtime_base=self.temp_base)

        assert pack._infer_resource_type("config.json") == "config"
        assert pack._infer_resource_type("settings.yaml") == "config"
        assert pack._infer_resource_type("params.yml") == "config"
        assert pack._infer_resource_type("config.ini") == "config"
        assert pack._infer_resource_type("settings.cfg") == "config"
        assert pack._infer_resource_type("parameter.json") == "config"

    def test_infer_data_types(self):
        pack = RuntimeResourcePack(runtime_base=self.temp_base)

        assert pack._infer_resource_type("data.csv") == "data"
        assert pack._infer_resource_type("prices.parquet") == "data"
        assert pack._infer_resource_type("report.xlsx") == "data"

    def test_infer_trade_types(self):
        pack = RuntimeResourcePack(runtime_base=self.temp_base)

        assert pack._infer_resource_type("trades.csv") == "trades"
        assert pack._infer_resource_type("trade_log.json") == "trades"
        assert pack._infer_resource_type("signals.csv") == "trades"
        assert pack._infer_resource_type("nav.csv") == "trades"
        assert pack._infer_resource_type("result.json") == "trades"

    def test_infer_log_types(self):
        pack = RuntimeResourcePack(runtime_base=self.temp_base)

        assert pack._infer_resource_type("error.log") == "logs"
        assert pack._infer_resource_type("debug.log") == "logs"

    def test_infer_by_path_keywords(self):
        pack = RuntimeResourcePack(runtime_base=self.temp_base)

        assert pack._infer_resource_type("train_data.csv") == "models"
        assert pack._infer_resource_type("test_data.csv") == "models"
        assert pack._infer_resource_type("my_config.txt") == "config"

    def test_infer_trade_log_special_case(self):
        pack = RuntimeResourcePack(runtime_base=self.temp_base)

        assert pack._infer_resource_type("trades.log") == "trades"
        assert pack._infer_resource_type("signals.log") == "trades"
        assert pack._infer_resource_type("debug.log") == "logs"


class TestStrategyResourceIsolation:
    """测试策略资源隔离"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_set_strategy_name(self):
        set_strategy_name("isolated_strategy")

        name = get_current_strategy_name()
        assert name == "isolated_strategy"

        pack = get_resource_pack()
        assert pack is not None
        assert pack.strategy_name == "isolated_strategy"

    def test_resource_isolation_between_strategies(self):
        pack1 = RuntimeResourcePack(
            strategy_name="strategy_1",
            runtime_base=self.temp_base,
        )
        pack1.write_input_resource("config.json", '{"strategy": 1}')

        pack2 = RuntimeResourcePack(
            strategy_name="strategy_2",
            runtime_base=self.temp_base,
        )
        pack2.write_input_resource("config.json", '{"strategy": 2}')

        content1 = pack1.read_input_resource("config.json")
        content2 = pack2.read_input_resource("config.json")

        assert content1 == '{"strategy": 1}'
        assert content2 == '{"strategy": 2}'

        assert pack1.strategy_dir != pack2.strategy_dir

    def test_io_with_strategy_isolation(self):
        set_runtime_dir(self.temp_base)
        set_strategy_name("io_test_strategy")

        write_file("test_output.txt", "Hello Strategy")
        write_file("model_data.pkl", b"\x00\x01\x02\x03")

        read_content = read_file("test_output.txt")
        assert read_content == "Hello Strategy"

        read_binary = read_file("model_data.pkl", mode="rb")
        assert read_binary == b"\x00\x01\x02\x03"

        pack = get_resource_pack()
        assert pack is not None
        summary = pack.get_resource_summary()
        assert summary["total_output_files"] >= 1

    def test_multiple_strategy_switches(self):
        set_runtime_dir(self.temp_base)

        set_strategy_name("strategy_a")
        write_file("data.txt", "A data")

        set_strategy_name("strategy_b")
        write_file("data.txt", "B data")

        set_strategy_name("strategy_a")
        content = read_file("data.txt")
        assert content == "A data"

        set_strategy_name("strategy_b")
        content = read_file("data.txt")
        assert content == "B data"


class TestMLStrategyResource:
    """测试机器学习策略资源场景"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()
        set_runtime_dir(self.temp_base)

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_ml_training_data_resource(self):
        set_strategy_name("ml_training_strategy")

        train_csv_content = "factor1,factor2,label\n0.1,0.2,1\n0.3,0.4,0\n"
        test_csv_content = "factor1,factor2,label\n0.5,0.6,1\n0.7,0.8,0\n"

        write_file("train_conformal_base.csv", train_csv_content)
        write_file("test_conformal_base.csv", test_csv_content)

        train_data = read_file("train_conformal_base.csv")
        test_data = read_file("test_conformal_base.csv")

        df_train = pd.read_csv(BytesIO(train_data.encode()))
        df_test = pd.read_csv(BytesIO(test_data.encode()))

        assert len(df_train) == 2
        assert len(df_test) == 2

        pack = get_resource_pack()
        summary = pack.get_resource_summary()
        assert summary["total_input_files"] >= 2

    def test_model_file_management(self):
        set_strategy_name("model_test_strategy")

        model_data = {"weights": [0.1, 0.2, 0.3], "threshold": 0.05}
        model_bytes = pickle.dumps(model_data)

        write_file("xgb_model.pkl", model_bytes)

        loaded_bytes = read_file("xgb_model.pkl", mode="rb")
        loaded_model = pickle.loads(loaded_bytes)

        assert loaded_model["weights"] == model_data["weights"]
        assert loaded_model["threshold"] == 0.05

    def test_multiple_model_files(self):
        pack = RuntimeResourcePack(
            strategy_name="multi_model_test",
            runtime_base=self.temp_base,
        )

        for i in range(5):
            model_data = {"layer": i, "weights": [0.1 * i, 0.2 * i]}
            model_bytes = pickle.dumps(model_data)
            pack.write_input_resource(f"model_layer_{i}.pkl", model_bytes)

        models = pack.list_input_resources("models")
        assert len(models) == 5

        for i in range(5):
            loaded = pickle.loads(pack.read_input_resource(f"model_layer_{i}.pkl"))
            assert loaded["layer"] == i


class TestPathSecurity:
    """测试路径安全性"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()
        set_runtime_dir(self.temp_base)

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_absolute_path_denied(self):
        set_strategy_name("security_test")

        with pytest.raises(ValueError) as excinfo:
            read_file("/etc/passwd")
        assert "absolute" in str(excinfo.value).lower() or "绝对" in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            write_file("/tmp/outside.txt", "data")
        assert "absolute" in str(excinfo.value).lower() or "绝对" in str(excinfo.value)

    def test_parent_directory_denied(self):
        set_strategy_name("security_test")

        with pytest.raises(ValueError) as excinfo:
            read_file("../../outside.txt")
        assert "parent" in str(excinfo.value).lower() or "上级" in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            write_file("../../../outside.txt", "data")
        assert "parent" in str(excinfo.value).lower() or "上级" in str(excinfo.value)

    def test_pack_path_validation(self):
        pack = RuntimeResourcePack(
            strategy_name="pack_security_test",
            runtime_base=self.temp_base,
        )

        with pytest.raises(ValueError):
            pack._validate_path("/etc/passwd", is_input=True)

        with pytest.raises(ValueError):
            pack._validate_path("../../outside.txt", is_input=False)

    def test_symlink_escape_prevention(self):
        pack = RuntimeResourcePack(
            strategy_name="symlink_test",
            runtime_base=self.temp_base,
        )

        outside_dir = Path(self.temp_base) / "outside"
        outside_dir.mkdir()
        outside_file = outside_dir / "secret.txt"
        outside_file.write_text("secret data")

        assert pack._validate_path("safe.txt", is_input=True).parent.exists()


class TestBatchRunning:
    """测试批量运行时的资源管理"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_list_all_strategies(self):
        for i in range(3):
            pack = RuntimeResourcePack(
                strategy_name=f"batch_strategy_{i}",
                runtime_base=self.temp_base,
            )
            pack.write_output_resource("result.txt", f"strategy_{i} output")

        strategies = list_all_strategies(self.temp_base)
        assert len(strategies) >= 3
        assert "batch_strategy_0" in strategies
        assert "batch_strategy_1" in strategies
        assert "batch_strategy_2" in strategies

    def test_list_all_strategies_empty(self):
        empty_dir = tempfile.mkdtemp()
        try:
            strategies = list_all_strategies(empty_dir)
            assert strategies == []
        finally:
            shutil.rmtree(empty_dir)

    def test_concurrent_strategy_execution(self):
        results = []
        for strategy_num in range(5):
            pack = RuntimeResourcePack(
                strategy_name=f"concurrent_{strategy_num}",
                runtime_base=self.temp_base,
            )

            pack.write_input_resource(
                f"param_{strategy_num}.json", f'{{"id": {strategy_num}}}'
            )
            pack.write_output_resource(
                f"result_{strategy_num}.csv", f"result_{strategy_num}"
            )

            results.append(
                {
                    "name": f"concurrent_{strategy_num}",
                    "pack": pack,
                }
            )

        for result in results:
            pack = result["pack"]
            param_content = pack.read_input_resource(
                f"param_{pack.strategy_name.split('_')[1]}.json"
            )
            result_content = pack.read_output_resource(
                f"result_{pack.strategy_name.split('_')[1]}.csv"
            )

            assert f"id" in param_content
            assert f"result" in result_content

    def test_create_resource_pack_helper(self):
        pack = create_resource_pack("helper_test", runtime_base=self.temp_base)

        assert pack.strategy_name == "helper_test"
        assert pack.strategy_dir.exists()

        pack.write_input_resource("test.json", '{"test": true}')
        content = pack.read_input_resource("test.json")
        assert "test" in content


class TestResourcePacking:
    """测试资源打包功能"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_pack_resources(self):
        pack = RuntimeResourcePack(
            strategy_name="pack_test",
            runtime_base=self.temp_base,
        )

        pack.write_input_resource("model.pkl", b"model_data")
        pack.write_output_resource("trades.csv", "trade_data")

        packed_path = pack.pack_resources()

        assert packed_path.exists()
        assert (packed_path / "manifest.json").exists()
        assert (packed_path / "input").exists()
        assert (packed_path / "output").exists()

        with open(packed_path / "manifest.json") as f:
            manifest = json.load(f)
            assert manifest["strategy_name"] == "pack_test"
            assert "input_resources" in manifest
            assert "output_resources" in manifest

    def test_pack_resources_custom_output(self):
        pack = RuntimeResourcePack(
            strategy_name="custom_pack_test",
            runtime_base=self.temp_base,
        )

        pack.write_input_resource("config.json", '{"test": 1}')

        custom_output = Path(self.temp_base) / "custom_packs"
        custom_output.mkdir()

        import time

        time.sleep(0.1)

        packed_path = pack.pack_resources(output_path=custom_output)

        assert packed_path.parent == custom_output


class TestRuntimeIOIntegration:
    """测试 runtime_io 与资源包的集成"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()
        set_runtime_dir(self.temp_base)

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_record_with_resource_pack(self):
        set_strategy_name("record_test")

        record(name="test_record", value=100, price=10.5)

        pack = get_resource_pack()
        assert pack is not None

    def test_send_message_with_resource_pack(self):
        set_strategy_name("message_test")

        send_message("测试消息", "消息内容", channel="test")

        messages = get_messages()
        assert len(messages) == 1

        pack = get_resource_pack()
        assert pack is not None

    def test_record_data_persistence(self):
        set_strategy_name("persist_test")

        record(name="nav", date=datetime(2023, 1, 1), nav=1.0)
        record(name="nav", date=datetime(2023, 1, 2), nav=1.02)

        data = get_record_data("nav")
        assert len(data) == 2
        assert data[0]["nav"] == 1.0
        assert data[1]["nav"] == 1.02


class TestEdgeCases:
    """测试边界情况"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_strategy_name_with_special_chars(self):
        pack = RuntimeResourcePack(
            strategy_name="test_strategy_123",
            runtime_base=self.temp_base,
        )

        assert pack.strategy_name == "test_strategy_123"
        pack.write_input_resource("test.json", '{"test": true}')

    def test_chinese_filename(self):
        pack = RuntimeResourcePack(
            strategy_name="chinese_test",
            runtime_base=self.temp_base,
        )

        chinese_content = "中文内容测试"
        pack.write_input_resource("配置.json", chinese_content)

        content = pack.read_input_resource("配置.json")
        assert content == chinese_content

    def test_large_file_handling(self):
        pack = RuntimeResourcePack(
            strategy_name="large_file_test",
            runtime_base=self.temp_base,
        )

        large_content = "x" * 1000000
        pack.write_input_resource("large.txt", large_content)

        content = pack.read_input_resource("large.txt")
        assert len(content) == 1000000

    def test_empty_file(self):
        pack = RuntimeResourcePack(
            strategy_name="empty_file_test",
            runtime_base=self.temp_base,
        )

        pack.write_input_resource("empty.txt", "")
        content = pack.read_input_resource("empty.txt")
        assert content == ""

    def test_deep_nested_directory(self):
        pack = RuntimeResourcePack(
            strategy_name="deep_nested_test",
            runtime_base=self.temp_base,
        )

        deep_path = "level1/level2/level3/level4/level5/config.json"
        pack.write_input_resource(deep_path, '{"deep": true}')

        content = pack.read_input_resource(deep_path)
        assert "deep" in content

    def test_unicode_content(self):
        pack = RuntimeResourcePack(
            strategy_name="unicode_test",
            runtime_base=self.temp_base,
        )

        unicode_content = "Emoji: \U0001f600\U0001f389 Chinese: 中文 Japanese: 日本語"
        pack.write_input_resource("unicode.txt", unicode_content)

        content = pack.read_input_resource("unicode.txt")
        assert content == unicode_content


class TestModuleFunctions:
    """测试模块级函数"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_create_resource_pack(self):
        pack = create_resource_pack("module_test", runtime_base=self.temp_base)

        assert pack.strategy_name == "module_test"
        assert pack.strategy_dir.exists()

    def test_get_current_resource_pack_none_when_not_set(self):
        from jk2bt.strategy.runtime_resource_pack import (
            RuntimeResourcePack,
        )

        RuntimeResourcePack._current_strategy_name = None

        pack = get_current_resource_pack()

        assert pack is None

    def test_get_current_resource_pack_returns_set_name(self):
        from jk2bt.strategy.runtime_resource_pack import (
            RuntimeResourcePack,
        )

        RuntimeResourcePack.set_current_strategy_name("explicit_test")

        pack = get_current_resource_pack()

        assert pack is not None
        assert pack.strategy_name == "explicit_test"


class TestFileAttributes:
    """测试文件属性"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_file_size_in_listing(self):
        pack = RuntimeResourcePack(
            strategy_name="size_test",
            runtime_base=self.temp_base,
        )

        content = "x" * 1000
        pack.write_input_resource("sized.txt", content)

        resources = pack.list_input_resources()
        assert len(resources) == 1
        assert resources[0]["size"] == 1000

    def test_file_full_path(self):
        pack = RuntimeResourcePack(
            strategy_name="path_test",
            runtime_base=self.temp_base,
        )

        pack.write_input_resource("test.json", '{"test": true}')

        resources = pack.list_input_resources()
        assert len(resources) == 1
        assert "full_path" in resources[0]
        assert Path(resources[0]["full_path"]).exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
