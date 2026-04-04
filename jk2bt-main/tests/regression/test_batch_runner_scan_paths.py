#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TEST-1: 批量Runner回归测试

覆盖P0/P1关键功能:
1. 扫描成功路径 - scanner正确识别可执行策略
2. 扫描拒绝路径 - scanner正确拒绝非策略/语法错误/缺失API
3. scan_results非空 - run_strategies_parallel返回scan_results字段
4. 状态归因正确 - _classify_run_status正确分类各种运行状态

这些测试确保核心功能不再回归。
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from concurrent.futures import TimeoutError as FuturesTimeoutError
import json
from pathlib import Path

# 设置路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestScannerSuccessPath(unittest.TestCase):
    """
    P0: 扫描成功路径测试

    确保scanner能正确识别可执行策略，包括:
    - 有initialize + run_daily
    - 有initialize + handle_data
    - 有initialize + before_trading_start
    """

    def setUp(self):
        from jk2bt.strategy.scanner import StrategyScanner, StrategyStatus
        self.scanner = StrategyScanner()
        self.StrategyStatus = StrategyStatus
        self.temp_files = []

    def tearDown(self):
        for f in self.temp_files:
            if os.path.exists(f):
                os.unlink(f)

    def _create_temp_strategy(self, code, suffix=".txt"):
        """创建临时策略文件"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False) as f:
            f.write(code)
            f.flush()
            self.temp_files.append(f.name)
            return f.name

    def test_scan_success_with_run_daily(self):
        """P0: 有initialize + run_daily的策略应被识别为可执行"""
        code = '''
def initialize(context):
    set_option('use_real_price', True)
    run_daily(my_trade, 'open')

def my_trade(context):
    order_value('600519.XSHG', 10000)
'''
        filepath = self._create_temp_strategy(code)
        result = self.scanner.scan_file(filepath)

        self.assertTrue(result.has_initialize, "应检测到initialize函数")
        self.assertTrue(result.is_executable, "应被识别为可执行策略")
        self.assertEqual(result.status, self.StrategyStatus.VALID)
        self.assertEqual(len(result.missing_apis), 0, "不应有缺失API")

    def test_scan_success_with_handle_data(self):
        """P0: 有initialize + handle_data的策略应被识别为可执行"""
        code = '''
def initialize(context):
    set_benchmark('000300.XSHG')

def handle_data(context, data):
    order('600519.XSHG', 100)
'''
        filepath = self._create_temp_strategy(code)
        result = self.scanner.scan_file(filepath)

        self.assertTrue(result.has_initialize)
        self.assertTrue(result.has_handle)
        self.assertTrue(result.is_executable)
        self.assertEqual(result.status, self.StrategyStatus.VALID)

    def test_scan_success_with_before_trading_start(self):
        """P0: 有initialize + before_trading_start的策略应被识别为可执行"""
        code = '''
def initialize(context):
    pass

def before_trading_start(context):
    stocks = get_index_stocks('000300.XSHG')

def handle_data(context, data):
    pass
'''
        filepath = self._create_temp_strategy(code)
        result = self.scanner.scan_file(filepath)

        self.assertTrue(result.has_initialize)
        self.assertTrue(result.has_handle)
        self.assertTrue(result.is_executable)

    def test_scan_success_with_after_trading_end(self):
        """P0: 有initialize + after_trading_end的策略应被识别为可执行"""
        code = '''
def initialize(context):
    pass

def after_trading_end(context):
    log.info('trading ended')

def handle_data(context, data):
    pass
'''
        filepath = self._create_temp_strategy(code)
        result = self.scanner.scan_file(filepath)

        self.assertTrue(result.has_initialize)
        self.assertTrue(result.has_handle)
        self.assertTrue(result.is_executable)

    def test_scan_success_with_run_weekly(self):
        """P0: run_weekly也应被视为有效的handle函数模式"""
        code = '''
def initialize(context):
    run_weekly(rebalance, 1)

def rebalance(context):
    order_target('600519.XSHG', 100)
'''
        filepath = self._create_temp_strategy(code)
        result = self.scanner.scan_file(filepath)

        self.assertTrue(result.has_initialize)
        self.assertTrue(result.is_executable)

    def test_scan_success_with_run_monthly(self):
        """P0: run_monthly也应被视为有效的handle函数模式"""
        code = '''
def initialize(context):
    run_monthly(rebalance, 1)

def rebalance(context):
    order_target_value('600519.XSHG', 10000)
'''
        filepath = self._create_temp_strategy(code)
        result = self.scanner.scan_file(filepath)

        self.assertTrue(result.has_initialize)
        self.assertTrue(result.is_executable)

    def test_scan_result_to_dict(self):
        """P0: ScanResult.to_dict应正确序列化所有字段"""
        code = '''
def initialize(context):
    pass
def handle_data(context, data):
    pass
'''
        filepath = self._create_temp_strategy(code)
        result = self.scanner.scan_file(filepath)
        result_dict = result.to_dict()

        self.assertIn('file_path', result_dict)
        self.assertIn('file_name', result_dict)
        self.assertIn('status', result_dict)
        self.assertIn('has_initialize', result_dict)
        self.assertIn('has_handle', result_dict)
        self.assertIn('missing_apis', result_dict)
        self.assertIn('is_executable', result_dict)
        self.assertTrue(result_dict['is_executable'])


class TestScannerRejectPath(unittest.TestCase):
    """
    P1: 扫描拒绝路径测试

    确保scanner正确拒绝以下类型:
    - NOT_STRATEGY: 非策略文件（文档、notebook等）
    - SYNTAX_ERROR: 语法错误
    - NO_INITIALIZE: 缺少initialize函数
    - MISSING_API: 缺失未实现的API
    - EMPTY_FILE: 空文件
    """

    def setUp(self):
        from jk2bt.strategy.scanner import StrategyScanner, StrategyStatus
        self.scanner = StrategyScanner()
        self.StrategyStatus = StrategyStatus
        self.temp_files = []

    def tearDown(self):
        for f in self.temp_files:
            if os.path.exists(f):
                os.unlink(f)

    def _create_temp_file(self, content, filename):
        """创建临时文件"""
        filepath = os.path.join(tempfile.gettempdir(), filename)
        with open(filepath, 'w') as f:
            f.write(content)
        self.temp_files.append(filepath)
        return filepath

    def test_reject_not_strategy_readme(self):
        """P1: README.md应被拒绝"""
        filepath = self._create_temp_file("# README\n", "README.md")
        result = self.scanner.scan_file(filepath)

        self.assertFalse(result.is_executable)
        self.assertEqual(result.status, self.StrategyStatus.NOT_STRATEGY)

    def test_reject_not_strategy_ipynb(self):
        """P1: notebook文件应被拒绝"""
        filepath = self._create_temp_file('{"cells": []}', "test.ipynb")
        result = self.scanner.scan_file(filepath)

        self.assertFalse(result.is_executable)
        self.assertEqual(result.status, self.StrategyStatus.NOT_STRATEGY)

    def test_reject_not_strategy_research_doc(self):
        """P1: 研究文档应被拒绝"""
        filepath = self._create_temp_file("研究说明\n", "研究.txt")
        result = self.scanner.scan_file(filepath)

        self.assertFalse(result.is_executable)
        self.assertEqual(result.status, self.StrategyStatus.NOT_STRATEGY)

    def test_reject_not_strategy_notes(self):
        """P1: 笔记文件应被拒绝"""
        filepath = self._create_temp_file("我的笔记\n", "笔记.txt")
        result = self.scanner.scan_file(filepath)

        self.assertFalse(result.is_executable)
        self.assertEqual(result.status, self.StrategyStatus.NOT_STRATEGY)

    def test_reject_not_strategy_test_file(self):
        """P1: 测试文件应被拒绝"""
        filepath = self._create_temp_file("def test(): pass", "test_strategy.py")
        result = self.scanner.scan_file(filepath)

        self.assertFalse(result.is_executable)
        self.assertEqual(result.status, self.StrategyStatus.NOT_STRATEGY)

    def test_reject_syntax_error_missing_paren(self):
        """P1: 语法错误（缺少括号）应被拒绝"""
        code = '''
def initialize(context):
    log.info('test'
    # 缺少括号
'''
        filepath = self._create_temp_file(code, "syntax_error.txt")
        result = self.scanner.scan_file(filepath)

        self.assertFalse(result.is_executable)
        self.assertEqual(result.status, self.StrategyStatus.SYNTAX_ERROR)
        self.assertIn("语法错误", result.error_message)

    def test_reject_syntax_error_invalid_indent(self):
        """P1: 语法错误（缩进错误）应被拒绝"""
        code = '''
def initialize(context):
pass
'''
        filepath = self._create_temp_file(code, "indent_error.txt")
        result = self.scanner.scan_file(filepath)

        self.assertFalse(result.is_executable)
        self.assertEqual(result.status, self.StrategyStatus.SYNTAX_ERROR)

    def test_reject_no_initialize(self):
        """P1: 缺少initialize函数的策略应被拒绝"""
        code = '''
def my_trade(context):
    order('600519.XSHG', 100)
'''
        filepath = self._create_temp_file(code, "no_init.txt")
        result = self.scanner.scan_file(filepath)

        self.assertFalse(result.has_initialize)
        self.assertFalse(result.is_executable)
        self.assertEqual(result.status, self.StrategyStatus.NO_INITIALIZE)

    def test_reject_missing_api_get_dividends(self):
        """P1: 使用未实现API(get_dividends)的策略应被拒绝"""
        code = '''
def initialize(context):
    pass

def handle_data(context, data):
    div = get_dividends('600519.XSHG')
'''
        filepath = self._create_temp_file(code, "missing_api.txt")
        result = self.scanner.scan_file(filepath)

        self.assertTrue(result.has_initialize)
        self.assertFalse(result.is_executable)
        self.assertEqual(result.status, self.StrategyStatus.MISSING_API)
        self.assertIn("get_dividends", result.missing_apis)

    def test_reject_missing_api_get_splits(self):
        """P1: 使用未实现API(get_splits)的策略应被拒绝"""
        code = '''
def initialize(context):
    pass

def handle_data(context, data):
    splits = get_splits('600519.XSHG')
'''
        filepath = self._create_temp_file(code, "missing_splits.txt")
        result = self.scanner.scan_file(filepath)

        self.assertEqual(result.status, self.StrategyStatus.MISSING_API)
        self.assertIn("get_splits", result.missing_apis)

    def test_reject_missing_api_get_yield_curve(self):
        """P1: 使用未实现API(get_yield_curve)的策略应被拒绝"""
        code = '''
def initialize(context):
    pass

def handle_data(context, data):
    curve = get_yield_curve()
'''
        filepath = self._create_temp_file(code, "missing_yield.txt")
        result = self.scanner.scan_file(filepath)

        self.assertEqual(result.status, self.StrategyStatus.MISSING_API)
        self.assertIn("get_yield_curve", result.missing_apis)

    def test_reject_empty_file(self):
        """P1: 空文件应被拒绝"""
        filepath = self._create_temp_file("", "empty.txt")
        result = self.scanner.scan_file(filepath)

        self.assertFalse(result.is_executable)
        self.assertEqual(result.status, self.StrategyStatus.EMPTY_FILE)

    def test_reject_file_not_exist(self):
        """P1: 不存在的文件应被拒绝"""
        result = self.scanner.scan_file("/nonexistent/path/strategy.txt")

        self.assertFalse(result.is_executable)
        self.assertEqual(result.status, self.StrategyStatus.NOT_STRATEGY)
        self.assertIn("文件不存在", result.error_message)

    def test_reject_only_comments(self):
        """P1: 只有注释的文件应被拒绝"""
        code = '''
# 这只是一个注释文件
# 没有任何策略代码
'''
        filepath = self._create_temp_file(code, "comments_only.txt")
        result = self.scanner.scan_file(filepath)

        self.assertFalse(result.is_executable)


class TestScanResultsNonEmpty(unittest.TestCase):
    """
    P0: scan_results非空测试

    确保run_strategies_parallel在扫描模式下返回scan_results字段，
    且字段结构正确。
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_files = []

    def tearDown(self):
        import shutil
        for f in self.temp_files:
            if os.path.exists(f):
                os.unlink(f)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def _create_strategy(self, name, code):
        """在临时目录创建策略文件"""
        filepath = os.path.join(self.temp_dir, name)
        with open(filepath, 'w') as f:
            f.write(code)
        self.temp_files.append(filepath)
        return filepath

    def test_scan_results_field_exists(self):
        """P0: run_strategies_parallel应返回scan_results字段"""
        from run_strategies_parallel import run_strategies_parallel

        valid_code = '''
def initialize(context):
    pass
def handle_data(context, data):
    pass
'''
        valid_path = self._create_strategy("valid.txt", valid_code)

        # 使用mock避免实际运行策略
        with patch('run_strategies_parallel.run_single_strategy') as mock_run:
            mock_run.return_value = MagicMock(
                strategy="valid.txt",
                strategy_file=valid_path,
                success=True,
                run_status="success_zero_return",
            )

            result = run_strategies_parallel(
                strategy_files=[valid_path],
                skip_scan=False,
            )

            self.assertIn('scan_results', result)
            self.assertIsInstance(result['scan_results'], dict)

    def test_scan_results_has_correct_structure(self):
        """P0: scan_results字段应包含正确的结构"""
        from run_strategies_parallel import run_strategies_parallel

        valid_code = '''
def initialize(context):
    pass
def handle_data(context, data):
    pass
'''
        valid_path = self._create_strategy("valid.txt", valid_code)

        with patch('run_strategies_parallel.run_single_strategy') as mock_run:
            mock_run.return_value = MagicMock(
                strategy="valid.txt",
                strategy_file=valid_path,
                success=True,
                run_status="success_zero_return",
            )

            result = run_strategies_parallel(
                strategy_files=[valid_path],
                skip_scan=False,
            )

            scan_results = result['scan_results']
            self.assertIn(valid_path, scan_results)
            scan_data = scan_results[valid_path]

            # 检查必需字段
            required_fields = ['file_path', 'file_name', 'status',
                              'has_initialize', 'has_handle',
                              'missing_apis', 'is_executable']
            for field in required_fields:
                self.assertIn(field, scan_data)

    def test_scan_results_rejected_file_included(self):
        """P0: 扫描拒绝的文件也应出现在scan_results中"""
        from run_strategies_parallel import run_strategies_parallel

        # 创建一个会被拒绝的文件（无initialize）
        invalid_code = '''
def my_trade(context):
    pass
'''
        invalid_path = self._create_strategy("invalid.txt", invalid_code)

        result = run_strategies_parallel(
            strategy_files=[invalid_path],
            skip_scan=False,
        )

        # scan_results应包含被拒绝的文件
        self.assertIn('scan_results', result)
        self.assertIn(invalid_path, result['scan_results'])

        # 被拒绝文件应标记为不可执行
        scan_data = result['scan_results'][invalid_path]
        self.assertFalse(scan_data['is_executable'])

    def test_scan_results_mixed_files(self):
        """P0: 混合文件场景下scan_results应完整记录所有扫描结果"""
        from run_strategies_parallel import run_strategies_parallel

        valid_code = '''
def initialize(context):
    pass
def handle_data(context, data):
    pass
'''
        invalid_code = '''
def my_func(context):
    pass
'''

        valid_path = self._create_strategy("valid.txt", valid_code)
        invalid_path = self._create_strategy("invalid.txt", invalid_code)

        with patch('run_strategies_parallel.run_single_strategy') as mock_run:
            mock_run.return_value = MagicMock(
                strategy="valid.txt",
                strategy_file=valid_path,
                success=True,
                run_status="success_zero_return",
            )

            result = run_strategies_parallel(
                strategy_files=[valid_path, invalid_path],
                skip_scan=False,
            )

            scan_results = result['scan_results']
            self.assertEqual(len(scan_results), 2)
            self.assertIn(valid_path, scan_results)
            self.assertIn(invalid_path, scan_results)


