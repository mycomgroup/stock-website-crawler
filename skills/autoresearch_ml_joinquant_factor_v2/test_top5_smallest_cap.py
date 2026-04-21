"""
测试极端集中策略：5支最小市值股票

策略：
1. 第一阶段：先取预测值Top 10%的股票
2. 第二阶段：用EPS阈值过滤
3. 第三阶段：选市值最小的5支

对比不同的EPS阈值和持仓数量
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


def calculate_smallest_cap_portfolio(
    predictions,
    actual_data,
    n_stocks=5,
    top_pct=0.1,
    eps_threshold=0.5,
    pred_col='prediction'
):
    """
    选择最小市值股票的策略
    
    Parameters
    ----------
    n_stocks : int
        持仓数量
    top_pct : float
        第一阶段选取的比例
    eps_threshold : float
        EPS阈值
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
        # 第一阶段：选取预测值Top 10%
        n_stage1 = max(int(len(group) * top_pct), n_stocks)
        stage1_pool = group.nlargest(n_stage1, pred_col)
        
        # 第二阶段：EPS过滤
        if eps_threshold is not None:
            stage2_pool = stage1_pool[stage1_pool['eps'] > eps_threshold]
        else:
            stage2_pool = stage1_pool
        
        if len(stage2_pool) == 0:
            return np.nan
        
        # 第三阶段：选市值最小的N支
        if len(stage2_pool) < n_stocks:
            final_pool = stage2_pool
        else:
            final_pool = stage2_pool.nsmallest(n_stocks, 'circulating_market_cap')
        
        return final_pool['pchg'].mean()
    
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
    logger.info("最小市值选股策略对比")
    logger.info("=" * 140)
    
    report_lines = []
    report_lines.append("=" * 140)
    report_lines.append("最小市值选股策略对比")
    report_lines.append("=" * 140)
    report_lines.append("")
    
    report_lines.append("【策略说明】")
    report_lines.append("")
    report_lines.append("选股流程：")
    report_lines.append("  1. 第一阶段：按模型预测值，选取Top 10%的股票")
    report_lines.append("  2. 第二阶段：用EPS阈值过滤")
    report_lines.append("  3. 第三阶段：选市值最小的N支")
    report_lines.append("")
    report_lines.append("测试组合：")
    report_lines.append("  - 不同EPS阈值：0, 0.1, 0.5")
    report_lines.append("  - 不同持仓数量：5, 10, 20, 30, 50支")
    report_lines.append("")
    
    report_lines.append("【详细结果】")
    report_lines.append("")
    report_lines.append(f"{'策略描述':<40} | {'年化收益':<10} | {'年化波动':<10} | {'夏普比率':<10} | {'最大回撤':<10} | {'胜率':<8}")
    report_lines.append("-" * 140)
    
    for _, row in results_df.iterrows():
        report_lines.append(
            f"{row['strategy_name']:<40} | "
            f"{row['annual_return']:>9.2f}% | "
            f"{row['annual_vol']:>9.2f}% | "
            f"{row['sharpe']:>10.2f} | "
            f"{row['max_drawdown']:>9.2f}% | "
            f"{row['win_rate']:>7.1f}%"
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
    
    # 5支股票分析
    top5_rows = results_df[results_df['n_stocks'] == 5]
    if len(top5_rows) > 0:
        report_lines.append("3. 极端集中（5支股票）分析:")
        report_lines.append("")
        for _, row in top5_rows.iterrows():
            report_lines.append(f"   {row['strategy_name']}:")
            report_lines.append(f"     年化收益: {row['annual_return']:.2f}%")
            report_lines.append(f"     夏普比率: {row['sharpe']:.2f}")
            report_lines.append(f"     年化波动: {row['annual_vol']:.2f}%")
            report_lines.append(f"     最大回撤: {row['max_drawdown']:.2f}%")
            report_lines.append("")
    
    # 对比之前的最优策略
    report_lines.append("4. 与之前最优策略对比:")
    report_lines.append("")
    report_lines.append("   之前最优（Top10%→EPS>0.5+按预测值选Top50）:")
    report_lines.append("     年化收益: 24.77%, 夏普: 1.13")
    report_lines.append("")
    report_lines.append(f"   当前最优（{best_sharpe_row['strategy_name']}）:")
    report_lines.append(f"     年化收益: {best_sharpe_row['annual_return']:.2f}%, 夏普: {best_sharpe_row['sharpe']:.2f}")
    report_lines.append("")
    
    improvement = best_sharpe_row['annual_return'] - 24.77
    if improvement > 1:
        report_lines.append(f"   ✅ 最小市值策略显著优于预测值策略（+{improvement:.2f}pp）")
    elif improvement > 0:
        report_lines.append(f"   ⚠️ 最小市值策略略优于预测值策略（+{improvement:.2f}pp）")
    else:
        report_lines.append(f"   ❌ 最小市值策略未改善收益（{improvement:.2f}pp）")
    
    report_lines.append("")
    
    # EPS阈值效应
    report_lines.append("5. EPS阈值效应（以5支股票为例）:")
    if len(top5_rows) > 0:
        for _, row in top5_rows.iterrows():
            eps_label = f"EPS>{row['eps_threshold']}" if row['eps_threshold'] is not None else "不过滤EPS"
            report_lines.append(f"   {eps_label}: 年化收益 {row['annual_return']:.2f}%, 夏普 {row['sharpe']:.2f}")
    
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
    report_path = OUTPUT_DIR / 'analysis' / 'smallest_cap_strategy_analysis.txt'
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
        
        # 定义测试组合
        test_configs = []
        
        # 不同EPS阈值 + 不同持仓数量
        for eps_val in [0, 0.1, 0.5]:
            for n_stocks in [5, 10, 20, 30, 50]:
                eps_label = f"EPS>{eps_val}" if eps_val is not None else "不过滤EPS"
                test_configs.append({
                    'name': f'Top10%→{eps_label}→最小市值{n_stocks}支',
                    'n_stocks': n_stocks,
                    'eps_threshold': eps_val,
                })
        
        logger.info("\n" + "=" * 80)
        logger.info("开始测试最小市值选股策略")
        logger.info("=" * 80)
        
        results = []
        for config in test_configs:
            logger.info(f"\n测试: {config['name']}")
            
            perf = calculate_smallest_cap_portfolio(
                phase2_pred,
                df_2026,
                n_stocks=config['n_stocks'],
                top_pct=0.1,
                eps_threshold=config['eps_threshold'],
                pred_col='prediction'
            )
            
            if perf is not None:
                result = {
                    'strategy_name': config['name'],
                    'n_stocks': config['n_stocks'],
                    'eps_threshold': config['eps_threshold'],
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
        csv_path = OUTPUT_DIR / 'analysis' / 'smallest_cap_strategy_results.csv'
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
