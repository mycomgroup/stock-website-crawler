"""
为2025和2026年的weekly factors数据生成预测分数
使用family_beta方法（与pipeline一致）
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / 'output'
DATA_DIR = BASE_DIR / 'data' / 'weekly_factors'


def load_family_config():
    """加载family配置"""
    with open(OUTPUT_DIR / 'phase2' / 'run_snapshot_phase2.json') as f:
        snap = json.load(f)
    return snap['config']['use_family_map'], snap['family_beta']


def score_weekly_file(filepath, family_map, family_beta):
    """对单个weekly factors文件打分"""
    df = pd.read_csv(filepath)
    df = df.rename(columns={'Unnamed: 0': 'stock_id'})
    df['date'] = pd.to_datetime(df['date'])
    
    # 对每个family内的因子做截面rank，然后加权
    prediction = np.zeros(len(df))
    
    for family_name, factors in family_map.items():
        beta = family_beta.get(family_name, 0)
        if beta == 0:
            continue
        
        # 只用存在的列
        available_factors = [f for f in factors if f in df.columns]
        if not available_factors:
            continue
        
        # 对每个因子做截面rank（0-1之间）
        family_score = np.zeros(len(df))
        for factor in available_factors:
            col = df[factor].fillna(df[factor].median())
            ranked = col.rank(pct=True)
            family_score += ranked.values
        
        family_score /= len(available_factors)  # 平均rank
        prediction += beta * family_score
    
    df['prediction'] = prediction
    return df[['date', 'stock_id', 'prediction', 'pchg', 'eps_ttm', 'circulating_market_cap']]


def generate_predictions_for_years(years):
    """为指定年份生成预测"""
    family_map, family_beta = load_family_config()
    
    all_results = []
    
    files = sorted(os.listdir(DATA_DIR))
    
    for filename in files:
        if not filename.endswith('_all.csv'):
            continue
        
        # 从文件名提取年份
        date_str = filename.replace('factors_', '').replace('_all.csv', '')
        year = int(date_str[:4])
        
        if year not in years:
            continue
        
        filepath = DATA_DIR / filename
        logger.info(f"处理 {filename}...")
        
        try:
            df = score_weekly_file(filepath, family_map, family_beta)
            all_results.append(df)
        except Exception as e:
            logger.warning(f"  跳过 {filename}: {e}")
    
    if all_results:
        combined = pd.concat(all_results, ignore_index=True)
        logger.info(f"生成预测: {len(combined)} 行，年份: {sorted(combined['date'].dt.year.unique())}")
        return combined
    
    return pd.DataFrame()


def run_comparison_with_2025_2026():
    """运行包含2025/2026的完整对比"""
    
    logger.info("=== 生成2025/2026预测 ===")
    
    # 生成2025预测（从weekly factors）
    logger.info("生成2025年预测...")
    df_2025 = generate_predictions_for_years([2025])
    
    # 加载2026 holdout（已有prediction+pchg）
    logger.info("加载2026年holdout数据...")
    holdout_2026 = pd.read_csv(OUTPUT_DIR / 'phase2' / 'predictions_2026_holdout.csv')
    holdout_2026['date'] = pd.to_datetime(holdout_2026['date'])
    
    # 2026需要eps_ttm和circulating_market_cap，从weekly factors获取
    logger.info("加载2026年因子数据...")
    df_2026_factors = generate_predictions_for_years([2026])
    
    # 合并2026的prediction（来自holdout）和因子数据（来自weekly factors）
    if len(df_2026_factors) > 0:
        # 用holdout的prediction替换（更准确）
        df_2026 = df_2026_factors.copy()
        
        # 找最近的holdout日期匹配
        holdout_dates = sorted(holdout_2026['date'].unique())
        factor_dates = sorted(df_2026['date'].unique())
        
        # 建立日期映射
        date_map = {}
        for fd in factor_dates:
            for hd in holdout_dates:
                diff = abs((hd - fd).days)
                if diff <= 7:
                    date_map[fd] = hd
                    break
        
        # 替换prediction
        for factor_date, holdout_date in date_map.items():
            holdout_slice = holdout_2026[holdout_2026['date'] == holdout_date][['stock_id', 'prediction', 'pchg']].copy()
            holdout_slice = holdout_slice.rename(columns={'prediction': 'holdout_pred', 'pchg': 'holdout_pchg'})
            
            mask = df_2026['date'] == factor_date
            df_2026.loc[mask, 'date_matched'] = holdout_date
            
            # 合并
            df_2026_slice = df_2026[mask].merge(holdout_slice, on='stock_id', how='inner')
            df_2026.loc[df_2026['date'] == factor_date, 'prediction'] = np.nan
            
            # 更新prediction和pchg
            for _, row in df_2026_slice.iterrows():
                idx = df_2026[(df_2026['date'] == factor_date) & (df_2026['stock_id'] == row['stock_id'])].index
                if len(idx) > 0:
                    df_2026.loc[idx[0], 'prediction'] = row['holdout_pred']
                    df_2026.loc[idx[0], 'pchg'] = row['holdout_pchg']
        
        df_2026 = df_2026.dropna(subset=['prediction'])
    
    logger.info(f"2025数据: {len(df_2025)} 行")
    logger.info(f"2026数据: {len(df_2026)} 行")
    
    return df_2025, df_2026


def analyze_year(year_data, year_label):
    """分析单年数据"""
    results = []
    
    for date in sorted(year_data['date'].unique()):
        df_date = year_data[year_data['date'] == date]
        
        # 过滤无效数据
        df_date = df_date.dropna(subset=['prediction', 'pchg', 'eps_ttm', 'circulating_market_cap'])
        
        if len(df_date) < 50:
            continue
        
        # 第一阶段：Top10%
        n_stage1 = max(int(len(df_date) * 0.1), 50)
        stage1 = df_date.nlargest(n_stage1, 'prediction')
        
        # 第二阶段：EPS>0.5
        stage2 = stage1[stage1['eps_ttm'] > 0.5]
        
        if len(stage2) < 5:
            continue
        
        # 策略1：原策略 Top 50（按预测值）
        n_top50 = min(50, len(stage2))
        top50_pred = stage2.nlargest(n_top50, 'prediction')
        return_top50 = top50_pred['pchg'].mean() * 100
        
        # 策略2：小市值 Top 5
        n_top5 = min(5, len(stage2))
        top5_smallcap = stage2.nsmallest(n_top5, 'circulating_market_cap')
        return_top5_smallcap = top5_smallcap['pchg'].mean() * 100
        avg_cap_top5 = top5_smallcap['circulating_market_cap'].mean() / 1e8
        
        # 策略3：基准 Top 20（按预测值）
        n_top20 = min(20, len(stage2))
        top20_pred = stage2.nlargest(n_top20, 'prediction')
        return_top20_pred = top20_pred['pchg'].mean() * 100
        
        results.append({
            'date': date,
            'top50_pred': return_top50,
            'top5_smallcap': return_top5_smallcap,
            'top20_pred': return_top20_pred,
            'avg_cap_top5': avg_cap_top5
        })
    
    return pd.DataFrame(results) if results else pd.DataFrame()


def main():
    """主函数"""
    
    # 先运行2010-2024的对比（用OOF预测）
    logger.info("=== 加载2010-2024历史数据 ===")
    
    actual = pd.read_csv(
        BASE_DIR / 'train_merged_all.csv',
        usecols=['Unnamed: 0', 'date', 'pchg', 'eps_ttm', 'circulating_market_cap']
    )
    actual['date'] = pd.to_datetime(actual['date'])
    actual = actual.rename(columns={'Unnamed: 0': 'stock_id'})
    
    oof = pd.read_csv(OUTPUT_DIR / 'phase2' / 'oof_predictions_phase2.csv')
    oof['date'] = pd.to_datetime(oof['date'])
    if 'oof_prediction' in oof.columns:
        oof = oof.rename(columns={'oof_prediction': 'prediction'})
    
    # 匹配
    actual_dates = sorted(actual['date'].unique())
    
    def find_next_date(pred_date):
        for actual_date in actual_dates:
            days_diff = (actual_date - pred_date).days
            if 3 <= days_diff <= 14:
                return actual_date
        return None
    
    oof['match_date'] = oof['date'].apply(find_next_date)
    oof = oof[oof['match_date'].notna()]
    
    merged_hist = oof[['date', 'match_date', 'stock_id', 'prediction']].merge(
        actual[['date', 'stock_id', 'pchg', 'eps_ttm', 'circulating_market_cap']].rename(columns={'date': 'match_date'}),
        on=['match_date', 'stock_id'],
        how='inner'
    )
    merged_hist['year'] = merged_hist['date'].dt.year
    
    # 生成2025/2026预测
    df_2025, df_2026 = run_comparison_with_2025_2026()
    df_2025['year'] = df_2025['date'].dt.year
    df_2026['year'] = df_2026['date'].dt.year
    
    # 分析所有年份
    all_results = {}
    
    for year in range(2010, 2025):
        year_data = merged_hist[merged_hist['year'] == year]
        if len(year_data) > 0:
            result = analyze_year(year_data, str(year))
            if len(result) > 0:
                all_results[year] = result
                logger.info(f"{year}年: {len(result)} 条记录")
    
    # 2025
    if len(df_2025) > 0:
        result_2025 = analyze_year(df_2025, '2025')
        if len(result_2025) > 0:
            all_results[2025] = result_2025
            logger.info(f"2025年: {len(result_2025)} 条记录")
    
    # 2026
    if len(df_2026) > 0:
        result_2026 = analyze_year(df_2026, '2026')
        if len(result_2026) > 0:
            all_results[2026] = result_2026
            logger.info(f"2026年: {len(result_2026)} 条记录")
    
    # 生成报告
    print_full_report(all_results)


def print_full_report(all_results):
    """打印完整报告"""
    
    lines = []
    lines.append("=" * 140)
    lines.append("三策略完整对比（2010-2026）")
    lines.append("=" * 140)
    lines.append("")
    lines.append("策略1（原策略）：Top10% → EPS>0.5 → 按预测值选Top 50")
    lines.append("策略2（小市值）：Top10% → EPS>0.5 → 按市值最小选Top 5")
    lines.append("策略3（基准）  ：Top10% → EPS>0.5 → 按预测值选Top 20")
    lines.append("")
    lines.append("=" * 140)
    lines.append(f"{'年份':<8} | {'原Top50':<12} | {'小市值Top5':<12} | {'基准Top20':<12} | "
                f"{'Top5 vs Top50':<15} | {'Top5 vs Top20':<15}")
    lines.append("-" * 140)
    
    summary = []
    
    for year in sorted(all_results.keys()):
        df = all_results[year]
        
        avg_top50 = df['top50_pred'].mean()
        avg_top5 = df['top5_smallcap'].mean()
        avg_top20 = df['top20_pred'].mean()
        
        annual_top50 = ((1 + avg_top50/100) ** 52 - 1) * 100
        annual_top5 = ((1 + avg_top5/100) ** 52 - 1) * 100
        annual_top20 = ((1 + avg_top20/100) ** 52 - 1) * 100
        
        diff_50 = annual_top5 - annual_top50
        diff_20 = annual_top5 - annual_top20
        
        w50 = "✅" if diff_50 > 0 else "❌"
        w20 = "✅" if diff_20 > 0 else "❌"
        
        lines.append(
            f"{year:<8} | {annual_top50:>11.1f}% | {annual_top5:>11.1f}% | {annual_top20:>11.1f}% | "
            f"{diff_50:>+6.1f}% {w50:<6} | {diff_20:>+6.1f}% {w20:<6}"
        )
        
        summary.append({
            'year': year,
            'top50': annual_top50,
            'top5': annual_top5,
            'top20': annual_top20
        })
    
    lines.append("")
    lines.append("=" * 140)
    lines.append("【汇总】")
    lines.append("=" * 140)
    
    top50_vals = [d['top50'] for d in summary]
    top5_vals = [d['top5'] for d in summary]
    top20_vals = [d['top20'] for d in summary]
    n = len(summary)
    
    lines.append(f"平均年化：原Top50={np.mean(top50_vals):.1f}%  小市值Top5={np.mean(top5_vals):.1f}%  基准Top20={np.mean(top20_vals):.1f}%")
    lines.append(f"中位数：  原Top50={np.median(top50_vals):.1f}%  小市值Top5={np.median(top5_vals):.1f}%  基准Top20={np.median(top20_vals):.1f}%")
    lines.append(f"正收益年份：原Top50={sum(1 for v in top50_vals if v>0)}/{n}  小市值Top5={sum(1 for v in top5_vals if v>0)}/{n}  基准Top20={sum(1 for v in top20_vals if v>0)}/{n}")
    lines.append(f"Top5 vs Top50 胜率：{sum(1 for d in summary if d['top5']>d['top50'])}/{n} ({sum(1 for d in summary if d['top5']>d['top50'])/n*100:.1f}%)")
    lines.append(f"Top5 vs Top20 胜率：{sum(1 for d in summary if d['top5']>d['top20'])}/{n} ({sum(1 for d in summary if d['top5']>d['top20'])/n*100:.1f}%)")
    
    lines.append("")
    lines.append("=" * 140)
    
    report = "\n".join(lines)
    print(report)
    
    # 保存
    path = OUTPUT_DIR / 'analysis' / 'full_comparison_2010_2026.txt'
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(report)
    logger.info(f"报告已保存: {path}")


if __name__ == "__main__":
    import sys
    try:
        main()
        sys.exit(0)
    except Exception as e:
        logger.error(f"失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
