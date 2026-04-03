#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Task 40: 跑批真值 v2 集成测试

测试真实策略文件的验证功能，覆盖各种策略类型：
- 简单策略
- 复杂策略
- ETF轮动策略
- 小市值策略
- 机器学习策略
- 缺失API策略
- 语法错误策略
"""

import os
import sys
import pytest
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from jk2bt.core.validator import (
        ValidationStatus,
        validate_single_strategy,
    )
except ImportError as e:
    pytest.skip(f"导入失败: {e}", allow_module_level=True)


STRATEGY_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "jkcode", "jkcode"
)


def get_strategy_path(filename):
    """获取策略文件路径"""
    return os.path.join(STRATEGY_DIR, filename)


def strategy_exists(filename):
    """检查策略文件是否存在"""
    return os.path.exists(get_strategy_path(filename))


@pytest.mark.integration
class TestRealStrategyValidation:
    """真实策略验证测试"""

    @pytest.mark.skipif(
        not strategy_exists("03 一个简单而持续稳定的懒人超额收益策略.txt"),
        reason="策略文件不存在",
    )
    def test_simple_strategy_validation(self):
        """测试简单策略验证"""
        strategy_file = get_strategy_path("03 一个简单而持续稳定的懒人超额收益策略.txt")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result is not None
        assert result.load_success is True
        assert result.evidence["loaded"] is True
        assert "initialize" in result.functions_found

        if result.is_really_running:
            assert result.evidence["entered_backtest_loop"] is True
            assert result.evidence["nav_series_length"] > 0

    @pytest.mark.skipif(
        not strategy_exists("04 高股息低市盈率高增长的价投策略.txt"),
        reason="策略文件不存在",
    )
    def test_value_strategy_validation(self):
        """测试价值策略验证"""
        strategy_file = get_strategy_path("04 高股息低市盈率高增长的价投策略.txt")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result is not None
        assert result.load_success is True
        assert "initialize" in result.functions_found

    @pytest.mark.skipif(
        not strategy_exists("05 8年10倍回撤小,有滑点,ETF动量简单轮动策略.txt"),
        reason="策略文件不存在",
    )
    def test_etf_rotation_strategy_validation(self):
        """测试ETF轮动策略验证"""
        strategy_file = get_strategy_path(
            "05 8年10倍回撤小,有滑点,ETF动量简单轮动策略.txt"
        )

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result is not None
        assert result.load_success is True

        result_dict = result.to_dict()
        assert "strategy_name" in result_dict
        assert "evidence" in result_dict

    @pytest.mark.skipif(
        not strategy_exists("01 龙回头3.0回测速度优化版.txt"), reason="策略文件不存在"
    )
    def test_dragon_head_strategy_validation(self):
        """测试龙回头策略验证"""
        strategy_file = get_strategy_path("01 龙回头3.0回测速度优化版.txt")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result is not None
        assert result.load_success is True

    @pytest.mark.skipif(
        not strategy_exists("01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt"),
        reason="策略文件不存在",
    )
    def test_ml_strategy_validation(self):
        """测试机器学习策略验证"""
        strategy_file = get_strategy_path(
            "01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt"
        )

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result is not None
        assert result.load_success is True

    @pytest.mark.skipif(
        not strategy_exists("02 龙头底分型战法-两年23倍.txt"), reason="策略文件不存在"
    )
    def test_missing_api_strategy_validation(self):
        """测试缺失API策略验证"""
        strategy_file = get_strategy_path("02 龙头底分型战法-两年23倍.txt")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result is not None

    @pytest.mark.skipif(
        not strategy_exists("100 配套资料说明.txt"), reason="策略文件不存在"
    )
    def test_non_strategy_file_validation(self):
        """测试非策略文件验证"""
        strategy_file = get_strategy_path("100 配套资料说明.txt")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result is not None


@pytest.mark.integration
class TestValidationResultQuality:
    """验证结果质量测试"""

    @pytest.mark.skipif(
        not strategy_exists("03 一个简单而持续稳定的懒人超额收益策略.txt"),
        reason="策略文件不存在",
    )
    def test_evidence_completeness(self):
        """测试证据完整性"""
        strategy_file = get_strategy_path("03 一个简单而持续稳定的懒人超额收益策略.txt")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        required_evidence = [
            "loaded",
            "loaded_time",
            "entered_backtest_loop",
            "has_transactions",
            "transaction_count",
            "has_nav_series",
            "nav_series_length",
            "strategy_obj_valid",
            "cerebro_valid",
            "final_value",
            "pnl_pct",
        ]

        for field in required_evidence:
            assert field in result.evidence, f"缺少证据字段: {field}"

    @pytest.mark.skipif(
        not strategy_exists("03 一个简单而持续稳定的懒人超额收益策略.txt"),
        reason="策略文件不存在",
    )
    def test_attribution_completeness(self):
        """测试归因完整性"""
        strategy_file = get_strategy_path("03 一个简单而持续稳定的懒人超额收益策略.txt")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        required_attribution = [
            "failure_root_cause",
            "missing_dependency",
            "missing_api",
            "missing_resource_file",
            "error_category",
            "error_type",
            "recoverable",
            "recommendation",
        ]

        for field in required_attribution:
            assert field in result.attribution, f"缺少归因字段: {field}"

    @pytest.mark.skipif(
        not strategy_exists("03 一个简单而持续稳定的懒人超额收益策略.txt"),
        reason="策略文件不存在",
    )
    def test_json_serialization(self):
        """测试JSON序列化"""
        strategy_file = get_strategy_path("03 一个简单而持续稳定的懒人超额收益策略.txt")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        result_dict = result.to_dict()

        try:
            json_str = json.dumps(result_dict, ensure_ascii=False, indent=2)
            parsed = json.loads(json_str)
            assert parsed is not None
        except Exception as e:
            pytest.fail(f"JSON序列化失败: {e}")


@pytest.mark.integration
class TestVariousStrategyTypes:
    """各种策略类型测试"""

    @pytest.mark.parametrize(
        "strategy_file,expected_load",
        [
            ("03 一个简单而持续稳定的懒人超额收益策略.txt", True),
            ("04 红利搬砖，年化29%.txt", True),
            ("04 高股息低市盈率高增长的价投策略.txt", True),
            ("05 随机森林策略，低换手率，年化近50%.txt", True),
            ("05 8年10倍回撤小,有滑点,ETF动量简单轮动策略.txt", True),
            ("01 龙回头3.0回测速度优化版.txt", True),
        ],
    )
    def test_various_strategies_load(self, strategy_file, expected_load):
        """测试各种策略加载"""
        full_path = get_strategy_path(strategy_file)

        if not os.path.exists(full_path):
            pytest.skip(f"策略文件不存在: {strategy_file}")

        result = validate_single_strategy(
            full_path,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result.load_success == expected_load, f"策略加载失败: {strategy_file}"


@pytest.mark.integration
class TestValidationPerformance:
    """验证性能测试"""

    @pytest.mark.skipif(
        not strategy_exists("03 一个简单而持续稳定的懒人超额收益策略.txt"),
        reason="策略文件不存在",
    )
    def test_validation_time(self):
        """测试验证时间"""
        import time

        strategy_file = get_strategy_path("03 一个简单而持续稳定的懒人超额收益策略.txt")

        start_time = time.time()
        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )
        elapsed_time = time.time() - start_time

        assert elapsed_time < 120, f"验证时间过长: {elapsed_time:.2f}秒"
        assert result is not None

    @pytest.mark.skipif(
        not strategy_exists("03 一个简单而持续稳定的懒人超额收益策略.txt"),
        reason="策略文件不存在",
    )
    def test_loaded_time_recorded(self):
        """测试加载时间记录"""
        strategy_file = get_strategy_path("03 一个简单而持续稳定的懒人超额收益策略.txt")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result.evidence["loaded_time"] >= 0


@pytest.mark.integration
class TestStatusClassification:
    """状态分类测试"""

    @pytest.mark.skipif(
        not strategy_exists("03 一个简单而持续稳定的懒人超额收益策略.txt"),
        reason="策略文件不存在",
    )
    def test_success_status_classification(self):
        """测试成功状态分类"""
        strategy_file = get_strategy_path("03 一个简单而持续稳定的懒人超额收益策略.txt")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        if result.is_really_running:
            assert result.final_status in [
                ValidationStatus.SUCCESS_NO_TRADE.value,
                ValidationStatus.SUCCESS_WITH_NAV.value,
                ValidationStatus.SUCCESS_WITH_TRANSACTIONS.value,
            ]

    @pytest.mark.skipif(
        not strategy_exists("02 龙头底分型战法-两年23倍.txt"), reason="策略文件不存在"
    )
    def test_missing_api_status_classification(self):
        """测试缺失API状态分类"""
        strategy_file = get_strategy_path("02 龙头底分型战法-两年23倍.txt")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        if result.attribution.get("error_category") == "api_missing":
            assert result.final_status in [
                ValidationStatus.MISSING_API.value,
                ValidationStatus.RUN_EXCEPTION.value,
            ]


@pytest.mark.integration
class TestBatchValidation:
    """批量验证测试"""

    def test_batch_validation_output(self):
        """测试批量验证输出"""
        strategies = [
            "03 一个简单而持续稳定的懒人超额收益策略.txt",
            "04 红利搬砖，年化29%.txt",
        ]

        results = []
        for strategy_name in strategies:
            strategy_file = get_strategy_path(strategy_name)
            if os.path.exists(strategy_file):
                result = validate_single_strategy(
                    strategy_file,
                    start_date="2022-01-01",
                    end_date="2022-03-31",
                    initial_capital=100000,
                )
                results.append(result.to_dict())

        if len(results) > 0:
            output = {
                "validation_time": datetime.now().isoformat(),
                "total": len(results),
                "results": results,
            }

            assert output["total"] > 0
            assert len(output["results"]) == output["total"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-m", "integration"])
