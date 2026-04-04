"""
tests/validation/test_golden_benchmark.py
金标基准策略测试 - 硬验收门槛

这是CI必须通过的硬gate测试，用于验证产品链路达标。

测试原理：
1. 使用固定策略：validation_v4_double_ma.txt（双均线择时）
2. 固定参数：start_date='2023-01-01', end_date='2023-12-31'
3. 固定股票池：['600519.XSHG', '000858.XSHE']（贵州茅台、五粮液）
4. 预期结果：经过预热和验证的基准值，带容差范围
5. 硬验收：结果不符合基准则测试失败

基准值来源：
- 需要先预热数据：python tools/offline_data/prewarm_daily.py --stocks 600519.XSHG 000858.XSHE --start 2023-01-01 --end 2023-12-31
- 然后运行策略记录基准
- 将基准值写入此测试文件

容差范围：
- final_value误差容忍<5%（考虑到数据源差异）
- pnl_pct误差容忍<10%（绝对百分比误差）
- 策略必须正常运行不抛异常
"""

import os
import sys
import pytest
import json
import datetime
from typing import Dict, Any

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from jk2bt import run_jq_strategy
from jk2bt.db.cache_status import get_cache_manager


# =============================================================================
# 金标基准配置 - 固定参数，不可随意修改
# =============================================================================

GOLDEN_BENCHMARK_CONFIG = {
    # 策略文件
    "strategy_file": "strategies/validation_v4_double_ma.txt",

    # 固定日期区间
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",

    # 固定股票池（2只蓝筹股，数据稳定可靠）
    "stock_pool": ["600519.XSHG", "000858.XSHE"],  # 贵州茅台、五粮液

    # 初始资金
    "initial_capital": 1000000,

    # 预期基准结果（需要预热数据后运行获取）
    # 注意：这些值需要根据实际运行结果更新
    "expected_baseline": {
        # 最终资金基准值（容差5%）
        "final_value": None,  # 待预热后填充
        "final_value_tolerance_pct": 5.0,

        # 收益率基准值（容差10%绝对误差）
        "pnl_pct": None,  # 待预热后填充
        "pnl_pct_tolerance": 10.0,  # 绝对百分比误差

        # 运行时间限制（秒）
        "max_run_time_seconds": 60,

        # 基准更新日期
        "baseline_updated": None,
    },

    # 测试级别：P0最高优先级，CI必须通过
    "validation_priority": "P0",

    # 描述
    "description": "双均线择时策略金标基准测试",
}


def check_cache_availability() -> Dict[str, Any]:
    """
    检查金标基准所需数据缓存是否可用

    Returns:
        Dict: 包含available、missing_stocks、details等字段
    """
    cache_manager = get_cache_manager()
    result = {
        "available": True,
        "missing_stocks": [],
        "missing_meta": [],
        "details": {}
    }

    start = GOLDEN_BENCHMARK_CONFIG["start_date"]
    end = GOLDEN_BENCHMARK_CONFIG["end_date"]
    stock_pool = GOLDEN_BENCHMARK_CONFIG["stock_pool"]

    # 检查元数据
    meta_status = cache_manager.check_meta_cache()
    result["details"]["meta"] = meta_status

    if not meta_status.get("trade_days", False):
        result["missing_meta"].append("trade_days")
        result["available"] = False

    if not meta_status.get("securities", False):
        result["missing_meta"].append("securities")
        result["available"] = False

    # 检查股票日线数据
    for symbol in stock_pool:
        status = cache_manager.check_stock_daily_cache(symbol, start, end, "qfq")
        result["details"][symbol] = status

        if not status.get("is_complete", False):
            result["missing_stocks"].append(symbol)
            result["available"] = False

    return result


def load_or_create_baseline() -> Dict[str, Any]:
    """
    加载或创建基准结果

    如果基准文件存在，加载已记录的基准值
    如果不存在，运行策略并记录基准

    Returns:
        Dict: 基准结果数据
    """
    baseline_file = os.path.join(_project_root, "tests/validation/golden_baseline.json")

    # 尝试加载已有基准
    if os.path.exists(baseline_file):
        with open(baseline_file, "r", encoding="utf-8") as f:
            baseline = json.load(f)
        return baseline

    # 基准不存在，需要创建
    return {
        "needs_creation": True,
        "baseline_file": baseline_file,
        "message": "基准文件不存在，请先运行数据预热并生成基准"
    }


