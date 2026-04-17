"""
策略库存管理模块单元测试
测试 inventory.py 中的 StrategyClassification 和 StrategyInventory 类
"""

import os
import json
import csv
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from jk2bt.engine.inventory import StrategyInventory, StrategyClassification
from jk2bt.scanner.scanner import ScanResult, StrategyStatus


class TestStrategyClassification:
    """测试 StrategyClassification 数据类"""

    def test_default_initialization(self):
        cls = StrategyClassification(
            file_path="/test/strategy.txt",
            file_name="strategy.txt",
            strategy_type=["股票策略"],
            is_real_strategy=True,
            is_executable=True,
            has_ml_dependency=False,
            has_file_dependency=False,
            time_frame="日线",
            market_type="股票",
            account_type="单账户",
        )
        assert cls.file_path == "/test/strategy.txt"
        assert cls.keywords == []
        assert cls.ml_libraries == []
        assert cls.file_dependencies == []
        assert cls.code_lines == 0
        assert cls.scan_result is None

    def test_custom_initialization(self):
        scan_result = MagicMock()
        cls = StrategyClassification(
            file_path="/test/strategy.txt",
            file_name="strategy.txt",
            strategy_type=["ETF策略", "依赖ML库策略"],
            is_real_strategy=True,
            is_executable=True,
            has_ml_dependency=True,
            has_file_dependency=True,
            time_frame="分钟级",
            market_type="ETF",
            account_type="多账户",
            scan_result=scan_result,
            keywords=["ETF", "talib"],
            ml_libraries=["talib", "sklearn"],
            file_dependencies=[".csv", "pd.read_"],
            code_lines=150,
        )
        assert cls.strategy_type == ["ETF策略", "依赖ML库策略"]
        assert len(cls.ml_libraries) == 2
        assert cls.code_lines == 150


class TestStrategyInventoryInit:
    """测试 StrategyInventory 初始化"""

    def test_init_with_valid_dir(self, tmp_path):
        strategy_dir = str(tmp_path / "strategies")
        os.makedirs(strategy_dir)
        inventory = StrategyInventory(strategy_dir)
        assert inventory.strategy_dir == strategy_dir
        assert inventory.classifications == []
        assert inventory.scanner is not None

    def test_init_with_nonexistent_dir(self):
        nonexistent = "/nonexistent/path/that/does/not/exist"
        inventory = StrategyInventory(nonexistent)
        assert inventory.strategy_dir == nonexistent
        assert inventory.classifications == []


