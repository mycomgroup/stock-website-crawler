"""
测试小市值策略在历史数据上的表现

策略：Top10% → EPS>0.5 → 按市值最小选Top N
目标：找出最优的N值，验证策略是否稳定work
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / 'output'


def test_smallcap_strategy():
    """测试小市值策略"""
    
    logger.info("加载数据...")
    
    # 加载实际数据（只加载需要的列以节省内存）
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
    n_values = [5, 10, 15, 20, 25, 30, 40, 50]
    
    results_by_year = {}
    
    for year in sorted(merged['year'].unique()):
        if year < 2010:  # 跳过2009年（数据太少）
            continue
        
        logger.info(f"\n分析 {year} 年...")
        year_data = merged[merged['year'] == year]
        
        year_results = []
        
        for date in sorted(year_data['date'].unique()):
            df_date = year_data[year_data['date'] == date]
            
            # 第一阶段：Top10%
            n_stage1 = max(int(len(df_date) * 0.1), 50)
            stage1 = df_date.nlargest(n_stage1, 'prediction')
            
            # 第二阶段：EPS>0.5
            stage2 = stage1[stage1['eps_ttm'] > 0.5]
            
            if len(stage2) < 5:
                continue
            
            # 第三阶段：按市值最小选Top N
            for n in n_values:
                if len(stage2) < n:
                    continue
                
                top_n = stage2.nsmallest(n, 'circulating_market_cap')
                avg_return = top_n['pchg'].mean() * 100
                avg_cap = top_n['circulating_market_cap'].mean() / 1e8
                
                year_results.append({
                    'date': date,
                    'n_stocks': n,
                    'avg_return': avg_return,
                    'avg_cap': avg_cap
                })
        
        if year_results:
            results_by_year[year] = pd.DataFrame(year_results)
            logger.info(f"  {year}年: {len(year_results)} 条记录")
    
    return results_by_year


def generate_report(results_by_year):
    """生成报告"""
    
    report_lines = []
    report_lines.append("=" * 120)
    report_lines.append("小市值策略历史表现分析")
    report_lines.append("=" * 120)
    report_lines.append("")
    
    report_lines.append("【策略说明】")
    report_lines.append("")
    report_lines.append("策略：Top10% → EPS>0.5 → 按市值最小选Top N")
    report_lines.append("测试：N = 5, 10, 15, 20, 25, 30, 40, 50")
    report_lines.append("目标：找出最优的N值，验证策略稳定性")
    report_lines.append("")
    report_lines.append("=" * 120)
    
    # 按年份汇总
    summary_data = []
    
    for year in sorted(results_by_year.keys()):
        df_year = results_by_year[year]
        
        report_lines.append("")
        report_lines.append(f"\n{'=' * 120}")
        report_lines.append(f"{year}年 各持仓数量表现")
        report_lines.append("=" * 120)
        report_lines.append("")
        
        report_lines.append(f"{'持仓数':<10} | {'周均收益':<12} | {'年化收益':<12} | {'平均市值(亿)':<15}")
        report_lines.append("-" * 120)
        
        year_summary = {'year': year}
        
        for n in sorted(df_year['n_stocks'].unique()):
            data = df_year[df_year['n_stocks'] == n]
            avg_weekly = data['avg_return'].mean()
            annual = ((1 + avg_weekly/100) ** 52 - 1) * 100
            avg_cap = data['avg_cap'].mean()
            
            report_lines.append(f"Top {n:<6} | {avg_weekly:>11.2f}% | {annual:>11.2f}% | {avg_cap:>14.1f}")
            
            year_summary[f'Top{n}'] = annual
        
        summary_data.append(year_summary)
        report_lines.append("")
    
    # 生成汇总表
    report_lines.append("")
    report_lines.append("=" * 120)
    report_lines.append("【历史年份汇总 - 年化收益】")
    report_lines.append("=" * 120)
    report_lines.append("")
    
    # 表头
    n_values = [5, 10, 15, 20, 25, 30, 40, 50]
    header = f"{'年份':<8}"
    for n in n_values:
        header += f" | {'Top'+str(n):<10}"
    report_lines.append(header)
    report_lines.append("-" * 120)
    
    # 数据行
    for data in summary_data:
        year = data['year']
        line = f"{year:<8}"
        for n in n_values:
            value = data.get(f'Top{n}', 0)
            line += f" | {value:>9.1f}%"
        report_lines.append(line)
    
    report_lines.append("")
    
    # 计算平均值
    report_lines.append("=" * 120)
    report_lines.append("【平均年化收益】")
    report_lines.append("=" * 120)
    report_lines.append("")
    
    avg_line = f"{'平均':<8}"
    best_n = None
    best_avg = -999
    
    for n in n_values:
        values = [d.get(f'Top{n}', 0) for d in summary_data if f'Top{n}' in d]
        if values:
            avg = np.mean(values)
            avg_line += f" | {avg:>9.1f}%"
            
            if avg > best_avg:
                best_avg = avg
                best_n = n
        else:
            avg_line += f" | {'N/A':>9}"
    
    report_lines.append(avg_line)
    report_lines.append("")
    
    # 关键结论
    report_lines.append("=" * 120)
    report_lines.append("【关键结论】")
    report_lines.append("=" * 120)
    report_lines.append("")
    
    report_lines.append(f"1. 最优持仓数量: Top {best_n}")
    report_lines.append(f"2. 平均年化收益: {best_avg:.1f}%")
    report_lines.append("")
    
    # 稳定性分析
    report_lines.append("3. 策略稳定性分析:")
    report_lines.append("")
    
    for n in n_values:
        values = [d.get(f'Top{n}', 0) for d in summary_data if f'Top{n}' in d]
        if values:
            avg = np.mean(values)
            std = np.std(values)
            positive_years = sum(1 for v in values if v > 0)
            total_years = len(values)
            
            report_lines.append(f"   Top {n:2d}: 平均{avg:>6.1f}%, 标准差{std:>6.1f}%, 正收益年份{positive_years}/{total_years}")
    
    report_lines.append("")
    
    # 建议
    report_lines.append("=" * 120)
    report_lines.append("【策略建议】")
    report_lines.append("=" * 120)
    report_lines.append("")
    
    # 找出前3名
    n_performance = []
    for n in n_values:
        values = [d.get(f'Top{n}', 0) for d in summary_data if f'Top{n}' in d]
        if values:
            avg = np.mean(values)
            n_performance.append((n, avg))
    
    n_performance.sort(key=lambda x: x[1], reverse=True)
    
    report_lines.append("表现最好的3个持仓数量:")
    for i, (n, avg) in enumerate(n_performance[:3], 1):
        report_lines.append(f"{i}. Top {n}: 平均年化{avg:.1f}%")
    
    report_lines.append("")
    
    if best_n <= 20:
        report_lines.append(f"✅ 建议采用 Top {best_n} 策略")
        report_lines.append(f"   理由：历史平均年化收益最高（{best_avg:.1f}%）")
    else:
        report_lines.append(f"⚠️ 最优持仓数量为 Top {best_n}，但建议考虑 Top 20")
        report_lines.append(f"   理由：持仓过多可能降低小市值溢价效果")
    
    report_lines.append("")
    report_lines.append("=" * 120)
    
    report_text = "\n".join(report_lines)
    print("\n" + report_text)
    
    # 保存报告
    report_path = OUTPUT_DIR / 'analysis' / 'smallcap_strategy_history.txt'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    logger.info(f"\n报告已保存: {report_path}")


def main():
    """主函数"""
    try:
        results = test_smallcap_strategy()
        generate_report(results)
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
