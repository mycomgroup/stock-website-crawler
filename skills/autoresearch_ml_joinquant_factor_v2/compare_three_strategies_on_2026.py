"""
对比四种策略在2026年的表现

Strategy 1 (Phase 1): 使用2015-2023年数据训练，Top-50选股
Strategy 2 (Phase 2): 使用2015-2025年数据训练，Top-50选股
Strategy 3 (Phase 2 + 市值EPS过滤): 使用2015-2025年数据训练，先按流通市值升序+EPS过滤，再从中选Top-50
Strategy 4 (Phase 1 + 市值EPS过滤): 使用2015-2023年数据训练，先按流通市值升序+EPS过滤，再从中选Top-50

目标：验证加入市值和EPS过滤后，收益是否有改善
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / 'output'


def load_2026_data():
    """加载2026年的实际收益数据"""
    logger.info("加载2026年数据...")
    
    import glob
    data_dir = BASE_DIR / "data" / "weekly_factors"
    files_2026 = sorted(glob.glob(str(data_dir / "factors_2026*.csv")))
    
    dfs = []
    for file_path in files_2026:
        df = pd.read_csv(file_path)
        date_str = Path(file_path).stem.split('_')[1]
        df['date'] = pd.to_datetime(date_str)
        dfs.append(df)
    
    df_2026 = pd.concat(dfs, ignore_index=True)
    
    if 'Unnamed: 0' in df_2026.columns:
        df_2026 = df_2026.rename(columns={'Unnamed: 0': 'stock_id'})
    
    # 过滤异常数据
    dates_to_remove = []
    for date in sorted(df_2026['date'].unique()):
        df_date = df_2026[df_2026['date'] == date]
        pchg_valid = df_date['pchg'].dropna()
        
        if len(pchg_valid) == 0:
            dates_to_remove.append(date)
        elif (pchg_valid == -1.0).sum() > len(pchg_valid) * 0.5:
            dates_to_remove.append(date)
        elif np.isinf(pchg_valid).sum() > 0:
            dates_to_remove.append(date)
    
    if dates_to_remove:
        df_2026 = df_2026[~df_2026['date'].isin(dates_to_remove)]
        logger.info(f"  移除了 {len(dates_to_remove)} 个异常日期")
    
    logger.info(f"  2026年数据: {len(df_2026)} 行, {df_2026['date'].nunique()} 个日期")
    
    return df_2026


def calculate_ic_on_2026(predictions, actual_data, strategy_name, pred_col='prediction'):
    """计算在2026年数据上的IC"""
    logger.info(f"\n计算{strategy_name}在2026年的IC...")
    
    # 合并预测和实际数据
    merged = predictions[['date', 'stock_id', pred_col]].merge(
        actual_data[['date', 'stock_id', 'pchg']],
        on=['date', 'stock_id'],
        how='inner'
    )
    
    logger.info(f"  匹配数据: {len(merged)} 行")
    
    # 按日期计算IC
    ic_series = []
    dates = sorted(merged['date'].unique())
    
    for date in dates:
        df_date = merged[merged['date'] == date]
        
        valid_mask = df_date[pred_col].notna() & df_date['pchg'].notna()
        if valid_mask.sum() > 10:
            corr, _ = stats.spearmanr(
                df_date.loc[valid_mask, pred_col],
                df_date.loc[valid_mask, 'pchg']
            )
            if np.isfinite(corr):
                ic_series.append(corr)
    
    if len(ic_series) == 0:
        logger.warning(f"  {strategy_name}没有有效的IC数据")
        return {
            'ic_series': [],
            'ic_mean': 0,
            'ic_std': 0,
            'ic_ir': 0,
            'ic_positive_ratio': 0,
        }
    
    ic_mean = np.mean(ic_series)
    ic_std = np.std(ic_series)
    ic_ir = ic_mean / ic_std if ic_std > 0 else 0
    
    logger.info(f"  IC均值: {ic_mean:.4f}")
    logger.info(f"  IC标准差: {ic_std:.4f}")
    logger.info(f"  IC IR: {ic_ir:.4f}")
    logger.info(f"  IC>0占比: {sum(ic > 0 for ic in ic_series) / len(ic_series) * 100:.2f}%")
    
    return {
        'ic_series': ic_series,
        'ic_mean': ic_mean,
        'ic_std': ic_std,
        'ic_ir': ic_ir,
        'ic_positive_ratio': sum(ic > 0 for ic in ic_series) / len(ic_series),
    }


def calculate_portfolio_returns_simple(predictions, actual_data, strategy_name, pred_col='prediction'):
    """计算简单Top-50组合收益"""
    logger.info(f"\n计算{strategy_name}的组合收益（简单Top-50）...")
    
    # 合并数据
    merged = predictions[['date', 'stock_id', pred_col]].merge(
        actual_data[['date', 'stock_id', 'pchg']],
        on=['date', 'stock_id'],
        how='inner'
    )
    
    if len(merged) == 0:
        logger.warning(f"  {strategy_name}没有匹配的数据")
        return None
    
    # Top-50组合
    def simulate_top50(group):
        top50 = group.nlargest(50, pred_col)
        return top50['pchg'].mean()
    
    portfolio_returns = merged.groupby('date').apply(simulate_top50)
    market_returns = merged.groupby('date')['pchg'].mean()
    
    return calculate_metrics(portfolio_returns, market_returns, strategy_name)


def calculate_portfolio_returns_with_filter(predictions, actual_data, strategy_name, pred_col='prediction'):
    """计算带市值EPS过滤的Top-50组合收益"""
    logger.info(f"\n计算{strategy_name}的组合收益（市值EPS过滤+Top-50）...")
    
    # 合并数据，需要包含市值和EPS (使用eps_ttm)
    eps_col = 'eps_ttm' if 'eps_ttm' in actual_data.columns else 'eps'
    merged = predictions[['date', 'stock_id', pred_col]].merge(
        actual_data[['date', 'stock_id', 'pchg', 'circulating_market_cap', eps_col]],
        on=['date', 'stock_id'],
        how='inner'
    )
    
    # 统一列名为eps
    if eps_col == 'eps_ttm':
        merged = merged.rename(columns={'eps_ttm': 'eps'})
    
    if len(merged) == 0:
        logger.warning(f"  {strategy_name}没有匹配的数据")
        return None
    
    # 带过滤的Top-50组合
    def simulate_top50_with_filter(group):
        # 1. 按流通市值升序排序
        group_sorted = group.sort_values('circulating_market_cap', ascending=True)
        
        # 2. 过滤EPS > 0
        group_filtered = group_sorted[group_sorted['eps'] > 0]
        
        # 3. 如果过滤后不足50只，则使用所有过滤后的股票
        if len(group_filtered) < 50:
            logger.debug(f"  日期 {group.name}: 过滤后仅{len(group_filtered)}只股票")
            if len(group_filtered) == 0:
                return np.nan
            return group_filtered['pchg'].mean()
        
        # 4. 从过滤后的股票中，按预测值选Top-50
        top50 = group_filtered.nlargest(50, pred_col)
        return top50['pchg'].mean()
    
    portfolio_returns = merged.groupby('date').apply(simulate_top50_with_filter)
    portfolio_returns = portfolio_returns.dropna()  # 移除无效日期
    
    market_returns = merged.groupby('date')['pchg'].mean()
    market_returns = market_returns[market_returns.index.isin(portfolio_returns.index)]
    
    return calculate_metrics(portfolio_returns, market_returns, strategy_name)


def calculate_metrics(portfolio_returns, market_returns, strategy_name):
    """计算收益指标"""
    n_weeks = len(portfolio_returns)
    if n_weeks == 0:
        return {
            'ytd_return': 0,
            'annual_return': 0,
            'annual_vol': 0,
            'sharpe': 0,
            'ytd_excess': 0,
            'annual_excess': 0,
            'max_drawdown': 0,
        }
    
    port_cum = (1 + portfolio_returns).cumprod()
    mkt_cum = (1 + market_returns).cumprod()
    
    # 使用实际天数计算年化
    date_range = portfolio_returns.index.max() - portfolio_returns.index.min()
    n_days = date_range.days
    
    ytd_port = (port_cum.iloc[-1] - 1) * 100
    ytd_mkt = (mkt_cum.iloc[-1] - 1) * 100
    
    if n_days > 0:
        ann_port = ((port_cum.iloc[-1]) ** (365.25 / n_days) - 1) * 100
        ann_mkt = ((mkt_cum.iloc[-1]) ** (365.25 / n_days) - 1) * 100
    else:
        ann_port = 0
        ann_mkt = 0
    
    ann_vol_port = portfolio_returns.std() * np.sqrt(52) * 100
    sharpe_port = ann_port / ann_vol_port if ann_vol_port > 0 else 0
    
    # 计算最大回撤
    cumulative = (1 + portfolio_returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_dd = drawdown.min() * 100
    
    logger.info(f"  YTD收益: {ytd_port:.2f}%")
    logger.info(f"  年化收益: {ann_port:.2f}%")
    logger.info(f"  年化波动: {ann_vol_port:.2f}%")
    logger.info(f"  夏普比率: {sharpe_port:.2f}")
    logger.info(f"  YTD超额: {ytd_port - ytd_mkt:.2f}%")
    logger.info(f"  最大回撤: {max_dd:.2f}%")
    
    return {
        'ytd_return': ytd_port,
        'annual_return': ann_port,
        'annual_vol': ann_vol_port,
        'sharpe': sharpe_port,
        'ytd_excess': ytd_port - ytd_mkt,
        'annual_excess': ann_port - ann_mkt,
        'max_drawdown': max_dd,
    }


def generate_four_way_comparison_report(s1_ic, s2_ic, s3_ic, s4_ic, s1_perf, s2_perf, s3_perf, s4_perf):
    """生成四策略对比报告"""
    logger.info("\n" + "=" * 120)
    logger.info("四策略在2026年的对比报告")
    logger.info("=" * 120)
    
    report_lines = []
    report_lines.append("=" * 120)
    report_lines.append("四策略在2026年的对比报告")
    report_lines.append("=" * 120)
    report_lines.append("")
    
    report_lines.append("【一、策略定义】")
    report_lines.append("")
    report_lines.append("Strategy 1 (Phase 1 基准):")
    report_lines.append("  - 训练数据: 2015-2023年")
    report_lines.append("  - 选股方法: 简单Top-50（按预测值降序）")
    report_lines.append("")
    report_lines.append("Strategy 2 (Phase 2 基准):")
    report_lines.append("  - 训练数据: 2015-2025年（增加2024-2025年）")
    report_lines.append("  - 选股方法: 简单Top-50（按预测值降序）")
    report_lines.append("")
    report_lines.append("Strategy 3 (Phase 2 + 市值EPS过滤):")
    report_lines.append("  - 训练数据: 2015-2025年")
    report_lines.append("  - 选股方法: 先按流通市值升序排序 → 过滤EPS>0 → 从中选Top-50（按预测值降序）")
    report_lines.append("")
    report_lines.append("Strategy 4 (Phase 1 + 市值EPS过滤):")
    report_lines.append("  - 训练数据: 2015-2023年")
    report_lines.append("  - 选股方法: 先按流通市值升序排序 → 过滤EPS>0 → 从中选Top-50（按预测值降序）")
    report_lines.append("")
    
    report_lines.append("【二、IC表现对比】")
    report_lines.append("")
    report_lines.append(f"{'指标':<15} | {'Strategy 1':<12} | {'Strategy 2':<12} | {'Strategy 3':<12} | {'Strategy 4':<12} | {'S4 vs S1':<10}")
    report_lines.append("-" * 100)
    report_lines.append(f"{'IC均值':<15} | {s1_ic['ic_mean']:>12.4f} | {s2_ic['ic_mean']:>12.4f} | {s3_ic['ic_mean']:>12.4f} | {s4_ic['ic_mean']:>12.4f} | {(s4_ic['ic_mean'] - s1_ic['ic_mean']) / abs(s1_ic['ic_mean']) * 100:>+9.1f}%")
    report_lines.append(f"{'IC标准差':<15} | {s1_ic['ic_std']:>12.4f} | {s2_ic['ic_std']:>12.4f} | {s3_ic['ic_std']:>12.4f} | {s4_ic['ic_std']:>12.4f} | {(s4_ic['ic_std'] - s1_ic['ic_std']) / s1_ic['ic_std'] * 100:>+9.1f}%")
    report_lines.append(f"{'IC IR':<15} | {s1_ic['ic_ir']:>12.4f} | {s2_ic['ic_ir']:>12.4f} | {s3_ic['ic_ir']:>12.4f} | {s4_ic['ic_ir']:>12.4f} | {(s4_ic['ic_ir'] - s1_ic['ic_ir']) / abs(s1_ic['ic_ir']) * 100:>+9.1f}%")
    report_lines.append(f"{'IC>0占比':<15} | {s1_ic['ic_positive_ratio'] * 100:>11.2f}% | {s2_ic['ic_positive_ratio'] * 100:>11.2f}% | {s3_ic['ic_positive_ratio'] * 100:>11.2f}% | {s4_ic['ic_positive_ratio'] * 100:>11.2f}% | {(s4_ic['ic_positive_ratio'] - s1_ic['ic_positive_ratio']) * 100:>+9.1f}pp")
    report_lines.append("")
    
    report_lines.append("【三、收益表现对比】")
    report_lines.append("")
    report_lines.append(f"{'指标':<15} | {'Strategy 1':<12} | {'Strategy 2':<12} | {'Strategy 3':<12} | {'Strategy 4':<12} | {'S4 vs S1':<10}")
    report_lines.append("-" * 100)
    report_lines.append(f"{'YTD收益':<15} | {s1_perf['ytd_return']:>11.2f}% | {s2_perf['ytd_return']:>11.2f}% | {s3_perf['ytd_return']:>11.2f}% | {s4_perf['ytd_return']:>11.2f}% | {s4_perf['ytd_return'] - s1_perf['ytd_return']:>+9.2f}pp")
    report_lines.append(f"{'年化收益':<15} | {s1_perf['annual_return']:>11.2f}% | {s2_perf['annual_return']:>11.2f}% | {s3_perf['annual_return']:>11.2f}% | {s4_perf['annual_return']:>11.2f}% | {s4_perf['annual_return'] - s1_perf['annual_return']:>+9.2f}pp")
    report_lines.append(f"{'年化波动':<15} | {s1_perf['annual_vol']:>11.2f}% | {s2_perf['annual_vol']:>11.2f}% | {s3_perf['annual_vol']:>11.2f}% | {s4_perf['annual_vol']:>11.2f}% | {s4_perf['annual_vol'] - s1_perf['annual_vol']:>+9.2f}pp")
    report_lines.append(f"{'夏普比率':<15} | {s1_perf['sharpe']:>12.2f} | {s2_perf['sharpe']:>12.2f} | {s3_perf['sharpe']:>12.2f} | {s4_perf['sharpe']:>12.2f} | {s4_perf['sharpe'] - s1_perf['sharpe']:>+9.2f}")
    report_lines.append(f"{'YTD超额':<15} | {s1_perf['ytd_excess']:>11.2f}% | {s2_perf['ytd_excess']:>11.2f}% | {s3_perf['ytd_excess']:>11.2f}% | {s4_perf['ytd_excess']:>11.2f}% | {s4_perf['ytd_excess'] - s1_perf['ytd_excess']:>+9.2f}pp")
    report_lines.append(f"{'年化超额':<15} | {s1_perf['annual_excess']:>11.2f}% | {s2_perf['annual_excess']:>11.2f}% | {s3_perf['annual_excess']:>11.2f}% | {s4_perf['annual_excess']:>11.2f}% | {s4_perf['annual_excess'] - s1_perf['annual_excess']:>+9.2f}pp")
    report_lines.append(f"{'最大回撤':<15} | {s1_perf['max_drawdown']:>11.2f}% | {s2_perf['max_drawdown']:>11.2f}% | {s3_perf['max_drawdown']:>11.2f}% | {s4_perf['max_drawdown']:>11.2f}% | {s4_perf['max_drawdown'] - s1_perf['max_drawdown']:>+9.2f}pp")
    report_lines.append("")
    
    report_lines.append("【四、结论】")
    report_lines.append("")
    
    # 评估Strategy 4 vs Strategy 1 (过滤对Phase 1的效果)
    s4_vs_s1_improvements = sum([
        s4_ic['ic_mean'] > s1_ic['ic_mean'],
        s4_ic['ic_ir'] > s1_ic['ic_ir'],
        s4_perf['annual_return'] > s1_perf['annual_return'],
        s4_perf['sharpe'] > s1_perf['sharpe'],
    ])
    
    report_lines.append("1. 市值EPS过滤对Phase 1的效果 (Strategy 4 vs Strategy 1): ⭐ 核心对比")
    if s4_vs_s1_improvements >= 3:
        report_lines.append(f"   ✅ 市值EPS过滤显著改善Phase 1收益 ({s4_vs_s1_improvements}/4 指标改善)")
        report_lines.append(f"   年化收益提升: {s4_perf['annual_return'] - s1_perf['annual_return']:+.2f}pp")
        report_lines.append(f"   夏普比率提升: {s4_perf['sharpe'] - s1_perf['sharpe']:+.2f}")
    elif s4_vs_s1_improvements >= 2:
        report_lines.append(f"   ⚠️ 市值EPS过滤略有改善 ({s4_vs_s1_improvements}/4 指标改善)")
        report_lines.append(f"   年化收益变化: {s4_perf['annual_return'] - s1_perf['annual_return']:+.2f}pp")
    else:
        report_lines.append(f"   ❌ 市值EPS过滤未改善收益 ({s4_vs_s1_improvements}/4 指标改善)")
        report_lines.append(f"   年化收益变化: {s4_perf['annual_return'] - s1_perf['annual_return']:+.2f}pp")
    
    report_lines.append("")
    
    # Strategy 3 vs Strategy 4 对比
    s3_vs_s4_better = sum([
        s3_perf['annual_return'] > s4_perf['annual_return'],
        s3_perf['sharpe'] > s4_perf['sharpe'],
    ])
    
    report_lines.append("2. Phase 2 vs Phase 1 在加过滤后的对比 (Strategy 3 vs Strategy 4):")
    if s3_vs_s4_better >= 2:
        report_lines.append(f"   ✅ Phase 2+过滤 优于 Phase 1+过滤")
        report_lines.append(f"   年化收益差异: {s3_perf['annual_return'] - s4_perf['annual_return']:+.2f}pp")
        report_lines.append(f"   夏普比率差异: {s3_perf['sharpe'] - s4_perf['sharpe']:+.2f}")
    else:
        report_lines.append(f"   ⚠️ Phase 1+过滤 表现更好")
        report_lines.append(f"   年化收益差异: {s3_perf['annual_return'] - s4_perf['annual_return']:+.2f}pp")
        report_lines.append(f"   夏普比率差异: {s3_perf['sharpe'] - s4_perf['sharpe']:+.2f}")
    
    report_lines.append("")
    
    # 最终推荐
    best_strategy = max(
        [('Strategy 1', s1_perf['sharpe']), 
         ('Strategy 2', s2_perf['sharpe']), 
         ('Strategy 3', s3_perf['sharpe']),
         ('Strategy 4', s4_perf['sharpe'])],
        key=lambda x: x[1]
    )[0]
    
    report_lines.append("3. 最终推荐:")
    report_lines.append(f"   🏆 {best_strategy} 表现最佳（夏普比率最高）")
    
    if best_strategy == 'Strategy 3':
        report_lines.append("   建议使用Phase 2模型 + 市值EPS过滤选股")
    elif best_strategy == 'Strategy 4':
        report_lines.append("   建议使用Phase 1模型 + 市值EPS过滤选股")
    elif best_strategy == 'Strategy 2':
        report_lines.append("   建议使用Phase 2模型 + 简单Top-50选股")
    else:
        report_lines.append("   建议继续使用Phase 1模型")
    
    report_lines.append("")
    report_lines.append("=" * 120)
    
    report_text = "\n".join(report_lines)
    print("\n" + report_text)
    
    # 保存报告
    report_path = OUTPUT_DIR / 'analysis' / 'four_strategies_comparison.txt'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    logger.info(f"\n对比报告已保存: {report_path}")
    
    # 保存JSON数据
    json_data = {
        'strategy_1': {
            'name': 'Phase 1 (2015-2023, Top-50)',
            'ic': s1_ic,
            'performance': s1_perf,
        },
        'strategy_2': {
            'name': 'Phase 2 (2015-2025, Top-50)',
            'ic': s2_ic,
            'performance': s2_perf,
        },
        'strategy_3': {
            'name': 'Phase 2 + 市值EPS过滤',
            'ic': s3_ic,
            'performance': s3_perf,
        },
        'strategy_4': {
            'name': 'Phase 1 + 市值EPS过滤',
            'ic': s4_ic,
            'performance': s4_perf,
        },
        'best_strategy': best_strategy,
    }
    
    json_path = OUTPUT_DIR / 'analysis' / 'four_strategies_comparison.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    logger.info(f"JSON数据已保存: {json_path}")
    
    return report_text


def main():
    """主函数"""
    try:
        # 加载2026年实际数据（需要包含市值和EPS）
        df_2026 = load_2026_data()
        
        # 检查是否有市值和EPS字段 (eps或eps_ttm)
        has_eps = 'eps' in df_2026.columns or 'eps_ttm' in df_2026.columns
        if 'circulating_market_cap' not in df_2026.columns or not has_eps:
            logger.error("2026年数据缺少 circulating_market_cap 或 eps/eps_ttm 字段")
            logger.error("请确保weekly_factors数据包含这些字段")
            return False
        
        # 加载Phase 1和Phase 2的holdout预测
        phase1_pred_path = OUTPUT_DIR / 'phase1' / 'predictions_2026_holdout.csv'
        phase2_pred_path = OUTPUT_DIR / 'phase2' / 'predictions_2026_holdout.csv'
        
        # 检查是否存在holdout预测文件
        if not phase1_pred_path.exists() or not phase2_pred_path.exists():
            logger.error("找不到2026 holdout预测文件")
            logger.error("请先运行 predict_2026_holdout.py 生成预测")
            return False
        
        # 加载预测
        phase1_pred = pd.read_csv(phase1_pred_path)
        phase1_pred['date'] = pd.to_datetime(phase1_pred['date'])
        
        phase2_pred = pd.read_csv(phase2_pred_path)
        phase2_pred['date'] = pd.to_datetime(phase2_pred['date'])
        
        logger.info(f"\nPhase 1在2026年的预测: {len(phase1_pred)} 行")
        logger.info(f"Phase 2在2026年的预测: {len(phase2_pred)} 行")
        
        # 计算IC
        s1_ic = calculate_ic_on_2026(phase1_pred, df_2026, 'Strategy 1', pred_col='prediction')
        s2_ic = calculate_ic_on_2026(phase2_pred, df_2026, 'Strategy 2', pred_col='prediction')
        s3_ic = calculate_ic_on_2026(phase2_pred, df_2026, 'Strategy 3', pred_col='prediction')
        s4_ic = calculate_ic_on_2026(phase1_pred, df_2026, 'Strategy 4', pred_col='prediction')
        
        # 计算收益
        s1_perf = calculate_portfolio_returns_simple(phase1_pred, df_2026, 'Strategy 1', pred_col='prediction')
        s2_perf = calculate_portfolio_returns_simple(phase2_pred, df_2026, 'Strategy 2', pred_col='prediction')
        s3_perf = calculate_portfolio_returns_with_filter(phase2_pred, df_2026, 'Strategy 3', pred_col='prediction')
        s4_perf = calculate_portfolio_returns_with_filter(phase1_pred, df_2026, 'Strategy 4', pred_col='prediction')
        
        if s1_perf is None or s2_perf is None or s3_perf is None or s4_perf is None:
            logger.error("某个策略的收益计算失败")
            return False
        
        # 生成对比报告
        generate_four_way_comparison_report(s1_ic, s2_ic, s3_ic, s4_ic, s1_perf, s2_perf, s3_perf, s4_perf)
        
        return True
        
    except Exception as e:
        logger.error(f"对比分析失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