class TestClassifyStrategy:
    """测试 classify_strategy 方法"""

    def test_classify_valid_stock_strategy(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
def initialize(context):
    set_benchmark('000001.XSHG')

def handle_data(context, data):
    stocks = get_index_stocks('000001.XSHG')
    order('000001.XSHG', 100)
"""
        file_path = str(tmp_path / "stock_strategy.txt")
        (tmp_path / "stock_strategy.txt").write_text(content, encoding="utf-8")
        cls = inventory.classify_strategy(file_path, content)

        assert cls.file_name == "stock_strategy.txt"
        assert cls.is_real_strategy is True
        assert cls.is_executable is True
        assert cls.has_ml_dependency is False
        assert cls.has_file_dependency is False
        assert cls.time_frame == "日线"
        assert cls.market_type == "股票"
        assert cls.account_type == "单账户"
        assert cls.code_lines == len(content.splitlines())

    def test_classify_etf_strategy(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
def initialize(context):
    pass

def handle_data(context, data):
    etf_list = ['510300.XSHG', '510500.XSHG']
    # ETF轮动策略
"""
        file_path = str(tmp_path / "etf_strategy.txt")
        cls = inventory.classify_strategy(file_path, content)

        assert "ETF策略" in cls.strategy_type
        assert cls.market_type == "ETF"

    def test_classify_future_strategy(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
def initialize(context):
    pass

def handle_data(context, data):
    # 期货策略，使用IF主力合约
    # 做空机制
"""
        file_path = str(tmp_path / "future_strategy.txt")
        cls = inventory.classify_strategy(file_path, content)

        assert "期货/股指策略" in cls.strategy_type
        assert cls.market_type == "期货/股指"

    def test_classify_intraday_strategy(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
def initialize(context):
    pass

def handle_data(context, data):
    # 分钟线策略
    # 日内交易
"""
        file_path = str(tmp_path / "intraday_strategy.txt")
        cls = inventory.classify_strategy(file_path, content)

        assert "分钟级/日内策略" in cls.strategy_type
        assert cls.time_frame == "分钟级"

    def test_classify_ml_dependent_strategy(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
import sklearn
import talib
from xgboost import XGBClassifier

def initialize(context):
    pass

def handle_data(context, data):
    pass
"""
        file_path = str(tmp_path / "ml_strategy.txt")
        cls = inventory.classify_strategy(file_path, content)

        assert cls.has_ml_dependency is True
        assert "依赖ML库策略" in cls.strategy_type
        assert "sklearn" in cls.ml_libraries
        assert "talib" in cls.ml_libraries

    def test_classify_file_dependency_strategy(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
import pandas as pd

def initialize(context):
    pass

def handle_data(context, data):
    df = pd.read_csv('data.csv')
"""
        file_path = str(tmp_path / "file_dep_strategy.txt")
        cls = inventory.classify_strategy(file_path, content)

        assert cls.has_file_dependency is True
        assert "依赖文件资源策略" in cls.strategy_type

    def test_classify_research_document(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
# 策略研究说明文档
# 这是一个笔记文件，不是策略
"""
        file_path = str(tmp_path / "研究说明.txt")
        cls = inventory.classify_strategy(file_path, content)

        assert cls.is_real_strategy is False
        assert "研究说明/非策略文档" in cls.strategy_type

    def test_classify_no_initialize(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
# 只是一个普通文件
print("hello")
"""
        file_path = str(tmp_path / "no_init.txt")
        cls = inventory.classify_strategy(file_path, content)

        assert cls.is_real_strategy is False
        assert cls.is_executable is False

    def test_classify_multi_account_strategy(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
def initialize(context):
    pass

def handle_data(context, data):
    # 子账户管理
    # 资产配置
"""
        file_path = str(tmp_path / "multi_account.txt")
        cls = inventory.classify_strategy(file_path, content)

        assert "多账户/子账户策略" in cls.strategy_type
        assert cls.account_type == "多账户"

    def test_classify_tick_strategy(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
def initialize(context):
    pass

def handle_data(context, data):
    # tick数据处理
    # 高频策略
"""
        file_path = str(tmp_path / "tick_strategy.txt")
        cls = inventory.classify_strategy(file_path, content)

        assert "分钟级/日内策略" in cls.strategy_type

    def test_classify_nonexistent_file(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = "def initialize(context): pass\ndef handle_data(context, data): pass"
        file_path = "/nonexistent/file.txt"
        cls = inventory.classify_strategy(file_path, content)

        assert cls.is_executable is False
        assert cls.scan_result is not None
        assert cls.scan_result.is_executable is False

    def test_classify_empty_content(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = ""
        file_path = str(tmp_path / "empty.txt")
        cls = inventory.classify_strategy(file_path, content)

        assert cls.code_lines == 0
        assert cls.is_executable is False


class TestScanAllStrategies:
    """测试 scan_all_strategies 方法"""

    def test_scan_empty_directory(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)
        results = inventory.scan_all_strategies()
        assert results == []
        assert inventory.classifications == []

    def test_scan_single_strategy_file(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
def initialize(context):
    pass

def handle_data(context, data):
    pass
"""
        (tmp_path / "strategy1.txt").write_text(content, encoding="utf-8")

        results = inventory.scan_all_strategies()
        assert len(results) == 1
        assert results[0].file_name == "strategy1.txt"
        assert results[0].is_real_strategy is True

    def test_scan_multiple_strategy_files(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        for i in range(5):
            content = f"""
def initialize(context):
    pass

def handle_data(context, data):
    # 策略 {i}
    pass
"""
            (tmp_path / f"strategy_{i}.txt").write_text(content, encoding="utf-8")

        results = inventory.scan_all_strategies()
        assert len(results) == 5

    def test_scan_mixed_files(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        valid_content = """
def initialize(context):
    pass

def handle_data(context, data):
    pass
"""
        (tmp_path / "valid.txt").write_text(valid_content, encoding="utf-8")
        (tmp_path / "research_说明.txt").write_text(
            "这是一个研究文档", encoding="utf-8"
        )
        (tmp_path / "not_a_txt.py").write_text("print('hello')", encoding="utf-8")

        results = inventory.scan_all_strategies()
        assert len(results) == 2

    def test_scan_gbk_encoded_file(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
def initialize(context):
    pass

def handle_data(context, data):
    # 中文注释
    pass
"""
        file_path = tmp_path / "gbk_strategy.txt"
        with open(file_path, "w", encoding="gbk") as f:
            f.write(content)

        results = inventory.scan_all_strategies()
        assert len(results) == 1
        assert results[0].is_real_strategy is True

    def test_scan_ignores_non_txt_files(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        (tmp_path / "readme.md").write_text("# README", encoding="utf-8")
        (tmp_path / "data.csv").write_text("a,b,c", encoding="utf-8")
        (tmp_path / "notes.txt").write_text("just notes", encoding="utf-8")

        results = inventory.scan_all_strategies()
        assert len(results) == 1

    def test_scan_handles_binary_file(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        file_path = tmp_path / "binary.txt"
        with open(file_path, "wb") as f:
            f.write(b"\x00\x01\x02\x03\x04\x05")

        results = inventory.scan_all_strategies()
        assert len(results) == 1


class TestGenerateReport:
    """测试 generate_report 方法"""

    def _create_inventory_with_data(self, tmp_path):
        strategy_dir = str(tmp_path / "strategies")
        os.makedirs(strategy_dir)
        inventory = StrategyInventory(strategy_dir)

        content1 = """
def initialize(context):
    pass

def handle_data(context, data):
    # ETF轮动策略
    pass
"""
        content2 = """
import sklearn

def initialize(context):
    pass

def handle_data(context, data):
    # 股票策略
    pass
"""
        content3 = """
# 研究说明文档
# 这不是策略
"""
        (tmp_path / "etf.txt").write_text(content1, encoding="utf-8")
        (tmp_path / "ml_stock.txt").write_text(content2, encoding="utf-8")
        (tmp_path / "研究说明.txt").write_text(content3, encoding="utf-8")

        inventory.scan_all_strategies()
        return inventory

    def test_generate_report_creates_files(self, tmp_path):
        inventory = self._create_inventory_with_data(tmp_path)
        output_dir = str(tmp_path / "output")

        md_file, json_file, csv_file = inventory.generate_report(output_dir)

        assert os.path.exists(md_file)
        assert os.path.exists(json_file)
        assert os.path.exists(csv_file)

    def test_generate_report_returns_correct_paths(self, tmp_path):
        inventory = self._create_inventory_with_data(tmp_path)
        output_dir = str(tmp_path / "output")

        md_file, json_file, csv_file = inventory.generate_report(output_dir)

        assert "task11_strategy_inventory_result.md" in md_file
        assert "task11_strategy_inventory.json" in json_file
        assert "task11_strategy_inventory.csv" in csv_file

    def test_generate_report_creates_output_dir(self, tmp_path):
        inventory = self._create_inventory_with_data(tmp_path)
        output_dir = str(tmp_path / "new_output_dir")

        inventory.generate_report(output_dir)

        assert os.path.exists(output_dir)


class TestMarkdownReport:
    """测试 Markdown 报告生成"""

    def _create_inventory_with_data(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
def initialize(context):
    pass

def handle_data(context, data):
    pass
"""
        (tmp_path / "strategy.txt").write_text(content, encoding="utf-8")
        inventory.scan_all_strategies()
        return inventory

    def test_markdown_report_has_header(self, tmp_path):
        inventory = self._create_inventory_with_data(tmp_path)
        md_file = str(tmp_path / "report.md")

        inventory._write_markdown_report(md_file)

        content = Path(md_file).read_text(encoding="utf-8")
        assert "Task 11 策略资产盘点与分层报告" in content

    def test_markdown_report_has_statistics(self, tmp_path):
        inventory = self._create_inventory_with_data(tmp_path)
        md_file = str(tmp_path / "report.md")

        inventory._write_markdown_report(md_file)

        content = Path(md_file).read_text(encoding="utf-8")
        assert "总文件数" in content
        assert "真策略数" in content
        assert "可执行策略数" in content

    def test_markdown_report_has_type_table(self, tmp_path):
        inventory = self._create_inventory_with_data(tmp_path)
        md_file = str(tmp_path / "report.md")

        inventory._write_markdown_report(md_file)

        content = Path(md_file).read_text(encoding="utf-8")
        assert "| 类型 | 数量 | 占比 |" in content

    def test_markdown_report_with_empty_inventory(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)
        md_file = str(tmp_path / "report.md")

        inventory._write_markdown_report(md_file)

        content = Path(md_file).read_text(encoding="utf-8")
        assert "总文件数" in content


class TestJsonReport:
    """测试 JSON 报告生成"""

    def _create_inventory_with_data(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
def initialize(context):
    pass

def handle_data(context, data):
    pass
"""
        (tmp_path / "strategy.txt").write_text(content, encoding="utf-8")
        inventory.scan_all_strategies()
        return inventory

    def test_json_report_is_valid_json(self, tmp_path):
        inventory = self._create_inventory_with_data(tmp_path)
        json_file = str(tmp_path / "report.json")

        inventory._write_json_report(json_file)

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, dict)

    def test_json_report_has_required_fields(self, tmp_path):
        inventory = self._create_inventory_with_data(tmp_path)
        json_file = str(tmp_path / "report.json")

        inventory._write_json_report(json_file)

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "scan_time" in data
        assert "strategy_dir" in data
        assert "total_files" in data
        assert "real_strategies" in data
        assert "executable_strategies" in data
        assert "classifications" in data

    def test_json_report_has_classification_data(self, tmp_path):
        inventory = self._create_inventory_with_data(tmp_path)
        json_file = str(tmp_path / "report.json")

        inventory._write_json_report(json_file)

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data["classifications"]) == 1
        cls = data["classifications"][0]
        assert "file_name" in cls
        assert "strategy_type" in cls
        assert "is_real_strategy" in cls
        assert "is_executable" in cls

    def test_json_report_with_empty_inventory(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)
        json_file = str(tmp_path / "report.json")

        inventory._write_json_report(json_file)

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["total_files"] == 0
        assert data["classifications"] == []


class TestCsvReport:
    """测试 CSV 报告生成"""

    def _create_inventory_with_data(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
def initialize(context):
    pass

def handle_data(context, data):
    pass
"""
        (tmp_path / "strategy.txt").write_text(content, encoding="utf-8")
        inventory.scan_all_strategies()
        return inventory

    def test_csv_report_has_header(self, tmp_path):
        inventory = self._create_inventory_with_data(tmp_path)
        csv_file = str(tmp_path / "report.csv")

        inventory._write_csv_report(csv_file)

        with open(csv_file, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            header = next(reader)
        assert "文件名" in header
        assert "策略类型" in header
        assert "真策略" in header

    def test_csv_report_has_data_rows(self, tmp_path):
        inventory = self._create_inventory_with_data(tmp_path)
        csv_file = str(tmp_path / "report.csv")

        inventory._write_csv_report(csv_file)

        with open(csv_file, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = list(reader)

        assert len(rows) == 1
        assert len(rows[0]) == len(header)

    def test_csv_report_with_empty_inventory(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)
        csv_file = str(tmp_path / "report.csv")

        inventory._write_csv_report(csv_file)

        with open(csv_file, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = list(reader)

        assert len(rows) == 0


class TestEdgeCases:
    """测试边界条件"""

    def test_classify_strategy_with_syntax_error(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
def initialize(context):
    if True
        pass
"""
        file_path = str(tmp_path / "syntax_error.txt")
        cls = inventory.classify_strategy(file_path, content)

        assert cls.is_executable is False

    def test_classify_strategy_with_null_bytes(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = "def initialize(context): pass\ndef handle_data(context, data): pass"
        file_path = str(tmp_path / "null_bytes.txt")
        with open(file_path, "wb") as f:
            f.write(content.replace("pass", "pass\x00").encode("utf-8"))
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        cls = inventory.classify_strategy(file_path, file_content)

        assert cls.is_real_strategy is True

    def test_classify_strategy_with_many_ml_libraries(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
import talib
import sklearn
import xgboost
import lightgbm
import torch
import tensorflow
import keras
import pandas
import numpy
import scipy

def initialize(context):
    pass

def handle_data(context, data):
    pass
"""
        file_path = str(tmp_path / "ml_heavy.txt")
        cls = inventory.classify_strategy(file_path, content)

        assert cls.has_ml_dependency is True
        assert len(cls.ml_libraries) > 0

    def test_scan_all_strategies_progress_output(self, tmp_path, capsys):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        for i in range(55):
            content = f"""
def initialize(context):
    pass

def handle_data(context, data):
    pass
"""
            (tmp_path / f"strategy_{i:03d}.txt").write_text(content, encoding="utf-8")

        inventory.scan_all_strategies()
        captured = capsys.readouterr()
        assert "进度: 50/" in captured.out

    def test_generate_report_with_multiple_types(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        etf_content = """
def initialize(context):
    pass

def handle_data(context, data):
    # ETF轮动
    pass
"""
        future_content = """
def initialize(context):
    pass

def handle_data(context, data):
    # 期货策略 IF主力合约
    pass
"""
        (tmp_path / "etf.txt").write_text(etf_content, encoding="utf-8")
        (tmp_path / "future.txt").write_text(future_content, encoding="utf-8")

        inventory.scan_all_strategies()

        output_dir = str(tmp_path / "output")
        md_file, json_file, csv_file = inventory.generate_report(output_dir)

        md_content = Path(md_file).read_text(encoding="utf-8")
        assert "ETF策略" in md_content
        assert "期货/股指策略" in md_content

    def test_priority_list_in_markdown(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
def initialize(context):
    pass

def handle_data(context, data):
    pass
"""
        (tmp_path / "simple.txt").write_text(content, encoding="utf-8")
        inventory.scan_all_strategies()

        md_file = str(tmp_path / "report.md")
        inventory._write_markdown_report(md_file)

        content = Path(md_file).read_text(encoding="utf-8")
        assert "优先级 1" in content
        assert "优先级 2" in content
        assert "优先级 3" in content
        assert "优先级 4" in content

    def test_ml_library_stats_in_markdown(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
import sklearn
import talib

def initialize(context):
    pass

def handle_data(context, data):
    pass
"""
        (tmp_path / "ml.txt").write_text(content, encoding="utf-8")
        inventory.scan_all_strategies()

        md_file = str(tmp_path / "report.md")
        inventory._write_markdown_report(md_file)

        content = Path(md_file).read_text(encoding="utf-8")
        assert "ML库依赖统计" in content
        assert "sklearn" in content
        assert "talib" in content


class TestKeywordClassification:
    """测试关键词分类逻辑"""

    def test_stock_keyword_detection(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
def initialize(context):
    pass

def handle_data(context, data):
    # 小市值策略
    # 因子选股
    pass
"""
        file_path = str(tmp_path / "stock.txt")
        cls = inventory.classify_strategy(file_path, content)

        assert "股票策略" in cls.strategy_type
        assert cls.market_type == "股票"

    def test_keyword_limit_in_classification(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content_lines = [
            "def initialize(context): pass",
            "def handle_data(context, data): pass",
        ]
        for kw in StrategyInventory._INTRADAY_KEYWORDS:
            content_lines.append(f"# {kw}")
        for kw in StrategyInventory._FUTURE_KEYWORDS:
            content_lines.append(f"# {kw}")

        content = "\n".join(content_lines)
        file_path = str(tmp_path / "many_keywords.txt")
        cls = inventory.classify_strategy(file_path, content)

        assert len(cls.keywords) <= 20

    def test_file_dependency_pattern_detection(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
import pandas as pd

def initialize(context):
    pass

def handle_data(context, data):
    df = pd.read_excel('data.xlsx')
    with open('config.pkl', 'rb') as f:
        pass
"""
        file_path = str(tmp_path / "file_deps.txt")
        cls = inventory.classify_strategy(file_path, content)

        assert cls.has_file_dependency is True
        assert len(cls.file_dependencies) > 0

    def test_file_dependency_limit(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content_lines = [
            "def initialize(context): pass",
            "def handle_data(context, data): pass",
        ]
        for i in range(20):
            content_lines.append(f"# data_{i}.csv")

        content = "\n".join(content_lines)
        file_path = str(tmp_path / "many_deps.txt")
        cls = inventory.classify_strategy(file_path, content)

        assert len(cls.file_dependencies) <= 10


class TestStrategyTypeDeduplication:
    """测试策略类型去重"""

    def test_strategy_types_are_unique(self, tmp_path):
        strategy_dir = str(tmp_path)
        inventory = StrategyInventory(strategy_dir)

        content = """
def initialize(context):
    pass

def handle_data(context, data):
    # 股票
    # 因子
    # 小市值
    # 动量
    pass
"""
        file_path = str(tmp_path / "dedup.txt")
        cls = inventory.classify_strategy(file_path, content)

        assert len(cls.strategy_type) == len(set(cls.strategy_type))