def save_baseline(result: Dict[str, Any]) -> None:
    """
    保存基准结果到文件
    """
    baseline_file = os.path.join(_project_root, "tests/validation/golden_baseline.json")

    baseline_data = {
        "strategy_file": GOLDEN_BENCHMARK_CONFIG["strategy_file"],
        "start_date": GOLDEN_BENCHMARK_CONFIG["start_date"],
        "end_date": GOLDEN_BENCHMARK_CONFIG["end_date"],
        "stock_pool": GOLDEN_BENCHMARK_CONFIG["stock_pool"],
        "initial_capital": GOLDEN_BENCHMARK_CONFIG["initial_capital"],
        "final_value": result.get("final_value"),
        "pnl_pct": result.get("pnl_pct"),
        "baseline_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "run_environment": "local",
    }

    with open(baseline_file, "w", encoding="utf-8") as f:
        json.dump(baseline_data, f, indent=2, ensure_ascii=False)

    print(f"基准已保存至: {baseline_file}")


class TestGoldenBenchmark:
    """
    金标基准策略测试类

    CI硬验收门槛：测试失败则CI失败
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前设置"""
        self.config = GOLDEN_BENCHMARK_CONFIG
        self.cache_check = check_cache_availability()
        self.baseline = load_or_create_baseline()

    def test_config_is_valid(self):
        """
        测试配置有效性验证

        硬验收：配置必须正确
        """
        # 验证策略文件存在
        strategy_file = self.config["strategy_file"]
        if not strategy_file.startswith("strategies/"):
            strategy_file = os.path.join("strategies", strategy_file)

        full_path = os.path.join(_project_root, strategy_file)

        assert os.path.exists(full_path), \
            f"金标策略文件不存在: {full_path}\n这是硬验收失败，请检查策略文件路径"

        # 验证股票池不为空
        assert len(self.config["stock_pool"]) > 0, \
            "股票池为空，这是硬验收失败"

        # 验证日期有效
        start = self.config["start_date"]
        end = self.config["end_date"]

        try:
            start_dt = datetime.datetime.strptime(start, "%Y-%m-%d")
            end_dt = datetime.datetime.strptime(end, "%Y-%m-%d")
            assert end_dt > start_dt, \
                f"结束日期必须大于开始日期: {start} -> {end}"
        except ValueError as e:
            pytest.fail(f"日期格式错误: {e}")

    def test_cache_availability_check(self):
        """
        缓存可用性检查

        软性检查：输出警告但不硬失败
        如果缓存不可用，后续test_golden_benchmark_run会真正失败
        """
        if not self.cache_check["available"]:
            msg = "缓存数据检查结果（不影响测试，仅作诊断）：\n"
            if self.cache_check["missing_meta"]:
                msg += f"  缺失元数据: {self.cache_check['missing_meta']}\n"
            if self.cache_check["missing_stocks"]:
                msg += f"  缺失股票数据: {self.cache_check['missing_stocks']}\n"
            msg += "  建议: 运行 python tools/offline_data/prewarm_daily.py 预热数据"
            print(f"\nWARNING: {msg}")

    def test_golden_benchmark_run(self):
        """
        金标基准策略运行测试

        这是核心硬验收测试：
        1. 策略必须成功运行（不抛异常）
        2. 结果必须有有效数值（final_value > 0）
        3. 如果基准存在，结果必须在容差范围内

        失败条件：
        - 策略运行抛异常 -> pytest.fail
        - final_value <= 0 -> pytest.fail
        - 结果超出容差 -> pytest.fail
        """
        # 检查策略文件
        strategy_file = self.config["strategy_file"]
        if not strategy_file.startswith("strategies/"):
            strategy_file = os.path.join("strategies", strategy_file)

        full_path = os.path.join(_project_root, strategy_file)

        # 硬验收：文件必须存在
        if not os.path.exists(full_path):
            pytest.fail(f"金标策略文件不存在: {full_path}")

        # 运行策略
        try:
            result = run_jq_strategy(
                strategy_file=full_path,
                start_date=self.config["start_date"],
                end_date=self.config["end_date"],
                initial_capital=self.config["initial_capital"],
                stock_pool=self.config["stock_pool"],
                auto_discover_stocks=False,  # 使用固定股票池
                use_cache_only=False,  # 允许网络下载
            )
        except Exception as e:
            import traceback
            tb_lines = traceback.format_exc()
            pytest.fail(
                f"金标策略运行失败（硬验收）:\n"
                f"  策略: {strategy_file}\n"
                f"  错误: {str(e)}\n"
                f"  Traceback:\n{tb_lines[-10:]}"
            )

        # 硬验收：结果必须有效
        if result is None:
            pytest.fail(
                f"金标策略返回None（硬验收）:\n"
                f"  策略: {strategy_file}\n"
                f"  可能原因: 数据加载失败或策略未正确初始化\n"
                f"  建议: 检查缓存数据是否存在，或运行数据预热脚本"
            )

        # 硬验收：final_value必须存在且大于0
        assert "final_value" in result, \
            f"结果缺少final_value字段: {result.keys()}"

        final_value = result["final_value"]

        assert final_value > 0, \
            f"最终资金无效: {final_value}"

        # 硬验收：pnl_pct必须存在
        assert "pnl_pct" in result, \
            f"结果缺少pnl_pct字段: {result.keys()}"

        pnl_pct = result["pnl_pct"]

        # 验证收益率合理性（不应该有极端异常值）
        assert abs(pnl_pct) < 500, \
            f"收益率异常（>{500}%），可能数据问题: pnl_pct={pnl_pct}"

        # GATE-2硬验收：runtime_errors必须为0
        runtime_errors = result.get("runtime_errors", [])
        if len(runtime_errors) > 0:
            error_details = "\n".join([
                f"    - {err.get('function', 'unknown')}: {err.get('error_type', 'unknown')} - {err.get('error', '')[:100]}"
                for err in runtime_errors[:5]
            ])
            pytest.fail(
                f"金标基准运行时存在错误（硬验收失败）:\n"
                f"  错误数量: {len(runtime_errors)}\n"
                f"  错误详情:\n{error_details}"
                f"{f'\n  ... 还有 {len(runtime_errors) - 5} 个错误' if len(runtime_errors) > 5 else ''}\n"
                f"  建议: 检查策略代码和数据完整性，确保无运行时错误"
            )

        # 输出运行结果
        print(f"\n金标基准策略运行结果:")
        print(f"  策略: {strategy_file}")
        print(f"  日期区间: {self.config['start_date']} ~ {self.config['end_date']}")
        print(f"  股票池: {self.config['stock_pool']}")
        print(f"  初始资金: {self.config['initial_capital']}")
        print(f"  最终资金: {final_value:,.2f}")
        print(f"  收益率: {pnl_pct:.2f}%")

        # 如果基准存在，进行容差检查
        if not self.baseline.get("needs_creation", False):
            expected_final = self.baseline.get("final_value")
            expected_pnl = self.baseline.get("pnl_pct")

            if expected_final is not None:
                # 硬验收：final_value容差检查
                tolerance_pct = self.config["expected_baseline"]["final_value_tolerance_pct"]
                diff_pct = abs(final_value - expected_final) / expected_final * 100

                if diff_pct > tolerance_pct:
                    pytest.fail(
                        f"金标基准final_value超出容差（硬验收）:\n"
                        f"  实际值: {final_value:,.2f}\n"
                        f"  预期值: {expected_final:,.2f}\n"
                        f"  误差: {diff_pct:.2f}%\n"
                        f"  容差: {tolerance_pct}%\n"
                        f"  可能原因: 数据源变化、策略逻辑变更、缓存数据不完整\n"
                        f"  建议: 检查数据完整性，或更新基准值"
                    )
                else:
                    print(f"  final_value容差检查通过: 误差{diff_pct:.2f}% < 容差{tolerance_pct}%")

            if expected_pnl is not None:
                # 硬验收：pnl_pct容差检查
                tolerance = self.config["expected_baseline"]["pnl_pct_tolerance"]
                diff = abs(pnl_pct - expected_pnl)

                if diff > tolerance:
                    pytest.fail(
                        f"金标基准pnl_pct超出容差（硬验收）:\n"
                        f"  实际值: {pnl_pct:.2f}%\n"
                        f"  预期值: {expected_pnl:.2f}%\n"
                        f"  误差: {diff:.2f}%\n"
                        f"  容差: {tolerance}%\n"
                        f"  可能原因: 数据源变化、策略逻辑变更\n"
                        f"  建议: 检查数据完整性，或更新基准值"
                    )
                else:
                    print(f"  pnl_pct容差检查通过: 误差{diff:.2f}% < 容差{tolerance}%")
        else:
            # GATE-2硬验收：基准文件必须存在
            pytest.fail(
                f"金标基准文件不存在（硬验收失败）:\n"
                f"  期望文件: {self.baseline.get('baseline_file', 'tests/validation/golden_baseline.json')}\n"
                f"  当前结果: final_value={final_value:,.2f}, pnl_pct={pnl_pct:.2f}%\n"
                f"  建议: 运行以下命令生成基准文件:\n"
                f"    python tests/validation/create_golden_baseline.py\n"
                f"  注意: 基准文件是CI硬门槛，必须存在且通过验收才能合并代码"
            )

    def test_strategy_runs_without_error(self):
        """
        简化版验收：仅验证策略能运行

        用于快速CI验收，不检查具体数值
        """
        strategy_file = self.config["strategy_file"]
        if not strategy_file.startswith("strategies/"):
            strategy_file = os.path.join("strategies", strategy_file)

        full_path = os.path.join(_project_root, strategy_file)

        if not os.path.exists(full_path):
            pytest.fail(f"策略文件不存在: {full_path}")

        # 尝试运行，捕获所有异常
        exc_info = None
        result = None

        try:
            result = run_jq_strategy(
                strategy_file=full_path,
                start_date=self.config["start_date"],
                end_date=self.config["end_date"],
                initial_capital=self.config["initial_capital"],
                stock_pool=self.config["stock_pool"],
                auto_discover_stocks=False,
            )
        except Exception as e:
            exc_info = e

        # 硬验收：不能有异常
        if exc_info is not None:
            pytest.fail(
                f"策略运行抛出异常（硬验收失败）:\n"
                f"  异常类型: {type(exc_info).__name__}\n"
                f"  异常信息: {str(exc_info)}"
            )

        # 硬验收：必须有返回值
        if result is None:
            pytest.fail("策略返回None（硬验收失败）")

        # 硬验收：返回值必须有基本字段
        assert "final_value" in result, "结果缺少final_value"
        assert "pnl_pct" in result, "结果缺少pnl_pct"
        assert result["final_value"] > 0, f"final_value无效: {result['final_value']}"


