#!/usr/bin/env python3
"""
test_task23_whitelist.py
Task 23: 日线策略真实白名单测试
全面测试策略加载、类型识别、白名单验证等功能
"""

import os
import sys
import pytest
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"),
)

from jk2bt.core.runner import load_jq_strategy


class TestStrategyTypeAnalyzer:
    """测试策略类型分析功能"""

    def test_etf_rotation_strategy_detection(self):
        """测试ETF轮动策略识别"""
        strategy_content = """
# ETF轮动策略
def initialize(context):
    g.etf_pool = ['510300.XSHG', '159915.XSHE']
    run_daily(rebalance, 'open')

def rebalance(context):
    # ETF动量轮动
    for etf in g.etf_pool:
        price = history(20, unit='1d', fields='close', security=etf)
        momentum = price[-1] / price[0]
        order_value(etf, 10000)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            result = self._analyze_strategy(f.name)
            assert result is not None
            assert "ETF轮动" in result.get("priority_type", [])

            os.unlink(f.name)

    def test_index_tracking_strategy_detection(self):
        """测试指数跟踪策略识别"""
        strategy_content = """
# 指数跟踪策略
def initialize(context):
    g.index = '000300.XSHG'
    run_monthly(rebalance, 1, 'open')

def rebalance(context):
    stocks = get_index_stocks('000300.XSHG')
    for stock in stocks[:10]:
        order_value(stock, 10000)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            result = self._analyze_strategy(f.name)
            assert result is not None
            assert "指数跟踪" in result.get("priority_type", [])

            os.unlink(f.name)

    def test_fundamental_strategy_detection(self):
        """测试基本面选股策略识别"""
        strategy_content = """
# 基本面选股策略
def initialize(context):
    run_monthly(select_stocks, 1, 'open')

def select_stocks(context):
    q = query(valuation.pe_ratio, valuation.pb_ratio).filter(
        valuation.pe_ratio < 20,
        valuation.pb_ratio < 2
    )
    df = get_fundamentals(q)
    for stock in df.index[:5]:
        order_value(stock, 10000)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            result = self._analyze_strategy(f.name)
            assert result is not None
            assert "基本面选股" in result.get("priority_type", [])

            os.unlink(f.name)

    def test_minute_strategy_exclusion(self):
        """测试分钟线策略排除"""
        strategy_content = """
# 分钟线策略（应该被排除）
def initialize(context):
    run_daily(trade, time='9:30')

def trade(context):
    # 使用分钟数据
    price = history(20, unit='1m', fields='close', security='600519.XSHG')
    order_value('600519.XSHG', 10000)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            result = self._analyze_strategy(f.name)
            assert result is not None
            assert result["is_daily"] == False
            assert "分钟线" in result.get("exclude_reason", [])

            os.unlink(f.name)

    def test_ml_strategy_exclusion(self):
        """测试机器学习策略排除"""
        strategy_content = """
# 机器学习策略（应该被排除）
from sklearn.ensemble import RandomForestRegressor

def initialize(context):
    g.model = RandomForestRegressor()
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            result = self._analyze_strategy(f.name)
            assert result is not None
            assert result["is_daily"] == False
            assert "机器学习" in result.get("exclude_reason", [])

            os.unlink(f.name)

    def _analyze_strategy(self, strategy_file):
        """分析策略类型"""
        try:
            with open(strategy_file, "r", encoding="utf-8") as f:
                content = f.read()
        except:
            return None

        priority_keywords = {
            "ETF轮动": ["ETF", "轮动", "动量", "轮换"],
            "指数跟踪": ["指数", "沪深300", "中证500", "创业板", "000300", "399006"],
            "基本面选股": [
                "基本面",
                "财务",
                "财报",
                "PE",
                "PB",
                "ROE",
                "股息率",
                "市盈率",
                "估值",
            ],
        }

        exclude_keywords = {
            "分钟线": [
                "frequency='1m'",
                "frequency='5m'",
                "分钟",
                "tick",
                "get_ticks",
                "current_price",
            ],
            "期货": ["期货", "future", "IF", "IC", "IH", "主力合约"],
            "机器学习": [
                "xgboost",
                "sklearn",
                "机器学习",
                "RandomForest",
                "LSTM",
                "神经网络",
            ],
        }

        analysis = {
            "is_daily": True,
            "priority_score": 0,
            "priority_type": [],
            "exclude_reason": [],
        }

        for category, keywords in exclude_keywords.items():
            if any(kw in content for kw in keywords):
                analysis["is_daily"] = False
                analysis["exclude_reason"].append(category)

        for category, keywords in priority_keywords.items():
            if any(kw in content for kw in keywords):
                analysis["priority_score"] += 10
                analysis["priority_type"].append(category)

        return analysis


class TestStrategyLoader:
    """测试策略加载功能"""

    def test_simple_strategy_load_success(self):
        """测试简单策略加载成功"""
        strategy_content = """
