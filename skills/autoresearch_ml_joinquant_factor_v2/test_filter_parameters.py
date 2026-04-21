"""
测试不同过滤参数的效果

测试维度：
1. 市值方向：升序（小市值优先）vs 降序（大市值优先）vs 不过滤
2. EPS阈值：> 0 vs > 0.1 vs > 0.5 vs 不过滤
3. 组合测试：各种参数组合

目标：找到最优的过滤参数组合
"""

import pandas as pd
import numpy as np
from pathlib import Path
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
    
    logger.info(f"  2026年数据: {len(df_2026)} 行, {df_2026['date'].nunique()} 个日期")
    
    return df_2026


def calculate_portfolio_with_params(
    predictions, 
    actual_data, 
    n_stocks=50,
    market_cap_order='asc',  # 'asc'=小市值优先, 'desc'=大市值优先, None=不过滤
    eps_threshold=0,  # EPS阈值，None=不过滤
    pred_col='prediction'
):
    """
    使用指定参数计算组合收益
    
    Parameters
    ----------
    market_cap_order : str or None
        'asc' = 小市值优先
        'desc' = 大市值优先
        None = 不按市值过滤
    eps_threshold : float or None
        EPS阈值，None表示不过滤
    """
    
    # 合并数据
    eps_col = 'eps_ttm' if 'eps_ttm' in actual_data.columns else 'eps'
    merged = predictions[['date', 'stock_id', pred_col]].merge(
        actual_data[['date', 'stock_id', 'pchg', 'circulating_market_cap', eps_col]],
        on=['date', 'stock_id'],
        how='inner'
    )
    
    if eps_col == 'eps_ttm':
        merged = merged.rename(columns={'eps_ttm': 'eps'})
    
    if len(merged) == 0:
        return None
    
    def simulate_portfolio(group):
        # 1. 市值过滤
        if market_cap_order == 'asc':
            group = group.sort_values('circulating_market_cap', ascending=True)
        elif market_cap_order == 'desc':
            group = group.sort_values('circulating_market_cap', ascending=False)
        # None的话不排序
        
        # 2. EPS过滤
        if eps_threshold is not None:
            group = group[group['eps'] > eps_threshold]
        
        # 3. 如果过滤后股票不足
        if len(group) < n_stocks:
            if len(group) == 0:
                return np.nan
            return group['pchg'].mean()
        
        # 4. 按预测值选Top-N
        topn = group.nlargest(n_stocks, pred_col)
        return topn['pchg'].mean()
    
    portfolio_returns = merged.groupby('date').apply(simulate_portfolio)
    portfolio_returns = portfolio_returns.dropna()
    
    market_returns = merged.groupby('date')['pchg'].mean()
    market_returns = market_returns[market_returns.index.isin(portfolio_returns.index)]
    
    return calculate_metrics(portfolio_returns, market_returns)


