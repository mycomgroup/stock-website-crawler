"""
验证预测能力：能否提前识别出表现好的股票？

关键问题：
1. 模型预测值能否区分Top 20 vs Bottom 30？
2. 如果选20支，实际表现如何？
3. 事后最优 vs 事前可预测的差距
"""

import pandas as pd
import numpy as np
from scipy import stats
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


def analyze_predictability(predictions, actual_data, pred_col='prediction'):
    """
    分析预测能力
    
    对比：
    1. 按预测值选Top 20 vs Top 50
    2. 预测值在Top 20 vs Bottom 30中的分布
    3. 事后最优 vs 事前预测的差距
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
    
    results = []
    
    for date in sorted(merged['date'].unique()):
        df_date = merged[merged['date'] == date]
        
        # 第一阶段：Top10%
        n_stage1 = max(int(len(df_date) * 0.1), 50)
        stage1_pool = df_date.nlargest(n_stage1, pred_col)
        
        # 第二阶段：EPS>0.5
        stage2_pool = stage1_pool[stage1_pool['eps'] > 0.5]
        
        if len(stage2_pool) < 50:
            final_pool = stage2_pool.nlargest(len(stage2_pool), pred_col)
        else:
            final_pool = stage2_pool.nlargest(50, pred_col)
        
        # 按实际收益排序
        final_pool_sorted = final_pool.sort_values('pchg', ascending=False)
        
        # 事后分析：Top 20 vs Bottom 30
        top20_actual = final_pool_sorted.head(20)
        bottom30_actual = final_pool_sorted.tail(30)
        
        # 事前预测：按预测值选Top 20
        top20_predicted = final_pool.nlargest(20, pred_col)
        
        # 计算指标
        result = {
            'date': date,
            # 事后最优（按实际收益）
            'top20_actual_return': top20_actual['pchg'].mean(),
            'top20_actual_pred_mean': top20_actual[pred_col].mean(),
            'bottom30_actual_return': bottom30_actual['pchg'].mean(),
            'bottom30_actual_pred_mean': bottom30_actual[pred_col].mean(),
            # 事前预测（按预测值）
            'top20_predicted_return': top20_predicted['pchg'].mean(),
            'top20_predicted_pred_mean': top20_predicted[pred_col].mean(),
            # 全部50支
            'all50_return': final_pool['pchg'].mean(),
            'all50_pred_mean': final_pool[pred_col].mean(),
            # 重叠度
            'overlap': len(set(top20_actual['stock_id']) & set(top20_predicted['stock_id'])),
        }
        
        results.append(result)
    
    df_results = pd.DataFrame(results)
    
    return df_results


def generate_report(df_results):
    """生成验证报告"""
    
    logger.info("\n" + "=" * 120)
    logger.info("预测能力验证报告")
    logger.info("=" * 120)
    
    report_lines = []
    report_lines.append("=" * 120)
    report_lines.append("预测能力验证报告：能否提前识别出表现好的股票？")
    report_lines.append("=" * 120)
    report_lines.append("")
    
    report_lines.append("【核心问题】")
    report_lines.append("")
    report_lines.append("我们发现事后看Top 20股票贡献了220%的收益，但关键问题是：")
    report_lines.append("能否在选股时就识别出这Top 20？还是只能事后才知道？")
    report_lines.append("")
    
    # 1. 预测值区分能力
    report_lines.append("【1. 预测值能否区分好坏股票？】")
    report_lines.append("")
    
    top20_pred_mean = df_results['top20_actual_pred_mean'].mean()
    bottom30_pred_mean = df_results['bottom30_actual_pred_mean'].mean()
    pred_diff = top20_pred_mean - bottom30_pred_mean
    
    report_lines.append(f"事后Top 20的平均预测值: {top20_pred_mean:.4f}")
    report_lines.append(f"事后Bottom 30的平均预测值: {bottom30_pred_mean:.4f}")
    report_lines.append(f"预测值差异: {pred_diff:.4f}")
    report_lines.append("")
    
    if abs(pred_diff) < 0.001:
        report_lines.append("❌ 预测值几乎无法区分好坏股票（差异<0.001）")
        report_lines.append("   结论：模型无法提前识别出表现好的股票")
    elif abs(pred_diff) < 0.01:
        report_lines.append("⚠️ 预测值区分能力较弱（差异<0.01）")
        report_lines.append("   结论：模型有一定区分能力，但不强")
    else:
        report_lines.append("✅ 预测值有明显区分能力（差异>0.01）")
        report_lines.append("   结论：模型可以一定程度识别好股票")
    
    report_lines.append("")
    
    # 2. 事前选Top 20的实际表现
    report_lines.append("【2. 按预测值选Top 20的实际表现】")
    report_lines.append("")
    
    top20_pred_return = df_results['top20_predicted_return'].mean()
    top20_actual_return = df_results['top20_actual_return'].mean()
    all50_return = df_results['all50_return'].mean()
    
    report_lines.append(f"事前按预测值选Top 20的实际收益: {top20_pred_return * 100:.2f}%")
    report_lines.append(f"事后最优Top 20的收益: {top20_actual_return * 100:.2f}%")
    report_lines.append(f"全部50支的收益: {all50_return * 100:.2f}%")
    report_lines.append("")
    
    improvement_vs_50 = (top20_pred_return - all50_return) / abs(all50_return) * 100 if all50_return != 0 else 0
    gap_vs_optimal = (top20_actual_return - top20_pred_return) / abs(top20_actual_return) * 100 if top20_actual_return != 0 else 0
    
    report_lines.append(f"事前Top 20 vs 全部50支: {improvement_vs_50:+.1f}%")
    report_lines.append(f"事前Top 20 vs 事后最优: {-gap_vs_optimal:+.1f}%")
    report_lines.append("")
    
    if top20_pred_return > all50_return * 1.5:
        report_lines.append("✅ 按预测值选Top 20显著优于50支")
        report_lines.append("   建议：可以减少持仓至20支")
    elif top20_pred_return > all50_return:
        report_lines.append("⚠️ 按预测值选Top 20略优于50支")
        report_lines.append("   建议：可以考虑减少持仓，但提升有限")
    else:
        report_lines.append("❌ 按预测值选Top 20未优于50支")
        report_lines.append("   建议：保持50支持仓，不要减少")
    
    report_lines.append("")
    
    # 3. 重叠度分析
    report_lines.append("【3. 事前预测 vs 事后最优的重叠度】")
    report_lines.append("")
    
    avg_overlap = df_results['overlap'].mean()
    overlap_ratio = avg_overlap / 20 * 100
    
    report_lines.append(f"平均重叠股票数: {avg_overlap:.1f} / 20")
    report_lines.append(f"重叠比例: {overlap_ratio:.1f}%")
    report_lines.append("")
    
    if overlap_ratio > 70:
        report_lines.append("✅ 重叠度高：模型能较好预测哪些股票会表现好")
    elif overlap_ratio > 50:
        report_lines.append("⚠️ 重叠度中等：模型有一定预测能力")
    else:
        report_lines.append("❌ 重叠度低：模型难以预测哪些股票会表现好")
    
    report_lines.append("")
    
    # 4. 周度表现对比
    report_lines.append("【4. 周度表现对比】")
    report_lines.append("")
    report_lines.append(f"{'日期':<12} | {'事前Top20':<12} | {'事后Top20':<12} | {'全部50支':<12} | {'重叠数':<8}")
    report_lines.append("-" * 120)
    
    for _, row in df_results.iterrows():
        report_lines.append(
            f"{row['date'].strftime('%Y-%m-%d'):<12} | "
            f"{row['top20_predicted_return'] * 100:>11.2f}% | "
            f"{row['top20_actual_return'] * 100:>11.2f}% | "
            f"{row['all50_return'] * 100:>11.2f}% | "
            f"{row['overlap']:>7.0f}"
        )
    
    report_lines.append("")
    
    # 5. 最终结论
    report_lines.append("【5. 最终结论】")
    report_lines.append("")
    
    if top20_pred_return > all50_return and overlap_ratio > 60:
        report_lines.append("✅ 可以减少持仓至20支")
        report_lines.append(f"   理由1: 事前Top 20收益({top20_pred_return * 100:.2f}%) > 全部50支({all50_return * 100:.2f}%)")
        report_lines.append(f"   理由2: 重叠度{overlap_ratio:.1f}%，模型有预测能力")
        report_lines.append(f"   预期提升: {improvement_vs_50:+.1f}%")
    elif top20_pred_return > all50_return:
        report_lines.append("⚠️ 可以尝试减少持仓，但需谨慎")
        report_lines.append(f"   事前Top 20略优于50支，但重叠度仅{overlap_ratio:.1f}%")
        report_lines.append("   建议：先测试25-30支")
    else:
        report_lines.append("❌ 不建议减少持仓")
        report_lines.append(f"   事前Top 20收益({top20_pred_return * 100:.2f}%) ≤ 全部50支({all50_return * 100:.2f}%)")
        report_lines.append("   原因：事后看Top 20好，但事前无法识别")
        report_lines.append("   建议：保持50支分散风险")
    
    report_lines.append("")
    
    # 6. 关键洞察
    report_lines.append("【6. 关键洞察】")
    report_lines.append("")
    report_lines.append("事后诸葛亮 vs 事前可预测：")
    report_lines.append(f"  - 事后最优Top 20: {top20_actual_return * 100:.2f}%（我们现在知道的）")
    report_lines.append(f"  - 事前预测Top 20: {top20_pred_return * 100:.2f}%（选股时能做到的）")
    report_lines.append(f"  - 差距: {(top20_actual_return - top20_pred_return) * 100:.2f}pp")
    report_lines.append("")
    report_lines.append("这个差距说明：")
    if abs(top20_actual_return - top20_pred_return) < 0.005:
        report_lines.append("  ✅ 模型预测能力强，事前事后差距小")
    else:
        report_lines.append("  ⚠️ 存在较大的不可预测成分，需要分散持仓")
    
    report_lines.append("")
    report_lines.append("=" * 120)
    
    report_text = "\n".join(report_lines)
    print("\n" + report_text)
    
    # 保存报告
    report_path = OUTPUT_DIR / 'analysis' / 'predictability_validation.txt'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    logger.info(f"\n验证报告已保存: {report_path}")
    
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
        
        # 分析预测能力
        logger.info("\n开始验证预测能力...")
        df_results = analyze_predictability(phase2_pred, df_2026, pred_col='prediction')
        
        if len(df_results) == 0:
            logger.error("没有有效数据")
            return False
        
        logger.info(f"分析了 {len(df_results)} 个交易日")
        
        # 保存详细数据
        csv_path = OUTPUT_DIR / 'analysis' / 'predictability_validation_details.csv'
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        df_results.to_csv(csv_path, index=False)
        logger.info(f"详细数据已保存: {csv_path}")
        
        # 生成报告
        generate_report(df_results)
        
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