def test_golden_benchmark_quick():
    """
    快速金标验收测试（独立函数）

    用于CI快速验收，验证核心链路可用
    """
    config = GOLDEN_BENCHMARK_CONFIG

    strategy_file = config["strategy_file"]
    if not strategy_file.startswith("strategies/"):
        strategy_file = os.path.join("strategies", strategy_file)

    full_path = os.path.join(_project_root, strategy_file)

    # 硬验收：文件存在
    assert os.path.exists(full_path), f"策略文件不存在: {full_path}"

    # 运行策略
    result = None
    exception = None

    try:
        result = run_jq_strategy(
            strategy_file=full_path,
            start_date=config["start_date"],
            end_date=config["end_date"],
            initial_capital=config["initial_capital"],
            stock_pool=config["stock_pool"],
            auto_discover_stocks=False,
        )
    except Exception as e:
        exception = e

    # 硬验收：无异常
    if exception is not None:
        pytest.fail(
            f"金标基准策略运行失败:\n"
            f"  策略: {config['strategy_file']}\n"
            f"  参数: start={config['start_date']}, end={config['end_date']}\n"
            f"  股票池: {config['stock_pool']}\n"
            f"  错误: {str(exception)}"
        )

    # 硬验收：有结果
    if result is None:
        pytest.fail("策略返回None - 数据可能缺失，请检查缓存")

    # 硬验收：结果有效
    assert result["final_value"] > 0, \
        f"最终资金无效: {result['final_value']}"

    assert abs(result["pnl_pct"]) < 500, \
        f"收益率异常: {result['pnl_pct']}%"

    print(f"\n金标基准验收通过:")
    print(f"  最终资金: {result['final_value']:,.2f}")
    print(f"  收益率: {result['pnl_pct']:.2f}%")


