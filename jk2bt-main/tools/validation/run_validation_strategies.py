"""
run_validation_strategies.py
运行验收策略集并生成验收报告

功能：
1. 运行所有验收策略
2. 收集运行结果
3. 生成验收报告
4. 统计数据使用情况

使用方法：
    python run_validation_strategies.py --offline
    python run_validation_strategies.py --limit 3
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime
from typing import Dict, List
import time

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from jk2bt import run_jq_strategy
from jk2bt.db.cache_status import get_cache_manager


def load_validation_strategies() -> List[Dict]:
    """加载验收策略配置"""
    config_file = os.path.join(_project_root, "tools/validation/validation_strategies.json")
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def run_single_strategy(strategy: Dict, offline_mode: bool = False) -> Dict:
    """
    运行单个验收策略

    Returns:
        Dict: {
            'success': bool,
            'strategy_id': str,
            'strategy_name': str,
            'final_value': float,
            'pnl_pct': float,
            'run_time': float,
            'error': str (if failed)
        }
    """
    result = {
        'success': False,
        'strategy_id': strategy['id'],
        'strategy_name': strategy['name'],
        'start_time': datetime.now().isoformat(),
    }

    # 检查策略文件
    strategy_file = strategy.get('file')
    if not strategy_file.startswith('strategies/'):
        strategy_file = os.path.join('strategies', strategy_file)

    full_path = os.path.join(_project_root, strategy_file)
    if not os.path.exists(full_path):
        result['error'] = f'策略文件不存在: {full_path}'
        result['end_time'] = datetime.now().isoformat()
        return result

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
            logger.info(f"策略 {strategy['id']} 使用fixed_stock_pool fallback")

    ep = strategy.get('etf_pool', {})
    if ep.get('type') == 'fixed':
        etf_pool = ep.get('symbols', [])

    all_pool = stock_pool + etf_pool

    if len(all_pool) == 0:
        result['error'] = '股票池/ETF池为空，请检查配置（需要fixed_stock_pool fallback）'
        result['end_time'] = datetime.now().isoformat()
        return result

    # 运行策略
    start_time = time.time()

    try:
        logger.info(f"运行策略 {strategy['id']}: {strategy['name']}")

        run_result = run_jq_strategy(
            strategy_file=full_path,
            start_date=start,
            end_date=end,
            initial_capital=1000000,
            stock_pool=all_pool[:10],  # 限制股票池大小以加快运行
            use_cache_only=offline_mode,  # 离线模式传递到use_cache_only
        )

        if run_result:
            result['success'] = True
            result['final_value'] = run_result.get('final_value', 0)
            result['pnl_pct'] = run_result.get('pnl_pct', 0)
            logger.info(f"✅ 策略 {strategy['id']} 运行成功: "
                       f"收益率 {result['pnl_pct']:.2f}%")
        else:
            result['error'] = '运行结果为None'
            logger.error(f"❌ 策略 {strategy['id']} 运行失败: {result['error']}")

    except Exception as e:
        result['error'] = str(e)
        logger.error(f"❌ 策略 {strategy['id']} 运行失败: {e}")

    end_time = time.time()
    result['run_time'] = end_time - start_time
    result['end_time'] = datetime.now().isoformat()

    return result


def generate_validation_report(results: List[Dict]) -> str:
    """生成验收报告"""

    cache_manager = get_cache_manager()
    cache_summary = cache_manager.get_cache_summary()

    report_lines = []
    report_lines.append("# jk2bt 验收策略集运行报告")
    report_lines.append(f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"\n## 运行结果汇总\n")

    # 统计结果
    total = len(results)
    success_count = sum(1 for r in results if r['success'])
    failed_count = total - success_count
    p0_count = sum(1 for r in results if r.get('priority') == 'P0')
    p0_success = sum(1 for r in results if r['success'] and r.get('priority') == 'P0')

    report_lines.append(f"- 总策略数: {total}\n")
    report_lines.append(f"- 成功: {success_count}\n")
    report_lines.append(f"- 失败: {failed_count}\n")
    report_lines.append(f"- P0策略: {p0_count}（必须通过）\n")
    report_lines.append(f"- P0通过: {p0_success}\n")

    if p0_success == p0_count:
        report_lines.append(f"\n✅ **验收通过：所有P0策略运行成功**\n")
    else:
        report_lines.append(f"\n❌ **验收失败：{p0_count - p0_success}个P0策略失败**\n")

    # 详细结果
    report_lines.append(f"\n## 策略运行详情\n")
    report_lines.append("| ID | 策略名称 | 优先级 | 状态 | 收益率 | 运行时间 | 备注 |\n")
    report_lines.append("|----|---------|-------|------|--------|---------|-----|\n")

    for result in results:
        status = "✅ 通过" if result['success'] else "❌ 失败"
        priority = result.get('priority', 'P1')
        pnl = f"{result.get('pnl_pct', 0):.2f}%" if result['success'] else "N/A"
        run_time = f"{result.get('run_time', 0):.1f}s" if result['success'] else "N/A"
        note = result.get('error', '')[:30] if not result['success'] else ""

        report_lines.append(
            f"| {result['strategy_id']} | {result['strategy_name']} | {priority} | "
            f"{status} | {pnl} | {run_time} | {note} |\n"
        )

    # 数据统计
    report_lines.append(f"\n## 数据缓存统计\n")
    report_lines.append(f"- 股票数据: {cache_summary['stock_count']}只\n")
    report_lines.append(f"- ETF数据: {cache_summary['etf_count']}只\n")
    report_lines.append(f"- 指数数据: {cache_summary['index_count']}只\n")
    report_lines.append(f"- 总记录数: {cache_summary['total_records']}\n")

    # 失败策略详情
    failed_results = [r for r in results if not r['success']]
    if failed_results:
        report_lines.append(f"\n## 失败策略详情\n")
        for result in failed_results:
            report_lines.append(f"\n### {result['strategy_id']}: {result['strategy_name']}\n")
            report_lines.append(f"- **错误信息**: {result.get('error', 'N/A')}\n")
            report_lines.append(f"- **开始时间**: {result.get('start_time', 'N/A')}\n")
            report_lines.append(f"- **结束时间**: {result.get('end_time', 'N/A')}\n")

    report_lines.append(f"\n---\n")
    report_lines.append(f"Generated by jk2bt tools/validation/run_validation_strategies.py\n")

    return ''.join(report_lines)


def main():
    parser = argparse.ArgumentParser(description="运行验收策略集")
    parser.add_argument("--offline", action="store_true", help="离线模式运行")
    parser.add_argument("--limit", type=int, default=None, help="限制运行策略数量")
    parser.add_argument("--p0-only", action="store_true", help="仅运行P0优先级策略")

    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info("开始运行验收策略集...")
    logger.info("=" * 80)

    # 加载策略
    strategies = load_validation_strategies()
    logger.info(f"加载了 {len(strategies)} 个验收策略")

    # 过滤策略
    if args.p0_only:
        strategies = [s for s in strategies if s.get('validation_priority') == 'P0']
        logger.info(f"仅运行P0策略: {len(strategies)}个")

    if args.limit:
        strategies = strategies[:args.limit]
        logger.info(f"限制运行策略数: {len(strategies)}个")

    # 运行策略
    results = []

    for i, strategy in enumerate(strategies, 1):
        logger.info(f"\n[{i}/{len(strategies)}] 运行策略 {strategy['id']}: {strategy['name']}")

        result = run_single_strategy(strategy, args.offline)
        result['priority'] = strategy.get('validation_priority', 'P1')
        results.append(result)

        # 显示进度
        success_so_far = sum(1 for r in results if r['success'])
        logger.info(f"进度: {success_so_far}/{i} 成功")

    # 生成报告
    logger.info("\n" + "=" * 80)
    logger.info("生成验收报告...")
    logger.info("=" * 80)

    report_content = generate_validation_report(results)

    report_file = os.path.join(_project_root, "validation_report.md")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)

    logger.info(f"✅ 验收报告已生成: {report_file}")

    # 打印摘要
    print("\n" + "=" * 80)
    print("验收策略集运行完成")
    print("=" * 80)

    success_count = sum(1 for r in results if r['success'])
    failed_count = len(results) - success_count

    print(f"\n运行结果:")
    print(f"  总策略数: {len(results)}")
    print(f"  成功: {success_count}")
    print(f"  失败: {failed_count}")

    if failed_count == 0:
        print("\n✅ 所有验收策略运行成功！")
    else:
        print(f"\n❌ {failed_count}个策略运行失败")
        print("请查看验收报告: validation_report.md")

    print("=" * 80)

    # 返回状态
    return success_count == len(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)