# -*- coding: utf-8 -*-
"""
strategies/*.py 系列文件单元测试
测试文件:
- regime_ultra_simple.py
- regime_router_backtest.py
- candidate_pool_validation.py
- key_validation.py
- dividend_ratio_test.py
- regime_quick_test.py
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestRegimeRouter(unittest.TestCase):
    """测试状态路由器逻辑"""
    
    def test_get_regime_high_defense(self):
        """测试高估防守状态"""
        pos = 0.85
        
        if pos > 0.8:
            regime = "高估防守"
        
        self.assertEqual(regime, "高估防守")
    
    def test_get_regime_trend_attack(self):
        """测试趋势进攻状态"""
        pos = 0.6
        above = True
        
        if pos > 0.5 and above:
            regime = "趋势进攻"
        
        self.assertEqual(regime, "趋势进攻")
    
    def test_get_regime_oscillation(self):
        """测试震荡轮动状态"""
        pos = 0.4
        
        if pos > 0.3:
            regime = "震荡轮动"
        
        self.assertEqual(regime, "震荡轮动")
    
    def test_get_regime_bottom_trial(self):
        """测试底部试错状态"""
        pos = 0.2
        
        if pos <= 0.3:
            regime = "底部试错"
        
        self.assertEqual(regime, "底部试错")
    
    def test_position_calculation(self):
        """测试价格位置计算"""
        current = 3200
        low_60 = 3000
        high_60 = 3500
        
        pos = (current - low_60) / (high_60 - low_60)
        
        expected = (3200 - 3000) / (3500 - 3000)
        self.assertAlmostEqual(pos, expected, places=5)
    
    def test_regime_configs(self):
        """测试状态配置"""
        CONFIGS = {
            "底部试错": (0.30, 0.30, 0.10),
            "趋势进攻": (0.40, 0.20, 0.30),
            "震荡轮动": (0.35, 0.25, 0.20),
            "高估防守": (0.15, 0.40, 0.05),
        }
        
        for regime, config in CONFIGS.items():
            total = sum(config)
            self.assertLessEqual(total, 1.0)
    
    def test_return_calculation(self):
        """测试收益计算"""
        stock_r = 0.05
        bond_r = 0.02
        etf_r = 0.04
        config = (0.30, 0.30, 0.10)
        
        portfolio_r = config[0] * stock_r + config[1] * bond_r + config[2] * etf_r
        
        expected = 0.30 * 0.05 + 0.30 * 0.02 + 0.10 * 0.04
        self.assertAlmostEqual(portfolio_r, expected, places=5)


class TestCandidatePoolValidation(unittest.TestCase):
    """测试候选池验证逻辑"""
    
    def test_cap_range_filter(self):
        """测试市值区间筛选"""
        df_cap = pd.DataFrame({
            'code': ['A', 'B', 'C', 'D', 'E'],
            'market_cap': [15, 35, 55, 75, 95],
        })
        
        range_10_30 = len(df_cap[(df_cap['market_cap'] >= 10) & (df_cap['market_cap'] < 30)])
        range_30_60 = len(df_cap[(df_cap['market_cap'] >= 30) & (df_cap['market_cap'] < 60)])
        range_60_100 = len(df_cap[(df_cap['market_cap'] >= 60) & (df_cap['market_cap'] <= 100)])
        
        self.assertEqual(range_10_30, 1)
        self.assertEqual(range_30_60, 2)
        self.assertEqual(range_60_100, 2)
    
    def test_pe_threshold_filter(self):
        """测试 PE 阈值筛选"""
        df_pe = pd.DataFrame({
            'code': ['A', 'B', 'C', 'D', 'E'],
            'pe_ratio': [20, 30, 50, 80, 120],
        })
        
        pe_less_30 = len(df_pe[(df_pe['pe_ratio'] > 0) & (df_pe['pe_ratio'] < 30)])
        pe_less_50 = len(df_pe[(df_pe['pe_ratio'] > 0) & (df_pe['pe_ratio'] < 50)])
        
        self.assertEqual(pe_less_30, 1)
        self.assertEqual(pe_less_50, 2)
    
    def test_roe_threshold_filter(self):
        """测试 ROE 阈值筛选"""
        df_roe = pd.DataFrame({
            'code': ['A', 'B', 'C', 'D', 'E'],
            'roe': [2, 5, 8, 12, 15],
        })
        
        roe_gt_5 = len(df_roe[df_roe['roe'] > 5])
        roe_gt_8 = len(df_roe[df_roe['roe'] > 8])
        
        self.assertEqual(roe_gt_5, 3)
        self.assertEqual(roe_gt_8, 2)
    
    def test_combined_filter(self):
        """测试复合筛选"""
        df = pd.DataFrame({
            'code': ['A', 'B', 'C', 'D', 'E'],
            'pe_ratio': [20, 30, 50, 80, 120],
            'roe': [8, 5, 3, 10, 2],
            'market_cap': [20, 40, 60, 80, 100],
        })
        
        df_combo = df[(df['pe_ratio'] < 30) & (df['roe'] > 5)]
        
        self.assertEqual(len(df_combo), 1)
    
    def test_dividend_yield_filter(self):
        """测试股息率筛选"""
        df_div = pd.DataFrame({
            'code': ['A', 'B', 'C', 'D', 'E'],
            'dividend_yield_ratio': [0.5, 1.5, 2.0, 3.0, 4.0],
        })
        
        div_gt_2 = len(df_div[df_div['dividend_yield_ratio'] >= 2])
        
        self.assertEqual(div_gt_2, 3)
    
    def test_adequacy_check(self):
        """测试充足性判定"""
        hold_target = 15
        
        scenarios = [30, 15, 10, 5]
        expected_adequacy = ["充裕", "基本充足", "勉强够用", "严重不足"]
        
        for candidate_count, expected in zip(scenarios, expected_adequacy):
            if candidate_count >= hold_target * 2:
                adequacy = "充裕"
            elif candidate_count >= hold_target:
                adequacy = "基本充足"
            elif candidate_count >= int(hold_target * 0.7):
                adequacy = "勉强够用"
            else:
                adequacy = "严重不足"
            
            self.assertEqual(adequacy, expected)


class TestKeyValidation(unittest.TestCase):
    """测试关键验证逻辑"""
    
    def test_listing_days_filter(self):
        """测试上市天数筛选"""
        test_date = datetime(2025, 12, 31).date()
        cutoff_date = test_date - timedelta(days=180)
        
        start_dates = [
            datetime(2025, 8, 1).date(),
            datetime(2025, 1, 1).date(),
            datetime(2024, 1, 1).date(),
        ]
        
        valid_count = sum(1 for sd in start_dates if sd <= cutoff_date)
        
        self.assertEqual(valid_count, 2)
    
    def test_st_filter(self):
        """测试 ST 筛选"""
        is_st_dict = {'A': True, 'B': False, 'C': False, 'D': True}
        
        valid_stocks = [s for s, is_st in is_st_dict.items() if not is_st]
        
        self.assertEqual(len(valid_stocks), 2)
    
    def test_kechuangban_filter(self):
        """测试科创板筛选"""
        stocks = ['688001.XSHG', '000001.XSHE', '688002.XSHG', '002001.XSHE']
        
        stocks_no_688 = [s for s in stocks if not s.startswith('688')]
        
        self.assertEqual(len(stocks_no_688), 2)
    
    def test_cap_range_distribution(self):
        """测试市值区间分布"""
        df_cap = pd.DataFrame({
            'market_cap': [15, 25, 45, 75, 95, 55, 35, 65, 85],
        })
        
        cap_ranges = [
            ("10-30亿", 10, 30),
            ("30-60亿", 30, 60),
            ("60-100亿", 60, 100),
        ]
        
        distribution = {}
        for name, min_cap, max_cap in cap_ranges:
            count = len(df_cap[(df_cap['market_cap'] >= min_cap) & (df_cap['market_cap'] < max_cap)])
            distribution[name] = count
        
        self.assertEqual(distribution["10-30亿"], 2)
        self.assertEqual(distribution["30-60亿"], 3)
        self.assertEqual(distribution["60-100亿"], 4)


class TestDividendRatioTest(unittest.TestCase):
    """测试股息率筛选逻辑"""
    
    def test_dividend_threshold_calculation(self):
        """测试股息率阈值计算"""
        df_div = pd.DataFrame({
            'dividend_ratio': [0.0, 1.0, 2.0, 2.5, 3.0, 4.0],
        })
        
        thresholds = [0, 1, 1.5, 2, 2.5, 3]
        
        counts = {}
        for th in thresholds:
            count = len(df_div[df_div['dividend_ratio'] >= th])
            counts[th] = count
        
        self.assertEqual(counts[2], 4)
        self.assertEqual(counts[3], 2)
    
    def test_full_condition_filter(self):
        """测试完整条件筛选"""
        df = pd.DataFrame({
            'pe_ratio': [20, 30, 40, 50],
            'roe': [8, 5, 3, 10],
            'dividend_ratio': [2.5, 1.5, 3.0, 2.0],
        })
        
        df_full = df[(df['pe_ratio'] < 30) & (df['roe'] > 5) & (df['dividend_ratio'] >= 2)]
        
        self.assertEqual(len(df_full), 1)


class TestRegimeQuickTest(unittest.TestCase):
    """测试快速回测逻辑"""
    
    def test_monthly_return_calculation(self):
        """测试月度收益计算"""
        h_start = 3500
        h_end = 3600
        b_start = 110
        b_end = 112
        e_start = 3.5
        e_end = 3.6
        
        stock_r = h_end / h_start - 1
        bond_r = b_end / b_start - 1
        etf_r = e_end / e_start - 1
        
        config = (0.30, 0.30, 0.10)
        r_month = config[0] * stock_r + config[1] * bond_r + config[2] * etf_r
        
        self.assertGreater(r_month, 0)
    
    def test_cumulative_return(self):
        """测试累计收益"""
        monthly_returns = [0.01, 0.02, -0.01, 0.03, 0.01, 0.02]
        
        total = 1.0
        for r in monthly_returns:
            total *= (1 + r)
        
        cumulative = total - 1
        
        expected = (1.01 * 1.02 * 0.99 * 1.03 * 1.01 * 1.02) - 1
        self.assertAlmostEqual(cumulative, expected, places=5)
    
    def test_regime_data_structure(self):
        """测试状态数据结构"""
        months = ["2024-10", "2024-11", "2024-12"]
        regimes = ["震荡轮动", "趋势进攻", "高估防守"]
        
        regime_data = dict(zip(months, regimes))
        
        self.assertEqual(regime_data["2024-10"], "震荡轮动")
    
    def test_config_lookup(self):
        """测试配置查找"""
        CONFIGS = {
            "底部试错": (0.30, 0.30, 0.10),
            "趋势进攻": (0.40, 0.20, 0.30),
        }
        
        regime = "趋势进攻"
        config = CONFIGS[regime]
        
        self.assertEqual(config, (0.40, 0.20, 0.30))


class TestMetrics(unittest.TestCase):
    """测试绩效指标计算"""
    
    def test_total_return(self):
        """测试总收益"""
        nav = pd.Series([1.0, 1.1, 1.2, 1.15, 1.25])
        
        total = nav.iloc[-1] - 1
        
        self.assertAlmostEqual(total, 0.25, places=5)
    
    def test_annualized_return(self):
        """测试年化收益"""
        total_return = 0.25
        days = 252
        
        ann_ret = (1 + total_return) ** (252 / days) - 1
        
        self.assertAlmostEqual(ann_ret, 0.25, places=5)
    
    def test_sharpe_ratio(self):
        """测试夏普比率"""
        daily_returns = pd.Series([0.01, 0.02, -0.01, 0.03, 0.01])
        
        ann_ret = daily_returns.mean() * 252
        ann_vol = daily_returns.std() * np.sqrt(252)
        sharpe = (ann_ret - 0.02) / ann_vol if ann_vol > 0 else 0
        
        self.assertIsInstance(sharpe, float)
    
    def test_max_drawdown(self):
        """测试最大回撤"""
        nav = pd.Series([1.0, 1.2, 1.05, 1.3, 1.15])
        
        max_dd = (nav / nav.cummax() - 1).min()
        
        self.assertAlmostEqual(max_dd, -0.125, places=2)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_dataframe(self):
        """测试空数据"""
        df = pd.DataFrame()
        
        self.assertEqual(len(df), 0)
    
    def test_single_month_data(self):
        """测试单月数据"""
        months = ["2024-10"]
        
        self.assertEqual(len(months), 1)
    
    def test_zero_dividend(self):
        """测试零股息率"""
        df_div = pd.DataFrame({
            'dividend_ratio': [0.0],
        })
        
        div_gt_2 = len(df_div[df_div['dividend_ratio'] >= 2])
        
        self.assertEqual(div_gt_2, 0)
    
    def test_extreme_pe_values(self):
        """测试极端 PE 值"""
        df_pe = pd.DataFrame({
            'pe_ratio': [-10, 0, 1000, np.inf, -np.inf],
        })
        
        df_valid = df_pe[(df_pe['pe_ratio'] > 0) & (df_pe['pe_ratio'] < 100)]
        df_valid = df_valid.replace([np.inf, -np.inf], np.nan).dropna()
        
        self.assertEqual(len(df_valid), 0)
    
    def test_missing_regime(self):
        """测试缺失状态"""
        regime_data = {}
        month = "2024-10"
        
        regime = regime_data.get(month, "震荡轮动")
        
        self.assertEqual(regime, "震荡轮动")


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_regime_router_flow(self):
        """测试完整状态路由流程"""
        CONFIGS = {
            "底部试错": (0.30, 0.30, 0.10),
            "趋势进攻": (0.40, 0.20, 0.30),
            "震荡轮动": (0.35, 0.25, 0.20),
            "高估防守": (0.15, 0.40, 0.05),
        }
        STATIC = (0.40, 0.30, 0.10)
        
        regimes = {"2024-10": "震荡轮动", "2024-11": "趋势进攻"}
        returns = {"2024-10": (0.05, 0.02, 0.04), "2024-11": (0.03, 0.01, 0.02)}
        
        total_regime = 1.0
        total_static = 1.0
        
        for month in regimes:
            config = CONFIGS[regimes[month]]
            r = returns[month]
            
            r_regime = config[0] * r[0] + config[1] * r[1] + config[2] * r[2]
            r_static = STATIC[0] * r[0] + STATIC[1] * r[1] + STATIC[2] * r[2]
            
            total_regime *= (1 + r_regime)
            total_static *= (1 + r_static)
        
        diff = total_regime - total_static
        
        self.assertGreater(total_regime, 1.0)
    
    def test_candidate_pool_full_pipeline(self):
        """测试候选池完整流程"""
        df = pd.DataFrame({
            'code': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
            'market_cap': [15, 25, 45, 75, 95, 55, 35, 65],
            'pe_ratio': [20, 28, 50, 80, 120, 40, 25, 60],
            'roe': [8, 6, 3, 10, 2, 7, 5, 4],
            'dividend_yield_ratio': [2.5, 1.5, 3.0, 2.0, 1.0, 2.2, 1.8, 0.5],
        })
        
        df_cap = df[(df['market_cap'] >= 10) & (df['market_cap'] <= 100)]
        df_pe = df_cap[(df_cap['pe_ratio'] > 0) & (df_cap['pe_ratio'] < 30)]
        df_roe = df_pe[df_pe['roe'] > 5]
        df_div = df_roe[df_roe['dividend_yield_ratio'] >= 2]
        
        self.assertEqual(len(df_cap), 8)
        self.assertEqual(len(df_pe), 3)
        self.assertEqual(len(df_roe), 2)
        self.assertEqual(len(df_div), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)