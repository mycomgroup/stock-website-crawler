"""
批量策略兼容性测试脚本 - 简化版
快速测试策略能否成功加载并识别缺失的API
"""

import os
import sys
import time
import random
import traceback
import re
from datetime import datetime
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 输出目录
REPORTS_DIR = PROJECT_ROOT / "reports"

def get_all_strategy_files():
    """获取所有策略文件"""
    strategies_dir = PROJECT_ROOT / "strategies"
    strategy_files = []

    # 递归查找所有 txt 和 py 文件
    for root, dirs, files in os.walk(strategies_dir):
        for f in files:
            if f.endswith('.txt') or f.endswith('.py'):
                # 排除明显的非策略文件
                if f.startswith('.') or '测试' in f or 'test' in f.lower():
                    continue
                filepath = os.path.join(root, f)
                # 简单检查是否包含策略函数定义
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read(2000)  # 只读取前2000字符
                        strategy_funcs = ['def initialize', 'def handle_data', 'def before_trading_start',
                                          'def after_trading_end', 'def before_market_open', 'def after_market_close']
                        if any(func in content for func in strategy_funcs):
                            strategy_files.append(filepath)
                except Exception:
                    continue

    return strategy_files

def random_pick_strategies(num=20):
    """随机选择N个策略"""
    all_strategies = get_all_strategy_files()
    if len(all_strategies) < num:
        print(f"警告: 只有 {len(all_strategies)} 个有效策略，无法选择 {num} 个")
        return all_strategies
    return random.sample(all_strategies, num)