class TestStatusAttribution(unittest.TestCase):
    """
    P1: 状态归因正确性测试

    确保_classify_run_status正确分类各种运行状态:
    - SUCCESS_WITH_RETURN: 成功且有收益
    - SUCCESS_ZERO_RETURN: 成功但零收益
    - SUCCESS_NO_TRADE: 成功但无交易
    - LOAD_FAILED: 加载失败
    - RUN_EXCEPTION: 运行异常
    - TIMEOUT: 超时
    - DATA_MISSING: 数据缺失
    - MISSING_DEPENDENCY: 依赖缺失
    - MISSING_API: API缺失
    """

    def setUp(self):
        from run_strategies_parallel import RunStatus, _classify_run_status
        self.RunStatus = RunStatus
        self._classify_run_status = _classify_run_status

    def test_success_with_return_positive_pnl(self):
        """P1: 有正收益应归类为SUCCESS_WITH_RETURN"""
        mock_strategy = MagicMock()
        mock_strategy.navs = {'2022-01-01': 1.0, '2022-01-02': 1.1}

        backtest_result = {
            'strategy': mock_strategy,
            'pnl_pct': 10.0,
        }
        evidence = {
            'loaded': True,
            'entered_backtest_loop': True,
            'has_nav_series': True,
            'has_transactions': True,
        }

        status = self._classify_run_status(
            backtest_result=backtest_result,
            exception=None,
            has_data=True,
            scan_result=None,
            evidence=evidence,
        )
        self.assertEqual(status, self.RunStatus.SUCCESS_WITH_RETURN)

    def test_success_with_return_negative_pnl(self):
        """P1: 有负收益也应归类为SUCCESS_WITH_RETURN"""
        mock_strategy = MagicMock()
        mock_strategy.navs = {'2022-01-01': 1.0, '2022-01-02': 0.9}

        backtest_result = {
            'strategy': mock_strategy,
            'pnl_pct': -10.0,
        }
        evidence = {
            'loaded': True,
            'entered_backtest_loop': True,
            'has_nav_series': True,
            'has_transactions': True,
        }

        status = self._classify_run_status(
            backtest_result=backtest_result,
            exception=None,
            has_data=True,
            scan_result=None,
            evidence=evidence,
        )
        self.assertEqual(status, self.RunStatus.SUCCESS_WITH_RETURN)

    def test_success_zero_return(self):
        """P1: 零收益应归类为SUCCESS_ZERO_RETURN"""
        mock_strategy = MagicMock()
        mock_strategy.navs = {'2022-01-01': 1.0, '2022-01-02': 1.0}

        backtest_result = {
            'strategy': mock_strategy,
            'pnl_pct': 0.0,
        }
        evidence = {
            'loaded': True,
            'entered_backtest_loop': True,
            'has_nav_series': True,
            'has_transactions': False,
        }

        status = self._classify_run_status(
            backtest_result=backtest_result,
            exception=None,
            has_data=True,
            scan_result=None,
            evidence=evidence,
        )
        self.assertEqual(status, self.RunStatus.SUCCESS_ZERO_RETURN)

    def test_success_no_trade_no_nav(self):
        """P1: 无交易无nav应归类为SUCCESS_NO_TRADE"""
        mock_strategy = MagicMock()
        mock_strategy.navs = None

        backtest_result = {
            'strategy': mock_strategy,
            'pnl_pct': 0.0,
        }
        evidence = {
            'loaded': True,
            'entered_backtest_loop': True,
            'has_nav_series': False,
            'has_transactions': False,
        }

        status = self._classify_run_status(
            backtest_result=backtest_result,
            exception=None,
            has_data=True,
            scan_result=None,
            evidence=evidence,
        )
        self.assertEqual(status, self.RunStatus.SUCCESS_NO_TRADE)

    def test_load_failed_no_result(self):
        """P1: 无回测结果应归类为LOAD_FAILED"""
        status = self._classify_run_status(
            backtest_result=None,
            exception=None,
            has_data=True,
            scan_result=None,
            evidence={'loaded': False},
        )
        self.assertEqual(status, self.RunStatus.LOAD_FAILED)

    def test_run_exception_generic(self):
        """P1: 普通异常应归类为RUN_EXCEPTION"""
        exception = ValueError("some error")
        status = self._classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=True,
            scan_result=None,
        )
        self.assertEqual(status, self.RunStatus.RUN_EXCEPTION)

    def test_timeout(self):
        """P1: TimeoutError应归类为TIMEOUT"""
        exception = FuturesTimeoutError()
        status = self._classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=True,
            scan_result=None,
        )
        self.assertEqual(status, self.RunStatus.TIMEOUT)

    def test_data_missing_chinese_keyword(self):
        """P1: 包含中文关键词的异常应归类为DATA_MISSING"""
        exception = Exception("无数据")
        status = self._classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=False,
            scan_result=None,
        )
        self.assertEqual(status, self.RunStatus.DATA_MISSING)

    def test_data_missing_stock_keyword(self):
        """P1: 包含股票关键词的异常应归类为DATA_MISSING"""
        exception = Exception("找不到股票数据")
        status = self._classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=False,
            scan_result=None,
        )
        self.assertEqual(status, self.RunStatus.DATA_MISSING)

    def test_missing_dependency_module_keyword(self):
        """P1: 包含module关键词的异常应归类为MISSING_DEPENDENCY"""
        exception = ImportError("No module named 'missing_module'")
        status = self._classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=True,
            scan_result=None,
        )
        self.assertEqual(status, self.RunStatus.MISSING_DEPENDENCY)

    def test_missing_dependency_import_keyword(self):
        """P1: 包含import关键词的异常应归类为MISSING_DEPENDENCY"""
        exception = Exception("cannot import name 'missing_func'")
        status = self._classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=True,
            scan_result=None,
        )
        self.assertEqual(status, self.RunStatus.MISSING_DEPENDENCY)

    def test_missing_api_attribute_keyword(self):
        """P1: 包含attribute关键词(不包含module)的异常应归类为MISSING_API"""
        # 注意：异常消息中不应包含"module"，否则会被MISSING_DEPENDENCY优先匹配
        exception = AttributeError("'strategy' object has no attribute 'missing_api'")
        status = self._classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=True,
            scan_result=None,
        )
        self.assertEqual(status, self.RunStatus.MISSING_API)

    def test_missing_api_get_prefix(self):
        """P1: 包含get_前缀的异常应归类为MISSING_API"""
        # 注意：异常消息中不应包含"module"，否则会被MISSING_DEPENDENCY优先匹配
        exception = AttributeError("'strategy' object has no attribute 'get_missing'")
        status = self._classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=True,
            scan_result=None,
        )
        self.assertEqual(status, self.RunStatus.MISSING_API)

    def test_missing_api_with_module_keyword_classified_as_dependency(self):
        """P1: 同时包含module和attribute关键词的异常会被MISSING_DEPENDENCY优先匹配"""
        # 这是分类逻辑的特性：module关键词优先于attribute
        exception = AttributeError("'module' has no attribute 'missing_api'")
        status = self._classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=True,
            scan_result=None,
        )
        # module关键词优先匹配，所以是MISSING_DEPENDENCY
        self.assertEqual(status, self.RunStatus.MISSING_DEPENDENCY)

    def test_missing_api_not_defined(self):
        """P1: 包含not defined关键词的异常应归类为MISSING_API"""
        exception = NameError("name 'missing_api' is not defined")
        status = self._classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=True,
            scan_result=None,
        )
        self.assertEqual(status, self.RunStatus.MISSING_API)

    def test_missing_resource_file_keyword(self):
        """P1: 包含file关键词的异常应归类为MISSING_RESOURCE"""
        exception = FileNotFoundError("file not found")
        status = self._classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=True,
            scan_result=None,
        )
        self.assertEqual(status, self.RunStatus.MISSING_RESOURCE)


