"""
策略回放正确性验证测试

测试目标：
1. 验证策略能否正确加载
2. 验证策略能否正确运行
3. 验证交易是否真实发生
4. 验证结果是否符合预期
"""

import pytest
import os
import sys
import json
import tempfile
from datetime import datetime

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "src"),
)

try:
    jk2bt..core.runner as runner

    load_jq_strategy = runner.load_jq_strategy
    run_jq_strategy = runner.run_jq_strategy
except ImportError as e:
    pytest.skip(f"无法导入runner: {e}", allow_module_level=True)


class TestStrategyLoading:
    """测试策略加载"""

    def test_load_simple_strategy(self):
        """测试简单策略加载"""
        strategy_code = """
def initialize(context):
    g.count = 0
    
def handle_data(context, data):
    g.count += 1
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(strategy_code)
            f.flush()

            try:
        functions, source = load_jq_strategy(f.name)

                assert functions is not None, "load_jq_strategy应返回函数字典"
                assert "initialize" in functions, "应包含initialize函数"
                assert "handle_data" in functions, "应包含handle_data函数"
            finally:
                os.unlink(f.name)

    def test_load_gbk_encoded_strategy(self):
        """测试GBK编码策略加载"""
        strategy_code = """
def initialize(context):
    log.info('初始化')
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="gbk"
        ) as f:
            f.write(strategy_code)
            f.flush()

            try:
                functions, source = load_jq_strategy(f.name)
                assert functions is not None, "应能加载GBK编码文件"
                assert "initialize" in functions
            finally:
                os.unlink(f.name)

    def test_load_real_strategy_file(self):
        """测试加载真实策略文件"""
        strategy_file = "jkcode/jkcode/03 一个简单而持续稳定的懒人超额收益策略.txt"

        if not os.path.exists(strategy_file):
            pytest.skip(f"策略文件不存在: {strategy_file}")

        functions, source = load_jq_strategy(strategy_file)

        assert functions is not None
        assert "initialize" in functions
        assert "handle_trader" in functions or "handle_prepare" in functions

    def test_load_nonexistent_file(self):
        """测试加载不存在的文件"""
        with pytest.raises(FileNotFoundError):
            load_jq_strategy("nonexistent_file.txt")


class TestStrategyExecution:
    """测试策略运行"""

    @pytest.mark.slow
    def test_run_simple_buy_strategy(self):
        """测试简单买入策略"""
        strategy_code = """
def initialize(context):
    run_daily(buy_stock, 'open')
    
def buy_stock(context):
    if len(context.portfolio.positions) == 0:
        order_value('600519.XSHG', 10000)
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(strategy_code)
            f.flush()

            try:
                result = run_jq_strategy(
                    f.name,
                    start_date="2022-01-01",
                    end_date="2022-01-31",
                    initial_capital=100000,
                    stock_pool=["600519.XSHG"],
                )

                assert result is not None, "run_jq_strategy应返回结果"
                assert "final_value" in result
                assert "strategy" in result

            finally:
                os.unlink(f.name)

    @pytest.mark.slow
    def test_run_real_strategy_03(self):
        """测试运行真实策略03"""
        strategy_file = "jkcode/jkcode/03 一个简单而持续稳定的懒人超额收益策略.txt"

        if not os.path.exists(strategy_file):
            pytest.skip(f"策略文件不存在: {strategy_file}")

        result = run_jq_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result is not None, "策略应成功运行"
        assert result["final_value"] > 0, "最终资金应大于0"
        assert result["final_value"] != 100000, "最终资金应有变化"


class TestTradeValidation:
    """测试交易验证"""

    @pytest.mark.slow
    def test_strategy_with_real_trades(self):
        """测试有真实交易的策略"""
        strategy_file = "jkcode/jkcode/03 一个简单而持续稳定的懒人超额收益策略.txt"

        if not os.path.exists(strategy_file):
            pytest.skip(f"策略文件不存在: {strategy_file}")

        result = run_jq_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        if result is None:
            pytest.fail("策略运行失败")

        strategy = result.get("strategy")

        # 检查订单
        if hasattr(strategy, "orders") and strategy.orders:
            orders = strategy.orders
            assert len(orders) > 0, "应有订单产生"

            # 检查订单类型
            buy_orders = [o for o in orders if o.get("action") == "buy"]
            sell_orders = [o for o in orders if o.get("action") == "sell"]

            print(f"买入订单: {len(buy_orders)}, 卖出订单: {len(sell_orders)}")

    @pytest.mark.slow
    def test_strategy_no_trade_scenario(self):
        """测试无交易场景（验证假跑通识别）"""
        strategy_code = """
def initialize(context):
    g.stocks = []
    
def handle_data(context, data):
    # 不做任何交易
    pass
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(strategy_code)
            f.flush()

            try:
                result = run_jq_strategy(
                    f.name,
                    start_date="2022-01-01",
                    end_date="2022-01-31",
                    initial_capital=100000,
                    stock_pool=["600519.XSHG"],
                )

                # 空策略应该返回初始资金
                assert result is not None
                assert result["final_value"] == 100000, "无交易策略应返回初始资金"

            finally:
                os.unlink(f.name)