def analyze_strategy_code(strategy_file):
    """
    分析策略代码，识别缺失的API和潜在问题

    返回:
        dict: {
            'strategy_file': str,
            'strategy_name': str,
            'success': bool,
            'error': str,
            'missing_api': list,
            'missing_modules': list,
            'load_time': float,
            'has_initialize': bool,
            'has_handle_data': bool,
        }
    """
    strategy_name = os.path.basename(strategy_file)
    start_time = time.time()

    result = {
        'strategy_file': strategy_file,
        'strategy_name': strategy_name,
        'success': False,
        'error': '',
        'missing_api': [],
        'missing_modules': [],
        'load_time': 0,
        'has_initialize': False,
        'has_handle_data': False,
    }

    # 聚宽已实现的API列表
    implemented_apis = {
        # 核心API
        'get_price', 'history', 'attribute_history', 'get_fundamentals',
        'get_all_securities', 'get_security_info', 'get_current_data',
        'get_index_weights', 'get_index_stocks', 'get_factor_values',
        'get_all_trade_days', 'get_trade_days', 'get_extras', 'get_bars',
        'get_billboard_list', 'get_call_auction', 'get_ticks', 'get_valuation',
        'get_current_tick',
        # 行业API
        'get_industry_classify', 'get_industry_stocks', 'get_stock_industry',
        'get_all_industry_stocks', 'get_industry_daily', 'get_industry_performance',
        # 北向资金API
        'get_north_money_flow', 'get_north_money_daily', 'get_north_money_holdings',
        'get_north_money_stock_flow',
        # 情绪指标API
        'compute_crowding_ratio', 'compute_gisi', 'compute_fed_model',
        'compute_graham_index', 'compute_below_net_ratio',
        # RSRS API
        'compute_rsrs', 'compute_rsrs_signal', 'get_rsrs_for_index',
        # 运行时IO
        'record', 'send_message', 'read_file', 'write_file',
        # 定时任务
        'run_daily', 'run_weekly', 'run_monthly',
        # 下单API
        'order', 'order_target', 'order_value', 'order_target_value',
        'order_shares', 'order_target_percent',
        # 指标API
        'MA', 'EMA', 'MACD', 'KDJ', 'RSI', 'BOLL', 'ATR',
        # 统计API
        'get_ols', 'get_zscore', 'get_rank',
        # 筛选API
        'filter_st', 'filter_paused', 'filter_limit_up', 'filter_limit_down',
        'filter_new_stocks',
        # Wizard函数
        'disable_cache', 'set_commission', 'PerTrade', 'neutralize',
        'security_stoploss', 'portfolio_stoploss',
        # 其他
        'get_concept_stocks', 'get_future_contracts', 'get_locked_shares',
        'get_trades',
        # 表查询
        'query', 'valuation', 'income', 'balance', 'cash_flow', 'indicator', 'finance',
    }

    # 已知缺失或部分实现的API
    missing_or_partial_apis = {
        'get_mar_signal': '市场情绪信号',
        'get_advance_decline_ratio': '涨跌比',
        'get_security_margin_info': '融资融券信息',
        'get_mtss': '融资融券数据',
        'get_locked_shares_detail': '锁定股份详情',
        'get_dividend_info': '分红信息',
        'get_share_changes': '股本变动',
        'get_ipos_info': 'IPO信息',
        'get_mutual_fund_holdings': '基金持仓',
        'get_insider_transactions': '内部交易',
        'get_short_interest': '做空兴趣',
        'get_options_data': '期权数据',
        'get_convertible_bond_info': '可转债信息',
        'get_warrant_info': '权证信息',
        'get_real_time_quotes': '实时行情',
        'get_l2_data': 'Level2数据',
        'get_order_flow': '订单流',
        'get_sector_rotation': '板块轮动',
        'get_style_factor': '风格因子',
        'get_risk_factor': '风险因子',
        'get_alpha101': 'Alpha101因子',
        'get_alpha191': 'Alpha191因子',
        'get_world_quant_alpha': 'WorldQuant Alpha',
        'get_statistical_arb': '统计套利信号',
        'get_pairs_trading': '配对交易信号',
        'get_event_study': '事件研究',
        'get_news_sentiment': '新闻情绪',
        'get_social_sentiment': '社交情绪',
        'get analyst_ratings': '分析师评级',
        'get_earnings_forecast': '盈利预测',
        'get_target_price': '目标价格',
        'get_credit_rating': '信用评级',
        'get_esg_rating': 'ESG评级',
        'get_consensus_estimate': '一致性估计',
        'get_pe_ratio_forecast': 'PE预测',
        'get_eps_forecast': 'EPS预测',
        'get_revenue_forecast': '收入预测',
        'get_margin_forecast': '利润率预测',
        'get_roe_forecast': 'ROE预测',
    }

    try:
        # 读取策略代码
        with open(strategy_file, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()

        # 检查是否有策略函数
        result['has_initialize'] = 'def initialize' in code
        result['has_handle_data'] = 'def handle_data' in code

        # 提取代码中的API调用
        # 匹配 get_xxx( 和 xxx.xxx( 形式的调用
        api_pattern = r'(get_\w+|compute_\w+|order_\w+|run_\w+|filter_\w+|MA|EMA|MACD|KDJ|RSI|BOLL|ATR)\s*\('
        found_apis = re.findall(api_pattern, code)

        # 检查缺失的API
        for api in set(found_apis):
            if api not in implemented_apis:
                result['missing_api'].append(api)

        # 检查是否有其他未实现的模块引用
        module_patterns = [
            r'from\s+(\w+)\s+import',
            r'import\s+(\w+)',
        ]
        for pattern in module_patterns:
            modules = re.findall(pattern, code)
            for module in modules:
                if module in ['jqdata', 'jqlib', 'kuanke', 'jqfactor', 'kqapi']:
                    continue  # 这些模块已被模拟
                if module.startswith('_'):
                    continue
                # 检查是否有不可用的模块
                unavailable_modules = [
                    'xgboost', 'lightgbm', 'catboost', 'tensorflow', 'torch', 'keras',
                    'skopt', 'hyperopt', 'optuna', 'bayesian_optimization',
                    'cvxpy', 'pyportfolioopt', 'riskfolio',
                    'statsmodels.tsa', 'arch', 'pmdarima',
                    'nltk', 'spacy', 'gensim', 'transformers',
                    'requests_html', 'selenium', 'playwright',
                    'pandas.stats', 'pandas_datareader',
                ]
                for unavailable in unavailable_modules:
                    if unavailable in module.lower() or module.lower() in unavailable:
                        result['missing_modules'].append(module)

        # 尝试实际加载策略
        try:
            from jk2bt.core.runner import load_jq_strategy
            functions = load_jq_strategy(strategy_file)

            if functions:
                result['success'] = True
                result['error'] = ''
            else:
                result['success'] = False
                result['error'] = '策略加载返回空函数列表'

        except SyntaxError as e:
            result['success'] = False
            result['error'] = f"语法错误 (行 {e.lineno}): {e.msg}"

        except ModuleNotFoundError as e:
            result['success'] = False
            result['error'] = str(e)
            module_name = str(e).replace("No module named '", "").replace("'", "")
            result['missing_modules'].append(module_name)

        except NameError as e:
            result['success'] = False
            result['error'] = str(e)
            # 提取未定义的名称
            if "is not defined" in str(e):
                parts = str(e).split("'")
                if len(parts) >= 2:
                    result['missing_api'].append(parts[1])

        except AttributeError as e:
            result['success'] = False
            result['error'] = str(e)
            if "has no attribute" in str(e):
                parts = str(e).split("'")
                if len(parts) >= 2:
                    result['missing_api'].append(parts[1])

        except ImportError as e:
            result['success'] = False
            result['error'] = str(e)

        except Exception as e:
            result['success'] = False
            result['error'] = f"{type(e).__name__}: {str(e)[:200]}"

    except Exception as e:
        result['success'] = False
        result['error'] = f"文件读取错误: {str(e)}"

    result['load_time'] = time.time() - start_time
    return result

def generate_report(results, output_file):
    """生成兼容性报告"""
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]

    # 统计缺失的API
    missing_apis = {}
    for r in results:
        for api in r['missing_api']:
            missing_apis[api] = missing_apis.get(api, 0) + 1

    # 统计缺失的模块
    missing_modules = {}
    for r in results:
        for module in r['missing_modules']:
            missing_modules[module] = missing_modules.get(module, 0) + 1

    # 统计错误类型
    error_types = {}
    for r in failed:
        error_type = r['error'].split(':')[0] if ':' in r['error'] else r['error'][:50]
        error_types[error_type] = error_types.get(error_type, 0) + 1

    # 生成报告内容
    report_lines = []
    report_lines.append("# 策略兼容性测试报告")
    report_lines.append("")
    report_lines.append("## 测试概要")
    report_lines.append(f"- 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report_lines.append(f"- 测试策略数: {len(results)}")
    report_lines.append(f"- 成功数: {len(successful)}")
    report_lines.append(f"- 失败数: {len(failed)}")
    report_lines.append(f"- 成功率: {len(successful)/len(results)*100:.1f}%")
    report_lines.append(f"- 测试类型: 策略加载兼容性测试（不运行回测）")
    report_lines.append("")

    report_lines.append("## 详细结果")
    report_lines.append("")

    for i, r in enumerate(results, 1):
        status = "成功" if r['success'] else "失败"
        report_lines.append(f"### 策略{i}: {r['strategy_name']}")
        report_lines.append(f"- 状态: {status}")
        report_lines.append(f"- 加载时间: {r['load_time']:.2f}秒")
        report_lines.append(f"- 包含initialize: {'是' if r['has_initialize'] else '否'}")
        report_lines.append(f"- 包含handle_data: {'是' if r['has_handle_data'] else '否'}")
        if not r['success']:
            report_lines.append(f"- 错误信息: {r['error'][:200]}")
        if r['missing_api']:
            report_lines.append(f"- 缺失API: `{', '.join(r['missing_api'])}`")
        if r['missing_modules']:
            report_lines.append(f"- 缺失模块: `{', '.join(r['missing_modules'])}`")
        report_lines.append("")

    report_lines.append("## 问题汇总")
    report_lines.append("")

    report_lines.append("### 缺失的API列表")
    if missing_apis:
        report_lines.append("以下API在策略代码中被调用，但jk2bt尚未完全实现:")
        report_lines.append("")
        for api, count in sorted(missing_apis.items(), key=lambda x: -x[1]):
            report_lines.append(f"- `{api}`: {count} 次调用")
    else:
        report_lines.append("- 无缺失API")
    report_lines.append("")

    report_lines.append("### 缺失的Python模块")
    if missing_modules:
        report_lines.append("以下Python模块在策略中被引用，但环境中未安装:")
        report_lines.append("")
        for module, count in sorted(missing_modules.items(), key=lambda x: -x[1]):
            report_lines.append(f"- `{module}`: {count} 次引用")
    else:
        report_lines.append("- 无缺失模块")
    report_lines.append("")

    report_lines.append("### 常见错误类型")
    if error_types:
        for error_type, count in sorted(error_types.items(), key=lambda x: -x[1]):
            report_lines.append(f"- {error_type}: {count} 次")
    else:
        report_lines.append("- 无错误")
    report_lines.append("")

    report_lines.append("## 成功策略列表")
    if successful:
        for r in successful:
            apis = ', '.join(r['missing_api']) if r['missing_api'] else '无缺失'
            report_lines.append(f"- {r['strategy_name']} (加载时间: {r['load_time']:.2f}秒)")
    else:
        report_lines.append("- 无成功策略")
    report_lines.append("")

    report_lines.append("## 建议")
    report_lines.append("")
    if missing_apis:
        report_lines.append("### 需要实现的API")
        for api in sorted(missing_apis.keys()):
            report_lines.append(f"- 实现 `{api}` 函数")
        report_lines.append("")
    if missing_modules:
        report_lines.append("### 需要安装的模块")
        for module in sorted(missing_modules.keys()):
            report_lines.append(f"- pip install {module}")
        report_lines.append("")

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))

    print(f"\n报告已保存: {output_file}")
    return report_lines

