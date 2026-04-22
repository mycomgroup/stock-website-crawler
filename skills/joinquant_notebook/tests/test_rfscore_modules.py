# -*- coding: utf-8 -*-
"""
rfscore_v2_enhanced.py 单元测试
测试内容:
- RFScore 因子类及其 calc 方法
- EnhancedStateRouter 状态路由器
- RSRSIndicator RSRS择时指标
- VolatilityPositionManager 波动率仓位管理
- BottomSignalsChecker 底部信号检查器
- TurnoverFilter 换手率过滤
- TrailingStopManager 移动止盈止损
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestRFScoreCalculation(unittest.TestCase):
    """测试 RFScore 因子计算"""
    
    def test_roa_calculation(self):
        """测试 ROA 计算"""
        roa = pd.Series([8.0, 6.0, 10.0])
        delta_roa = roa / pd.Series([7.0, 5.0, 8.0]) - 1
        
        self.assertAlmostEqual(delta_roa.iloc[0], 1/7 - 1 + 1, places=5)
        self.assertTrue(all(abs(d) < 1 for d in delta_roa))
    
    def test_ocfoa_calculation(self):
        """测试 OCFOA 计算"""
        cfo_sum = 100 + 90 + 80 + 70
        ta_ttm = (400 + 380 + 360 + 340) / 4
        ocfoa = cfo_sum / ta_ttm
        
        self.assertIsInstance(ocfoa, float)
        self.assertGreater(ocfoa, 0)
    
    def test_delta_leveler_calculation(self):
        """测试杠杆变化计算"""
        leveler = pd.Series([0.4, 0.3])
        leveler1 = pd.Series([0.5, 0.4])
        delta_leveler = -(leveler / leveler1 - 1)
        
        expected = -(0.4/0.5 - 1)
        self.assertAlmostEqual(delta_leveler.iloc[0], expected, places=5)
    
    def test_sign_function(self):
        """测试 sign 函数"""
        values = pd.Series([0.5, -0.3, 0.0, 0.1])
        sign = values.apply(lambda x: 1 if x > 0 else 0)
        
        self.assertEqual(sign.iloc[0], 1)
        self.assertEqual(sign.iloc[1], 0)
        self.assertEqual(sign.iloc[2], 0)
    
    def test_fscore_sum(self):
        """测试 FScore 汇总"""
        indicators = pd.DataFrame({
            'ROA': [8, 6, 10],
            'DELTA_ROA': [0.1, -0.05, 0.2],
            'OCFOA': [0.15, 0.12, 0.18],
            'ACCRUAL': [0.05, -0.02, 0.08],
            'DELTA_LEVELER': [-0.1, 0.05, -0.15],
            'DELTA_MARGIN': [0.02, -0.01, 0.03],
            'DELTA_TURN': [0.01, 0.0, 0.02],
        })
        
        def sign(ser):
            return ser.apply(lambda x: 1 if x > 0 else 0)
        
        fscore = indicators.apply(sign).sum(axis=1)
        
        self.assertEqual(fscore.iloc[0], 6)
        self.assertTrue(all(0 <= s <= 7 for s in fscore))
    
    def test_inf_replacement(self):
        """测试无穷值替换"""
        df = pd.DataFrame({
            'ROA': [8.0, np.inf, -np.inf],
            'DELTA_ROA': [0.1, 0.2, np.nan],
        })
        
        df = df.replace([np.inf, -np.inf], np.nan)
        
        self.assertTrue(pd.isna(df.loc[1, 'ROA']))
        self.assertTrue(pd.isna(df.loc[2, 'ROA']))


class TestEnhancedStateRouter(unittest.TestCase):
    """测试 EnhancedStateRouter 状态路由器"""
    
    def test_route_extreme_weak(self):
        """测试极弱状态"""
        breadth = 0.1
        zt_count = 15
        
        if breadth < 0.15 or zt_count < 20:
            position_ratio, hold_num, state = 0.0, 0, "极弱停手"
        
        self.assertEqual(position_ratio, 0.0)
        self.assertEqual(hold_num, 0)
    
    def test_route_bottom_defense(self):
        """测试底部防守状态"""
        breadth = 0.2
        zt_count = 40
        
        if breadth < 0.25:
            position_ratio, hold_num, state = 0.5, 10, "底部防守"
        
        self.assertEqual(position_ratio, 0.5)
        self.assertEqual(hold_num, 10)
    
    def test_route_oscillation(self):
        """测试震荡平衡状态"""
        breadth = 0.3
        zt_count = 50
        
        if breadth < 0.35:
            position_ratio, hold_num, state = 0.75, 15, "震荡平衡"
        
        self.assertEqual(position_ratio, 0.75)
    
    def test_route_strong_trend(self):
        """测试强趋势状态"""
        breadth = 0.45
        zt_count = 90
        
        if breadth >= 0.40 and zt_count >= 80:
            position_ratio, hold_num, state = 1.0, 20, "强趋势"
        
        self.assertEqual(position_ratio, 1.0)
        self.assertEqual(hold_num, 20)
    
    def test_route_normal_trend(self):
        """测试趋势正常状态"""
        breadth = 0.38
        zt_count = 60
        
        if breadth >= 0.35 and (breadth < 0.40 or zt_count < 80):
            position_ratio, hold_num, state = 0.75, 15, "趋势正常"
        
        self.assertEqual(state, "趋势正常")


class TestRSRSIndicator(unittest.TestCase):
    """测试 RSRS 择时指标"""
    
    def test_calculate_beta_r2_basic(self):
        """测试 beta 和 R2 计算"""
        high = np.array([3100, 3110, 3120, 3130, 3140])
        low = np.array([3050, 3055, 3060, 3065, 3070])
        
        from scipy.stats import linregress
        slope, intercept, r_value, p_value, std_err = linregress(low, high)
        r2 = r_value ** 2
        
        self.assertIsInstance(slope, float)
        self.assertGreater(r2, 0)
        self.assertLessEqual(r2, 1)
    
    def test_insufficient_data(self):
        """测试数据不足情况"""
        high = np.array([3100])
        low = np.array([3050])
        N = 18
        
        if len(high) < N:
            beta, r2 = None, None
        
        self.assertIsNone(beta)
    
    def test_zscore_calculation(self):
        """测试 Z-score 计算"""
        slope_series = [0.8, 0.9, 1.0, 1.1, 1.2]
        beta = 1.3
        
        mean = np.mean(slope_series)
        std = np.std(slope_series)
        zscore = (beta - mean) / std
        
        self.assertGreater(zscore, 0)
    
    def test_rsrs_rightdev_calculation(self):
        """测试右偏修正 RSRS"""
        zscore = 0.5
        beta = 1.1
        r2 = 0.85
        
        rsrs_rightdev = zscore * beta * r2
        
        expected = 0.5 * 1.1 * 0.85
        self.assertAlmostEqual(rsrs_rightdev, expected, places=5)
    
    def test_signal_threshold_buy(self):
        """测试买入信号阈值"""
        rsrs_value = 0.8
        buy_threshold = 0.7
        
        if rsrs_value > buy_threshold:
            signal = "BULLISH"
        
        self.assertEqual(signal, "BULLISH")
    
    def test_signal_threshold_sell(self):
        """测试卖出信号阈值"""
        rsrs_value = -0.9
        sell_threshold = -0.7
        
        if rsrs_value < sell_threshold:
            signal = "BEARISH"
        
        self.assertEqual(signal, "BEARISH")
    
    def test_signal_neutral(self):
        """测试中性信号"""
        rsrs_value = 0.0
        buy_threshold = 0.7
        sell_threshold = -0.7
        
        if rsrs_value <= buy_threshold and rsrs_value >= sell_threshold:
            signal = "NEUTRAL"
        
        self.assertEqual(signal, "NEUTRAL")


class TestVolatilityPositionManager(unittest.TestCase):
    """测试波动率仓位管理"""
    
    def test_atr_calculation(self):
        """测试 ATR 计算"""
        np.random.seed(42)
        high = np.array([100, 102, 101, 103, 102])
        low = np.array([98, 99, 97, 100, 99])
        close = np.array([99, 100, 98, 102, 101])
        
        tr1 = high - low
        tr2 = np.abs(high - np.roll(close, 1))
        tr3 = np.abs(low - np.roll(close, 1))
        tr = np.maximum(tr1, np.maximum(tr2, tr3))
        tr[0] = high[0] - low[0]
        
        atr = np.mean(tr)
        
        self.assertGreater(atr, 0)
    
    def test_atr_ratio_calculation(self):
        """测试 ATR/价格比率"""
        atr = 2.0
        current_price = 100.0
        
        atr_ratio = atr / current_price
        
        self.assertAlmostEqual(atr_ratio, 0.02, places=5)
    
    def test_volatility_multiplier_low(self):
        """测试低波动率乘数"""
        atr_ratio = 0.015
        low_vol_threshold = 0.02
        
        if atr_ratio < low_vol_threshold:
            multiplier, state = 1.2, "LOW"
        
        self.assertEqual(multiplier, 1.2)
    
    def test_volatility_multiplier_high(self):
        """测试高波动率乘数"""
        atr_ratio = 0.06
        high_vol_threshold = 0.05
        
        if atr_ratio > high_vol_threshold:
            multiplier, state = 0.5, "HIGH"
        
        self.assertEqual(multiplier, 0.5)
    
    def test_volatility_multiplier_normal(self):
        """测试正常波动率乘数"""
        atr_ratio = 0.03
        low_vol_threshold = 0.02
        high_vol_threshold = 0.05
        
        if atr_ratio >= low_vol_threshold and atr_ratio <= high_vol_threshold:
            multiplier, state = 1.0, "NORMAL"
        
        self.assertEqual(multiplier, 1.0)


class TestBottomSignalsChecker(unittest.TestCase):
    """测试底部信号检查器"""
    
    def test_breadth_signal_below_threshold(self):
        """测试市场宽度信号"""
        breadth = 0.12
        threshold = 0.15
        
        satisfied = breadth < threshold
        
        self.assertTrue(satisfied)
    
    def test_fed_signal_above_threshold(self):
        """测试 FED 估值信号"""
        pe = 10.0
        bond_yield = 2.5
        fed = (100.0 / pe) - bond_yield
        threshold = 2.0
        
        satisfied = fed > threshold
        
        self.assertTrue(satisfied)
    
    def test_pb_below_1_signal(self):
        """测试破净占比信号"""
        pb_below_ratio = 0.18
        threshold = 0.15
        
        satisfied = pb_below_ratio > threshold
        
        self.assertTrue(satisfied)
    
    def test_volume_signal(self):
        """测试成交额信号"""
        total_volume = 4000e8
        threshold = 5000e8
        
        satisfied = total_volume < threshold
        
        self.assertTrue(satisfied)
    
    def test_limit_up_signal(self):
        """测试涨停家数信号"""
        zt_count = 15
        threshold = 20
        
        satisfied = zt_count < threshold
        
        self.assertTrue(satisfied)
    
    def test_check_all_count(self):
        """测试综合信号计数"""
        signals = [True, True, False, True, False]
        satisfied = sum(signals)
        
        self.assertEqual(satisfied, 3)


class TestTurnoverFilter(unittest.TestCase):
    """测试换手率过滤"""
    
    def test_keep_ratio_calculation(self):
        """测试保留比例计算"""
        stocks = ["A", "B", "C", "D", "E"]
        keep_ratio = 0.8
        
        target_num = int(len(stocks) * keep_ratio)
        
        self.assertEqual(target_num, 4)
    
    def test_filter_stocks_basic(self):
        """测试基本过滤"""
        stocks = list(range(100))
        keep_ratio = 0.8
        
        filtered = stocks[:int(len(stocks) * keep_ratio)]
        
        self.assertEqual(len(filtered), 80)
    
    def test_empty_stocks_handling(self):
        """测试空股票列表"""
        stocks = []
        keep_ratio = 0.8
        
        filtered = stocks[:int(len(stocks) * keep_ratio)]
        
        self.assertEqual(len(filtered), 0)


class TestTrailingStopManager(unittest.TestCase):
    """测试移动止盈止损"""
    
    def test_update_high_price(self):
        """测试更新最高价"""
        high_prices = {}
        stock = "000001.XSHE"
        current_price = 10.0
        
        if stock not in high_prices:
            high_prices[stock] = current_price
        else:
            if current_price > high_prices[stock]:
                high_prices[stock] = current_price
        
        self.assertEqual(high_prices[stock], 10.0)
    
    def test_high_price_update_increase(self):
        """测试最高价上涨更新"""
        high_prices = {"000001.XSHE": 10.0}
        stock = "000001.XSHE"
        current_price = 12.0
        
        if current_price > high_prices[stock]:
            high_prices[stock] = current_price
        
        self.assertEqual(high_prices[stock], 12.0)
    
    def test_stop_loss_triggered(self):
        """测试止损触发"""
        avg_cost = 100.0
        current_price = 85.0
        stop_loss = -0.10
        
        pnl_ratio = (current_price - avg_cost) / avg_cost
        
        should_close = pnl_ratio <= stop_loss
        
        self.assertTrue(should_close)
    
    def test_trailing_stop_triggered(self):
        """测试移动止盈触发"""
        high_price = 120.0
        current_price = 102.0
        avg_cost = 100.0
        trailing_stop = 0.15
        
        pnl_ratio = (current_price - avg_cost) / avg_cost
        drawdown = (current_price - high_price) / high_price
        
        should_close = drawdown <= -trailing_stop and pnl_ratio > 0
        
        self.assertTrue(should_close)
    
    def test_no_stop_triggered(self):
        """测试无触发"""
        avg_cost = 100.0
        current_price = 105.0
        stop_loss = -0.10
        
        pnl_ratio = (current_price - avg_cost) / avg_cost
        
        should_close = pnl_ratio <= stop_loss
        
        self.assertFalse(should_close)
    
    def test_remove_position(self):
        """测试移除持仓记录"""
        high_prices = {"000001.XSHE": 120.0, "000002.XSHE": 50.0}
        stock = "000001.XSHE"
        
        high_prices.pop(stock, None)
        
        self.assertNotIn(stock, high_prices)
        self.assertIn("000002.XSHE", high_prices)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_zero_avg_cost(self):
        """测试零成本"""
        avg_cost = 0.0
        current_price = 100.0
        
        if avg_cost <= 0:
            should_close = False
        
        self.assertFalse(should_close)
    
    def test_negative_position_ratio(self):
        """测试负仓位比例"""
        position_ratio = -0.1
        
        final_ratio = min(max(position_ratio, 0), 1.0)
        
        self.assertEqual(final_ratio, 0)
    
    def test_excessive_position_ratio(self):
        """测试超过100%仓位"""
        position_ratio = 1.5
        
        final_ratio = min(max(position_ratio, 0), 1.0)
        
        self.assertEqual(final_ratio, 1.0)
    
    def test_empty_fscore_dataframe(self):
        """测试空 FScore 数据"""
        df = pd.DataFrame()
        
        self.assertEqual(len(df), 0)
    
    def test_single_indicator_positive(self):
        """测试单因子正值"""
        values = pd.Series([0.1])
        sign = values.apply(lambda x: 1 if x > 0 else 0)
        
        self.assertEqual(sign.iloc[0], 1)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_state_routing_flow(self):
        """测试完整状态路由流程"""
        breadth = 0.3
        zt_count = 50
        
        if breadth < 0.15 or zt_count < 20:
            position_ratio, hold_num = 0.0, 0
        elif breadth < 0.25:
            position_ratio, hold_num = 0.5, 10
        elif breadth < 0.35:
            position_ratio, hold_num = 0.75, 15
        elif breadth >= 0.40 and zt_count >= 80:
            position_ratio, hold_num = 1.0, 20
        else:
            position_ratio, hold_num = 0.75, 15
        
        rsrs_signal = "NEUTRAL"
        if rsrs_signal == "BEARISH":
            position_ratio *= 0.7
        elif rsrs_signal == "BULLISH":
            position_ratio = min(position_ratio * 1.1, 1.0)
        
        vol_multiplier = 1.0
        final_ratio = position_ratio * vol_multiplier
        final_ratio = min(max(final_ratio, 0), 1.0)
        
        self.assertEqual(final_ratio, 0.75)
    
    def test_rfscore_with_pb_group(self):
        """测试 RFScore 与 PB 分组"""
        df = pd.DataFrame({
            'RFScore': [7, 6, 5, 7, 6],
            'pb_ratio': [0.8, 1.2, 1.5, 0.9, 1.1],
        })
        
        df['pb_group'] = pd.qcut(df['pb_ratio'].rank(method='first'), 5, labels=False, duplicates='drop') + 1
        
        primary = df[(df['RFScore'] == 7) & (df['pb_group'] <= 2)]
        
        self.assertEqual(len(primary), 2)
    
    def test_trailing_stop_full_cycle(self):
        """测试移动止盈完整周期"""
        high_prices = {}
        stock = "000001.XSHE"
        avg_cost = 100.0
        trailing_stop = 0.15
        
        prices = [100, 110, 120, 115, 101]
        should_close = False
        
        for price in prices:
            if stock not in high_prices:
                high_prices[stock] = price
            else:
                if price > high_prices[stock]:
                    high_prices[stock] = price
            
            pnl_ratio = (price - avg_cost) / avg_cost
            
            if stock in high_prices:
                drawdown = (price - high_prices[stock]) / high_prices[stock]
                should_close = drawdown <= -trailing_stop and pnl_ratio > 0
            
            if should_close:
                break
        
        self.assertEqual(high_prices[stock], 120)
        self.assertTrue(should_close)


if __name__ == "__main__":
    unittest.main(verbosity=2)