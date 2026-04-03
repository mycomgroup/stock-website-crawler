"""
资源依赖落地综合测试
测试资源包管理、文件IO、路径映射、安全限制等全面功能
"""

import pytest
import tempfile
import os
import shutil
import json
import pickle
import threading
import time
from pathlib import Path
from io import BytesIO, StringIO
from datetime import datetime
import pandas as pd
import numpy as np

from jk2bt.strategy.runtime_resource_pack import (
    RuntimeResourcePack,
    create_resource_pack,
    get_current_resource_pack,
    list_all_strategies,
)
from jk2bt.runtime_io import (
    set_strategy_name,
    get_current_strategy_name,
    get_resource_pack,
    read_file,
    write_file,
    set_runtime_dir,
    clear_runtime_data,
    record,
    send_message,
    get_record_data,
    get_messages,
    export_records_to_csv,
)


class TestResourcePackAdvancedFeatures:
    """测试资源包高级功能"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_pack_resources_with_manifest(self):
        pack = RuntimeResourcePack(
            strategy_name="pack_test",
            runtime_base=self.temp_base,
        )
        pack.write_input_resource("model.pkl", b"model_data")
        pack.write_input_resource("config.json", '{"param": 1}')
        pack.write_output_resource("trades.csv", "trade_log")
        pack.write_output_resource("result.json", '{"profit": 100}')

        pack_path = pack.pack_resources()

        assert pack_path.exists()
        assert (pack_path / "manifest.json").exists()

        with open(pack_path / "manifest.json", "r") as f:
            manifest = json.load(f)
        assert manifest["strategy_name"] == "pack_test"
        assert len(manifest["input_resources"]) == 2
        assert len(manifest["output_resources"]) == 2

    def test_resource_pack_timestamp(self):
        pack1 = RuntimeResourcePack(
            strategy_name="time_test_1", runtime_base=self.temp_base
        )
        time.sleep(0.1)
        pack2 = RuntimeResourcePack(
            strategy_name="time_test_2", runtime_base=self.temp_base
        )

        assert pack1.strategy_dir != pack2.strategy_dir

        all_strategies = list_all_strategies(self.temp_base)
        assert len(all_strategies) >= 2

    def test_resource_type_inference_comprehensive(self):
        pack = RuntimeResourcePack(
            strategy_name="inference_test", runtime_base=self.temp_base
        )

        test_cases = [
            ("model.pkl", "models"),
            ("trained_model.h5", "models"),
            ("xgb_model.onnx", "models"),
            ("config.json", "config"),
            ("params.yaml", "config"),
            ("settings.ini", "config"),
            ("data.csv", "data"),
            ("features.parquet", "data"),
            ("trade_log.csv", "trades"),
            (
                "signals.json",
                "trades",
            ),  # signals contains "signal" keyword, mapped to trades
            ("error.log", "logs"),
            ("output.log", "logs"),  # .log extension maps to logs
        ]

        for filepath, expected_type in test_cases:
            inferred = pack._infer_resource_type(filepath)
            assert inferred == expected_type, (
                f"{filepath} should be {expected_type}, got {inferred}"
            )

    def test_path_validation_edge_cases(self):
        pack = RuntimeResourcePack(
            strategy_name="validation_test", runtime_base=self.temp_base
        )

        valid_paths = [
            "data/file.csv",
            "models/subdir/model.pkl",
            "config/params.json",
            "output/result.txt",
        ]

        for path in valid_paths:
            validated = pack._validate_path(path, is_input=True)
            assert str(validated).startswith(str(pack.input_dir.resolve()))

        invalid_paths = [
            "/etc/passwd",
            "../../outside.txt",
            "../escape.txt",
            "subdir/../../escape.txt",
        ]

        for path in invalid_paths:
            with pytest.raises(ValueError):
                pack._validate_path(path, is_input=True)

    def test_resource_directory_auto_creation(self):
        pack = RuntimeResourcePack(
            strategy_name="auto_create_test", runtime_base=self.temp_base
        )

        pack.write_input_resource(
            "deep/nested/path/model.pkl", b"data", resource_type="data"
        )

        nested_path = pack.input_dir / "data" / "deep" / "nested" / "path" / "model.pkl"
        assert nested_path.exists()

        read_data = pack.read_input_resource(
            "deep/nested/path/model.pkl", resource_type="data"
        )
        assert read_data == b"data"


class TestIOWithResourcePack:
    """测试RuntimeIO与ResourcePack的集成"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()
        set_runtime_dir(self.temp_base)

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_auto_path_mapping_input(self):
        set_strategy_name("auto_map_input")

        model_content = b"\x00\x01\x02\x03"
        write_file("model.pkl", model_content, mode="wb")

        read_content = read_file("model.pkl", mode="rb")
        assert read_content == model_content

        pack = get_resource_pack()
        input_resources = pack.list_input_resources()
        model_files = [r for r in input_resources if "model" in r["path"]]
        assert len(model_files) >= 1

    def test_auto_path_mapping_output(self):
        set_strategy_name("auto_map_output")

        trade_content = "date,stock,action\n2023-01-01,600519,BUY\n"
        write_file("trade_log.csv", trade_content)

        read_content = read_file("trade_log.csv")
        assert read_content == trade_content

        pack = get_resource_pack()
        output_resources = pack.list_output_resources()
        trade_files = [r for r in output_resources if "trade" in r["path"]]
        assert len(trade_files) >= 1

    def test_path_mapping_config_files(self):
        set_strategy_name("config_test")

        config_data = {"threshold": 0.05, "max_pos": 100}
        write_file("strategy_config.json", json.dumps(config_data))

        read_content = read_file("strategy_config.json")
        parsed = json.loads(read_content)
        assert parsed["threshold"] == 0.05

        pack = get_resource_pack()
        input_resources = pack.list_input_resources()
        config_files = [r for r in input_resources if "config" in r["path"]]
        assert len(config_files) >= 1

    def test_fallback_to_direct_path(self):
        set_strategy_name("fallback_test")

        write_file("direct_file.txt", "direct content")

        read_content = read_file("direct_file.txt")
        assert read_content == "direct content"


