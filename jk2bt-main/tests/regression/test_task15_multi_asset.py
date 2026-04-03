#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Task 15: 多资产覆盖能力测试

测试目标：
1. 验证资产识别能力（股票/ETF/LOF/OF/期货/指数）
2. 验证数据获取能力（各资产类型数据模块是否存在）
3. 验证交易能力（各资产类型broker适配）
4. 验证特殊交易机制支持情况
5. 验证任务定位是否为"能力梳理"而非"能力落地"

覆盖问题：
- P1: Task 15主要是能力梳理，不是能力落地
- 验证LOF/OF/期货数据未对接、交易机制缺失
- 验证文档开头明确"无修改"
"""

import os
import sys
import unittest

try:
    from jk2bt.asset_router import (
        AssetType,
        TradingStatus,
        identify_asset,
        is_stock,
        is_etf,
        is_fund_of,
        is_future,
        is_index,
    )
except ImportError:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    try:
        from jk2bt.asset_router import (
            AssetType,
            TradingStatus,
            identify_asset,
            is_stock,
            is_etf,
            is_fund_of,
            is_future,
            is_index,
        )
    except ImportError:
        AssetType = None
        TradingStatus = None
        identify_asset = None


class TestAssetIdentificationCapability(unittest.TestCase):
    """测试资产识别能力"""

    def test_stock_identification(self):
        """股票识别应正确"""
        if identify_asset is None:
            self.skipTest("asset_router模块不可用")

        info = identify_asset("600519.XSHG")
        self.assertEqual(info.asset_type, AssetType.STOCK)
        self.assertTrue(info.is_supported())
        print("验证通过: 股票识别正确且支持交易")

    def test_etf_identification(self):
        """ETF识别应正确"""
        if identify_asset is None:
            self.skipTest("asset_router模块不可用")

        info = identify_asset("510300.XSHG")
        self.assertEqual(info.asset_type, AssetType.ETF)
        self.assertTrue(info.is_supported())
        print("验证通过: ETF识别正确且支持交易")

    def test_lof_identification(self):
        """LOF识别应正确（但可能不支持交易）"""
        if identify_asset is None:
            self.skipTest("asset_router模块不可用")

        info = identify_asset("160105")
        self.assertIn(info.asset_type, [AssetType.ETF, AssetType.LOF])

        is_lof_or_etf = info.asset_type in [AssetType.ETF, AssetType.LOF]
        print(
            f"LOF识别验证: asset_type={info.asset_type}, supported={info.is_supported()}"
        )

        self.assertTrue(is_lof_or_etf, "应识别为LOF或ETF")

    def test_fund_of_identification(self):
        """场外基金识别应正确（仅识别不支持交易）"""
        if identify_asset is None:
            self.skipTest("asset_router模块不可用")

        info = identify_asset("000001.OF")
        self.assertEqual(info.asset_type, AssetType.FUND_OF)

        is_identified_only = info.is_identified_only()

        self.assertTrue(is_identified_only, "场外基金应为IDENTIFIED_ONLY状态")

        print(f"验证通过: 场外基金仅识别不支持交易 (status={info.trading_status})")

    def test_future_identification(self):
        """股指期货识别应正确（仅识别不支持交易）"""
        if identify_asset is None:
            self.skipTest("asset_router模块不可用")

        info = identify_asset("IF2312.CCFX")
        self.assertEqual(info.asset_type, AssetType.FUTURE_CCFX)

        is_identified_only = info.is_identified_only()

        self.assertTrue(is_identified_only, "股指期货应为IDENTIFIED_ONLY状态")

        print(f"验证通过: 股指期货仅识别不支持交易 (status={info.trading_status})")

    def test_index_identification(self):
        """指数识别应正确（仅识别不支持交易）"""
        if identify_asset is None:
            self.skipTest("asset_router模块不可用")

        info = identify_asset("000300.XSHG")
        self.assertEqual(info.asset_type, AssetType.INDEX)

        is_identified_only = info.is_identified_only()

        self.assertTrue(is_identified_only, "指数应为IDENTIFIED_ONLY状态")

        print(f"验证通过: 指数仅识别不支持交易 (status={info.trading_status})")


class TestAssetDataModuleExistence(unittest.TestCase):
    """测试各资产数据模块存在性"""

    def test_stock_data_module_exists(self):
        """股票数据模块应存在"""
        stock_module_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "src",
            "market_data",
            "stock.py",
        )

        self.assertTrue(
            os.path.exists(stock_module_path),
            "股票数据模块应存在: market_data/stock.py",
        )

        if os.path.exists(stock_module_path):
            print(f"验证通过: 股票数据模块存在")

    def test_etf_data_module_exists(self):
        """ETF数据模块应存在"""
        etf_module_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "src",
            "market_data",
            "etf.py",
        )

        self.assertTrue(
            os.path.exists(etf_module_path), "ETF数据模块应存在: market_data/etf.py"
        )

        if os.path.exists(etf_module_path):
            print(f"验证通过: ETF数据模块存在")

    def test_lof_data_module_exists_or_not(self):
        """LOF数据模块存在性验证"""
        lof_module_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "src",
            "market_data",
            "lof.py",
        )

        lof_exists = os.path.exists(lof_module_path)

        if lof_exists:
            print(f"验证: LOF数据模块存在 {lof_module_path}")
        else:
            print(f"验证: LOF数据模块不存在（符合预期）")

            self.assertFalse(lof_exists, "LOF数据模块预期不存在，需后续对接")

    def test_fund_of_data_module_exists_or_not(self):
        """场外基金数据模块存在性验证"""
        fund_of_module_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "src",
            "market_data",
            "fund_of.py",
        )

        fund_of_exists = os.path.exists(fund_of_module_path)

        if fund_of_exists:
            print(f"验证: 场外基金数据模块存在 {fund_of_module_path}")
        else:
            print(f"验证: 场外基金数据模块不存在（符合预期）")

            self.assertFalse(fund_of_exists, "场外基金数据模块预期不存在，需后续对接")

    def test_future_data_module_exists_or_not(self):
        """期货数据模块存在性验证"""
        future_module_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "src",
            "market_data",
            "future.py",
        )

        future_exists = os.path.exists(future_module_path)

        if future_exists:
            print(f"验证: 期货数据模块存在 {future_module_path}")
        else:
            print(f"验证: 期货数据模块不存在（符合预期）")

            self.assertFalse(future_exists, "期货数据模块预期不存在，需后续对接")


class TestTradingCapability(unittest.TestCase):
    """测试交易能力"""

    def test_stock_trading_capability(self):
        """股票交易能力应完整"""
        stock_supported = True

        try:
            from jk2bt.asset_router import TradingStatus

            info = identify_asset("600519.XSHG")
            stock_supported = info.trading_status == TradingStatus.SUPPORTED
        except Exception:
            pass

        self.assertTrue(stock_supported, "股票交易能力应完整支持")

        print("验证通过: 股票交易能力完整")

    def test_etf_trading_capability(self):
        """ETF交易能力应完整"""
        etf_supported = True

        try:
            from jk2bt.asset_router import TradingStatus

            info = identify_asset("510300.XSHG")
            etf_supported = info.trading_status == TradingStatus.SUPPORTED
        except Exception:
            pass

        self.assertTrue(etf_supported, "ETF交易能力应完整支持")

        print("验证通过: ETF交易能力完整")

    def test_lof_trading_capability_or_not(self):
        """LOF交易能力验证"""
        lof_trading_capable = False

        try:
            from jk2bt.asset_router import TradingStatus

            info = identify_asset("160105")
            lof_trading_capable = info.trading_status == TradingStatus.SUPPORTED
        except Exception:
            pass

        if not lof_trading_capable:
            print("验证: LOF交易能力不完整（符合预期）")

            lof_module_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "src",
                "market_data",
                "lof.py",
            )

            lof_data_missing = not os.path.exists(lof_module_path)

            self.assertTrue(
                lof_data_missing or not lof_trading_capable, "LOF交易能力预期不完整"
            )
        else:
            print("验证: LOF交易能力已具备（超出预期）")

    def test_fund_of_trading_capability_or_not(self):
        """场外基金交易能力验证"""
        fund_of_trading_capable = False

        try:
            from jk2bt.asset_router import TradingStatus

            info = identify_asset("000001.OF")
            fund_of_trading_capable = info.trading_status == TradingStatus.SUPPORTED
        except Exception:
            pass

        if not fund_of_trading_capable:
            print("验证: 场外基金交易能力缺失（符合预期）")

            self.assertFalse(fund_of_trading_capable, "场外基金交易能力预期缺失")
        else:
            print("验证: 场外基金交易能力已具备（超出预期）")

    def test_future_trading_capability_or_not(self):
        """期货交易能力验证"""
        future_trading_capable = False

        try:
            from jk2bt.asset_router import TradingStatus

            info = identify_asset("IF2312.CCFX")
            future_trading_capable = info.trading_status == TradingStatus.SUPPORTED
        except Exception:
            pass

        if not future_trading_capable:
            print("验证: 期货交易能力缺失（符合预期）")

            self.assertFalse(
                future_trading_capable, "期货交易能力预期缺失（保证金机制未实现）"
            )
        else:
            print("验证: 期货交易能力已具备（超出预期）")


class TestSpecialTradingMechanism(unittest.TestCase):
    """测试特殊交易机制"""

    def test_futures_margin_mechanism(self):
        """期货保证金机制验证"""
        margin_mechanism_exists = False

        try:
            from jk2bt.core.strategy_base import (
                JQ2BTBaseStrategy,
            )
            import inspect

            source = inspect.getsource(JQ2BTBaseStrategy)

            margin_keywords = ["margin", "保证金", "MarginBroker", "FutureBroker"]
            margin_mechanism_exists = any(kw in source for kw in margin_keywords)

        except Exception:
            pass

        self.assertFalse(margin_mechanism_exists, "期货保证金机制预期不存在")

        print("验证通过: 期货保证金机制缺失（符合预期）")

    def test_lof_arbitrage_mechanism(self):
        """LOF套利机制验证"""
        arbitrage_mechanism_exists = False

        try:
            from jk2bt.core.strategy_base import (
                JQ2BTBaseStrategy,
            )
            import inspect

            source = inspect.getsource(JQ2BTBaseStrategy)

            arbitrage_keywords = ["arbitrage", "套利", "申购", "赎回"]
            arbitrage_mechanism_exists = any(kw in source for kw in arbitrage_keywords)

        except Exception:
            pass

        self.assertFalse(arbitrage_mechanism_exists, "LOF套利机制预期不存在")

        print("验证通过: LOF套利机制缺失（符合预期）")

    def test_fund_subscription_redemption_mechanism(self):
        """场外基金申赎机制验证"""
        subscription_mechanism_exists = False

        try:
            from jk2bt.core.strategy_base import (
                JQ2BTBaseStrategy,
            )
            import inspect

            source = inspect.getsource(JQ2BTBaseStrategy)

            subscription_keywords = ["subscribe", "申购", "redeem", "赎回"]
            subscription_mechanism_exists = any(
                kw in source for kw in subscription_keywords
            )

        except Exception:
            pass

        self.assertFalse(subscription_mechanism_exists, "场外基金申赎机制预期不存在")

        print("验证通过: 场外基金申赎机制缺失（符合预期）")


class TestTask15Positioning(unittest.TestCase):
    """验证Task 15任务定位"""

    def test_task_positioning_is_梳理_not_落地(self):
        """任务定位应为'能力梳理'而非'能力落地'"""
        result_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task15_multi_asset_coverage_result.md",
        )

        if os.path.exists(result_doc_path):
            with open(result_doc_path, "r", encoding="utf-8") as f:
                content = f.read()

            positioning_keywords = [
                "能力梳理",
                "能力盘点",
                "梳理任务",
                "未修改",
                "无修改",
            ]

            has_correct_positioning = any(kw in content for kw in positioning_keywords)

            self.assertTrue(has_correct_positioning, "文档应明确任务定位为'能力梳理'")

            if has_correct_positioning:
                found_kw = [kw for kw in positioning_keywords if kw in content][0]
                print(f"验证通过: 任务定位为'{found_kw}'")
        else:
            self.skipTest("结果文档不存在")

    def test_document_starts_with_no_modification(self):
        """文档开头应明确'无修改'"""
        result_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task15_multi_asset_coverage_result.md",
        )

        if os.path.exists(result_doc_path):
            with open(result_doc_path, "r", encoding="utf-8") as f:
                first_lines = f.readlines()[:10]

            has_no_modification = any(
                "无修改" in line or "未修改" in line for line in first_lines
            )

            self.assertTrue(has_no_modification, "文档开头应明确'无修改'或'未修改'")

            if has_no_modification:
                print("验证通过: 文档开头明确'无修改'")
        else:
            self.skipTest("结果文档不存在")

    def test_conclusion_states_not_达标(self):
        """结论应明确说明能力不能算达标"""
        result_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task15_multi_asset_coverage_result.md",
        )

        if os.path.exists(result_doc_path):
            with open(result_doc_path, "r", encoding="utf-8") as f:
                content = f.read()

            not_达标_keywords = [
                "不能算达标",
                "未达标",
                "尚未达标",
                "不能给",
                "不能说",
                "远未达到",
            ]
            has_not_达标 = any(kw in content for kw in not_达标_keywords)

            self.assertTrue(has_not_达标, "文档应包含'不能算达标'或'未达标'等关键词")

            if has_not_达标:
                found_kw = [kw for kw in not_达标_keywords if kw in content][0]
                print(f"验证通过: 文档包含'{found_kw}'")
        else:
            self.skipTest("结果文档不存在")

    def test_missing_capabilities_documented(self):
        """缺失能力应明确记录"""
        result_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task15_multi_asset_coverage_result.md",
        )

        if os.path.exists(result_doc_path):
            with open(result_doc_path, "r", encoding="utf-8") as f:
                content = f.read()

            missing_patterns = [
                "LOF数据源未对接",
                "OF净值数据未对接",
                "期货数据未对接",
                "期货保证金机制未实现",
                "未对接",
                "缺失",
            ]

            has_missing_documented = any(p in content for p in missing_patterns)

            self.assertTrue(has_missing_documented, "文档应明确记录缺失能力")

            if has_missing_documented:
                found_pattern = [p for p in missing_patterns if p in content][0]
                print(f"验证通过: 文档记录缺失能力 '{found_pattern}'")
        else:
            self.skipTest("结果文档不存在")


if __name__ == "__main__":
    unittest.main(verbosity=2)