def calculate_metrics(portfolio_returns, market_returns):
    """计算收益指标"""
    n_weeks = len(portfolio_returns)
    if n_weeks == 0:
        return None
    
    port_cum = (1 + portfolio_returns).cumprod()
    mkt_cum = (1 + market_returns).cumprod()
    
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
    
    cumulative = (1 + portfolio_returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_dd = drawdown.min() * 100
    
    win_rate = (portfolio_returns > 0).sum() / len(portfolio_returns) * 100
    
    return {
        'annual_return': ann_port,
        'annual_vol': ann_vol_port,
        'sharpe': sharpe_port,
        'max_drawdown': max_dd,
        'win_rate': win_rate,
        'annual_excess': ann_port - ann_mkt,
    }


def generate_report(results_df):
    """生成对比报告"""
    logger.info("\n" + "=" * 140)
    logger.info("不同过滤参数的表现对比")
    logger.info("=" * 140)
    
    report_lines = []
    report_lines.append("=" * 140)
    report_lines.append("不同过滤参数的表现对比（持仓50支）")
    report_lines.append("=" * 140)
    report_lines.append("")
    
    report_lines.append("【参数说明】")
    report_lines.append("")
    report_lines.append("市值方向：")
    report_lines.append("  - 小市值优先：按流通市值升序排序")
    report_lines.append("  - 大市值优先：按流通市值降序排序")
    report_lines.append("  - 不过滤：不按市值排序")
    report_lines.append("")
    report_lines.append("EPS阈值：")
    report_lines.append("  - > 0：只选盈利公司")
    report_lines.append("  - > 0.1：只选EPS大于0.1的公司")
    report_lines.append("  - > 0.5：只选EPS大于0.5的公司")
    report_lines.append("  - 不过滤：不限制EPS")
    report_lines.append("")
    
    report_lines.append("【详细结果】")
    report_lines.append("")
    report_lines.append(f"{'策略描述':<30} | {'年化收益':<10} | {'年化波动':<10} | {'夏普比率':<10} | {'最大回撤':<10} | {'胜率':<8} | {'年化超额':<10}")
    report_lines.append("-" * 140)
    
    for _, row in results_df.iterrows():
        report_lines.append(
            f"{row['strategy_name']:<30} | "
            f"{row['annual_return']:>9.2f}% | "
            f"{row['annual_vol']:>9.2f}% | "
            f"{row['sharpe']:>10.2f} | "
            f"{row['max_drawdown']:>9.2f}% | "
            f"{row['win_rate']:>7.1f}% | "
            f"{row['annual_excess']:>9.2f}%"
        )
    
    report_lines.append("")
    
    # 找出最佳策略
    best_sharpe_idx = results_df['sharpe'].idxmax()
    best_sharpe_row = results_df.loc[best_sharpe_idx]
    
    best_return_idx = results_df['annual_return'].idxmax()
    best_return_row = results_df.loc[best_return_idx]
    
    report_lines.append("【关键发现】")
    report_lines.append("")
    
    report_lines.append(f"1. 最佳夏普比率策略: {best_sharpe_row['strategy_name']}")
    report_lines.append(f"   夏普比率: {best_sharpe_row['sharpe']:.2f}")
    report_lines.append(f"   年化收益: {best_sharpe_row['annual_return']:.2f}%")
    report_lines.append(f"   年化波动: {best_sharpe_row['annual_vol']:.2f}%")
    report_lines.append("")
    
    report_lines.append(f"2. 最高年化收益策略: {best_return_row['strategy_name']}")
    report_lines.append(f"   年化收益: {best_return_row['annual_return']:.2f}%")
    report_lines.append(f"   夏普比率: {best_return_row['sharpe']:.2f}")
    report_lines.append("")
    
    # 市值效应分析
    small_cap = results_df[results_df['market_cap_order'] == 'asc']['annual_return'].mean()
    large_cap = results_df[results_df['market_cap_order'] == 'desc']['annual_return'].mean()
    no_cap = results_df[results_df['market_cap_order'].isna()]['annual_return'].mean()
    
    report_lines.append("3. 市值效应分析:")
    report_lines.append(f"   小市值优先平均收益: {small_cap:.2f}%")
    report_lines.append(f"   大市值优先平均收益: {large_cap:.2f}%")
    report_lines.append(f"   不过滤平均收益: {no_cap:.2f}%")
    
    if small_cap > large_cap and small_cap > no_cap:
        report_lines.append("   ✅ 小市值效应显著，小市值股票表现最佳")
    elif large_cap > small_cap and large_cap > no_cap:
        report_lines.append("   ⚠️ 大市值股票表现更好")
    else:
        report_lines.append("   ⚠️ 市值过滤效果不明显")
    
    report_lines.append("")
    
    # EPS效应分析
    eps_groups = results_df.groupby('eps_threshold')['annual_return'].mean().sort_values(ascending=False)
    report_lines.append("4. EPS阈值效应分析:")
    for eps_val, ret in eps_groups.items():
        eps_label = f"EPS > {eps_val}" if eps_val is not None else "不过滤EPS"
        report_lines.append(f"   {eps_label}: 平均收益 {ret:.2f}%")
    
    report_lines.append("")
    report_lines.append("【最终推荐】")
    report_lines.append("")
    report_lines.append(f"🎯 推荐策略: {best_sharpe_row['strategy_name']}")
    report_lines.append(f"   预期年化收益: {best_sharpe_row['annual_return']:.2f}%")
    report_lines.append(f"   预期夏普比率: {best_sharpe_row['sharpe']:.2f}")
    report_lines.append(f"   预期最大回撤: {best_sharpe_row['max_drawdown']:.2f}%")
    
    report_lines.append("")
    report_lines.append("=" * 140)
    
    report_text = "\n".join(report_lines)
    print("\n" + report_text)
    
    # 保存报告
    report_path = OUTPUT_DIR / 'analysis' / 'filter_parameters_analysis.txt'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    logger.info(f"\n对比报告已保存: {report_path}")
    
    return report_text


def main():
    """主函数"""
    try:
        # 加载数据
        df_2026 = load_2026_data()
        
        has_eps = 'eps' in df_2026.columns or 'eps_ttm' in df_2026.columns
        if 'circulating_market_cap' not in df_2026.columns or not has_eps:
            logger.error("2026年数据缺少必要字段")
            return False
        
        # 加载Phase 2预测
        phase2_pred_path = OUTPUT_DIR / 'phase2' / 'predictions_2026_holdout.csv'
        if not phase2_pred_path.exists():
            logger.error("找不到Phase 2的预测文件")
            return False
        
        phase2_pred = pd.read_csv(phase2_pred_path)
        phase2_pred['date'] = pd.to_datetime(phase2_pred['date'])
        
        logger.info(f"\nPhase 2在2026年的预测: {len(phase2_pred)} 行")
        
        # 定义测试参数组合
        test_configs = [
            # 基准：不过滤
            {'name': '基准（不过滤）', 'market_cap': None, 'eps': None},
            
            # 只过滤市值
            {'name': '小市值优先（不过滤EPS）', 'market_cap': 'asc', 'eps': None},
            {'name': '大市值优先（不过滤EPS）', 'market_cap': 'desc', 'eps': None},
            
            # 只过滤EPS
            {'name': '不过滤市值（EPS>0）', 'market_cap': None, 'eps': 0},
            {'name': '不过滤市值（EPS>0.1）', 'market_cap': None, 'eps': 0.1},
            {'name': '不过滤市值（EPS>0.5）', 'market_cap': None, 'eps': 0.5},
            
            # 小市值 + EPS组合
            {'name': '小市值+EPS>0', 'market_cap': 'asc', 'eps': 0},
            {'name': '小市值+EPS>0.1', 'market_cap': 'asc', 'eps': 0.1},
            {'name': '小市值+EPS>0.5', 'market_cap': 'asc', 'eps': 0.5},
            
            # 大市值 + EPS组合
            {'name': '大市值+EPS>0', 'market_cap': 'desc', 'eps': 0},
            {'name': '大市值+EPS>0.1', 'market_cap': 'desc', 'eps': 0.1},
            {'name': '大市值+EPS>0.5', 'market_cap': 'desc', 'eps': 0.5},
        ]
        
        logger.info("\n" + "=" * 80)
        logger.info("开始测试不同过滤参数组合")
        logger.info("=" * 80)
        
        results = []
        for config in test_configs:
            logger.info(f"\n测试: {config['name']}")
            
            perf = calculate_portfolio_with_params(
                phase2_pred,
                df_2026,
                n_stocks=50,
                market_cap_order=config['market_cap'],
                eps_threshold=config['eps'],
                pred_col='prediction'
            )
            
            if perf is not None:
                result = {
                    'strategy_name': config['name'],
                    'market_cap_order': config['market_cap'],
                    'eps_threshold': config['eps'],
                    **perf
                }
                results.append(result)
                logger.info(f"  年化收益: {perf['annual_return']:.2f}%")
                logger.info(f"  夏普比率: {perf['sharpe']:.2f}")
        
        if len(results) == 0:
            logger.error("所有测试都失败了")
            return False
        
        # 转换为DataFrame
        results_df = pd.DataFrame(results)
        
        # 保存详细结果
        csv_path = OUTPUT_DIR / 'analysis' / 'filter_parameters_results.csv'
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        results_df.to_csv(csv_path, index=False)
        logger.info(f"\n详细结果已保存: {csv_path}")
        
        # 生成对比报告
        generate_report(results_df)
        
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