class TestCSVResourceHandling:
    """测试CSV资源文件处理"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()
        set_runtime_dir(self.temp_base)
        set_strategy_name("csv_test")

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_csv_write_and_parse(self):
        df = pd.DataFrame(
            {
                "factor1": np.random.randn(100),
                "factor2": np.random.randn(100),
                "label": np.random.randint(0, 2, 100),
            }
        )

        write_file("train_data.csv", df.to_csv(index=False))

        csv_content = read_file("train_data.csv")
        df_loaded = pd.read_csv(BytesIO(csv_content.encode()))

        assert len(df_loaded) == 100
        assert list(df_loaded.columns) == ["factor1", "factor2", "label"]

    def test_csv_with_special_characters(self):
        df = pd.DataFrame(
            {
                "stock_code": ["600519.XSHG", "000001.XSHE", "300001.XSHE"],
                "name": ["贵州茅台", "平安银行", "特锐德"],
                "price": [1800.0, 15.5, 25.0],
            }
        )

        write_file("stock_list.csv", df.to_csv(index=False))

        csv_content = read_file("stock_list.csv")
        df_loaded = pd.read_csv(BytesIO(csv_content.encode()))

        assert df_loaded.iloc[0]["name"] == "贵州茅台"
        assert df_loaded.iloc[1]["stock_code"] == "000001.XSHE"

    def test_csv_append_mode(self):
        header = "date,price,volume\n"
        write_file("price_data.csv", header)

        row1 = "2023-01-01,100.5,1000\n"
        write_file("price_data.csv", row1, mode="a")

        row2 = "2023-01-02,101.0,1200\n"
        write_file("price_data.csv", row2, mode="a")

        csv_content = read_file("price_data.csv")
        df = pd.read_csv(BytesIO(csv_content.encode()))

        assert len(df) == 2
        assert df.iloc[0]["price"] == 100.5
        assert df.iloc[1]["volume"] == 1200

    def test_large_csv_file(self):
        large_df = pd.DataFrame(
            {
                "id": range(10000),
                "value": np.random.randn(10000),
                "category": np.random.choice(["A", "B", "C"], 10000),
            }
        )

        write_file("large_data.csv", large_df.to_csv(index=False))

        csv_content = read_file("large_data.csv")
        df_loaded = pd.read_csv(BytesIO(csv_content.encode()))

        assert len(df_loaded) == 10000


class TestJSONResourceHandling:
    """测试JSON资源文件处理"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()
        set_runtime_dir(self.temp_base)
        set_strategy_name("json_test")

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_json_config_write_and_parse(self):
        config = {
            "strategy_name": "ml_strategy",
            "parameters": {
                "fold": 5,
                "learning_rate": 0.1,
                "max_depth": 5,
            },
            "backtest": {
                "start": "2020-01-01",
                "end": "2023-12-31",
            },
        }

        write_file("strategy_config.json", json.dumps(config, indent=2))

        json_content = read_file("strategy_config.json")
        config_loaded = json.loads(json_content)

        assert config_loaded["parameters"]["fold"] == 5
        assert config_loaded["backtest"]["start"] == "2020-01-01"

    def test_json_with_nested_structure(self):
        nested_data = {
            "level1": {
                "level2": {
                    "level3": {
                        "value": "deep_value",
                        "array": [1, 2, 3, 4, 5],
                    },
                },
            },
        }

        write_file("nested_config.json", json.dumps(nested_data))

        content = read_file("nested_config.json")
        loaded = json.loads(content)

        assert loaded["level1"]["level2"]["level3"]["value"] == "deep_value"
        assert loaded["level1"]["level2"]["level3"]["array"] == [1, 2, 3, 4, 5]

    def test_json_array_data(self):
        array_data = [
            {"stock": "600519.XSHG", "weight": 0.3},
            {"stock": "000001.XSHE", "weight": 0.25},
            {"stock": "300001.XSHE", "weight": 0.2},
        ]

        write_file("portfolio.json", json.dumps(array_data))

        content = read_file("portfolio.json")
        loaded = json.loads(content)

        assert isinstance(loaded, list)
        assert len(loaded) == 3
        assert loaded[0]["stock"] == "600519.XSHG"


