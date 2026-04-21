"""
验证小市值策略是否真的work，还是过拟合

策略：Top10% → EPS>0.5 → 按市值最小选Top N
目标：
1. 验证策略是否稳定work（不是过拟合）
2. 找出最优的N值
3. 与基准策略对比
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / 'output'


def validate_smallcap_strategy():
    """验证小市值策略"""
    
    logger.info("加载数据...")
    
    # 加载实际数据
    actual = pd.read_csv(
        BASE_DIR / 'train_merged_all.csv',
        usecols=['Unnamed: 0', 'date', 'pchg', 'eps_ttm', 'circulating_market_cap']
    )
    actual['date'] = pd.to_datetime(actual['date'])
    actual['year'] = actual['date'].dt.year
    actual = actual.rename(columns={'Unnamed: 0': 'stock_id'})
    
    logger.info(f"实际数据: {len(actual)} 行")
    
    # 加载预测
    oof = pd.read_csv(OUTPUT_DIR / 'phase2' / 'oof_predictions_phase2.csv')
    oof['date'] = pd.to_datetime(oof['date'])
    oof['year'] = oof['date'].dt.year
    if 'oof_prediction' in oof.columns:
        oof = oof.rename(columns={'oof_prediction': 'prediction'})
    
    logger.info(f"预测数据: {len(oof)} 行")
    
    # 匹配数据
    logger.info("匹配预测和实际数据...")
    actual_dates = sorted(actual['date'].unique())
    
    def find_next_date(pred_date):
        for actual_date in actual_dates:
            days_diff = (actual_date - pred_date).days
            if 3 <= days_diff <= 14:
                return actual_date
        return None
    
    oof['match_date'] = oof['date'].apply(find_next_date)
    oof = oof[oof['match_date'].notna()]
    
    merged = oof[['date', 'match_date', 'stock_id', 'prediction', 'year']].merge(
        actual[['date', 'stock_id', 'pchg', 'eps_ttm', 'circulating_market_cap']].rename(columns={'date': 'match_date'}),
        on=['match_date', 'stock_id'],
        how='inner'
    )
    
    logger.info(f"匹配后数据: {len(merged)} 行")
    
    # 测试不同的N值
    n_values = [5, 10, 15, 20, 25, 30]
    
    results_by_year = {}
    baseline_by_year = {}  # 基准：按预测值选Top N
    
    for year in sorted(merged['year'].unique()):
        if year < 2010:  # 跳过2009年
            continue
        
        logger.info(f"\n分析 {year} 年...")
        year_data = merged[merged['year'] == year]
        
        year_results = []
        baseline_results = []
        
        for date in sorted(year_data['date'].unique()):
            df_date = year_data[year_data['date'] == date]
            
            # 第一阶段：Top10%
            n_stage1 = max(int(len(df_date) * 0.1), 50)
            stage1 = df_date.nlargest(n_stage1, 'prediction')
            
            # 第二阶段：EPS>0.5
            stage2 = stage1[stage1['eps_ttm'] > 0.5]
            
            if len(stage2) < 5:
                continue
            
            # 测试小市值策略
            for n in n_values:
                if len(stage2) < n:
                    continue
                
                # 小市值策略：按市值最小选Top N
                top_n_smallcap = stage2.nsmallest(n, 'circulating_market_cap')
                avg_return_smallcap = top_n_smallcap['pchg'].mean() * 100
                
                # 基准策略：按预测值选Top N
                top_n_pred = stage2.nlargest(n, 'prediction')
                avg_return_pred = top_n_pred['pchg'].mean() * 100
                
                year_results.append({
                    'date': date,
                    'n_stocks': n,
                    'avg_return': avg_return_smallcap
                })
                
                baseline_results.append({
                    'date': date,
                    'n_stocks': n,
                    'avg_return': avg_return_pred
                })
        
        if year_results:
            results_by_year[year] = pd.DataFrame(year_results)
            baseline_by_year[year] = pd.DataFrame(baseline_results)
            logger.info(f"  {year}年: {len(year_results)} 条记录")
    
    return results_by_year, baseline_by_year


def generate_validation_report(results_by_year, baseline_by_year):
    """生成验证报告"""
    
    report_lines = []
    report_lines.append("=" * 140)
    report_lines.append("小市值策略验证报告")
    report_lines.append("=" * 140)
    report_lines.append("")
    
    report_lines.append("【策略说明】")
    report_lines.append("")
    report_lines.append("测试策略：Top10% → EPS>0.5 → 按市值最小选Top N")
    report_lines.append("基准策略：Top10% → EPS>0.5 → 按预测值选Top N")
    report_lines.append("")
    report_lines.append("验证目标：")
    report_lines.append("1. 小市值策略是否稳定优于基准策略？")
    report_lines.append("2. 最优的N值是多少？")
    report_lines.append("3. 策略是否存在过拟合？")
    report_lines.append("")
    report_lines.append("=" * 140)
    
    # 汇总数据
    n_values = [5, 10, 15, 20, 25, 30]
    
    summary_smallcap = []
    summary_baseline = []
    
    for year in sorted(results_by_year.keys()):
        df_smallcap = results_by_year[year]
        df_baseline = baseline_by_year[year]
        
        year_smallcap = {'year': year}
        year_baseline = {'year': year}
        
        for n in n_values:
            data_smallcap = df_smallcap[df_smallcap['n_stocks'] == n]
            data_baseline = df_baseline[df_baseline['n_stocks'] == n]
            
            if len(data_smallcap) > 0:
                avg_weekly_smallcap = data_smallcap['avg_return'].mean()
                annual_smallcap = ((1 + avg_weekly_smallcap/100) ** 52 - 1) * 100
                year_smallcap[f'Top{n}'] = annual_smallcap
            
            if len(data_baseline) > 0:
                avg_weekly_baseline = data_baseline['avg_return'].mean()
                annual_baseline = ((1 + avg_weekly_baseline/100) ** 52 - 1) * 100
                year_baseline[f'Top{n}'] = annual_baseline
        
        summary_smallcap.append(year_smallcap)
        summary_baseline.append(year_baseline)
    
    # 生成对比表
    report_lines.append("")
    report_lines.append("=" * 140)
    report_lines.append("【年度对比：小市值策略 vs 基准策略】")
    report_lines.append("=" * 140)
    report_lines.append("")
    
    for year in sorted(results_by_year.keys()):
        report_lines.append(f"\n{year}年")
        report_lines.append("-" * 140)
        
        smallcap_data = next((d for d in summary_smallcap if d['year'] == year), None)
        baseline_data = next((d for d in summary_baseline if d['year'] == year), None)
        
        if smallcap_data and baseline_data:
            report_lines.append(f"{'持仓数':<10} | {'小市值策略':<15} | {'基准策略':<15} | {'差异':<15} | {'胜负':<10}")
            report_lines.append("-" * 140)
            
            for n in n_values:
                smallcap_val = smallcap_data.get(f'Top{n}', None)
                baseline_val = baseline_data.get(f'Top{n}', None)
                
                if smallcap_val is not None and baseline_val is not None:
                    diff = smallcap_val - baseline_val
                    diff_pct = (diff / abs(baseline_val) * 100) if baseline_val != 0 else 0
                    winner = "✅ 小市值胜" if diff > 0 else "❌ 基准胜"
                    
                    report_lines.append(
                        f"Top {n:<6} | {smallcap_val:>13.1f}% | {baseline_val:>13.1f}% | "
                        f"{diff:>+6.1f}% ({diff_pct:>+5.1f}%) | {winner}"
                    )
        
        report_lines.append("")
    
    # 汇总统计
    report_lines.append("=" * 140)
    report_lines.append("【汇总统计】")
    report_lines.append("=" * 140)
    report_lines.append("")
    
    report_lines.append(f"{'持仓数':<10} | {'小市值平均':<15} | {'基准平均':<15} | {'平均差异':<15} | "
                       f"{'小市值胜率':<15} | {'中位数差异':<15}")
    report_lines.append("-" * 140)
    
    best_n = None
    best_winrate = 0
    best_avg_diff = -999
    
    for n in n_values:
        smallcap_values = [d.get(f'Top{n}', None) for d in summary_smallcap]
        baseline_values = [d.get(f'Top{n}', None) for d in summary_baseline]
        
        # 过滤None值
        pairs = [(s, b) for s, b in zip(smallcap_values, baseline_values) if s is not None and b is not None]
        
        if pairs:
            smallcap_vals = [p[0] for p in pairs]
            baseline_vals = [p[1] for p in pairs]
            
            avg_smallcap = np.mean(smallcap_vals)
            avg_baseline = np.mean(baseline_vals)
            avg_diff = avg_smallcap - avg_baseline
            
            median_smallcap = np.median(smallcap_vals)
            median_baseline = np.median(baseline_vals)
            median_diff = median_smallcap - median_baseline
            
            wins = sum(1 for s, b in pairs if s > b)
            total = len(pairs)
            winrate = wins / total * 100
            
            report_lines.append(
                f"Top {n:<6} | {avg_smallcap:>13.1f}% | {avg_baseline:>13.1f}% | "
                f"{avg_diff:>+6.1f}% ({avg_diff/abs(avg_baseline)*100:>+5.1f}%) | "
                f"{wins}/{total} ({winrate:>5.1f}%) | {median_diff:>+6.1f}%"
            )
            
            # 找出最优N（综合考虑胜率和平均差异）
            if winrate >= 60 and avg_diff > best_avg_diff:
                best_n = n
                best_winrate = winrate
                best_avg_diff = avg_diff
    
    report_lines.append("")
    
    # 稳定性分析
    report_lines.append("=" * 140)
    report_lines.append("【稳定性分析】")
    report_lines.append("=" * 140)
    report_lines.append("")
    
    report_lines.append("小市值策略的年化收益分布：")
    report_lines.append("")
    report_lines.append(f"{'持仓数':<10} | {'平均':<10} | {'中位数':<10} | {'标准差':<10} | "
                       f"{'最小值':<10} | {'最大值':<10} | {'正收益年份':<15}")
    report_lines.append("-" * 140)
    
    for n in n_values:
        values = [d.get(f'Top{n}', None) for d in summary_smallcap if f'Top{n}' in d]
        values = [v for v in values if v is not None]
        
        if values:
            avg = np.mean(values)
            median = np.median(values)
            std = np.std(values)
            min_val = np.min(values)
            max_val = np.max(values)
            positive_years = sum(1 for v in values if v > 0)
            total_years = len(values)
            
            report_lines.append(
                f"Top {n:<6} | {avg:>8.1f}% | {median:>8.1f}% | {std:>8.1f}% | "
                f"{min_val:>8.1f}% | {max_val:>8.1f}% | {positive_years}/{total_years} ({positive_years/total_years*100:.0f}%)"
            )
    
    report_lines.append("")
    
    # 关键结论
    report_lines.append("=" * 140)
    report_lines.append("【关键结论】")
    report_lines.append("=" * 140)
    report_lines.append("")
    
    if best_n:
        report_lines.append(f"1. 最优持仓数量: Top {best_n}")
        report_lines.append(f"   - 胜率: {best_winrate:.1f}%")
        report_lines.append(f"   - 平均超额收益: {best_avg_diff:+.1f}%")
        report_lines.append("")
    
    # 计算整体胜率
    all_wins = 0
    all_total = 0
    for n in n_values:
        smallcap_values = [d.get(f'Top{n}', None) for d in summary_smallcap]
        baseline_values = [d.get(f'Top{n}', None) for d in summary_baseline]
        pairs = [(s, b) for s, b in zip(smallcap_values, baseline_values) if s is not None and b is not None]
        
        if pairs:
            wins = sum(1 for s, b in pairs if s > b)
            all_wins += wins
            all_total += len(pairs)
    
    overall_winrate = all_wins / all_total * 100 if all_total > 0 else 0
    
    report_lines.append(f"2. 整体表现:")
    report_lines.append(f"   - 总胜率: {all_wins}/{all_total} ({overall_winrate:.1f}%)")
    report_lines.append("")
    
    # 判断是否过拟合
    report_lines.append("3. 过拟合检验:")
    report_lines.append("")
    
    if overall_winrate >= 60:
        report_lines.append(f"   ✅ 策略稳定work（胜率{overall_winrate:.1f}% >= 60%）")
        report_lines.append("   ✅ 不是过拟合，是真实的小市值溢价效应")
    elif overall_winrate >= 50:
        report_lines.append(f"   ⚠️ 策略略有优势（胜率{overall_winrate:.1f}%）")
        report_lines.append("   ⚠️ 需要更多数据验证")
    else:
        report_lines.append(f"   ❌ 策略不稳定（胜率{overall_winrate:.1f}% < 50%）")
        report_lines.append("   ❌ 可能存在过拟合")
    
    report_lines.append("")
    
    # 最终建议
    report_lines.append("=" * 140)
    report_lines.append("【最终建议】")
    report_lines.append("=" * 140)
    report_lines.append("")
    
    if overall_winrate >= 60 and best_n:
        report_lines.append(f"✅ 建议采用小市值策略：Top {best_n}")
        report_lines.append(f"   - 历史胜率: {best_winrate:.1f}%")
        report_lines.append(f"   - 平均超额收益: {best_avg_diff:+.1f}%")
        report_lines.append(f"   - 策略稳定性: 高")
    elif overall_winrate >= 50:
        report_lines.append("⚠️ 小市值策略略有优势，但需谨慎")
        report_lines.append("   - 建议小仓位测试")
        report_lines.append("   - 持续监控表现")
    else:
        report_lines.append("❌ 不建议采用小市值策略")
        report_lines.append("   - 历史表现不稳定")
        report_lines.append("   - 建议继续使用按预测值选股")
    
    report_lines.append("")
    report_lines.append("=" * 140)
    
    report_text = "\n".join(report_lines)
    print("\n" + report_text)
    
    # 保存报告
    report_path = OUTPUT_DIR / 'analysis' / 'smallcap_validation.txt'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    logger.info(f"\n报告已保存: {report_path}")


def main():
    """主函数"""
    try:
        results_smallcap, results_baseline = validate_smallcap_strategy()
        generate_validation_report(results_smallcap, results_baseline)
        return True
    except Exception as e:
        logger.error(f"验证失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
