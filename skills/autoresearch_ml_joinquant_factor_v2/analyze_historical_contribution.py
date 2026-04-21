"""
分析历史上所有年份选50支股票的收益贡献分布

目标：
1. 分析2024、2025、2026年每年的收益贡献情况
2. 验证是否历史上也是20-30支股票贡献主要收益
3. 分析剩余股票是否拖后腿（负贡献）
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
    
    # 优先使用train_merged_all.csv（包含2009-2025年的完整数据）
    train_file = BASE_DIR / "train_merged_all.csv"
    
    if train_file.exists():
        logger.info(f"  从 {train_file.name} 加载历史数据...")
        df_all = pd.read_csv(train_file)
        
        # 统一列名
        if 'Unnamed: 0' in df_all.columns:
            df_all = df_all.rename(columns={'Unnamed: 0': 'stock_id'})
        
        df_all['date'] = pd.to_datetime(df_all['date'])
    else:
        # 如果没有train_merged_all.csv，则从weekly_factors加载
        logger.info("  从 weekly_factors 目录加载数据...")
        data_dir = BASE_DIR / "data" / "weekly_factors"
        all_files = sorted(glob.glob(str(data_dir / "factors_*.csv")))
        
        dfs = []
        for file_path in all_files:
            df = pd.read_csv(file_path)
            date_str = Path(file_path).stem.split('_')[1]
            df['date'] = pd.to_datetime(date_str)
            dfs.append(df)
        
        df_all = pd.concat(dfs, ignore_index=True)
        
        # 统一列名
        if 'Unnamed: 0' in df_all.columns:
            df_all = df_all.rename(columns={'Unnamed: 0': 'stock_id'})
    
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
    
    # 添加年份列
    df_all['year'] = df_all['date'].dt.year
    
    logger.info(f"  总数据: {len(df_all)} 行")
    for year in sorted(df_all['year'].unique()):
        year_data = df_all[df_all['year'] == year]
        logger.info(f"  {year}年: {len(year_data)} 行, {year_data['date'].nunique()} 个日期")
    
    return df_all


def load_predictions():
    """加载预测数据"""
    logger.info("\n加载预测数据...")
    
    # 加载OOF预测（2009-2024训练集）
    oof_path = OUTPUT_DIR / 'phase2' / 'oof_predictions_phase2.csv'
    oof_pred = pd.read_csv(oof_path)
    oof_pred['date'] = pd.to_datetime(oof_pred['date'])
    oof_pred['year'] = oof_pred['date'].dt.year
    # 统一列名
    if 'oof_prediction' in oof_pred.columns:
        oof_pred = oof_pred.rename(columns={'oof_prediction': 'prediction'})
    
    # 加载2026预测
    holdout_path = OUTPUT_DIR / 'phase2' / 'predictions_2026_holdout.csv'
    holdout_pred = pd.read_csv(holdout_path)
    holdout_pred['date'] = pd.to_datetime(holdout_pred['date'])
    holdout_pred['year'] = holdout_pred['date'].dt.year
    
    # 合并
    all_pred = pd.concat([oof_pred, holdout_pred], ignore_index=True)
    
    # 不再过滤年份，保留所有预测数据
    
    logger.info(f"  总预测: {len(all_pred)} 行")
    for year in sorted(all_pred['year'].unique()):
        year_pred = all_pred[all_pred['year'] == year]
        logger.info(f"  {year}年: {len(year_pred)} 行, {year_pred['date'].nunique()} 个日期")
    
    return all_pred


def analyze_return_contribution_by_year(predictions, actual_data):
    """
    按年份分析收益贡献
    
    策略：Top10% → EPS>0.5 → 按预测值选Top50
    
    注意：预测日期和实际收益日期可能不完全对齐
    我们使用最近的下一个实际日期来匹配预测
    """
    
    # 为每个预测找到最近的下一个实际日期
    predictions = predictions.copy()
    actual_dates = sorted(actual_data['date'].unique())
    
    def find_next_date(pred_date):
        """找到预测日期之后最近的实际日期（7-14天内）"""
        for actual_date in actual_dates:
            days_diff = (actual_date - pred_date).days
            if 3 <= days_diff <= 14:  # 允许3-14天的范围
                return actual_date
        return None
    
    predictions['match_date'] = predictions['date'].apply(find_next_date)
    
    # 过滤掉没有匹配日期的预测
    predictions = predictions[predictions['match_date'].notna()]
    
    logger.info(f"  匹配后保留 {len(predictions)} 条预测，{predictions['date'].nunique()} 个日期")
    
    # 合并数据
    eps_col = 'eps_ttm' if 'eps_ttm' in actual_data.columns else 'eps'
    
    # 重命名以便合并
    actual_data_renamed = actual_data.rename(columns={'date': 'match_date'})
    
    merged = predictions[['date', 'match_date', 'stock_id', 'prediction', 'year']].merge(
        actual_data_renamed[['match_date', 'stock_id', 'pchg', 'circulating_market_cap', eps_col]],
        on=['match_date', 'stock_id'],
        how='inner'
    )
    
    if eps_col == 'eps_ttm':
        merged = merged.rename(columns={'eps_ttm': 'eps'})
    
    # 按年份和日期分析
    results_by_year = {}
    
    for year in sorted(merged['year'].unique()):
        logger.info(f"\n分析 {year} 年...")
        year_data = merged[merged['year'] == year]
        
        all_stocks_returns = []
        
        for date in sorted(year_data['date'].unique()):
            df_date = year_data[year_data['date'] == date]
            
            # 第一阶段：Top10%
            n_stage1 = max(int(len(df_date) * 0.1), 50)
            stage1_pool = df_date.nlargest(n_stage1, 'prediction')
            
            # 第二阶段：EPS>0.5
            stage2_pool = stage1_pool[stage1_pool['eps'] > 0.5]
            
            # 第三阶段：按预测值选Top50
            if len(stage2_pool) < 50:
                final_pool = stage2_pool.nlargest(len(stage2_pool), 'prediction')
            else:
                final_pool = stage2_pool.nlargest(50, 'prediction')
            
            # 按收益率排序
            final_pool = final_pool.sort_values('pchg', ascending=False)
            final_pool['rank'] = range(1, len(final_pool) + 1)
            
            all_stocks_returns.append(final_pool[['date', 'stock_id', 'rank', 'pchg', 'prediction']])
        
        if all_stocks_returns:
            df_year = pd.concat(all_stocks_returns, ignore_index=True)
            results_by_year[year] = df_year
            logger.info(f"  {year}年: {len(df_year)} 条记录, {df_year['date'].nunique()} 个交易日")
    
    return results_by_year


def generate_yearly_report(results_by_year):
    """生成按年份的收益贡献分析报告"""
    
    report_lines = []
    report_lines.append("=" * 120)
    report_lines.append("历史年份50支股票收益贡献分析")
    report_lines.append("=" * 120)
    report_lines.append("")
    
    report_lines.append("【分析说明】")
    report_lines.append("")
    report_lines.append("策略：Top10% → EPS>0.5 → 按预测值选Top50")
    report_lines.append("分析维度：每周50支股票按实际收益率排序，分析不同排名的贡献")
    report_lines.append("")
    report_lines.append("【数据可用性】")
    report_lines.append("- OOF预测数据：2009-2024年（训练集的out-of-fold预测）")
    report_lines.append("- Holdout预测数据：2026年（测试集预测）")
    report_lines.append("- 实际收益数据：仅2024-2026年（weekly_factors文件）")
    report_lines.append("- 因此只能分析：2024年（部分）、2026年")
    report_lines.append("")
    report_lines.append("⚠️ 要分析2009-2023年，需要下载对应年份的weekly_factors数据")
    report_lines.append("⚠️ 2025年缺少预测数据（OOF只到2024年8月）")
    report_lines.append("")
    report_lines.append(f"实际分析年份：{', '.join(str(y) for y in sorted(results_by_year.keys()))}")
    report_lines.append("")
    report_lines.append("=" * 120)
    
    # 汇总表格
    summary_data = []
    
    for year in sorted(results_by_year.keys()):
        df_year = results_by_year[year]
        
        report_lines.append("")
        report_lines.append(f"\n{'=' * 120}")
        report_lines.append(f"{year}年 收益贡献分析")
        report_lines.append("=" * 120)
        report_lines.append("")
        
        # 基本统计
        total_return = df_year['pchg'].mean() * 100
        positive_ratio = (df_year['pchg'] > 0).sum() / len(df_year) * 100
        
        report_lines.append(f"交易周数: {df_year['date'].nunique()}")
        report_lines.append(f"组合平均收益: {total_return:.2f}%")
        report_lines.append(f"正收益股票占比: {positive_ratio:.1f}%")
        report_lines.append("")
        
        # 按排名分组统计
        report_lines.append("【按排名分组统计】")
        report_lines.append("")
        
        groups = [
            ('Top 1-5', 1, 5),
            ('Top 6-10', 6, 10),
            ('Top 11-20', 11, 20),
            ('Top 21-30', 21, 30),
            ('Top 31-40', 31, 40),
            ('Top 41-50', 41, 50),
        ]
        
        report_lines.append(f"{'排名区间':<15} | {'平均收益':<12} | {'正收益占比':<12} | {'对总收益贡献':<15}")
        report_lines.append("-" * 120)
        
        for group_name, start, end in groups:
            group_data = df_year[(df_year['rank'] >= start) & (df_year['rank'] <= end)]
            avg_return = group_data['pchg'].mean() * 100
            positive_pct = (group_data['pchg'] > 0).sum() / len(group_data) * 100 if len(group_data) > 0 else 0
            
            # 计算对总收益的贡献
            group_contribution = (avg_return * (end - start + 1) / 50)
            contribution_pct = (group_contribution / total_return * 100) if total_return != 0 else 0
            
            report_lines.append(
                f"{group_name:<15} | {avg_return:>11.2f}% | {positive_pct:>11.1f}% | {contribution_pct:>14.1f}%"
            )
        
        report_lines.append("")
        
        # 累计贡献分析
        report_lines.append("【累计收益贡献分析】")
        report_lines.append("")
        
        report_lines.append(f"{'Top N':<10} | {'平均收益':<12} | {'累计贡献':<12} | {'对总收益占比':<15}")
        report_lines.append("-" * 120)
        
        cumulative_data = []
        for n in [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]:
            top_n = df_year[df_year['rank'] <= n]
            top_n_return = top_n['pchg'].mean() * 100
            cumulative_contrib = top_n_return * n / 50
            contrib_pct = (cumulative_contrib / total_return * 100) if total_return != 0 else 0
            
            cumulative_data.append((n, top_n_return, cumulative_contrib, contrib_pct))
            
            report_lines.append(
                f"Top {n:<6} | {top_n_return:>11.2f}% | {cumulative_contrib:>11.2f}% | {contrib_pct:>14.1f}%"
            )
        
        report_lines.append("")
        
        # 关键发现
        report_lines.append("【关键发现】")
        report_lines.append("")
        
        top5_return = df_year[df_year['rank'] <= 5]['pchg'].mean() * 100
        top10_return = df_year[df_year['rank'] <= 10]['pchg'].mean() * 100
        top20_return = df_year[df_year['rank'] <= 20]['pchg'].mean() * 100
        top30_return = df_year[df_year['rank'] <= 30]['pchg'].mean() * 100
        
        top20_contrib = (top20_return * 20 / 50) / total_return * 100 if total_return != 0 else 0
        top30_contrib = (top30_return * 30 / 50) / total_return * 100 if total_return != 0 else 0
        
        bottom20_return = df_year[df_year['rank'] > 30]['pchg'].mean() * 100
        
        report_lines.append(f"1. Top 20股票贡献: {top20_contrib:.1f}% 的总收益")
        report_lines.append(f"2. Top 30股票贡献: {top30_contrib:.1f}% 的总收益")
        report_lines.append(f"3. 后20支股票(31-50)平均收益: {bottom20_return:.2f}%")
        
        if bottom20_return < 0:
            report_lines.append(f"   ⚠️ 后20支股票拖后腿，平均负收益 {bottom20_return:.2f}%")
        else:
            report_lines.append(f"   ✅ 后20支股票也有正贡献")
        
        report_lines.append("")
        
        # 收集汇总数据
        summary_data.append({
            'year': year,
            'total_return': total_return,
            'top20_contrib': top20_contrib,
            'top30_contrib': top30_contrib,
            'bottom20_return': bottom20_return,
            'positive_ratio': positive_ratio
        })
    
    # 生成汇总对比表
    report_lines.append("")
    report_lines.append("=" * 120)
    report_lines.append("【历史年份对比汇总】")
    report_lines.append("=" * 120)
    report_lines.append("")
    
    report_lines.append(f"{'年份':<8} | {'组合收益':<12} | {'Top20贡献':<12} | {'Top30贡献':<12} | {'后20支收益':<12} | {'正收益占比':<12}")
    report_lines.append("-" * 120)
    
    for data in summary_data:
        report_lines.append(
            f"{data['year']:<8} | {data['total_return']:>11.2f}% | {data['top20_contrib']:>11.1f}% | "
            f"{data['top30_contrib']:>11.1f}% | {data['bottom20_return']:>11.2f}% | {data['positive_ratio']:>11.1f}%"
        )
    
    report_lines.append("")
    
    # 总结
    report_lines.append("=" * 120)
    report_lines.append("【总体结论】")
    report_lines.append("=" * 120)
    report_lines.append("")
    
    avg_top20_contrib = np.mean([d['top20_contrib'] for d in summary_data])
    avg_top30_contrib = np.mean([d['top30_contrib'] for d in summary_data])
    avg_bottom20_return = np.mean([d['bottom20_return'] for d in summary_data])
    
    report_lines.append(f"1. 历史平均：Top 20股票贡献 {avg_top20_contrib:.1f}% 的总收益")
    report_lines.append(f"2. 历史平均：Top 30股票贡献 {avg_top30_contrib:.1f}% 的总收益")
    report_lines.append(f"3. 历史平均：后20支股票(31-50)平均收益 {avg_bottom20_return:.2f}%")
    report_lines.append("")
    
    if avg_top20_contrib > 80:
        report_lines.append("💡 建议：收益高度集中在Top 20，可以考虑减少持仓至20-30支")
    elif avg_top30_contrib > 80:
        report_lines.append("💡 建议：收益主要集中在Top 30，可以考虑减少持仓至30支左右")
    else:
        report_lines.append("💡 建议：收益相对分散，保持50支持仓有助于分散风险")
    
    report_lines.append("")
    
    if avg_bottom20_return < 0:
        report_lines.append("⚠️ 警告：后20支股票历史上平均拖后腿，建议优化选股策略或减少持仓数量")
    else:
        report_lines.append("✅ 后20支股票历史上也有正贡献，50支持仓策略合理")
    
    report_lines.append("")
    report_lines.append("=" * 120)
    
    report_text = "\n".join(report_lines)
    print("\n" + report_text)
    
    # 保存报告
    report_path = OUTPUT_DIR / 'analysis' / 'historical_contribution_analysis.txt'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    logger.info(f"\n分析报告已保存: {report_path}")
    
    return report_text, summary_data


def main():
    """主函数"""
    try:
        # 加载数据
        df_all = load_all_data()
        
        has_eps = 'eps' in df_all.columns or 'eps_ttm' in df_all.columns
        if 'circulating_market_cap' not in df_all.columns or not has_eps:
            logger.error("数据缺少必要字段")
            return False
        
        # 加载预测
        predictions = load_predictions()
        
        # 按年份分析收益贡献
        logger.info("\n开始按年份分析收益贡献...")
        results_by_year = analyze_return_contribution_by_year(predictions, df_all)
        
        if not results_by_year:
            logger.error("没有有效数据")
            return False
        
        # 保存详细数据
        for year, df_year in results_by_year.items():
            csv_path = OUTPUT_DIR / 'analysis' / f'contribution_details_{year}.csv'
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            df_year.to_csv(csv_path, index=False)
            logger.info(f"{year}年详细数据已保存: {csv_path}")
        
        # 生成报告
        generate_yearly_report(results_by_year)
        
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