def test_baseline_file_consistency():
    """
    基准文件一致性检查

    如果基准文件存在，验证其配置与当前测试配置一致
    """
    baseline_file = os.path.join(_project_root, "tests/validation/golden_baseline.json")

    if not os.path.exists(baseline_file):
        # 基准不存在，跳过一致性检查
        pytest.skip("基准文件不存在，跳过一致性检查")

    with open(baseline_file, "r", encoding="utf-8") as f:
        baseline = json.load(f)

    config = GOLDEN_BENCHMARK_CONFIG

    # 硬验收：策略文件一致
    assert baseline["strategy_file"] == config["strategy_file"], \
        f"策略文件不一致: 基准={baseline['strategy_file']}, 测试={config['strategy_file']}"

    # 硬验收：日期一致
    assert baseline["start_date"] == config["start_date"], \
        f"开始日期不一致: 基准={baseline['start_date']}, 测试={config['start_date']}"

    assert baseline["end_date"] == config["end_date"], \
        f"结束日期不一致: 基准={baseline['end_date']}, 测试={config['end_date']}"

    # 硬验收：股票池一致
    assert baseline["stock_pool"] == config["stock_pool"], \
        f"股票池不一致: 基准={baseline['stock_pool']}, 测试={config['stock_pool']}"

    print("基准文件配置一致性检查通过")


if __name__ == "__main__":
    # 运行金标基准测试
    pytest.main([__file__, "-v", "-s"])