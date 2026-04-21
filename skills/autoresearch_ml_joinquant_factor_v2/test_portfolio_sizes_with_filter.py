"""
测试不同持仓数量在市值EPS过滤下的表现

测试范围：5, 10, 20, 30, 40, 50, 60, 80, 100支股票
目标：验证是否股票越多越稳定，以及极端情况（5支）的表现
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


def calculate_portfolio_returns_with_filter(predictions, actual_data, n_stocks, pred_col='prediction'):
    """计算带市值EPS过滤的组合收益"""
    
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
        return None
    
    # 带过滤的Top-N组合
    def simulate_topn_with_filter(group):
        # 1. 按流通市值升序排序
        group_sorted = group.sort_values('circulating_market_cap', ascending=True)
        
        # 2. 过滤EPS > 0
        group_filtered = group_sorted[group_sorted['eps'] > 0]
        
        # 3. 如果过滤后不足n_stocks只，则使用所有过滤后的股票
        if len(group_filtered) < n_stocks:
            if len(group_filtered) == 0:
                return np.nan
            return group_filtered['pchg'].mean()
        
        # 4. 从过滤后的股票中，按预测值选Top-N
        topn = group_filtered.nlargest(n_stocks, pred_col)
        return topn['pchg'].mean()
    
    portfolio_returns = merged.groupby('date').apply(simulate_topn_with_filter)
    portfolio_returns = portfolio_returns.dropna()  # 移除无效日期
    
    market_returns = merged.groupby('date')['pchg'].mean()
    market_returns = market_returns[market_returns.index.isin(portfolio_returns.index)]
    
    return calculate_metrics(portfolio_returns, market_returns, n_stocks)


def calculate_metrics(portfolio_returns, market_returns, n_stocks):
    """计算收益指标"""
    n_weeks = len(portfolio_returns)
    if n_weeks == 0:
        return {
            'n_stocks': n_stocks,
            'ytd_return': 0,
            'annual_return': 0,
            'annual_vol': 0,
            'sharpe': 0,
            'ytd_excess': 0,
            'annual_excess': 0,
            'max_drawdown': 0,
            'win_rate': 0,
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
    
    # 计算胜率
    win_rate = (portfolio_returns > 0).sum() / len(portfolio_returns) * 100
    
    return {
        'n_stocks': n_stocks,
        'ytd_return': ytd_port,
        'annual_return': ann_port,
        'annual_vol': ann_vol_port,
        'sharpe': sharpe_port,
        'ytd_excess': ytd_port - ytd_mkt,
        'annual_excess': ann_port - ann_mkt,
        'max_drawdown': max_dd,
        'win_rate': win_rate,
    }


def generate_comparison_report(results_df):
    """生成对比报告"""
    logger.info("\n" + "=" * 120)
    logger.info("不同持仓数量在市值EPS过滤下的表现对比")
    logger.info("=" * 120)
    
    report_lines = []
    report_lines.append("=" * 120)
    report_lines.append("不同持仓数量在市值EPS过滤下的表现对比")
    report_lines.append("=" * 120)
    report_lines.append("")
    
    report_lines.append("【策略说明】")
    report_lines.append("")
    report_lines.append("使用Phase 2模型（2015-2025年训练）")
    report_lines.append("选股流程：")
    report_lines.append("  1. 按流通市值升序排序（优先小市值）")
    report_lines.append("  2. 过滤 EPS > 0（只选盈利公司）")
    report_lines.append("  3. 从过滤后的股票中，按预测值选Top-N")
    report_lines.append("")
    report_lines.append("测试持仓数量：5, 10, 20, 30, 40, 50, 60, 80, 100支")
    report_lines.append("")
    
    report_lines.append("【详细结果】")
    report_lines.append("")
    report_lines.append(f"{'持仓数':<8} | {'年化收益':<10} | {'年化波动':<10} | {'夏普比率':<10} | {'最大回撤':<10} | {'胜率':<8} | {'年化超额':<10}")
    report_lines.append("-" * 120)
    
    for _, row in results_df.iterrows():
        report_lines.append(
            f"{row['n_stocks']:<8} | "
            f"{row['annual_return']:>9.2f}% | "
            f"{row['annual_vol']:>9.2f}% | "
            f"{row['sharpe']:>10.2f} | "
            f"{row['max_drawdown']:>9.2f}% | "
            f"{row['win_rate']:>7.1f}% | "
            f"{row['annual_excess']:>9.2f}%"
        )
    
    report_lines.append("")
    
    # 分析趋势
    report_lines.append("【关键发现】")
    report_lines.append("")
    
    # 找出最佳夏普比率
    best_sharpe_idx = results_df['sharpe'].idxmax()
    best_sharpe_row = results_df.loc[best_sharpe_idx]
    
    # 找出最高年化收益
    best_return_idx = results_df['annual_return'].idxmax()
    best_return_row = results_df.loc[best_return_idx]
    
    # 找出最小回撤
    best_dd_idx = results_df['max_drawdown'].idxmax()  # 回撤是负数，最大值最接近0
    best_dd_row = results_df.loc[best_dd_idx]
    
    report_lines.append(f"1. 最佳夏普比率: {best_sharpe_row['n_stocks']:.0f}支股票")
    report_lines.append(f"   夏普比率: {best_sharpe_row['sharpe']:.2f}")
    report_lines.append(f"   年化收益: {best_sharpe_row['annual_return']:.2f}%")
    report_lines.append(f"   年化波动: {best_sharpe_row['annual_vol']:.2f}%")
    report_lines.append("")
    
    report_lines.append(f"2. 最高年化收益: {best_return_row['n_stocks']:.0f}支股票")
    report_lines.append(f"   年化收益: {best_return_row['annual_return']:.2f}%")
    report_lines.append(f"   夏普比率: {best_return_row['sharpe']:.2f}")
    report_lines.append("")
    
    report_lines.append(f"3. 最小回撤: {best_dd_row['n_stocks']:.0f}支股票")
    report_lines.append(f"   最大回撤: {best_dd_row['max_drawdown']:.2f}%")
    report_lines.append(f"   年化收益: {best_dd_row['annual_return']:.2f}%")
    report_lines.append("")
    
    # 极端情况分析（5支股票）
    extreme_row = results_df[results_df['n_stocks'] == 5].iloc[0] if 5 in results_df['n_stocks'].values else None
    if extreme_row is not None:
        report_lines.append("4. 极端情况（5支股票）分析:")
        report_lines.append(f"   年化收益: {extreme_row['annual_return']:.2f}%")
        report_lines.append(f"   年化波动: {extreme_row['annual_vol']:.2f}%")
        report_lines.append(f"   夏普比率: {extreme_row['sharpe']:.2f}")
        report_lines.append(f"   最大回撤: {extreme_row['max_drawdown']:.2f}%")
        
        # 与50支对比
        ref_row = results_df[results_df['n_stocks'] == 50].iloc[0] if 50 in results_df['n_stocks'].values else None
        if ref_row is not None:
            report_lines.append(f"   vs 50支股票:")
            report_lines.append(f"     收益差异: {extreme_row['annual_return'] - ref_row['annual_return']:+.2f}pp")
            report_lines.append(f"     波动差异: {extreme_row['annual_vol'] - ref_row['annual_vol']:+.2f}pp")
            report_lines.append(f"     夏普差异: {extreme_row['sharpe'] - ref_row['sharpe']:+.2f}")
        report_lines.append("")
    
    # 稳定性分析
    report_lines.append("5. 稳定性趋势:")
    
    # 计算波动率随持仓数的变化
    vol_5 = results_df[results_df['n_stocks'] == 5]['annual_vol'].values[0] if 5 in results_df['n_stocks'].values else None
    vol_50 = results_df[results_df['n_stocks'] == 50]['annual_vol'].values[0] if 50 in results_df['n_stocks'].values else None
    vol_100 = results_df[results_df['n_stocks'] == 100]['annual_vol'].values[0] if 100 in results_df['n_stocks'].values else None
    
    if vol_5 and vol_50:
        report_lines.append(f"   5支 → 50支: 波动率变化 {vol_50 - vol_5:+.2f}pp")
    if vol_50 and vol_100:
        report_lines.append(f"   50支 → 100支: 波动率变化 {vol_100 - vol_50:+.2f}pp")
    
    # 判断趋势
    if len(results_df) >= 3:
        # 计算波动率与持仓数的相关性
        corr_vol = results_df[['n_stocks', 'annual_vol']].corr().iloc[0, 1]
        corr_sharpe = results_df[['n_stocks', 'sharpe']].corr().iloc[0, 1]
        
        report_lines.append("")
        if corr_vol < -0.5:
            report_lines.append("   ✅ 持仓数增加，波动率显著降低（相关系数: {:.2f}）".format(corr_vol))
        elif corr_vol < 0:
            report_lines.append("   ⚠️ 持仓数增加，波动率略有降低（相关系数: {:.2f}）".format(corr_vol))
        else:
            report_lines.append("   ❌ 持仓数增加，波动率未降低（相关系数: {:.2f}）".format(corr_vol))
        
        if corr_sharpe > 0.5:
            report_lines.append("   ✅ 持仓数增加，夏普比率显著提升（相关系数: {:.2f}）".format(corr_sharpe))
        elif corr_sharpe > 0:
            report_lines.append("   ⚠️ 持仓数增加，夏普比率略有提升（相关系数: {:.2f}）".format(corr_sharpe))
        else:
            report_lines.append("   ❌ 持仓数增加，夏普比率未提升（相关系数: {:.2f}）".format(corr_sharpe))
    
    report_lines.append("")
    
    # 最终建议
    report_lines.append("【最终建议】")
    report_lines.append("")
    
    if best_sharpe_row['n_stocks'] <= 10:
        report_lines.append(f"🎯 推荐持仓: {best_sharpe_row['n_stocks']:.0f}支股票（集中持仓，高收益高波动）")
    elif best_sharpe_row['n_stocks'] <= 50:
        report_lines.append(f"🎯 推荐持仓: {best_sharpe_row['n_stocks']:.0f}支股票（平衡收益与风险）")
    else:
        report_lines.append(f"🎯 推荐持仓: {best_sharpe_row['n_stocks']:.0f}支股票（分散风险，稳健收益）")
    
    report_lines.append(f"   预期年化收益: {best_sharpe_row['annual_return']:.2f}%")
    report_lines.append(f"   预期夏普比率: {best_sharpe_row['sharpe']:.2f}")
    report_lines.append(f"   预期最大回撤: {best_sharpe_row['max_drawdown']:.2f}%")
    
    report_lines.append("")
    report_lines.append("=" * 120)
    
    report_text = "\n".join(report_lines)
    print("\n" + report_text)
    
    # 保存报告
    report_path = OUTPUT_DIR / 'analysis' / 'portfolio_size_analysis.txt'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    logger.info(f"\n对比报告已保存: {report_path}")
    
    return report_text


def main():
    """主函数"""
    try:
        # 加载2026年实际数据
        df_2026 = load_2026_data()
        
        # 检查是否有市值和EPS字段
        has_eps = 'eps' in df_2026.columns or 'eps_ttm' in df_2026.columns
        if 'circulating_market_cap' not in df_2026.columns or not has_eps:
            logger.error("2026年数据缺少 circulating_market_cap 或 eps/eps_ttm 字段")
            return False
        
        # 加载Phase 2的holdout预测
        phase2_pred_path = OUTPUT_DIR / 'phase2' / 'predictions_2026_holdout.csv'
        
        if not phase2_pred_path.exists():
            logger.error("找不到Phase 2的2026 holdout预测文件")
            logger.error("请先运行 predict_2026_holdout.py 生成预测")
            return False
        
        # 加载预测
        phase2_pred = pd.read_csv(phase2_pred_path)
        phase2_pred['date'] = pd.to_datetime(phase2_pred['date'])
        
        logger.info(f"\nPhase 2在2026年的预测: {len(phase2_pred)} 行")
        
        # 测试不同持仓数量
        test_sizes = [5, 10, 20, 30, 40, 50, 60, 80, 100]
        
        logger.info("\n" + "=" * 80)
        logger.info("开始测试不同持仓数量")
        logger.info("=" * 80)
        
        results = []
        for n_stocks in test_sizes:
            logger.info(f"\n测试 {n_stocks} 支股票...")
            
            perf = calculate_portfolio_returns_with_filter(
                phase2_pred, 
                df_2026, 
                n_stocks, 
                pred_col='prediction'
            )
            
            if perf is not None:
                results.append(perf)
                logger.info(f"  年化收益: {perf['annual_return']:.2f}%")
                logger.info(f"  夏普比率: {perf['sharpe']:.2f}")
                logger.info(f"  年化波动: {perf['annual_vol']:.2f}%")
                logger.info(f"  最大回撤: {perf['max_drawdown']:.2f}%")
        
        if len(results) == 0:
            logger.error("所有测试都失败了")
            return False
        
        # 转换为DataFrame
        results_df = pd.DataFrame(results)
        
        # 保存详细结果
        csv_path = OUTPUT_DIR / 'analysis' / 'portfolio_size_results.csv'
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        results_df.to_csv(csv_path, index=False)
        logger.info(f"\n详细结果已保存: {csv_path}")
        
        # 生成对比报告
        generate_comparison_report(results_df)
        
        return True
        
    except Exception as e:
        logger.error(f"分析失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