def initialize(context):
    g.stocks = ['600519.XSHG', '000858.XSHE']
    log.info('初始化策略')

def handle_data(context):
    for stock in g.stocks:
        order_value(stock, 10000)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            functions = load_jq_strategy(f.name)

            assert functions is not None
            assert "initialize" in functions
            assert "handle_data" in functions
            assert len(functions) >= 2

            os.unlink(f.name)

    def test_strategy_with_imports(self):
        """测试包含import语句的策略"""
        strategy_content = """
import pandas as pd
import numpy as np

def initialize(context):
    g.df = pd.DataFrame()
    g.arr = np.array([1, 2, 3])

def trade(context):
    log.info('交易执行')
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            functions = load_jq_strategy(f.name)

            assert functions is not None
            assert "initialize" in functions
            assert "trade" in functions

            os.unlink(f.name)

    def test_strategy_with_jq_functions(self):
        """测试包含聚宽函数的策略"""
        strategy_content = """
def initialize(context):
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    run_monthly(rebalance, 1, 'open')

def rebalance(context):
    stocks = get_index_stocks('000300.XSHG')
    for stock in stocks[:5]:
        current = get_current_data(stock)
        order_value(stock, 10000)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            functions = load_jq_strategy(f.name)

            assert functions is not None
            assert "initialize" in functions
            assert "rebalance" in functions

            os.unlink(f.name)

    def test_strategy_syntax_error(self):
        """测试语法错误的策略"""
        strategy_content = """
def initialize(context):
    g.stocks = ['600519.XSHG']
    # 语法错误：缩进不一致
     log.info('错误缩进')
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            with pytest.raises(SyntaxError):
                load_jq_strategy(f.name)

            os.unlink(f.name)

    def test_strategy_with_after_code_changed(self):
        """测试包含after_code_changed函数的策略"""
        strategy_content = """
def after_code_changed(context):
    g.params_updated = True
    log.info('代码已更新')

def initialize(context):
    g.params = {}
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            functions = load_jq_strategy(f.name)

            assert functions is not None
            assert "after_code_changed" in functions
            assert "initialize" in functions

            os.unlink(f.name)

    def test_strategy_with_timer_functions(self):
        """测试包含定时器函数的策略"""
        strategy_content = """
def initialize(context):
    run_daily(daily_task, 'open')
    run_weekly(weekly_task, 1, 'open')
    run_monthly(monthly_task, 1, 'open')

def daily_task(context):
    log.info('每日任务')

def weekly_task(context):
    log.info('每周任务')

def monthly_task(context):
    log.info('每月任务')
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            functions = load_jq_strategy(f.name)

            assert functions is not None
            assert "initialize" in functions
            assert "daily_task" in functions
            assert "weekly_task" in functions
            assert "monthly_task" in functions

            os.unlink(f.name)


class TestWhitelistValidation:
    """测试白名单验证功能"""

    def test_whitelist_strategy_structure(self):
        """测试白名单策略结构验证"""
        strategy_content = """
def initialize(context):
    g.stocks = ['600519.XSHG']
    g.num_stocks = 5
    log.info('初始化完成')

def handle_data(context):
    for stock in g.stocks:
        order_value(stock, context.portfolio.total_value / g.num_stocks)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            functions = load_jq_strategy(f.name)

            validation_result = {
                "load_success": functions is not None,
                "has_initialize": "initialize" in functions if functions else False,
                "has_handle": any(
                    k.startswith("handle_") or k.startswith("trading_")
                    for k in functions.keys()
                )
                if functions
                else False,
                "function_count": len(functions) if functions else 0,
                "functions_found": list(functions.keys()) if functions else [],
            }

            assert validation_result["load_success"] == True
            assert validation_result["has_initialize"] == True
            assert validation_result["has_handle"] == True
            assert validation_result["function_count"] >= 2

            os.unlink(f.name)

    def test_etf_rotation_whitelist(self):
        """测试ETF轮动策略白名单"""
        strategy_content = """
def initialize(context):
    g.etf_pool = {
        '沪深300': '510300.XSHG',
        '创业板': '159915.XSHE',
        '纳斯达克': '513100.XSHG'
    }
    run_daily(rebalance, 'open')

def rebalance(context):
    best_etf = None
    best_momentum = 0
    
    for name, etf in g.etf_pool.items():
        prices = history(20, unit='1d', fields='close', security=etf)
        momentum = prices[-1] / prices[0] - 1
        
        if momentum > best_momentum:
            best_momentum = momentum
            best_etf = etf
    
    if best_etf:
        order_target_value(best_etf, context.portfolio.total_value)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            functions = load_jq_strategy(f.name)

            assert functions is not None
            assert "initialize" in functions
            assert "rebalance" in functions

            os.unlink(f.name)

    def test_fundamental_selection_whitelist(self):
        """测试基本面选股策略白名单"""
        strategy_content = """
