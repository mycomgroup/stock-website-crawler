"""
分析50支股票的收益贡献分布

目标：
1. 分析每支股票对组合收益的贡献
2. 找出主要贡献收益的股票数量
3. 分析收益分布特征
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import matplotlib.pyplot as plt

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


def analyze_return_contribution(predictions, actual_data, pred_col='prediction'):
    """
    分析最优策略的收益贡献
    
    策略：Top10% → EPS>0.5 → 按预测值选Top50
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
    
    # 按日期分析
    all_stocks_returns = []
    
    for date in sorted(merged['date'].unique()):
        df_date = merged[merged['date'] == date]
        
        # 第一阶段：Top10%
        n_stage1 = max(int(len(df_date) * 0.1), 50)
        stage1_pool = df_date.nlargest(n_stage1, pred_col)
        
        # 第二阶段：EPS>0.5
        stage2_pool = stage1_pool[stage1_pool['eps'] > 0.5]
        
        # 第三阶段：按预测值选Top50（如果不足50支，则全选）
        if len(stage2_pool) < 50:
            final_pool = stage2_pool.nlargest(len(stage2_pool), pred_col)
        else:
            final_pool = stage2_pool.nlargest(50, pred_col)
        
        # 按收益率排序
        final_pool = final_pool.sort_values('pchg', ascending=False)
        final_pool['rank'] = range(1, len(final_pool) + 1)
        final_pool['date'] = date
        
        all_stocks_returns.append(final_pool[['date', 'stock_id', 'rank', 'pchg', pred_col]])
    
    df_all = pd.concat(all_stocks_returns, ignore_index=True)
    
    return df_all


