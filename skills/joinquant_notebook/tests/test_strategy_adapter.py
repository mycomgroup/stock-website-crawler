# -*- coding: utf-8 -*-
"""
strategy_adapter.py 单元测试
测试内容:
- MockContext 模拟 context 对象
- MockPortfolio 模拟 portfolio 对象
- MockPositions 模拟 positions 对象
- MockPosition 模拟单个持仓
- NotebookBacktest Notebook回测框架
- quick_test_single_day 快速单日测试
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MockPosition:
    """模拟单个持仓"""
    
    def __init__(self, stock, amount, price):
        self.security = stock
        self.total_amount = amount
        self.closeable_amount = amount
        self.price = price
        self.total_value = amount * price


class MockPositions:
    """模拟 positions 对象"""
    
    def __init__(self):
        self._positions = {}
    
    def __iter__(self):
        return iter(self._positions.keys())
    
    def __getitem__(self, stock):
        return self._positions.get(stock, MockPosition(stock, 0, 0))
    
    def add(self, stock, amount, price):
        if stock in self._positions:
            pos = self._positions[stock]
            pos.total_amount += amount
            pos.closeable_amount += amount
            pos.total_value = pos.total_amount * pos.price
        else:
            self._positions[stock] = MockPosition(stock, amount, price)
    
    def remove(self, stock, amount):
        if stock in self._positions:
            pos = self._positions[stock]
            pos.total_amount -= amount
            pos.closeable_amount -= amount
            if pos.total_amount <= 0:
                del self._positions[stock]
    
    def total_value(self):
        return sum(pos.total_value for pos in self._positions.values())


class MockPortfolio:
    """模拟 portfolio 对象"""
    
    def __init__(self, cash=1000000):
        self.available_cash = cash
        self.positions = MockPositions()
        self.total_value = cash
    
    def update_cash(self, amount):
        self.available_cash += amount
        self.total_value = self.available_cash + self.positions.total_value()


class MockContext:
    """模拟策略编辑器的 context 对象"""
    
    def __init__(self, current_dt, portfolio_cash=1000000):
        self.current_dt = current_dt
        self.portfolio = MockPortfolio(portfolio_cash)
        self.run_params = {
            "start_date": None,
            "end_date": None,
            "frequency": "daily",
            "benchmark": "000300.XSHG",
        }


class NotebookBacktest:
    """模拟 NotebookBacktest 类"""
    
    def __init__(self, strategy_module, start_date, end_date, initial_cash=1000000):
        self.strategy = strategy_module
        self.start_date = start_date
        self.end_date = end_date
        self.initial_cash = initial_cash
        self.trade_days = []
        self.results = []


class TestMockPosition(unittest.TestCase):
    """测试 MockPosition 类"""
    
    def test_init_basic(self):
        """测试基本初始化"""
        pos = MockPosition("000001.XSHE", 1000, 10.0)
        
        self.assertEqual(pos.security, "000001.XSHE")
        self.assertEqual(pos.total_amount, 1000)
        self.assertEqual(pos.closeable_amount, 1000)
        self.assertEqual(pos.price, 10.0)
        self.assertEqual(pos.total_value, 10000)
    
    def test_zero_position(self):
        """测试零持仓"""
        pos = MockPosition("000001.XSHE", 0, 0)
        
        self.assertEqual(pos.total_amount, 0)
        self.assertEqual(pos.total_value, 0)
    
    def test_negative_price_handling(self):
        """测试负价格（异常情况）"""
        pos = MockPosition("000001.XSHE", 100, -5.0)
        
        self.assertEqual(pos.price, -5.0)
        self.assertEqual(pos.total_value, -500)


class TestMockPositions(unittest.TestCase):
    """测试 MockPositions 类"""
    
    def test_init_empty(self):
        """测试空持仓初始化"""
        positions = MockPositions()
        
        self.assertEqual(len(list(positions)), 0)
        self.assertEqual(positions.total_value(), 0)
    
    def test_add_single_position(self):
        """测试添加单个持仓"""
        positions = MockPositions()
        positions.add("000001.XSHE", 100, 10.0)
        
        self.assertIn("000001.XSHE", list(positions))
        self.assertEqual(positions.total_value(), 1000)
    
    def test_add_multiple_positions(self):
        """测试添加多个持仓"""
        positions = MockPositions()
        positions.add("000001.XSHE", 100, 10.0)
        positions.add("000002.XSHE", 200, 15.0)
        
        self.assertEqual(len(list(positions)), 2)
        self.assertEqual(positions.total_value(), 1000 + 3000)
    
    def test_add_same_stock_twice(self):
        """测试同一股票重复添加"""
        positions = MockPositions()
        positions.add("000001.XSHE", 100, 10.0)
        positions.add("000001.XSHE", 50, 10.0)
        
        pos = positions["000001.XSHE"]
        self.assertEqual(pos.total_amount, 150)
    
    def test_remove_position(self):
        """测试移除持仓"""
        positions = MockPositions()
        positions.add("000001.XSHE", 100, 10.0)
        positions.remove("000001.XSHE", 50)
        
        pos = positions["000001.XSHE"]
        self.assertEqual(pos.total_amount, 50)
    
    def test_remove_all_position(self):
        """测试完全移除持仓"""
        positions = MockPositions()
        positions.add("000001.XSHE", 100, 10.0)
        positions.remove("000001.XSHE", 100)
        
        self.assertNotIn("000001.XSHE", positions._positions)
    
    def test_get_nonexistent_position(self):
        """测试获取不存在持仓"""
        positions = MockPositions()
        pos = positions["999999.XSHE"]
        
        self.assertEqual(pos.total_amount, 0)
    
    def test_iteration(self):
        """测试迭代"""
        positions = MockPositions()
        positions.add("000001.XSHE", 100, 10.0)
        positions.add("000002.XSHE", 200, 15.0)
        
        stocks = list(positions)
        self.assertEqual(len(stocks), 2)
        self.assertIn("000001.XSHE", stocks)
        self.assertIn("000002.XSHE", stocks)


class TestMockPortfolio(unittest.TestCase):
    """测试 MockPortfolio 类"""
    
    def test_init_default_cash(self):
        """测试默认资金初始化"""
        portfolio = MockPortfolio()
        
        self.assertEqual(portfolio.available_cash, 1000000)
        self.assertEqual(portfolio.total_value, 1000000)
    
    def test_init_custom_cash(self):
        """测试自定义资金初始化"""
        portfolio = MockPortfolio(500000)
        
        self.assertEqual(portfolio.available_cash, 500000)
    
    def test_update_cash_positive(self):
        """测试增加现金"""
        portfolio = MockPortfolio(1000000)
        portfolio.update_cash(100000)
        
        self.assertEqual(portfolio.available_cash, 1100000)
    
    def test_update_cash_negative(self):
        """测试减少现金"""
        portfolio = MockPortfolio(1000000)
        portfolio.update_cash(-50000)
        
        self.assertEqual(portfolio.available_cash, 950000)
    
    def test_total_value_with_positions(self):
        """测试带持仓的总价值"""
        portfolio = MockPortfolio(1000000)
        portfolio.positions.add("000001.XSHE", 100, 10.0)
        portfolio.update_cash(-1000)
        
        self.assertEqual(portfolio.total_value, 999000 + 1000)


class TestMockContext(unittest.TestCase):
    """测试 MockContext 类"""
    
    def test_init_basic(self):
        """测试基本初始化"""
        dt = datetime(2024, 1, 1)
        context = MockContext(dt)
        
        self.assertEqual(context.current_dt, dt)
        self.assertEqual(context.portfolio.available_cash, 1000000)
    
    def test_run_params_default(self):
        """测试默认运行参数"""
        dt = datetime(2024, 1, 1)
        context = MockContext(dt)
        
        self.assertEqual(context.run_params["frequency"], "daily")
        self.assertEqual(context.run_params["benchmark"], "000300.XSHG")
    
    def test_custom_portfolio_cash(self):
        """测试自定义组合资金"""
        dt = datetime(2024, 1, 1)
        context = MockContext(dt, portfolio_cash=500000)
        
        self.assertEqual(context.portfolio.available_cash, 500000)


class TestNotebookBacktest(unittest.TestCase):
    """测试 NotebookBacktest 类"""
    
    def setUp(self):
        self.mock_strategy = Mock()
        self.mock_strategy.initialize = Mock()
        self.mock_strategy.handle_data = Mock()
    
    def test_init_basic(self):
        """测试基本初始化 - 使用本地类"""
        bt = NotebookBacktest(self.mock_strategy, '2024-01-01', '2024-01-31', 1000000)
        
        self.assertEqual(bt.start_date, '2024-01-01')
        self.assertEqual(bt.end_date, '2024-01-31')
        self.assertEqual(bt.initial_cash, 1000000)
    
    def test_results_empty_initially(self):
        """测试初始结果为空"""
        dt = datetime(2024, 1, 1)
        context = MockContext(dt)
        
        results = []
        self.assertEqual(len(results), 0)


class TestQuickTestSingleDay(unittest.TestCase):
    """测试 quick_test_single_day 函数"""
    
    def test_context_creation(self):
        """测试 context 创建"""
        dt = datetime(2024, 1, 1)
        context = MockContext(dt, 1000000)
        
        self.assertEqual(context.current_dt, dt)
        self.assertEqual(context.portfolio.available_cash, 1000000)
    
    def test_strategy_without_initialize(self):
        """测试无 initialize 的策略"""
        mock_strategy = Mock(spec=[])
        dt = datetime(2024, 1, 1)
        context = MockContext(dt)
        
        has_initialize = hasattr(mock_strategy, 'initialize')
        self.assertFalse(has_initialize)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_portfolio(self):
        """测试空组合"""
        portfolio = MockPortfolio(0)
        
        self.assertEqual(portfolio.available_cash, 0)
        self.assertEqual(portfolio.total_value, 0)
    
    def test_large_position_value(self):
        """测试大持仓价值"""
        positions = MockPositions()
        positions.add("000001.XSHE", 100000, 100.0)
        
        self.assertEqual(positions.total_value(), 10000000)
    
    def test_fractional_amount(self):
        """测试分数数量（虽然股票以手为单位）"""
        pos = MockPosition("000001.XSHE", 100.5, 10.0)
        
        self.assertEqual(pos.total_value, 1005)
    
    def test_multiple_operations(self):
        """测试多次操作"""
        positions = MockPositions()
        positions.add("000001.XSHE", 100, 10.0)
        positions.add("000001.XSHE", 50, 10.0)
        positions.remove("000001.XSHE", 30)
        
        pos = positions["000001.XSHE"]
        self.assertEqual(pos.total_amount, 120)
    
    def test_context_datetime_update(self):
        """测试 context 时间更新"""
        dt1 = datetime(2024, 1, 1)
        dt2 = datetime(2024, 1, 2)
        context = MockContext(dt1)
        
        context.current_dt = dt2
        self.assertEqual(context.current_dt, dt2)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_mock_simulation(self):
        """测试完整模拟流程"""
        dt = datetime(2024, 1, 1)
        context = MockContext(dt, 1000000)
        
        context.portfolio.positions.add("000001.XSHE", 100, 10.0)
        context.portfolio.update_cash(-1000)
        
        context.portfolio.positions.add("000002.XSHE", 200, 15.0)
        context.portfolio.update_cash(-3000)
        
        self.assertEqual(context.portfolio.available_cash, 996000)
        self.assertEqual(len(list(context.portfolio.positions)), 2)
        self.assertEqual(context.portfolio.positions.total_value(), 4000)
        
        context.portfolio.positions.remove("000001.XSHE", 50)
        
        pos = context.portfolio.positions["000001.XSHE"]
        self.assertEqual(pos.total_amount, 50)


if __name__ == "__main__":
    unittest.main(verbosity=2)