def initialize(context):
    g.stock_num = 10
    run_monthly(select_stocks, 1, 'open')

def select_stocks(context):
    q = query(
        valuation.code,
        valuation.pe_ratio,
        valuation.pb_ratio,
        valuation.market_cap
    ).filter(
        valuation.pe_ratio > 0,
        valuation.pe_ratio < 30,
        valuation.pb_ratio > 0,
        valuation.pb_ratio < 3
    ).order_by(
        valuation.market_cap.asc()
    ).limit(g.stock_num)
    
    df = get_fundamentals(q)
    
    for stock in df['code']:
        order_value(stock, context.portfolio.total_value / g.stock_num)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            functions = load_jq_strategy(f.name)

            assert functions is not None
            assert "initialize" in functions
            assert "select_stocks" in functions

            os.unlink(f.name)


class TestFailedStrategyHandling:
    """测试失败策略处理"""

    def test_missing_module_error(self):
        """测试缺少模块错误处理"""
        strategy_content = """
from kuanke.api import *

def initialize(context):
    log.info('初始化')
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            with pytest.raises(RuntimeError) as exc_info:
                load_jq_strategy(f.name)

            assert "kuanke" in str(exc_info.value)

            os.unlink(f.name)

    def test_invalid_syntax_handling(self):
        """测试无效语法错误处理"""
        strategy_content = """
def initialize(context):
    g.stocks = ['600519.XSHG']
    print '错误：Python3需要括号'
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            with pytest.raises(SyntaxError):
                load_jq_strategy(f.name)

            os.unlink(f.name)

    def test_empty_strategy_file(self):
        """测试空策略文件"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("")
            f.flush()

            functions = load_jq_strategy(f.name)

            assert functions is not None
            assert len(functions) == 0

            os.unlink(f.name)

    def test_strategy_with_only_comments(self):
        """测试只有注释的策略文件"""
        strategy_content = """
# 这是一个只有注释的策略文件
# 没有任何函数定义
# 只是注释说明
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            functions = load_jq_strategy(f.name)

            assert functions is not None
            assert len(functions) == 0

            os.unlink(f.name)


class TestStrategyFunctionTypes:
    """测试策略函数类型"""

    def test_initialize_function_present(self):
        """测试initialize函数存在"""
        strategy_content = """
def initialize(context):
    g.params = {'lookback': 20}
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            functions = load_jq_strategy(f.name)

            assert "initialize" in functions

            os.unlink(f.name)

    def test_handle_functions_detection(self):
        """测试handle函数检测"""
        strategy_content = """
def initialize(context):
    pass

def handle_data(context):
    log.info('每日执行')

def trading_logic(context):
    log.info('交易逻辑')

def handle_trader(context):
    log.info('处理交易')
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            functions = load_jq_strategy(f.name)

            handle_funcs = [
                k
                for k in functions.keys()
                if k.startswith("handle_") or k.startswith("trading_")
            ]
            assert len(handle_funcs) >= 2

            os.unlink(f.name)

    def test_helper_functions(self):
        """测试辅助函数"""
        strategy_content = """
def initialize(context):
    run_daily(select_stocks, 'open')

def select_stocks(context):
    stocks = get_stock_pool()
    filtered = filter_stocks(stocks)
    rank_stocks(filtered)
    buy_top_stocks(filtered)

def get_stock_pool():
    return ['600519.XSHG', '000858.XSHE']

def filter_stocks(stocks):
    return stocks

def rank_stocks(stocks):
    return sorted(stocks)

def buy_top_stocks(stocks):
    for stock in stocks[:5]:
        order_value(stock, 10000)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_content)
            f.flush()

            functions = load_jq_strategy(f.name)

            assert "initialize" in functions
            assert "select_stocks" in functions
            assert "get_stock_pool" in functions
            assert "filter_stocks" in functions
            assert len(functions) >= 5

            os.unlink(f.name)


class TestRealStrategyFiles:
    """测试真实策略文件"""

    @pytest.fixture
    def strategy_dir(self):
        """策略目录fixture"""
        return os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "jkcode", "jkcode"
        )

    def test_load_real_etf_strategy(self, strategy_dir):
        """测试加载真实ETF策略"""
        strategy_file = os.path.join(strategy_dir, "06 iAlpha 基金投资策略.txt")

        if os.path.exists(strategy_file):
            functions = load_jq_strategy(strategy_file)

            assert functions is not None
            assert len(functions) >= 1

    def test_load_real_fundamental_strategy(self, strategy_dir):
        """测试加载真实基本面策略"""
        strategy_file = os.path.join(strategy_dir, "04 红利搬砖，年化29%.txt")

        if os.path.exists(strategy_file):
            functions = load_jq_strategy(strategy_file)

            assert functions is not None
            assert "initialize" in functions

    def test_load_real_index_strategy(self, strategy_dir):
        """测试加载真实指数跟踪策略"""
        strategy_file = os.path.join(
            strategy_dir, "05 价值低波（下）--十年十倍（2020拜年）.txt"
        )

        if os.path.exists(strategy_file):
            functions = load_jq_strategy(strategy_file)

            assert functions is not None
            assert "initialize" in functions

    def test_multiple_real_strategies(self, strategy_dir):
        """测试批量加载真实策略"""
        whitelist_strategies = [
            "04 红利搬砖，年化29%.txt",
            "22 “开弓”ETF轮动模型——改.txt",
            "61 简单ETF策略，年化97%.txt",
        ]

        success_count = 0
        for strategy_name in whitelist_strategies:
            strategy_file = os.path.join(strategy_dir, strategy_name)

            if os.path.exists(strategy_file):
                try:
                    functions = load_jq_strategy(strategy_file)
                    if functions and len(functions) > 0:
                        success_count += 1
                except Exception:
                    pass

        assert success_count >= 2


class TestEdgeCases:
    """测试边界情况"""

    def test_nonexistent_file(self):
        """测试不存在的文件"""
        with pytest.raises(FileNotFoundError):
            load_jq_strategy("/nonexistent/path/to/strategy.txt")

    def test_special_characters_in_filename(self):
        """测试文件名包含特殊字符"""
        strategy_content = """