def generate_contribution_report(df_all):
    """生成收益贡献分析报告"""
    
    logger.info("\n" + "=" * 100)
    logger.info("50支股票收益贡献分析")
    logger.info("=" * 100)
    
    report_lines = []
    report_lines.append("=" * 100)
    report_lines.append("50支股票收益贡献分析")
    report_lines.append("=" * 100)
    report_lines.append("")
    
    report_lines.append("【分析说明】")
    report_lines.append("")
    report_lines.append("策略：Top10% → EPS>0.5 → 按预测值选Top50")
    report_lines.append("分析维度：每周50支股票按实际收益率排序，分析不同排名的贡献")
    report_lines.append("")
    
    # 按排名分组统计
    report_lines.append("【按排名分组统计】")
    report_lines.append("")
    
    # 定义分组
    groups = [
        ('Top 5', 1, 5),
        ('Top 6-10', 6, 10),
        ('Top 11-20', 11, 20),
        ('Top 21-30', 21, 30),
        ('Top 31-40', 31, 40),
        ('Top 41-50', 41, 50),
    ]
    
    report_lines.append(f"{'排名区间':<15} | {'平均收益':<12} | {'正收益占比':<12} | {'累计贡献':<12}")
    report_lines.append("-" * 100)
    
    cumulative_return = 0
    for group_name, start, end in groups:
        group_data = df_all[(df_all['rank'] >= start) & (df_all['rank'] <= end)]
        avg_return = group_data['pchg'].mean() * 100
        positive_ratio = (group_data['pchg'] > 0).sum() / len(group_data) * 100
        cumulative_return += avg_return * (end - start + 1) / 50
        
        report_lines.append(
            f"{group_name:<15} | {avg_return:>11.2f}% | {positive_ratio:>11.1f}% | {cumulative_return:>11.2f}%"
        )
    
    report_lines.append("")
    
    # 累计贡献分析
    report_lines.append("【累计收益贡献分析】")
    report_lines.append("")
    
    total_return = df_all['pchg'].mean() * 100
    
    cumulative_contributions = []
    for n in [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]:
        top_n = df_all[df_all['rank'] <= n]
        top_n_return = top_n['pchg'].mean() * 100
        contribution_pct = (top_n_return * n / 50) / total_return * 100 if total_return != 0 else 0
        cumulative_contributions.append((n, top_n_return, contribution_pct))
    
    report_lines.append(f"{'Top N':<10} | {'平均收益':<12} | {'对总收益贡献':<15}")
    report_lines.append("-" * 100)
    
    for n, avg_ret, contrib in cumulative_contributions:
        report_lines.append(f"Top {n:<6} | {avg_ret:>11.2f}% | {contrib:>14.1f}%")
    
    report_lines.append("")
    
    # 关键发现
    report_lines.append("【关键发现】")
    report_lines.append("")
    
    # 找出主要贡献者
    top5_return = df_all[df_all['rank'] <= 5]['pchg'].mean() * 100
    top10_return = df_all[df_all['rank'] <= 10]['pchg'].mean() * 100
    top20_return = df_all[df_all['rank'] <= 20]['pchg'].mean() * 100
    
    top5_contrib = (top5_return * 5 / 50) / total_return * 100 if total_return != 0 else 0
    top10_contrib = (top10_return * 10 / 50) / total_return * 100 if total_return != 0 else 0
    top20_contrib = (top20_return * 20 / 50) / total_return * 100 if total_return != 0 else 0
    
    report_lines.append(f"1. 组合总平均收益: {total_return:.2f}%")
    report_lines.append("")
    
    report_lines.append(f"2. Top 5股票（10%持仓）:")
    report_lines.append(f"   平均收益: {top5_return:.2f}%")
    report_lines.append(f"   贡献总收益的: {top5_contrib:.1f}%")
    report_lines.append("")
    
    report_lines.append(f"3. Top 10股票（20%持仓）:")
    report_lines.append(f"   平均收益: {top10_return:.2f}%")
    report_lines.append(f"   贡献总收益的: {top10_contrib:.1f}%")
    report_lines.append("")
    
    report_lines.append(f"4. Top 20股票（40%持仓）:")
    report_lines.append(f"   平均收益: {top20_return:.2f}%")
    report_lines.append(f"   贡献总收益的: {top20_contrib:.1f}%")
    report_lines.append("")
    
    # 收益分布特征
    positive_stocks = (df_all['pchg'] > 0).sum()
    total_stocks = len(df_all)
    positive_ratio = positive_stocks / total_stocks * 100
    
    report_lines.append("5. 收益分布特征:")
    report_lines.append(f"   正收益股票占比: {positive_ratio:.1f}%")
    report_lines.append(f"   平均正收益: {df_all[df_all['pchg'] > 0]['pchg'].mean() * 100:.2f}%")
    report_lines.append(f"   平均负收益: {df_all[df_all['pchg'] < 0]['pchg'].mean() * 100:.2f}%")
    report_lines.append("")
    
    # 收益集中度
    if top20_contrib > 80:
        report_lines.append("6. 收益集中度分析:")
        report_lines.append(f"   ⚠️ 收益高度集中：Top 20股票贡献{top20_contrib:.1f}%的收益")
        report_lines.append("   建议：可以考虑减少持仓至20-30支")
    elif top20_contrib > 60:
        report_lines.append("6. 收益集中度分析:")
        report_lines.append(f"   ✅ 收益适度集中：Top 20股票贡献{top20_contrib:.1f}%的收益")
        report_lines.append("   建议：当前50支持仓合理")
    else:
        report_lines.append("6. 收益集中度分析:")
        report_lines.append(f"   ✅ 收益分散：Top 20股票贡献{top20_contrib:.1f}%的收益")
        report_lines.append("   建议：当前50支持仓有助于分散风险")
    
    report_lines.append("")
    report_lines.append("=" * 100)
    
    report_text = "\n".join(report_lines)
    print("\n" + report_text)
    
    # 保存报告
    report_path = OUTPUT_DIR / 'analysis' / 'return_contribution_analysis.txt'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    logger.info(f"\n分析报告已保存: {report_path}")
    
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
        
        # 分析收益贡献
        logger.info("\n开始分析收益贡献...")
        df_all = analyze_return_contribution(phase2_pred, df_2026, pred_col='prediction')
        
        if len(df_all) == 0:
            logger.error("没有有效数据")
            return False
        
        logger.info(f"分析了 {df_all['date'].nunique()} 个交易日，共 {len(df_all)} 条记录")
        
        # 保存详细数据
        csv_path = OUTPUT_DIR / 'analysis' / 'return_contribution_details.csv'
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        df_all.to_csv(csv_path, index=False)
        logger.info(f"详细数据已保存: {csv_path}")
        
        # 生成报告
        generate_contribution_report(df_all)
        
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
