"""
对比四个策略：
1. 原策略：Top10% → EPS>0.5 → 按预测值选Top 50
2. 小市值策略：Top10% → EPS>0.5 → 按市值最小选Top 5
3. 基准策略：Top10% → EPS>0.5 → 按预测值选Top 20
4. 中期大涨策略：Top10% → EPS>0.5 → 按预测值选Top 50 → 筛选中期大涨过的股票

回答用户的问题：
1. 按小市值排 vs 按打分排，哪个是因子有效？
2. 小市值的好处是不用取50支了？可以5支？
3. 对比原来的50支和小市值Top 5
4. 从Top 50中筛选最近中期大涨过的股票效果如何？
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / 'output'


def compare_strategies():
    """对比四个策略"""
    
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
    
    # 计算历史涨幅数据用于中期大涨筛选
    logger.info("计算历史涨幅数据...")
    actual_sorted = actual.sort_values(['stock_id', 'date'])
    
    # 计算过去20天和过去40天的累计涨幅
    def calculate_historical_returns(group):
        group = group.sort_values('date')
        group['pchg_20d'] = group['pchg'].rolling(window=20, min_periods=10).sum()  # 过去20天累计涨幅
        group['pchg_40d'] = group['pchg'].rolling(window=40, min_periods=20).sum()  # 过去40天累计涨幅
        group['pchg_2d'] = group['pchg'].rolling(window=2, min_periods=1).sum()    # 过去2天累计涨幅
        return group
    
    actual_with_hist = actual_sorted.groupby('stock_id').apply(calculate_historical_returns).reset_index(drop=True)
    
    # 将历史涨幅数据合并到主数据
    merged = merged.merge(
        actual_with_hist[['date', 'stock_id', 'pchg_20d', 'pchg_40d', 'pchg_2d']].rename(columns={'date': 'match_date'}),
        on=['match_date', 'stock_id'],
        how='left'
    )
    
    logger.info(f"合并历史涨幅后数据: {len(merged)} 行")
    
    # 对比四个策略
    results_by_year = {}
    
    for year in sorted(merged['year'].unique()):
        if year < 2010:  # 跳过2009年
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
            
            # 策略4：中期大涨策略
            # 从Top 50中筛选：过去20-40天有大涨（>15%），但最近2天涨幅不超过8%
            top50_with_hist = top50_pred.dropna(subset=['pchg_20d', 'pchg_40d', 'pchg_2d'])
            
            if len(top50_with_hist) > 0:
                # 筛选条件：
                # 1. 过去20天累计涨幅 > 15% 或 过去40天累计涨幅 > 25%（中期大涨过）
                # 2. 最近2天涨幅 <= 8%（排除刚刚大涨的）
                mid_term_surge = top50_with_hist[
                    ((top50_with_hist['pchg_20d'] > 15) | (top50_with_hist['pchg_40d'] > 25)) &
                    (top50_with_hist['pchg_2d'] <= 8)
                ]
                
                if len(mid_term_surge) >= 3:  # 至少3支股票
                    # 从符合条件的股票中选择预测值最高的5-10支
                    n_surge = min(max(5, len(mid_term_surge) // 2), 10)
                    selected_surge = mid_term_surge.nlargest(n_surge, 'prediction')
                    return_surge = selected_surge['pchg'].mean() * 100
                    count_surge = len(selected_surge)
                    avg_20d_surge = selected_surge['pchg_20d'].mean()
                    avg_2d_surge = selected_surge['pchg_2d'].mean()
                else:
                    # 如果符合条件的股票太少，则选择Top 5
                    return_surge = top50_pred.head(5)['pchg'].mean() * 100
                    count_surge = 5
                    avg_20d_surge = 0
                    avg_2d_surge = 0
            else:
                return_surge = return_top50
                count_surge = n_top50
                avg_20d_surge = 0
                avg_2d_surge = 0
            
            year_results.append({
                'date': date,
                'top50_pred': return_top50,
                'top5_smallcap': return_top5_smallcap,
                'top20_pred': return_top20_pred,
                'surge_strategy': return_surge,
                'avg_cap_top5': avg_cap_top5,
                'surge_count': count_surge,
                'surge_avg_20d': avg_20d_surge,
                'surge_avg_2d': avg_2d_surge
            })
        
        if year_results:
            results_by_year[year] = pd.DataFrame(year_results)
            logger.info(f"  {year}年: {len(year_results)} 条记录")
    
    return results_by_year


def generate_comparison_report(results_by_year):
    """生成对比报告"""
    
    report_lines = []
    report_lines.append("=" * 160)
    report_lines.append("四策略对比：原Top50 vs 小市值Top5 vs 基准Top20 vs 中期大涨策略")
    report_lines.append("=" * 160)
    report_lines.append("")
    
    report_lines.append("【策略说明】")
    report_lines.append("")
    report_lines.append("策略1（原策略）  ：Top10% → EPS>0.5 → 按预测值选Top 50")
    report_lines.append("策略2（小市值）  ：Top10% → EPS>0.5 → 按市值最小选Top 5")
    report_lines.append("策略3（基准）    ：Top10% → EPS>0.5 → 按预测值选Top 20")
    report_lines.append("策略4（中期大涨）：Top10% → EPS>0.5 → 按预测值选Top 50 → 筛选中期大涨股票")
    report_lines.append("")
    report_lines.append("中期大涨筛选条件：")
    report_lines.append("- 过去20天累计涨幅 > 15% 或 过去40天累计涨幅 > 25%（证明有中期上涨动能）")
    report_lines.append("- 最近2天涨幅 <= 8%（排除刚刚大涨的，避免追高）")
    report_lines.append("- 从符合条件的股票中选择预测值最高的5-10支")
    report_lines.append("")
    report_lines.append("=" * 160)
    
    # 汇总数据
    summary_data = []
    
    for year in sorted(results_by_year.keys()):
        df_year = results_by_year[year]
        
        # 计算年化收益
        avg_weekly_top50 = df_year['top50_pred'].mean()
        avg_weekly_top5 = df_year['top5_smallcap'].mean()
        avg_weekly_top20 = df_year['top20_pred'].mean()
        avg_weekly_surge = df_year['surge_strategy'].mean()
        
        annual_top50 = ((1 + avg_weekly_top50/100) ** 52 - 1) * 100
        annual_top5 = ((1 + avg_weekly_top5/100) ** 52 - 1) * 100
        annual_top20 = ((1 + avg_weekly_top20/100) ** 52 - 1) * 100
        annual_surge = ((1 + avg_weekly_surge/100) ** 52 - 1) * 100
        
        avg_cap = df_year['avg_cap_top5'].mean()
        avg_surge_count = df_year['surge_count'].mean()
        avg_surge_20d = df_year['surge_avg_20d'].mean()
        
        summary_data.append({
            'year': year,
            'top50_pred': annual_top50,
            'top5_smallcap': annual_top5,
            'top20_pred': annual_top20,
            'surge_strategy': annual_surge,
            'avg_cap': avg_cap,
            'surge_count': avg_surge_count,
            'surge_20d': avg_surge_20d
        })
    
    # 生成年度对比表
    report_lines.append("")
    report_lines.append("=" * 160)
    report_lines.append("【历史年度对比 - 年化收益】")
    report_lines.append("=" * 160)
    report_lines.append("")
    
    report_lines.append(f"{'年份':<8} | {'原Top50':<12} | {'小市值Top5':<12} | {'基准Top20':<12} | {'中期大涨':<12} | "
                       f"{'大涨 vs Top50':<15} | {'大涨 vs 小市值':<15} | {'平均持仓数':<10}")
    report_lines.append("-" * 160)
    
    for data in summary_data:
        year = data['year']
        top50 = data['top50_pred']
        top5 = data['top5_smallcap']
        top20 = data['top20_pred']
        surge = data['surge_strategy']
        count = data['surge_count']
        
        diff_50 = surge - top50
        diff_5 = surge - top5
        
        winner_50 = "✅" if diff_50 > 0 else "❌"
        winner_5 = "✅" if diff_5 > 0 else "❌"
        
        report_lines.append(
            f"{year:<8} | {top50:>11.1f}% | {top5:>11.1f}% | {top20:>11.1f}% | {surge:>11.1f}% | "
            f"{diff_50:>+6.1f}% {winner_50:<6} | {diff_5:>+6.1f}% {winner_5:<6} | {count:>9.1f}"
        )
    
    report_lines.append("")
    
    # 汇总统计
    report_lines.append("=" * 160)
    report_lines.append("【汇总统计】")
    report_lines.append("=" * 160)
    report_lines.append("")
    
    top50_values = [d['top50_pred'] for d in summary_data]
    top5_values = [d['top5_smallcap'] for d in summary_data]
    top20_values = [d['top20_pred'] for d in summary_data]
    surge_values = [d['surge_strategy'] for d in summary_data]
    
    avg_top50 = np.mean(top50_values)
    avg_top5 = np.mean(top5_values)
    avg_top20 = np.mean(top20_values)
    avg_surge = np.mean(surge_values)
    
    median_top50 = np.median(top50_values)
    median_top5 = np.median(top5_values)
    median_top20 = np.median(top20_values)
    median_surge = np.median(surge_values)
    
    std_top50 = np.std(top50_values)
    std_top5 = np.std(top5_values)
    std_top20 = np.std(top20_values)
    std_surge = np.std(surge_values)
    
    positive_top50 = sum(1 for v in top50_values if v > 0)
    positive_top5 = sum(1 for v in top5_values if v > 0)
    positive_top20 = sum(1 for v in top20_values if v > 0)
    positive_surge = sum(1 for v in surge_values if v > 0)
    
    total_years = len(summary_data)
    
    wins_vs_top50 = sum(1 for d in summary_data if d['top5_smallcap'] > d['top50_pred'])
    wins_vs_top20 = sum(1 for d in summary_data if d['top5_smallcap'] > d['top20_pred'])
    surge_wins_vs_top50 = sum(1 for d in summary_data if d['surge_strategy'] > d['top50_pred'])
    surge_wins_vs_top5 = sum(1 for d in summary_data if d['surge_strategy'] > d['top5_smallcap'])
    
    report_lines.append(f"{'指标':<20} | {'原Top50':<15} | {'小市值Top5':<15} | {'基准Top20':<15} | {'中期大涨':<15}")
    report_lines.append("-" * 160)
    report_lines.append(f"{'平均年化收益':<20} | {avg_top50:>13.1f}% | {avg_top5:>13.1f}% | {avg_top20:>13.1f}% | {avg_surge:>13.1f}%")
    report_lines.append(f"{'中位数年化收益':<20} | {median_top50:>13.1f}% | {median_top5:>13.1f}% | {median_top20:>13.1f}% | {median_surge:>13.1f}%")
    report_lines.append(f"{'标准差':<20} | {std_top50:>13.1f}% | {std_top5:>13.1f}% | {std_top20:>13.1f}% | {std_surge:>13.1f}%")
    report_lines.append(f"{'正收益年份':<20} | {positive_top50}/{total_years} ({positive_top50/total_years*100:.0f}%) | "
                       f"{positive_top5}/{total_years} ({positive_top5/total_years*100:.0f}%) | "
                       f"{positive_top20}/{total_years} ({positive_top20/total_years*100:.0f}%) | "
                       f"{positive_surge}/{total_years} ({positive_surge/total_years*100:.0f}%)")
    report_lines.append("")
    report_lines.append(f"小市值Top5 vs 原Top50 胜率: {wins_vs_top50}/{total_years} ({wins_vs_top50/total_years*100:.1f}%)")
    report_lines.append(f"小市值Top5 vs 基准Top20 胜率: {wins_vs_top20}/{total_years} ({wins_vs_top20/total_years*100:.1f}%)")
    report_lines.append(f"中期大涨 vs 原Top50 胜率: {surge_wins_vs_top50}/{total_years} ({surge_wins_vs_top50/total_years*100:.1f}%)")
    report_lines.append(f"中期大涨 vs 小市值Top5 胜率: {surge_wins_vs_top5}/{total_years} ({surge_wins_vs_top5/total_years*100:.1f}%)")
    report_lines.append("")
    
    # 关键结论
    report_lines.append("=" * 160)
    report_lines.append("【关键结论】")
    report_lines.append("=" * 160)
    report_lines.append("")
    
    report_lines.append("1. 收益对比：")
    report_lines.append(f"   - 原Top50：平均{avg_top50:.1f}%，中位数{median_top50:.1f}%")
    report_lines.append(f"   - 小市值Top5：平均{avg_top5:.1f}%，中位数{median_top5:.1f}%")
    report_lines.append(f"   - 基准Top20：平均{avg_top20:.1f}%，中位数{median_top20:.1f}%")
    report_lines.append(f"   - 中期大涨策略：平均{avg_surge:.1f}%，中位数{median_surge:.1f}%")
    report_lines.append("")
    
    # 找出最佳策略
    strategies = [
        ('原Top50', avg_top50),
        ('小市值Top5', avg_top5),
        ('基准Top20', avg_top20),
        ('中期大涨', avg_surge)
    ]
    best_strategy = max(strategies, key=lambda x: x[1])
    
    report_lines.append(f"   🏆 最佳策略：{best_strategy[0]}（平均年化{best_strategy[1]:.1f}%）")
    report_lines.append("")
    
    report_lines.append("2. 中期大涨策略分析：")
    if avg_surge > avg_top50:
        report_lines.append(f"   ✅ 中期大涨策略优于原Top50策略 {avg_surge-avg_top50:+.1f}%")
    else:
        report_lines.append(f"   ❌ 中期大涨策略不如原Top50策略 {avg_surge-avg_top50:+.1f}%")
    
    if avg_surge > avg_top5:
        report_lines.append(f"   ✅ 中期大涨策略优于小市值Top5策略 {avg_surge-avg_top5:+.1f}%")
    else:
        report_lines.append(f"   ❌ 中期大涨策略不如小市值Top5策略 {avg_surge-avg_top5:+.1f}%")
    
    avg_surge_count = np.mean([d['surge_count'] for d in summary_data])
    report_lines.append(f"   - 平均持仓数量：{avg_surge_count:.1f}支（介于Top5和Top50之间）")
    report_lines.append(f"   - 胜率 vs Top50：{surge_wins_vs_top50/total_years*100:.1f}%")
    report_lines.append(f"   - 胜率 vs 小市值Top5：{surge_wins_vs_top5/total_years*100:.1f}%")
    report_lines.append("")
    
    report_lines.append("3. 稳定性对比：")
    report_lines.append(f"   - 原Top50：正收益年份{positive_top50}/{total_years}，标准差{std_top50:.1f}%")
    report_lines.append(f"   - 小市值Top5：正收益年份{positive_top5}/{total_years}，标准差{std_top5:.1f}%")
    report_lines.append(f"   - 中期大涨：正收益年份{positive_surge}/{total_years}，标准差{std_surge:.1f}%")
    report_lines.append("")
    
    report_lines.append("4. 策略机制分析：")
    report_lines.append("")
    report_lines.append("   a) 小市值因子：")
    report_lines.append("      - 利用小市值溢价效应")
    report_lines.append("      - 小公司成长空间大，弹性高")
    report_lines.append(f"      - 平均年化收益{avg_top5:.1f}%")
    report_lines.append("")
    report_lines.append("   b) 中期大涨因子：")
    report_lines.append("      - 利用动量效应（Momentum Factor）")
    report_lines.append("      - 筛选有中期上涨动能但未过度追高的股票")
    report_lines.append("      - 避免刚刚大涨的股票（防止追高）")
    report_lines.append(f"      - 平均年化收益{avg_surge:.1f}%")
    report_lines.append("")
    
    # 最终建议
    report_lines.append("=" * 160)
    report_lines.append("【最终建议】")
    report_lines.append("=" * 160)
    report_lines.append("")
    
    if best_strategy[0] == '中期大涨':
        report_lines.append("🏆 强烈推荐：中期大涨策略")
        report_lines.append("")
        report_lines.append("理由：")
        report_lines.append(f"1. 平均年化收益最高（{avg_surge:.1f}%）")
        report_lines.append(f"2. 胜率较高（vs Top50: {surge_wins_vs_top50/total_years*100:.1f}%）")
        report_lines.append(f"3. 持仓数量适中（平均{avg_surge_count:.1f}支）")
        report_lines.append("4. 结合了预测因子和动量因子的优势")
        report_lines.append("5. 有效避免追高风险")
    elif best_strategy[0] == '小市值Top5':
        report_lines.append("🏆 推荐：小市值Top5策略")
        report_lines.append("")
        report_lines.append("理由：")
        report_lines.append(f"1. 平均年化收益高（{avg_top5:.1f}%）")
        report_lines.append("2. 持仓数量最少（5支）")
        report_lines.append("3. 交易成本和管理难度最低")
        if avg_surge > avg_top5 * 0.95:  # 如果中期大涨策略接近
            report_lines.append("")
            report_lines.append("备选：中期大涨策略")
            report_lines.append(f"- 收益相近（{avg_surge:.1f}%）")
            report_lines.append("- 更好的风险分散")
    else:
        report_lines.append(f"🏆 推荐：{best_strategy[0]}策略")
        report_lines.append("")
        report_lines.append(f"平均年化收益最高：{best_strategy[1]:.1f}%")
    
    report_lines.append("")
    report_lines.append("【策略优化建议】")
    report_lines.append("")
    report_lines.append("1. 中期大涨策略可进一步优化：")
    report_lines.append("   - 调整时间窗口（如15天、30天）")
    report_lines.append("   - 调整涨幅阈值（如20%、30%）")
    report_lines.append("   - 加入成交量确认")
    report_lines.append("")
    report_lines.append("2. 组合策略：")
    report_lines.append("   - 50%小市值Top5 + 50%中期大涨")
    report_lines.append("   - 根据市场环境动态调整权重")
    report_lines.append("")
    report_lines.append("3. 风险控制：")
    report_lines.append("   - 加入流动性过滤")
    report_lines.append("   - 设置单股最大权重")
    report_lines.append("   - 行业分散度控制")
    
    report_lines.append("")
    report_lines.append("=" * 160)
    
    report_text = "\n".join(report_lines)
    print("\n" + report_text)
    
    # 保存报告
    report_path = OUTPUT_DIR / 'analysis' / 'four_strategies_comparison.txt'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    logger.info(f"\n报告已保存: {report_path}")


def main():
    """主函数"""
    try:
        results = compare_strategies()
        generate_comparison_report(results)
        return True
    except Exception as e:
        logger.error(f"对比失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