def initialize(context):
    pass
"""

        special_names = [
            "策略-测试.txt",
            "strategy_test_2024.txt",
            "带空格的策略名.txt",
        ]

        for name in special_names:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False, prefix=name[:10]
            ) as f:
                f.write(strategy_content)
                f.flush()

                functions = load_jq_strategy(f.name)
                assert functions is not None

                os.unlink(f.name)

    def test_encoding_variations(self):
        """测试不同编码的文件"""
        strategy_content_utf8 = """
def initialize(context):
    log.info('UTF-8编码')
"""
        strategy_content_gbk = """
def initialize(context):
    log.info('GBK编码')
""".encode("gbk")

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(strategy_content_utf8)
            f.flush()

            functions = load_jq_strategy(f.name)
            assert functions is not None

            os.unlink(f.name)

    def test_large_strategy_file(self):
        """测试大型策略文件"""
        large_strategy = """
def initialize(context):
    pass

def helper_1():
    pass

def helper_2():
    pass

def helper_3():
    pass
"""

        for i in range(4, 100):
            large_strategy += f"\ndef helper_{i}():\n    pass\n"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(large_strategy)
            f.flush()

            functions = load_jq_strategy(f.name)

            assert functions is not None
            assert len(functions) >= 100

            os.unlink(f.name)


class TestWhitelistMetrics:
    """测试白名单指标"""

    def test_success_rate_calculation(self):
        """测试成功率计算"""
        results = [
            {"status": "success"},
            {"status": "success"},
            {"status": "failed"},
            {"status": "error"},
            {"status": "success"},
        ]

        success_count = len([r for r in results if r["status"] == "success"])
        total_count = len(results)
        success_rate = success_count / total_count

        assert success_count == 3
        assert success_rate == 0.6

    def test_strategy_type_distribution(self):
        """测试策略类型分布"""
        strategies = [
            {"priority_type": ["ETF轮动", "指数跟踪"]},
            {"priority_type": ["指数跟踪", "基本面选股"]},
            {"priority_type": ["ETF轮动"]},
            {"priority_type": ["基本面选股"]},
            {"priority_type": ["指数跟踪"]},
        ]

        etf_count = len([s for s in strategies if "ETF轮动" in s["priority_type"]])
        index_count = len([s for s in strategies if "指数跟踪" in s["priority_type"]])
        fundamental_count = len(
            [s for s in strategies if "基本面选股" in s["priority_type"]]
        )

        assert etf_count == 2
        assert index_count == 3
        assert fundamental_count == 2

    def test_function_count_statistics(self):
        """测试函数数量统计"""
        results = [
            {"function_count": 3},
            {"function_count": 8},
            {"function_count": 12},
            {"function_count": 2},
            {"function_count": 5},
        ]

        avg_count = sum([r["function_count"] for r in results]) / len(results)
        max_count = max([r["function_count"] for r in results])
        min_count = min([r["function_count"] for r in results])

        assert avg_count == 6.0
        assert max_count == 12
        assert min_count == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