class TestPKLResourceHandling:
    """测试PKL模型文件处理"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()
        set_runtime_dir(self.temp_base)
        set_strategy_name("pkl_test")

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_pickle_model_write_and_load(self):
        model_data = {
            "type": "XGBRegressor",
            "params": {"n_estimators": 100, "max_depth": 5},
            "weights": np.random.randn(100, 5).tolist(),
            "feature_importance": [0.3, 0.25, 0.2, 0.15, 0.1],
        }

        model_bytes = pickle.dumps(model_data)
        write_file("trained_model.pkl", model_bytes, mode="wb")

        loaded_bytes = read_file("trained_model.pkl", mode="rb")
        loaded_model = pickle.loads(loaded_bytes)

        assert loaded_model["type"] == "XGBRegressor"
        assert len(loaded_model["feature_importance"]) == 5

    def test_pickle_dataframe(self):
        df = pd.DataFrame(
            {
                "feature1": np.random.randn(1000),
                "feature2": np.random.randn(1000),
                "target": np.random.randint(0, 2, 1000),
            }
        )

        df_bytes = pickle.dumps(df)
        write_file("features.pkl", df_bytes, mode="wb")

        loaded_bytes = read_file("features.pkl", mode="rb")
        df_loaded = pickle.loads(loaded_bytes)

        assert len(df_loaded) == 1000
        assert list(df_loaded.columns) == ["feature1", "feature2", "target"]

    def test_pickle_numpy_array(self):
        arr = np.random.randn(100, 50)

        arr_bytes = pickle.dumps(arr)
        write_file("weights.pkl", arr_bytes, mode="wb")

        loaded_bytes = read_file("weights.pkl", mode="rb")
        arr_loaded = pickle.loads(loaded_bytes)

        assert arr_loaded.shape == (100, 50)

    def test_pickle_complex_object(self):
        model_data = {
            "class": "MockModel",
            "params": {"lr": 0.01, "epochs": 100},
            "trained": True,
            "version": "v1.0",
            "weights": np.random.randn(10, 5).tolist(),
            "predict_multiplier": 2,
        }

        model_bytes = pickle.dumps(model_data)
        write_file("mock_model.pkl", model_bytes, mode="wb")

        loaded_bytes = read_file("mock_model.pkl", mode="rb")
        loaded_model = pickle.loads(loaded_bytes)

        assert loaded_model["params"]["lr"] == 0.01
        assert loaded_model["trained"] == True
        assert loaded_model["predict_multiplier"] == 2


class TestMultiThreadedResourceAccess:
    """测试多线程并发资源访问"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()
        set_runtime_dir(self.temp_base)

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_concurrent_write_different_strategies(self):
        results = []
        errors = []
        lock = threading.Lock()

        def worker(strategy_id):
            try:
                pack = RuntimeResourcePack(
                    strategy_name=f"concurrent_strategy_{strategy_id}",
                    runtime_base=self.temp_base,
                )
                pack.write_output_resource(
                    f"output_{strategy_id}.txt", f"content_{strategy_id}"
                )
                content = pack.read_output_resource(f"output_{strategy_id}.txt")
                with lock:
                    results.append((strategy_id, content))
            except Exception as e:
                with lock:
                    errors.append((strategy_id, str(e)))

        threads = []
        for i in range(10):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(errors) == 0
        assert len(results) == 10

        for strategy_id, content in results:
            assert content == f"content_{strategy_id}"

    def test_concurrent_read_same_resource(self):
        set_strategy_name("shared_read_test")
        write_file("shared_data.txt", "shared_content")

        results = []
        errors = []

        def reader(reader_id):
            try:
                content = read_file("shared_data.txt")
                results.append((reader_id, content))
            except Exception as e:
                errors.append((reader_id, str(e)))

        threads = []
        for i in range(20):
            t = threading.Thread(target=reader, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(errors) == 0
        assert len(results) == 20

        for reader_id, content in results:
            assert content == "shared_content"

    def test_concurrent_mixed_operations(self):
        set_strategy_name("mixed_ops_test")

        results = {"writes": [], "reads": [], "errors": []}
        lock = threading.Lock()

        def writer(writer_id):
            try:
                write_file(f"file_{writer_id}.txt", f"data_{writer_id}")
                with lock:
                    results["writes"].append(writer_id)
            except Exception as e:
                with lock:
                    results["errors"].append(("write", writer_id, str(e)))

        def reader(reader_id, file_id):
            try:
                content = read_file(f"file_{file_id}.txt")
                with lock:
                    results["reads"].append((reader_id, content))
            except Exception as e:
                with lock:
                    results["errors"].append(("read", reader_id, str(e)))

        write_threads = []
        for i in range(5):
            t = threading.Thread(target=writer, args=(i,))
            write_threads.append(t)
            t.start()

        for t in write_threads:
            t.join()

        read_threads = []
        for i in range(10):
            file_id = i % 5
            t = threading.Thread(target=reader, args=(i, file_id))
            read_threads.append(t)
            t.start()

        for t in read_threads:
            t.join()

        assert len(results["errors"]) == 0
        assert len(results["writes"]) == 5
        assert len(results["reads"]) == 10


class TestEdgeCasesAndErrorHandling:
    """测试边界情况和错误处理"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()
        set_runtime_dir(self.temp_base)
        set_strategy_name("edge_test")

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_empty_file(self):
        write_file("empty.txt", "")

        content = read_file("empty.txt")
        assert content == ""

    def test_empty_binary_file(self):
        write_file("empty.bin", b"", mode="wb")

        content = read_file("empty.bin", mode="rb")
        assert content == b""

    def test_special_characters_in_filename(self):
        special_names = [
            "file_with_underscore.txt",
            "file-with-dash.txt",
            "file.with.dots.txt",
        ]

        for name in special_names:
            write_file(name, f"content of {name}")
            content = read_file(name)
            assert content == f"content of {name}"

    def test_unicode_content(self):
        unicode_content = "中文内容测试 日本語テスト 한국어 테스트"

        write_file("unicode.txt", unicode_content)

        content = read_file("unicode.txt")
        assert content == unicode_content

    def test_very_long_filename(self):
        long_name = "a" * 200 + ".txt"

        write_file(long_name, "long filename content")

        content = read_file(long_name)
        assert content == "long filename content"

    def test_deep_directory_path(self):
        deep_path = "level1/level2/level3/level4/level5/file.txt"

        write_file(deep_path, "deep content")

        content = read_file(deep_path)
        assert content == "deep content"

    def test_file_not_found_error_message(self):
        with pytest.raises(FileNotFoundError) as excinfo:
            read_file("nonexistent_file.txt")

        assert "File not found" in str(excinfo.value) or "文件不存在" in str(
            excinfo.value
        )

    def test_mode_validation_errors(self):
        with pytest.raises(ValueError) as excinfo:
            read_file("test.txt", mode="invalid")

        assert "must be 'r' or 'rb'" in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            write_file("test.txt", "content", mode="invalid")

        assert "must be 'w', 'a', 'wb', or 'ab'" in str(excinfo.value)

    def test_encoding_validation(self):
        with pytest.raises(ValueError) as excinfo:
            read_file("test.txt", encoding="gbk")

        assert "utf-8" in str(excinfo.value)


class TestRealStrategyScenarios:
    """测试真实策略场景"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()
        set_runtime_dir(self.temp_base)

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_ml_conformal_strategy_scenario(self):
        set_strategy_name("ml_conformal")

        train_data = pd.DataFrame(
            {
                "LABEL": np.random.randn(100),
                "non_linear_size": np.random.randn(100),
                "beta": np.random.randn(100),
                "book_to_price_ratio": np.random.randn(100),
                "earnings_yield": np.random.randn(100),
                "growth": np.random.randn(100),
            }
        )

        test_data = train_data.iloc[:20].copy()

        write_file("train_conformal_base.csv", train_data.to_csv(index=False))
        write_file("test_conformal_base.csv", test_data.to_csv(index=False))

        train_csv = read_file("train_conformal_base.csv")
        test_csv = read_file("test_conformal_base.csv")

        df_train = pd.read_csv(BytesIO(train_csv.encode())).dropna()
        df_test = pd.read_csv(BytesIO(test_csv.encode())).dropna()

        X_train = pd.concat([df_train, df_test], axis=0)
        y = X_train["LABEL"]
        factor_list = [
            "non_linear_size",
            "beta",
            "book_to_price_ratio",
            "earnings_yield",
            "growth",
        ]
        X = X_train[factor_list]

        assert len(X) == 120
        assert len(y) == 120
        assert X.columns.tolist() == factor_list

    def test_factor_strategy_with_model(self):
        set_strategy_name("factor_strategy")

        model_data = {
            "type": "LinearRegression",
            "coefficients": np.random.randn(5).tolist(),
            "intercept": 0.5,
        }
        write_file("factor_model.pkl", pickle.dumps(model_data), mode="wb")

        config = {
            "factors": ["momentum", "volatility", "value", "quality", "growth"],
            "rebalance_freq": "monthly",
            "top_n": 10,
        }
        write_file("factor_config.json", json.dumps(config))

        model_bytes = read_file("factor_model.pkl", mode="rb")
        loaded_model = pickle.loads(model_bytes)

        config_content = read_file("factor_config.json")
        loaded_config = json.loads(config_content)

        assert len(loaded_model["coefficients"]) == 5
        assert len(loaded_config["factors"]) == 5

    def test_portfolio_strategy_with_outputs(self):
        set_strategy_name("portfolio_strategy")

        write_file("trades/trade_log.csv", "date,stock,action,price,shares\n")
        write_file("signals/signal_record.json", json.dumps([]))

        trade_log = read_file("trades/trade_log.csv")
        signals = read_file("signals/signal_record.json")

        assert "date" in trade_log
        assert signals == "[]"

    def test_strategy_with_record_and_message(self):
        set_strategy_name("recording_strategy")

        for day in range(5):
            record(
                name="daily_signals",
                date=datetime(2023, 1, day + 1),
                signal="buy" if day % 2 == 0 else "hold",
                price=100.0 + day * 0.5,
                position=100 + day * 10,
            )

        send_message("策略启动", "5天数据已记录")
        send_message("风控提醒", "持仓已达上限", channel="risk")

        data = get_record_data("daily_signals")
        messages = get_messages()

        assert len(data) == 5
        assert len(messages) == 2
        assert messages[1]["channel"] == "risk"


class TestResourceCleanupAndRecovery:
    """测试资源清理和恢复"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_clear_output_resources(self):
        pack = RuntimeResourcePack(
            strategy_name="cleanup_test", runtime_base=self.temp_base
        )

        pack.write_output_resource("log1.txt", "data1")
        pack.write_output_resource("log2.txt", "data2")
        pack.write_output_resource("trade1.csv", "trade_data")

        assert len(pack.list_output_resources()) == 3

        pack.clear_output_resources("logs")

        remaining = pack.list_output_resources()
        log_files = [r for r in remaining if r["type"] == "logs"]
        assert len(log_files) == 0

        trade_files = [r for r in remaining if r["type"] == "trades"]
        assert len(trade_files) == 1

    def test_clear_all_resources(self):
        pack = RuntimeResourcePack(
            strategy_name="full_cleanup_test", runtime_base=self.temp_base
        )

        pack.write_input_resource("model.pkl", b"model")
        pack.write_input_resource("config.json", "{}")
        pack.write_output_resource("log.txt", "log")
        pack.write_output_resource("trades.csv", "trades")

        pack.clear_all_resources()

        assert len(pack.list_input_resources()) == 0
        assert len(pack.list_output_resources()) == 0

    def test_strategy_switch_resource_cleanup(self):
        set_runtime_dir(self.temp_base)

        set_strategy_name("strategy_1")
        write_file("file1.txt", "content1")

        set_strategy_name("strategy_2")
        write_file("file2.txt", "content2")

        set_strategy_name("strategy_1")
        content1 = read_file("file1.txt")
        assert content1 == "content1"

        set_strategy_name("strategy_2")
        content2 = read_file("file2.txt")
        assert content2 == "content2"


class TestResourceTypeCategories:
    """测试资源类型分类"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_input_resource_categories(self):
        pack = RuntimeResourcePack(
            strategy_name="category_test", runtime_base=self.temp_base
        )

        pack.write_input_resource("model1.pkl", b"pkl_model")
        pack.write_input_resource("model2.h5", b"h5_model")
        pack.write_input_resource("model3.pth", b"pth_model")
        pack.write_input_resource("config1.json", "{}")
        pack.write_input_resource("config2.yaml", "yaml: true")
        pack.write_input_resource("data1.csv", "csv_data")
        pack.write_input_resource("data2.parquet", b"parquet")

        input_resources = pack.list_input_resources()

        model_files = [r for r in input_resources if r["type"] == "models"]
        assert len(model_files) >= 3

        config_files = [r for r in input_resources if r["type"] == "config"]
        assert len(config_files) >= 2

        data_files = [r for r in input_resources if r["type"] == "data"]
        assert len(data_files) >= 1

    def test_output_resource_categories(self):
        pack = RuntimeResourcePack(
            strategy_name="output_category_test", runtime_base=self.temp_base
        )

        pack.write_output_resource("trade1.csv", "trade_data", resource_type="trades")
        pack.write_output_resource("signal1.json", "{}", resource_type="signals")
        pack.write_output_resource("log1.txt", "log_data", resource_type="logs")
        pack.write_output_resource("nav.csv", "nav_data", resource_type="trades")

        output_resources = pack.list_output_resources()

        trade_files = [r for r in output_resources if r["type"] == "trades"]
        assert len(trade_files) >= 2

        signal_files = [r for r in output_resources if r["type"] == "signals"]
        assert len(signal_files) >= 1

        log_files = [r for r in output_resources if r["type"] == "logs"]
        assert len(log_files) >= 1


class TestExportRecordsFunctionality:
    """测试记录导出功能"""

    def setup_method(self):
        clear_runtime_data()
        self.temp_base = tempfile.mkdtemp()
        set_runtime_dir(self.temp_base)

    def teardown_method(self):
        clear_runtime_data()
        if os.path.exists(self.temp_base):
            shutil.rmtree(self.temp_base)

    def test_export_single_record_stream(self):
        set_strategy_name("export_test")

        for i in range(10):
            record(name="metrics", iteration=i, score=i * 0.1)

        exported_files = export_records_to_csv()

        assert "metrics" in exported_files

        csv_path = Path(exported_files["metrics"])
        assert csv_path.exists()

        df = pd.read_csv(csv_path)
        assert len(df) == 10

    def test_export_multiple_record_streams(self):
        set_strategy_name("multi_export_test")

        record(name="prices", high=105, low=95, close=100)
        record(name="volumes", traded=1000, cancelled=50)
        record(name="signals", signal_type="buy", confidence=0.85)

        exported_files = export_records_to_csv()

        assert len(exported_files) == 3
        assert "prices" in exported_files
        assert "volumes" in exported_files
        assert "signals" in exported_files


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
