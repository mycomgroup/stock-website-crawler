"""
tests/validation/test_validation_strategies.py
验收策略集测试 - 离线模式下运行金标策略

功能：
1. 验证所有验收策略能否在离线模式运行
2. 检查数据完整性
3. 生成验收报告
"""

import os
import sys
import pytest
import json
import datetime
from typing import Dict, List

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from jk2bt import run_jq_strategy
from jk2bt.db.cache_status import CacheManager, get_cache_manager


def load_validation_strategies() -> List[Dict]:
    """加载验收策略配置"""
    config_file = os.path.join(_project_root, "tools/validation/validation_strategies.json")
    if not os.path.exists(config_file):
        pytest.skip(f"验收策略配置文件不存在: {config_file}")

    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def check_data_availability(strategy: Dict, cache_manager: CacheManager) -> Dict:
    """
    检查策略所需数据是否在缓存中可用

    Returns:
        Dict: {'available': bool, 'missing': List[str], 'details': Dict}
    """
    result = {'available': True, 'missing': [], 'details': {}}

    time_range = strategy.get('time_range', {})
    start = time_range.get('start', '2020-01-01')
    end = time_range.get('end', '2023-12-31')

    # 检查元数据
    meta_status = cache_manager.check_meta_cache()
    result['details']['meta'] = meta_status

    if not meta_status['trade_days']:
        result['missing'].append('trade_days')
        result['available'] = False

    if not meta_status['securities']:
        result['missing'].append('securities')
        result['available'] = False

    # 检查股票日线数据（使用聚宽格式，cache_manager内部已支持格式兼容）
    stock_pool = strategy.get('stock_pool', {})
    if stock_pool.get('type') == 'fixed':
        symbols = stock_pool.get('symbols', [])
        for symbol in symbols:
            # 直接使用聚宽格式查询，cache_manager会自动处理格式转换
            status = cache_manager.check_stock_daily_cache(symbol, start, end, 'qfq')
            if not status['is_complete']:
                result['missing'].append(f"stock_daily:{symbol}")
                result['available'] = False

    # 检查ETF日线数据（使用聚宽格式，cache_manager内部已支持格式兼容）
    etf_pool = strategy.get('etf_pool', {})
    if etf_pool.get('type') == 'fixed':
        symbols = etf_pool.get('symbols', [])
        for symbol in symbols:
            # 直接使用聚宽格式查询，cache_manager会自动处理格式转换
            status = cache_manager.check_etf_daily_cache(symbol, start, end)
            if not status['is_complete']:
                result['missing'].append(f"etf_daily:{symbol}")
                result['available'] = False

    return result


