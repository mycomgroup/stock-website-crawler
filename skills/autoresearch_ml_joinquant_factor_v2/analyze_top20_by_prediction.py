"""
分析按预测值选Top 20的历史表现

对比：
1. 按预测值选Top 20 vs 按预测值选Top 50
2. 按预测值选Top 20 vs 按实际收益选Top 20（理想情况）
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import glob

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / 'output'


def load_all_data():
    """加载所有年份的数据"""
    logger.info("加载所有年份数据...")
    
    train_file = BASE_DIR / "train_merged_all.csv"
    
    if train_file.exists():
        logger.info(f"  从 {train_file.name} 加载历史数据...")
        df_all = pd.read_csv(train_file)
        
        if 'Unnamed: 0' in df_all.columns:
            df_all = df_all.rename(columns={'Unnamed: 0': 'stock_id'})
        
        df_all['date'] = pd.to_datetime(df_all['date'])
    else:
        logger.error("找不到train_merged_all.csv")
        return None
    
    # 过滤异常数据
    dates_to_remove = []
    for date in sorted(df_all['date'].unique()):
        df_date = df_all[df_all['date'] == date]
        pchg_valid = df_date['pchg'].dropna()
        
        if len(pchg_valid) == 0:
            dates_to_remove.append(date)
        elif (pchg_valid == -1.0).sum() > len(pchg_valid) * 0.5:
            dates_to_remove.append(date)
        elif np.isinf(pchg_valid).sum() > 0:
            dates_to_remove.append(date)
    
    if dates_to_remove:
        logger.info(f"  过滤掉 {len(dates_to_remove)} 个异常日期")
        df_all = df_all[~df_all['date'].isin(dates_to_remove)]
    
    df_all['year'] = df_all['date'].dt.year
    
    logger.info(f"  总数据: {len(df_all)} 行")
    for year in sorted(df_all['year'].unique()):
        year_data = df_all[df_all['year'] == year]
        logger.info(f"  {year}年: {len(year_data)} 行, {year_data['date'].nunique()} 个日期")
    
    return df_all


def load_predictions():
    """加载预测数据"""
    logger.info("\n加载预测数据...")
    
    oof_path = OUTPUT_DIR / 'phase2' / 'oof_predictions_phase2.csv'
    oof_pred = pd.read_csv(oof_path)
    oof_pred['date'] = pd.to_datetime(oof_pred['date'])
    oof_pred['year'] = oof_pred['date'].dt.year
    
    if 'oof_prediction' in oof_pred.columns:
        oof_pred = oof_pred.rename(columns={'oof_prediction': 'prediction'})
    
    holdout_path = OUTPUT_DIR / 'phase2' / 'predictions_2026_holdout.csv'
    holdout_pred = pd.read_csv(holdout_path)
    holdout_pred['date'] = pd.to_datetime(holdout_pred['date'])
    holdout_pred['year'] = holdout_pred['date'].dt.year
    
    all_pred = pd.concat([oof_pred, holdout_pred], ignore_index=True)
    
    logger.info(f"  总预测: {len(all_pred)} 行")
    
    return all_pred


def analyze_top_n_performance(predictions, actual_data, n_stocks=20):
    """
    分析按预测值选Top N的表现
    
    策略：Top10% → EPS>0.5 → 按预测值选Top N
    """
    
    # 为预测数据创建匹配日期
    predictions = predictions.copy()
    actual_dates = sorted(actual_data['date'].unique())
    
    def find_next_date(pred_date):
        for actual_date in actual_dates:
            days_diff = (actual_date - pred_date).days
            if 3 <= days_diff <= 14:
                return actual_date
        return None
    
    predictions['match_date'] = predictions['date'].apply(find_next_date)
    predictions = predictions[predictions['match_date'].notna()]
    
    # 合并数据
    eps_col = 'eps_ttm' if 'eps_ttm' in actual_data.columns else 'eps'
    actual_data_renamed = actual_data.rename(columns={'date': 'match_date'})
    
    merged = predictions[['date', 'match_date', 'stock_id', 'prediction', 'year']].merge(
        actual_data_renamed[['match_date', 'stock_id', 'pchg', 'circulating_market_cap', eps_col]],
        on=['match_date', 'stock_id'],
        how='inner'
    )
    
    if eps_col == 'eps_ttm':
        merged = merged.rename(columns={'eps_ttm': 'eps'})
    
    # 按年份分析
    results_by_year = {}
    
    for year in sorted(merged['year'].unique()):
        year_data = merged[merged['year'] == year]
        
        weekly_returns = []
        
        for date in sorted(year_data['date'].unique()):
            df_date = year_data[year_data['date'] == date]
            
            # 第一阶段：Top10%
            n_stage1 = max(int(len(df_date) * 0.1), n_stocks)
            stage1_pool = df_date.nlargest(n_stage1, 'prediction')
            
            # 第二阶段：EPS>0.5
            stage2_pool = stage1_pool[stage1_pool['eps'] > 0.5]
            
            # 第三阶段：按预测值选Top N
            if len(stage2_pool) < n_stocks:
                final_pool = stage2_pool.nlargest(len(stage2_pool), 'prediction')
            else:
                final_pool = stage2_pool.nlargest(n_stocks, 'prediction')
            
            # 计算平均收益
            avg_return = final_pool['pchg'].mean()
            weekly_returns.append({
                'date': date,
                'avg_return': avg_return,
                'n_stocks': len(final_pool)
            })
        
        if weekly_returns:
            df_year = pd.DataFrame(weekly_returns)
            results_by_year[year] = df_year
    
    return results_by_year


def compare_strategies():
    """对比不同持仓数量的策略"""
    
    # 加载数据
    actual_data = load_all_data()
    if actual_data is None:
        return False
    
    predictions = load_predictions()
    
    # 分析不同持仓数量
    strategies = {
        'Top 10': 10,
        'Top 20': 20,
        'Top 30': 30,
        'Top 50': 50,
    }
    
    all_results = {}
    
    for strategy_name, n_stocks in strategies.items():
        logger.info(f"\n分析策略: {strategy_name}")
        results = analyze_top_n_performance(predictions, actual_data, n_stocks)
        all_results[strategy_name] = results
    
    # 生成对比报告
    generate_comparison_report(all_results)
    
    return True


def generate_comparison_report(all_results):
    """生成对比报告"""
    
    report_lines = []
    report_lines.append("=" * 120)
    report_lines.append("按预测值选Top N的历史表现对比")
    report_lines.append("=" * 120)
    report_lines.append("")
    
    report_lines.append("【分析说明】")
    report_lines.append("")
    report_lines.append("策略：Top10% → EPS>0.5 → 按预测值选Top N")
    report_lines.append("对比：Top 10、Top 20、Top 30、Top 50")
    report_lines.append("关键：这是按预测值选股，不是按实际收益选股（事后诸葛亮）")
    report_lines.append("")
    report_lines.append("=" * 120)
    
    # 收集所有年份
    all_years = set()
    for strategy_results in all_results.values():
        all_years.update(strategy_results.keys())
    
    # 按年份对比
    summary_data = []
    
    for year in sorted(all_years):
        report_lines.append("")
        report_lines.append(f"\n{'=' * 120}")
        report_lines.append(f"{year}年 各策略表现对比")
        report_lines.append("=" * 120)
        report_lines.append("")
        
        year_summary = {'year': year}
        
        report_lines.append(f"{'策略':<12} | {'周数':<6} | {'周均收益':<12} | {'年化收益':<12} | {'相对Top50':<12}")
        report_lines.append("-" * 120)
        
        # 先计算Top 50作为基准
        top50_annual = None
        if 'Top 50' in all_results and year in all_results['Top 50']:
            df_50 = all_results['Top 50'][year]
            avg_50 = df_50['avg_return'].mean() * 100
            annual_50 = ((1 + avg_50/100) ** 52 - 1) * 100
            top50_annual = annual_50
        
        for strategy_name in ['Top 10', 'Top 20', 'Top 30', 'Top 50']:
            if strategy_name not in all_results:
                continue
            
            if year not in all_results[strategy_name]:
                continue
            
            df_year = all_results[strategy_name][year]
            weeks = len(df_year)
            avg_return = df_year['avg_return'].mean() * 100
            annual_return = ((1 + avg_return/100) ** 52 - 1) * 100
            
            # 相对Top 50的提升
            if top50_annual is not None and top50_annual != 0:
                relative = ((annual_return - top50_annual) / abs(top50_annual)) * 100
                relative_str = f"{relative:+.1f}%"
            else:
                relative_str = "N/A"
            
            report_lines.append(
                f"{strategy_name:<12} | {weeks:<6} | {avg_return:>11.2f}% | {annual_return:>11.2f}% | {relative_str:>11}"
            )
            
            # 保存到summary
            year_summary[strategy_name] = annual_return
        
        summary_data.append(year_summary)
        report_lines.append("")
    
    # 生成汇总表
    report_lines.append("")
    report_lines.append("=" * 120)
    report_lines.append("【历史年份汇总】")
    report_lines.append("=" * 120)
    report_lines.append("")
    
    report_lines.append(f"{'年份':<8} | {'Top 10':<12} | {'Top 20':<12} | {'Top 30':<12} | {'Top 50':<12}")
    report_lines.append("-" * 120)
    
    for data in summary_data:
        year = data['year']
        top10 = data.get('Top 10', 0)
        top20 = data.get('Top 20', 0)
        top30 = data.get('Top 30', 0)
        top50 = data.get('Top 50', 0)
        
        report_lines.append(
            f"{year:<8} | {top10:>11.2f}% | {top20:>11.2f}% | {top30:>11.2f}% | {top50:>11.2f}%"
        )
    
    report_lines.append("")
    
    # 计算平均值
    report_lines.append("=" * 120)
    report_lines.append("【平均年化收益】")
    report_lines.append("=" * 120)
    report_lines.append("")
    
    for strategy_name in ['Top 10', 'Top 20', 'Top 30', 'Top 50']:
        values = [d.get(strategy_name, 0) for d in summary_data if strategy_name in d]
        if values:
            avg = np.mean(values)
            report_lines.append(f"{strategy_name}: {avg:.2f}%")
    
    report_lines.append("")
    
    # 关键结论
    report_lines.append("=" * 120)
    report_lines.append("【关键结论】")
    report_lines.append("=" * 120)
    report_lines.append("")
    
    # 计算平均提升
    top10_avg = np.mean([d.get('Top 10', 0) for d in summary_data if 'Top 10' in d])
    top20_avg = np.mean([d.get('Top 20', 0) for d in summary_data if 'Top 20' in d])
    top30_avg = np.mean([d.get('Top 30', 0) for d in summary_data if 'Top 30' in d])
    top50_avg = np.mean([d.get('Top 50', 0) for d in summary_data if 'Top 50' in d])
    
    if top50_avg != 0:
        improvement_10 = ((top10_avg - top50_avg) / abs(top50_avg)) * 100
        improvement_20 = ((top20_avg - top50_avg) / abs(top50_avg)) * 100
        improvement_30 = ((top30_avg - top50_avg) / abs(top50_avg)) * 100
        
        report_lines.append(f"1. Top 10相比Top 50：年化收益提升 {improvement_10:+.1f}%")
        report_lines.append(f"2. Top 20相比Top 50：年化收益提升 {improvement_20:+.1f}%")
        report_lines.append(f"3. Top 30相比Top 50：年化收益提升 {improvement_30:+.1f}%")
        report_lines.append("")
    
    report_lines.append("💡 建议：")
    report_lines.append("")
    
    if top20_avg > top50_avg * 1.5:
        report_lines.append("✅ Top 20策略显著优于Top 50，建议减少持仓至20支")
    elif top30_avg > top50_avg * 1.3:
        report_lines.append("✅ Top 30策略明显优于Top 50，建议减少持仓至30支")
    else:
        report_lines.append("⚠️ 减少持仓的优势不明显，建议保持50支或进一步优化选股策略")
    
    report_lines.append("")
    report_lines.append("=" * 120)
    
    report_text = "\n".join(report_lines)
    print("\n" + report_text)
    
    # 保存报告
    report_path = OUTPUT_DIR / 'analysis' / 'top_n_comparison.txt'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    logger.info(f"\n对比报告已保存: {report_path}")


def main():
    """主函数"""
    try:
        success = compare_strategies()
        return success
    except Exception as e:
        logger.error(f"分析失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