class TestBatchRunnerIntegration(unittest.TestCase):
    """
    P0: 批量runner集成测试

    测试run_strategies_parallel的整体流程:
    - 扫描阶段正确分类文件
    - 拒绝文件正确标记
    - 结果结构完整
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def _create_strategy(self, name, code):
        filepath = os.path.join(self.temp_dir, name)
        with open(filepath, 'w') as f:
            f.write(code)
        return filepath

    def test_skipped_not_strategy_in_results(self):
        """P0: NOT_STRATEGY文件应出现在结果中并正确标记"""
        from run_strategies_parallel import run_strategies_parallel, RunStatus

        # 创建一个会被识别为NOT_STRATEGY的文件（研究文档）
        filepath = self._create_strategy("研究说明.txt", "这是一个研究说明文档")

        result = run_strategies_parallel(
            strategy_files=[filepath],
            skip_scan=False,
        )

        # 检查结果
        self.assertIn('results', result)
        results_list = result['results']

        # 应有结果记录
        self.assertEqual(len(results_list), 1)
        item = results_list[0]
        self.assertEqual(item['run_status'], RunStatus.SKIPPED_NOT_STRATEGY.value)
        self.assertFalse(item['success'])

    def test_skipped_syntax_error_in_results(self):
        """P0: SYNTAX_ERROR文件应出现在结果中并正确标记"""
        from run_strategies_parallel import run_strategies_parallel, RunStatus

        code = '''
def initialize(context):
    log.info('test'
'''
        filepath = self._create_strategy("syntax_error.txt", code)

        result = run_strategies_parallel(
            strategy_files=[filepath],
            skip_scan=False,
        )

        results_list = result['results']
        self.assertEqual(len(results_list), 1)
        item = results_list[0]
        self.assertEqual(item['run_status'], RunStatus.SKIPPED_SYNTAX_ERROR.value)
        self.assertFalse(item['success'])

    def test_skipped_no_initialize_in_results(self):
        """P0: NO_INITIALIZE文件应出现在结果中并正确标记"""
        from run_strategies_parallel import run_strategies_parallel, RunStatus

        code = '''
def my_trade(context):
    pass
'''
        filepath = self._create_strategy("no_init.txt", code)

        result = run_strategies_parallel(
            strategy_files=[filepath],
            skip_scan=False,
        )

        results_list = result['results']
        self.assertEqual(len(results_list), 1)
        item = results_list[0]
        self.assertEqual(item['run_status'], RunStatus.SKIPPED_NO_INITIALIZE.value)
        self.assertFalse(item['success'])

    def test_summary_status_counts(self):
        """P0: summary应包含正确的status_counts"""
        from run_strategies_parallel import run_strategies_parallel

        valid_code = '''
def initialize(context):
    pass
def handle_data(context, data):
    pass
'''
        invalid_code = '''
def my_func(context):
    pass
'''

        valid_path = self._create_strategy("valid.txt", valid_code)
        invalid_path = self._create_strategy("invalid.txt", invalid_code)

        with patch('run_strategies_parallel.run_single_strategy') as mock_run:
            mock_run.return_value = MagicMock(
                strategy="valid.txt",
                strategy_file=valid_path,
                success=True,
                run_status="success_zero_return",
            )

            result = run_strategies_parallel(
                strategy_files=[valid_path, invalid_path],
                skip_scan=False,
            )

            self.assertIn('status_counts', result['summary'])
            # 至少有valid和invalid两种状态
            self.assertGreater(len(result['summary']['status_counts']), 0)


class TestAPINameMapping(unittest.TestCase):
    """
    P1: API名称映射测试

    确保scanner正确处理API名称映射，避免误判已实现的API。
    """

    def setUp(self):
        from jk2bt.strategy.scanner import StrategyScanner, StrategyStatus
        self.scanner = StrategyScanner()
        self.StrategyStatus = StrategyStatus
        self.temp_files = []

    def tearDown(self):
        for f in self.temp_files:
            if os.path.exists(f):
                os.unlink(f)

    def _create_temp_strategy(self, code):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(code)
            f.flush()
            self.temp_files.append(f.name)
            return f.name

    def test_get_ticks_not_missing(self):
        """P1: get_ticks通过名称映射已实现，不应被标记为缺失"""
        code = '''
def initialize(context):
    pass

def handle_data(context, data):
    ticks = get_ticks('600519.XSHG')
'''
        filepath = self._create_temp_strategy(code)
        result = self.scanner.scan_file(filepath)

        # get_ticks映射到get_ticks_enhanced，已实现
        self.assertNotIn('get_ticks', result.missing_apis)
        self.assertEqual(result.status, self.StrategyStatus.VALID)

    def test_get_future_contracts_not_missing(self):
        """P1: get_future_contracts已实现，不应被标记为缺失"""
        code = '''
def initialize(context):
    pass

def handle_data(context, data):
    contracts = get_future_contracts('IF')
'''
        filepath = self._create_temp_strategy(code)
        result = self.scanner.scan_file(filepath)

        self.assertNotIn('get_future_contracts', result.missing_apis)

    def test_get_margin_stocks_not_missing(self):
        """P1: get_margin_stocks映射到新接口，不应被标记为缺失"""
        code = '''
def initialize(context):
    pass

def handle_data(context, data):
    stocks = get_margin_stocks()
'''
        filepath = self._create_temp_strategy(code)
        result = self.scanner.scan_file(filepath)

        # get_margin_stocks映射到get_margincash_stocks/get_marginsec_stocks
        self.assertNotIn('get_margin_stocks', result.missing_apis)


class TestEvidenceBasedClassification(unittest.TestCase):
    """
    P0: 证据驱动的状态分类测试

    确保_classify_run_status正确使用evidence字段进行分类。
    """

    def setUp(self):
        from run_strategies_parallel import RunStatus, _classify_run_status
        self.RunStatus = RunStatus
        self._classify_run_status = _classify_run_status

    def test_evidence_loaded_false(self):
        """P0: evidence.loaded=False应归类为LOAD_FAILED"""
        evidence = {
            'loaded': False,
            'entered_backtest_loop': False,
            'has_nav_series': False,
        }

        status = self._classify_run_status(
            backtest_result={'strategy': None},
            exception=None,
            has_data=True,
            scan_result=None,
            evidence=evidence,
        )
        self.assertEqual(status, self.RunStatus.LOAD_FAILED)

    def test_evidence_entered_backtest_loop_false(self):
        """P0: evidence.entered_backtest_loop=False但有nav应归类为SUCCESS_NO_TRADE"""
        mock_strategy = MagicMock()
        mock_strategy.navs = {'2022-01-01': 1.0}

        evidence = {
            'loaded': True,
            'entered_backtest_loop': False,
            'has_nav_series': True,
            'has_transactions': False,
        }

        backtest_result = {
            'strategy': mock_strategy,
            'pnl_pct': 0.0,
        }

        status = self._classify_run_status(
            backtest_result=backtest_result,
            exception=None,
            has_data=True,
            scan_result=None,
            evidence=evidence,
        )
        self.assertEqual(status, self.RunStatus.SUCCESS_NO_TRADE)

    def test_evidence_all_true_with_nav(self):
        """P0: evidence全部为True且有nav应正确分类"""
        evidence = {
            'loaded': True,
            'entered_backtest_loop': True,
            'has_nav_series': True,
            'has_transactions': True,
        }

        mock_strategy = MagicMock()
        mock_strategy.navs = {'2022-01-01': 1.0, '2022-01-02': 1.05}

        backtest_result = {
            'strategy': mock_strategy,
            'pnl_pct': 5.0,
        }

        status = self._classify_run_status(
            backtest_result=backtest_result,
            exception=None,
            has_data=True,
            scan_result=None,
            evidence=evidence,
        )
        self.assertEqual(status, self.RunStatus.SUCCESS_WITH_RETURN)


class TestScanCache(unittest.TestCase):
    """
    P1: Scanner缓存测试

    确保scanner正确使用缓存避免重复扫描。
    """

    def setUp(self):
        from jk2bt.strategy.scanner import StrategyScanner
        self.scanner = StrategyScanner()
        self.temp_files = []

    def tearDown(self):
        for f in self.temp_files:
            if os.path.exists(f):
                os.unlink(f)

    def _create_temp_strategy(self, code):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(code)
            f.flush()
            self.temp_files.append(f.name)
            return f.name

    def test_scan_result_cached(self):
        """P1: 同一文件的第二次扫描应使用缓存"""
        code = '''
def initialize(context):
    pass
def handle_data(context, data):
    pass
'''
        filepath = self._create_temp_strategy(code)

        # 第一次扫描
        result1 = self.scanner.scan_file(filepath)
        self.assertIn(filepath, self.scanner._cache)

        # 第二次扫描应返回相同对象
        result2 = self.scanner.scan_file(filepath)
        self.assertEqual(result1, result2)


if __name__ == '__main__':
    unittest.main(verbosity=2)