def main():
    """主函数"""
    print("=" * 80)
    print("批量策略兼容性测试（简化版）")
    print("=" * 80)
    print("测试内容: 策略加载兼容性")
    print("=" * 80)

    # 随机选取策略
    strategies = random_pick_strategies(20)
    print(f"\n选取了 {len(strategies)} 个策略进行测试:")
    for i, s in enumerate(strategies, 1):
        print(f"  {i}. {os.path.basename(s)}")

    # 运行测试
    results = []
    for i, strategy_file in enumerate(strategies, 1):
        print(f"\n[{i}/{len(strategies)}] 测试: {os.path.basename(strategy_file)}")
        result = analyze_strategy_code(strategy_file)
        results.append(result)

        if result['success']:
            status = "成功"
            extras = ""
            if result['missing_api']:
                extras = f" (潜在缺失API: {len(result['missing_api'])})"
            print(f"  {status}! 加载时间: {result['load_time']:.2f}秒{extras}")
        else:
            print(f"  失败: {result['error'][:80]}")
            if result['missing_api']:
                print(f"  缺失API: {', '.join(result['missing_api'][:5])}")
            if result['missing_modules']:
                print(f"  缺失模块: {', '.join(result['missing_modules'][:3])}")

    # 生成报告
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_file = REPORTS_DIR / "compatibility_report.md"
    generate_report(results, report_file)

    # 打印摘要
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]

    print("\n" + "=" * 80)
    print("测试汇总")
    print("=" * 80)
    print(f"总数: {len(results)}, 成功: {len(successful)}, 失败: {len(failed)}")
    print(f"成功率: {len(successful)/len(results)*100:.1f}%")

    # 统计缺失的API
    all_missing_apis = {}
    for r in results:
        for api in r['missing_api']:
            all_missing_apis[api] = all_missing_apis.get(api, 0) + 1

    if all_missing_apis:
        print("\n缺失的API:")
        for api, count in sorted(all_missing_apis.items(), key=lambda x: -x[1])[:10]:
            print(f"  {api}: {count} 次")

    if successful:
        print("\n成功的策略:")
        for r in successful[:10]:
            print(f"  {r['strategy_name']}")

    if failed:
        print("\n失败的策略:")
        for r in failed[:5]:
            print(f"  {r['strategy_name']}: {r['error'][:50]}")

    print("=" * 80)

if __name__ == "__main__":
    main()