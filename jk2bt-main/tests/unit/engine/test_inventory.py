"""
test_inventory.py
inventory.py 单元测试

测试场景覆盖:
1. StrategyClassification 数据类
2. StrategyInventory 策略盘点器
3. classify_strategy 策略分类
4. _ML_LIBRARIES 机器学习库集合
5. _INTRADAY_KEYWORDS 日内关键词
6. _FUTURE_KEYWORDS 期货关键词
7. _ETF_KEYWORDS ETF关键词
8. _STOCK_KEYWORDS 股票关键词
"""

import pytest
import os
from unittest.mock import MagicMock, patch
from dataclasses import is_dataclass

try:
    from jk2bt.engine.inventory import (
        StrategyClassification,
        StrategyInventory,
    )
except ImportError:
    pytest.skip("inventory module not available", allow_module_level=True)


class TestStrategyClassification:
    """测试 StrategyClassification 数据类"""

    def test_is_dataclass(self):
        """测试是数据类"""
        assert is_dataclass(StrategyClassification)

    def test_basic_creation(self):
        """测试基本创建"""
        classification = StrategyClassification(
            file_path="/path/to/strategy.txt",
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
        assert classification.file_name == "strategy.txt"
        assert "股票策略" in classification.strategy_type

    def test_defaults(self):
        """测试默认值"""
        classification = StrategyClassification(
            file_path="/path/to/strategy.txt",
            file_name="strategy.txt",
            strategy_type=[],
            is_real_strategy=False,
            is_executable=False,
            has_ml_dependency=False,
            has_file_dependency=False,
            time_frame="日线",
            market_type="股票",
            account_type="单账户",
        )
        assert classification.keywords == []
        assert classification.ml_libraries == []
        assert classification.file_dependencies == []

    def test_optional_fields(self):
        """测试可选字段"""
        classification = StrategyClassification(
            file_path="/path/to/strategy.txt",
            file_name="strategy.txt",
            strategy_type=["股票策略"],
            is_real_strategy=True,
            is_executable=True,
            has_ml_dependency=True,
            has_file_dependency=True,
            time_frame="分钟级",
            market_type="股票",
            account_type="多账户",
            ml_libraries=["sklearn", "pandas"],
            file_dependencies=["data.csv"],
            code_lines=500,
        )
        assert classification.ml_libraries == ["sklearn", "pandas"]
        assert classification.file_dependencies == ["data.csv"]
        assert classification.code_lines == 500


class TestStrategyInventory:
    """测试 StrategyInventory 策略盘点器"""

    def test_basic_creation(self):
        """测试基本创建"""
        inventory = StrategyInventory("/fake/path")
        assert inventory.strategy_dir == "/fake/path"
        assert inventory.scanner is not None
        assert inventory.classifications == []

    def test_ml_libraries_set(self):
        """测试机器学习库集合"""
        assert "sklearn" in StrategyInventory._ML_LIBRARIES
        assert "xgboost" in StrategyInventory._ML_LIBRARIES
        assert "lightgbm" in StrategyInventory._ML_LIBRARIES
        assert "talib" in StrategyInventory._ML_LIBRARIES

    def test_intraday_keywords(self):
        """测试日内关键词"""
        assert "分钟" in StrategyInventory._INTRADAY_KEYWORDS
        assert "日内" in StrategyInventory._INTRADAY_KEYWORDS
        assert "高频" in StrategyInventory._INTRADAY_KEYWORDS

    def test_future_keywords(self):
        """测试期货关键词"""
        assert "期货" in StrategyInventory._FUTURE_KEYWORDS
        assert "股指" in StrategyInventory._FUTURE_KEYWORDS
        assert "IC" in StrategyInventory._FUTURE_KEYWORDS

    def test_etf_keywords(self):
        """测试ETF关键词"""
        assert "ETF" in StrategyInventory._ETF_KEYWORDS
        assert "etf" in StrategyInventory._ETF_KEYWORDS

    def test_stock_keywords(self):
        """测试股票关键词"""
        assert "股票" in StrategyInventory._STOCK_KEYWORDS
        assert "选股" in StrategyInventory._STOCK_KEYWORDS
        assert "因子" in StrategyInventory._STOCK_KEYWORDS


class TestStrategyInventoryClassify:
    """测试策略分类功能"""

    def test_classify_stock_strategy(self):
        """测试分类股票策略"""
        inventory = StrategyInventory("/fake/path")
        content = """
def initialize(context):
    g.stocks = ["600519.XSHG"]

def handle_data(context, data):
    pass
"""
        result = inventory.classify_strategy("/fake/strategy.txt", content)
        assert isinstance(result, StrategyClassification)
        assert result.is_real_strategy is True

    def test_classify_research_document(self):
        """测试分类研究文档"""
        inventory = StrategyInventory("/fake/path")
        content = "这是一些研究笔记和学习材料"
        result = inventory.classify_strategy("/fake/readme.txt", content)
        assert "研究说明/非策略文档" in result.strategy_type

    def test_detects_ml_libraries(self):
        """测试检测机器学习库"""
        inventory = StrategyInventory("/fake/path")
        content = """
import sklearn
from xgboost import XGBClassifier
"""
        result = inventory.classify_strategy("/fake/strategy.txt", content)
        assert result.has_ml_dependency is True
        assert "sklearn" in result.ml_libraries

    def test_detects_file_dependencies(self):
        """测试检测文件依赖"""
        inventory = StrategyInventory("/fake/path")
        content = """
import pandas as pd
df = pd.read_csv("data.csv")
"""
        result = inventory.classify_strategy("/fake/strategy.txt", content)
        assert result.has_file_dependency is True

    def test_detects_intraday_strategy(self):
        """测试检测日内策略"""
        inventory = StrategyInventory("/fake/path")
        content = """
def initialize(context):
    context.frequency = "1m"
"""
        result = inventory.classify_strategy("/fake/strategy.txt", content)
        assert "分钟级/日内策略" in result.strategy_type
        assert result.time_frame == "分钟级"

    def test_detects_future_strategy(self):
        """测试检测期货策略"""
        inventory = StrategyInventory("/fake/path")
        content = """
def initialize(context):
    log.info("期货策略")
"""
        result = inventory.classify_strategy("/fake/strategy.txt", content)
        assert "期货/股指策略" in result.strategy_type

    def test_detects_etf_strategy(self):
        """测试检测ETF策略"""
        inventory = StrategyInventory("/fake/path")
        content = """
def initialize(context):
    etf_list = ["510500.XSHG"]
"""
        result = inventory.classify_strategy("/fake/strategy.txt", content)
        assert "ETF策略" in result.strategy_type

    def test_detects_multi_account(self):
        """测试检测多账户策略"""
        inventory = StrategyInventory("/fake/path")
        content = """
def initialize(context):
    context.subportfolio = True
"""
        result = inventory.classify_strategy("/fake/strategy.txt", content)
        assert "多账户/子账户策略" in result.strategy_type

    def test_classification_code_lines(self):
        """测试代码行数统计"""
        inventory = StrategyInventory("/fake/path")
        content = "line1\nline2\nline3"
        result = inventory.classify_strategy("/fake/strategy.txt", content)
        assert result.code_lines == 3


class TestStrategyInventoryScan:
    """测试策略扫描功能"""

    def test_scan_all_strategies_empty_dir(self, tmp_path):
        """测试扫描空目录"""
        inventory = StrategyInventory(str(tmp_path))
        results = inventory.scan_all_strategies()
        assert len(results) == 0

    def test_scan_all_strategies_with_files(self, tmp_path):
        """测试扫描包含文件目录"""
        strategy_file = tmp_path / "strategy.txt"
        strategy_file.write_text("""
def initialize(context):
    g.stocks = ["600519.XSHG"]

def handle_data(context, data):
    pass
""")
        inventory = StrategyInventory(str(tmp_path))
        results = inventory.scan_all_strategies()
        assert len(results) == 1


class TestStrategyInventoryGenerateReport:
    """测试报告生成功能"""

    def test_generate_report_creates_files(self, tmp_path):
        """测试生成报告创建文件"""
        inventory = StrategyInventory(str(tmp_path))

        md_file, json_file, csv_file = inventory.generate_report(str(tmp_path))

        assert os.path.exists(md_file)
        assert os.path.exists(json_file)
        assert os.path.exists(csv_file)

    def test_generate_report_json_structure(self, tmp_path):
        """测试JSON报告结构"""
        inventory = StrategyInventory(str(tmp_path))
        md_file, json_file, csv_file = inventory.generate_report(str(tmp_path))

        import json

        with open(json_file) as f:
            data = json.load(f)

        assert "scan_time" in data
        assert "strategy_dir" in data
        assert "total_files" in data
        assert "classifications" in data