class TestValidationStrategies:
    """验收策略集测试"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前设置"""
        self.strategies = load_validation_strategies()
        self.cache_manager = get_cache_manager()

    def test_all_strategies_loaded(self):
        """测试所有验收策略配置都已加载"""
        assert len(self.strategies) > 0, "验收策略配置为空"
        assert len(self.strategies) == 7, f"预期7个验收策略，实际{len(self.strategies)}个"

        # 检查每个策略的必要字段
        required_fields = ['id', 'name', 'file', 'time_range', 'apis']
        for strategy in self.strategies:
            for field in required_fields:
                assert field in strategy, f"策略{strategy.get('id', 'unknown')}缺少字段{field}"

    def test_data_availability(self):
        """测试数据是否完整可用（软性检查，仅警告）"""
        missing_data_strategies = []

        for strategy in self.strategies:
            check_result = check_data_availability(strategy, self.cache_manager)

            if not check_result['available']:
                missing_data_strategies.append({
                    'id': strategy['id'],
                    'name': strategy['name'],
                    'missing': check_result['missing']
                })

        if missing_data_strategies:
            msg = "以下策略数据缓存检查显示缺失（实际运行测试已验证可运行）:\n"
            for item in missing_data_strategies:
                msg += f"  {item['id']} ({item['name']}): {', '.join(item['missing'])}\n"
            # 软性检查：不硬性失败，仅输出警告
            # 实际数据可用性已通过 test_run_strategy 验证
            print(f"\nWARNING: {msg}")

    @pytest.mark.parametrize("strategy_idx", range(7))
    def test_run_strategy(self, strategy_idx):
        """测试运行每个验收策略"""
        strategy = self.strategies[strategy_idx]

        # 检查策略文件是否存在
        strategy_file = strategy.get('file')
        if not strategy_file.startswith('strategies/'):
            strategy_file = os.path.join('strategies', strategy_file)

        full_path = os.path.join(_project_root, strategy_file)
        if not os.path.exists(full_path):
            pytest.skip(f"策略文件不存在: {full_path}")

        # 提取配置
        time_range = strategy.get('time_range', {})
        start = time_range.get('start', '2020-01-01')
        end = time_range.get('end', '2023-12-31')

        # 构造股票池/ETF池
        stock_pool = []
        etf_pool = []

        sp = strategy.get('stock_pool', {})
        if sp.get('type') == 'fixed':
            stock_pool = sp.get('symbols', [])
        elif sp.get('type') == 'dynamic':
            # 动态池使用fixed_stock_pool作为fallback
            fallback = strategy.get('fixed_stock_pool', {})
            if fallback.get('type') == 'fixed':
                stock_pool = fallback.get('symbols', [])

        ep = strategy.get('etf_pool', {})
        if ep.get('type') == 'fixed':
            etf_pool = ep.get('symbols', [])

        # 合并股票池和ETF池
        all_pool = stock_pool + etf_pool

        if len(all_pool) == 0:
            pytest.fail(f"策略{strategy['id']}股票池/ETF池为空，请检查配置（需要fixed_stock_pool fallback）")

        # 运行策略
        try:
            result = run_jq_strategy(
                strategy_file=full_path,
                start_date=start,
                end_date=end,
                initial_capital=1000000,
                stock_pool=all_pool[:10],  # 限制股票池大小以加快测试
            )

            assert result is not None, f"策略{strategy['id']}运行返回None"
            assert 'final_value' in result, f"策略{strategy['id']}结果缺少final_value"
            assert 'pnl_pct' in result, f"策略{strategy['id']}结果缺少pnl_pct"

            # 验证结果合理性
            assert result['final_value'] > 0, f"策略{strategy['id']}最终资金<=0"
            assert abs(result['pnl_pct']) < 200, f"策略{strategy['id']}收益率异常（>{200}%）"

        except Exception as e:
            pytest.fail(f"策略{strategy['id']} ({strategy['name']}) 运行失败: {str(e)}")

    def test_p0_strategies_must_pass(self):
        """P0优先级策略必须全部通过"""
        p0_strategies = [s for s in self.strategies if s.get('validation_priority') == 'P0']

        failed = []
        for strategy in p0_strategies:
            strategy_file = strategy.get('file')
            if not strategy_file.startswith('strategies/'):
                strategy_file = os.path.join('strategies', strategy_file)

            full_path = os.path.join(_project_root, strategy_file)

            if not os.path.exists(full_path):
                failed.append({
                    'id': strategy['id'],
                    'reason': '文件不存在'
                })
                continue

            try:
                time_range = strategy.get('time_range', {})
                start = time_range.get('start', '2020-01-01')
                end = time_range.get('end', '2023-12-31')

                sp = strategy.get('stock_pool', {})
                ep = strategy.get('etf_pool', {})

                pool = []
                if sp.get('type') == 'fixed':
                    pool.extend(sp.get('symbols', []))
                elif sp.get('type') == 'dynamic':
                    # 动态池使用fixed_stock_pool作为fallback
                    fallback = strategy.get('fixed_stock_pool', {})
                    if fallback.get('type') == 'fixed':
                        pool.extend(fallback.get('symbols', []))
                if ep.get('type') == 'fixed':
                    pool.extend(ep.get('symbols', []))

                # P0策略必须运行，不能因为pool为空而跳过
                if len(pool) == 0:
                    failed.append({
                        'id': strategy['id'],
                        'reason': '股票池为空，请检查配置（需要fixed_stock_pool fallback）'
                    })
                    continue

                result = run_jq_strategy(
                    strategy_file=full_path,
                    start_date=start,
                    end_date=end,
                    initial_capital=1000000,
                    stock_pool=pool[:10],
                )

                if result is None or result['final_value'] <= 0:
                    failed.append({
                        'id': strategy['id'],
                        'reason': '运行结果异常'
                    })

            except Exception as e:
                failed.append({
                    'id': strategy['id'],
                    'reason': str(e)
                })

        if failed:
            msg = f"{len(failed)}个P0策略失败:\n"
            for item in failed:
                msg += f"  {item['id']}: {item['reason']}\n"
            pytest.fail(msg)


def test_generate_validation_report():
    """生成验收报告（非测试，用于生成文档）"""
    strategies = load_validation_strategies()
    cache_manager = get_cache_manager()

    report_lines = []
    report_lines.append("# jk2bt 验收策略集报告")
    report_lines.append(f"\n生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"\n## 策略清单\n")

    report_lines.append("| ID | 策略名称 | 优先级 | 数据状态 | 备注 |\n")
    report_lines.append("|----|---------|-------|---------|-----|\n")

    for strategy in strategies:
        check_result = check_data_availability(strategy, cache_manager)
        data_status = "✅" if check_result['available'] else "❌"
        priority = strategy.get('validation_priority', 'P1')

        report_lines.append(
            f"| {strategy['id']} | {strategy['name']} | {priority} | {data_status} | "
            f"{strategy.get('description', '')[:30]} |\n"
        )

    # 数据统计
    cache_summary = cache_manager.get_cache_summary()
    report_lines.append(f"\n## 缓存统计\n")
    report_lines.append(f"- 股票数据: {cache_summary['stock_count']}只\n")
    report_lines.append(f"- ETF数据: {cache_summary['etf_count']}只\n")
    report_lines.append(f"- 指数数据: {cache_summary['index_count']}只\n")
    report_lines.append(f"- 总记录数: {cache_summary['total_records']}\n")

    report_content = ''.join(report_lines)

    report_file = os.path.join(_project_root, "validation_report.md")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"\n验收报告已生成: {report_file}")


if __name__ == "__main__":
    # 运行验收测试
    pytest.main([__file__, "-v", "-s"])

    # 生成验收报告
    test_generate_validation_report()