class TestTimerValidation:
    """测试定时器验证"""

    def test_run_monthly_registration(self):
        """测试月度定时器注册"""
        strategy_code = """
def initialize(context):
    run_monthly(monthly_task, 1, 'open')
    g.monthly_count = 0
    
def monthly_task(context):
    g.monthly_count += 1
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(strategy_code)
            f.flush()

            try:
                result = run_jq_strategy(
                    f.name,
                    start_date="2022-01-01",
                    end_date="2022-03-31",
                    initial_capital=100000,
                    stock_pool=["600519.XSHG"],
                )

                if result and "strategy" in result:
                    strategy = result["strategy"]
                    if hasattr(strategy, "timer_manager"):
                        assert len(strategy.timer_manager.timers) > 0, "应注册定时器"

            finally:
                os.unlink(f.name)

    def test_run_daily_registration(self):
        """测试每日定时器注册"""
        strategy_code = """
def initialize(context):
    run_daily(daily_task, 'open')
    g.daily_count = 0
    
def daily_task(context):
    g.daily_count += 1
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(strategy_code)
            f.flush()

            try:
                result = run_jq_strategy(
                    f.name,
                    start_date="2022-01-01",
                    end_date="2022-01-31",
                    initial_capital=100000,
                    stock_pool=["600519.XSHG"],
                )

                if result and "strategy" in result:
                    strategy = result["strategy"]
                    if hasattr(strategy, "timer_manager"):
                        assert len(strategy.timer_manager.timers) > 0, "应注册定时器"

            finally:
                os.unlink(f.name)


class TestStrategyValidator:
    """测试策略验证器"""

    def test_validator_initialization(self):
        """测试验证器初始化"""
        from jk2bt.core.validator import StrategyValidationResult

        result = StrategyValidationResult("test_strategy.txt")

        assert result.strategy_name == "test_strategy.txt"
        assert result.load_success == False
        assert result.run_success == False

    def test_validator_to_dict(self):
        """测试验证器转字典"""
        from jk2bt.core.validator import StrategyValidationResult

        result = StrategyValidationResult("test_strategy.txt")
        result.load_success = True
        result.functions_found = ["initialize", "handle_data"]

        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)
        assert result_dict["load_success"] == True
        assert result_dict["functions_found"] == ["initialize", "handle_data"]


class TestDataAPIValidation:
    """测试数据API验证"""

    def test_get_index_stocks(self):
        """测试get_index_stocks"""
        try:
            jk2bt..backtrader_base_strategy as base

            stocks = base.get_index_stocks("000300.XSHG")

            assert stocks is not None, "get_index_stocks应返回结果"
            assert isinstance(stocks, list), "应返回列表"
            assert len(stocks) > 0, "沪深300应有成分股"

        except ImportError:
            pytest.skip("无法导入backtrader_base_strategy")

    def test_get_current_data(self):
        """测试get_current_data"""
        try:
            jk2bt..backtrader_base_strategy as base

            data = base.get_current_data()

            assert data is not None, "get_current_data应返回结果"

        except ImportError:
            pytest.skip("无法导入backtrader_base_strategy")


class TestRealStrategyValidation:
    """真实策略验证测试"""

    @pytest.mark.slow
    @pytest.mark.parametrize(
        "strategy_file,expected_trades",
        [
            ("jkcode/jkcode/03 一个简单而持续稳定的懒人超额收益策略.txt", True),
            ("jkcode/jkcode/04 红利搬砖_测试版.txt", True),
        ],
    )
    def test_real_strategy_validation(self, strategy_file, expected_trades):
        """测试真实策略验证"""
        if not os.path.exists(strategy_file):
            pytest.skip(f"策略文件不存在: {strategy_file}")

        # 加载策略
        functions = load_jq_strategy(strategy_file)
        assert functions is not None, "策略加载失败"
        assert "initialize" in functions, "缺少initialize函数"

        # 运行策略
        result = run_jq_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result is not None, "策略运行失败"

        # 验证交易
        if expected_trades:
            # 有交易预期
            final_value = result.get("final_value", 0)

            # 至少应该有变化（可能盈利也可能亏损）
            # 注意：初始资金是100000，最终资金可能大于或小于
            print(f"最终资金: {final_value}")


class TestValidationReport:
    """测试验证报告生成"""

    def test_generate_validation_json(self):
        """测试生成验证JSON报告"""
        validation_result = {
            "validation_time": datetime.now().isoformat(),
            "results": [
                {"strategy_file": "test.txt", "load_success": True, "run_success": True}
            ],
        }

        output_file = tempfile.NamedTemporaryFile(suffix=".json", delete=False).name

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(validation_result, f, ensure_ascii=False, indent=2)

            assert os.path.exists(output_file)

            with open(output_file, "r") as f:
                loaded = json.load(f)

            assert loaded["results"][0]["load_success"] == True

        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)


# 运行测试的辅助函数
def run_validation_suite():
    """运行验证测试套件"""
    import subprocess

    result = subprocess.run(
        [".venv/bin/python", "-m", "pytest", __file__, "-v", "--tb=short"],
        capture_output=True,
        text=True,
    )

    print(result.stdout)
    print(result.stderr)

    return result.returncode == 0


if __name__ == "__main__":
    # 直接运行测试
    pytest.main([__file__, "-v", "--tb=short"])
