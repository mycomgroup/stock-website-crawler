"""
对比Phase 1 vs Phase 2在2026年的表现

Phase 1: 使用2015-2023年数据训练
Phase 2: 使用2015-2025年数据训练

目标：验证加入2024-2025年数据后，模型在2026年的表现是否改善
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import json
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
        logger.info(f"  移除了 {len(dates_to_remove)} 个异常日期")
    
    logger.info(f"  2026年数据: {len(df_2026)} 行, {df_2026['date'].nunique()} 个日期")
    
    return df_2026


def load_phase_predictions(phase_name):
    """加载Phase的OOF预测"""
    logger.info(f"\n加载{phase_name}预测...")
    
    oof_path = OUTPUT_DIR / phase_name / f'oof_predictions_{phase_name}.csv'
    
    if not oof_path.exists():
        logger.warning(f"  {phase_name}预测文件不存在: {oof_path}")
        return None
    
    df = pd.read_csv(oof_path)
    df['date'] = pd.to_datetime(df['date'])
    
    logger.info(f"  {phase_name}预测: {len(df)} 行, {df['date'].nunique()} 个日期")
    
    return df


def calculate_ic_on_2026(predictions, actual_data, phase_name, pred_col='prediction'):
    """计算在2026年数据上的IC"""
    logger.info(f"\n计算{phase_name}在2026年的IC...")
    
    # 合并预测和实际数据 - 只从actual_data取pchg，避免重复
    merged = predictions[['date', 'stock_id', pred_col]].merge(
        actual_data[['date', 'stock_id', 'pchg']],
        on=['date', 'stock_id'],
        how='inner'
    )
    
    logger.info(f"  匹配数据: {len(merged)} 行")
    
    # 按日期计算IC
    ic_series = []
    dates = sorted(merged['date'].unique())
    
    for date in dates:
        df_date = merged[merged['date'] == date]
        
        valid_mask = df_date[pred_col].notna() & df_date['pchg'].notna()
        if valid_mask.sum() > 10:
            corr, _ = stats.spearmanr(
                df_date.loc[valid_mask, pred_col],
                df_date.loc[valid_mask, 'pchg']
            )
            if np.isfinite(corr):
                ic_series.append(corr)
    
    if len(ic_series) == 0:
        logger.warning(f"  {phase_name}没有有效的IC数据")
        return {
            'ic_series': [],
            'ic_mean': 0,
            'ic_std': 0,
            'ic_ir': 0,
            'ic_positive_ratio': 0,
        }
    
    ic_mean = np.mean(ic_series)
    ic_std = np.std(ic_series)
    ic_ir = ic_mean / ic_std if ic_std > 0 else 0
    
    logger.info(f"  IC均值: {ic_mean:.4f}")
    logger.info(f"  IC标准差: {ic_std:.4f}")
    logger.info(f"  IC IR: {ic_ir:.4f}")
    logger.info(f"  IC>0占比: {sum(ic > 0 for ic in ic_series) / len(ic_series) * 100:.2f}%")
    
    return {
        'ic_series': ic_series,
        'ic_mean': ic_mean,
        'ic_std': ic_std,
        'ic_ir': ic_ir,
        'ic_positive_ratio': sum(ic > 0 for ic in ic_series) / len(ic_series),
    }


def calculate_portfolio_returns(predictions, actual_data, phase_name, pred_col='prediction'):
    """计算组合收益"""
    logger.info(f"\n计算{phase_name}的组合收益...")
    
    # 合并数据 - 只从actual_data取pchg，避免重复
    merged = predictions[['date', 'stock_id', pred_col]].merge(
        actual_data[['date', 'stock_id', 'pchg']],
        on=['date', 'stock_id'],
        how='inner'
    )
    
    if len(merged) == 0:
        logger.warning(f"  {phase_name}没有匹配的数据")
        return {
            'ytd_return': 0,
            'annual_return': 0,
            'annual_vol': 0,
            'sharpe': 0,
            'ytd_excess': 0,
            'annual_excess': 0,
        }
    
    # Top-50组合
    def simulate_top50(group):
        top50 = group.nlargest(50, pred_col)
        return top50['pchg'].mean()
    
    portfolio_returns = merged.groupby('date').apply(simulate_top50)
    market_returns = merged.groupby('date')['pchg'].mean()
    
    # 计算收益指标
    n_weeks = len(portfolio_returns)
    port_cum = (1 + portfolio_returns).cumprod()
    mkt_cum = (1 + market_returns).cumprod()
    
    # 使用实际天数计算年化
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
    
    logger.info(f"  YTD收益: {ytd_port:.2f}%")
    logger.info(f"  年化收益: {ann_port:.2f}%")
    logger.info(f"  年化波动: {ann_vol_port:.2f}%")
    logger.info(f"  夏普比率: {sharpe_port:.2f}")
    logger.info(f"  YTD超额: {ytd_port - ytd_mkt:.2f}%")
    
    return {
        'ytd_return': ytd_port,
        'annual_return': ann_port,
        'annual_vol': ann_vol_port,
        'sharpe': sharpe_port,
        'ytd_excess': ytd_port - ytd_mkt,
        'annual_excess': ann_port - ann_mkt,
    }


def generate_comparison_report(phase1_ic, phase2_ic, phase1_perf, phase2_perf):
    """生成对比报告"""
    logger.info("\n" + "=" * 80)
    logger.info("Phase 1 vs Phase 2 在2026年的对比报告")
    logger.info("=" * 80)
    
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("Phase 1 vs Phase 2 在2026年的对比报告")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    report_lines.append("【一、训练数据对比】")
    report_lines.append("")
    report_lines.append("Phase 1: 2015-2023年数据训练")
    report_lines.append("Phase 2: 2015-2025年数据训练（增加2024-2025年）")
    report_lines.append("")
    
    report_lines.append("【二、IC表现对比】")
    report_lines.append("")
    report_lines.append(f"指标          | Phase 1    | Phase 2    | 变化")
    report_lines.append("-" * 60)
    report_lines.append(f"IC均值        | {phase1_ic['ic_mean']:>10.4f} | {phase2_ic['ic_mean']:>10.4f} | {(phase2_ic['ic_mean'] - phase1_ic['ic_mean']) / abs(phase1_ic['ic_mean']) * 100:>+6.1f}%")
    report_lines.append(f"IC标准差      | {phase1_ic['ic_std']:>10.4f} | {phase2_ic['ic_std']:>10.4f} | {(phase2_ic['ic_std'] - phase1_ic['ic_std']) / phase1_ic['ic_std'] * 100:>+6.1f}%")
    report_lines.append(f"IC IR         | {phase1_ic['ic_ir']:>10.4f} | {phase2_ic['ic_ir']:>10.4f} | {(phase2_ic['ic_ir'] - phase1_ic['ic_ir']) / abs(phase1_ic['ic_ir']) * 100:>+6.1f}%")
    report_lines.append(f"IC>0占比      | {phase1_ic['ic_positive_ratio'] * 100:>9.2f}% | {phase2_ic['ic_positive_ratio'] * 100:>9.2f}% | {(phase2_ic['ic_positive_ratio'] - phase1_ic['ic_positive_ratio']) * 100:>+6.1f}pp")
    report_lines.append("")
    
    report_lines.append("【三、收益表现对比】")
    report_lines.append("")
    report_lines.append(f"指标          | Phase 1    | Phase 2    | 变化")
    report_lines.append("-" * 60)
    report_lines.append(f"YTD收益       | {phase1_perf['ytd_return']:>9.2f}% | {phase2_perf['ytd_return']:>9.2f}% | {phase2_perf['ytd_return'] - phase1_perf['ytd_return']:>+6.2f}pp")
    report_lines.append(f"年化收益      | {phase1_perf['annual_return']:>9.2f}% | {phase2_perf['annual_return']:>9.2f}% | {phase2_perf['annual_return'] - phase1_perf['annual_return']:>+6.2f}pp")
    report_lines.append(f"年化波动      | {phase1_perf['annual_vol']:>9.2f}% | {phase2_perf['annual_vol']:>9.2f}% | {phase2_perf['annual_vol'] - phase1_perf['annual_vol']:>+6.2f}pp")
    report_lines.append(f"夏普比率      | {phase1_perf['sharpe']:>10.2f} | {phase2_perf['sharpe']:>10.2f} | {phase2_perf['sharpe'] - phase1_perf['sharpe']:>+6.2f}")
    report_lines.append(f"YTD超额       | {phase1_perf['ytd_excess']:>9.2f}% | {phase2_perf['ytd_excess']:>9.2f}% | {phase2_perf['ytd_excess'] - phase1_perf['ytd_excess']:>+6.2f}pp")
    report_lines.append(f"年化超额      | {phase1_perf['annual_excess']:>9.2f}% | {phase2_perf['annual_excess']:>9.2f}% | {phase2_perf['annual_excess'] - phase1_perf['annual_excess']:>+6.2f}pp")
    report_lines.append("")
    
    report_lines.append("【四、结论】")
    report_lines.append("")
    
    # 判断Phase 2是否改善
    ic_improved = phase2_ic['ic_mean'] > phase1_ic['ic_mean']
    ir_improved = phase2_ic['ic_ir'] > phase1_ic['ic_ir']
    return_improved = phase2_perf['annual_return'] > phase1_perf['annual_return']
    sharpe_improved = phase2_perf['sharpe'] > phase1_perf['sharpe']
    
    improvements = sum([ic_improved, ir_improved, return_improved, sharpe_improved])
    
    if improvements >= 3:
        report_lines.append("✅ Phase 2表现显著优于Phase 1")
        report_lines.append(f"   - {improvements}/4 个关键指标改善")
        report_lines.append("   - 建议使用Phase 2模型")
    elif improvements >= 2:
        report_lines.append("⚠️ Phase 2表现略优于Phase 1")
        report_lines.append(f"   - {improvements}/4 个关键指标改善")
        report_lines.append("   - 建议进一步验证后使用Phase 2")
    else:
        report_lines.append("❌ Phase 2表现未明显改善")
        report_lines.append(f"   - 仅{improvements}/4 个关键指标改善")
        report_lines.append("   - 可能存在过拟合，建议继续使用Phase 1")
    
    report_lines.append("")
    report_lines.append("=" * 80)
    
    report_text = "\n".join(report_lines)
    print("\n" + report_text)
    
    # 保存报告
    report_path = OUTPUT_DIR / 'analysis' / 'phase1_vs_phase2_comparison.txt'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    logger.info(f"\n对比报告已保存: {report_path}")
    
    return report_text


def main():
    """主函数"""
    try:
        # 加载2026年实际数据
        df_2026 = load_2026_data()
        
        # 加载Phase 1和Phase 2的holdout预测
        phase1_pred_path = OUTPUT_DIR / 'phase1' / 'predictions_2026_holdout.csv'
        phase2_pred_path = OUTPUT_DIR / 'phase2' / 'predictions_2026_holdout.csv'
        
        # 检查是否存在holdout预测文件
        if not phase1_pred_path.exists() or not phase2_pred_path.exists():
            logger.error("找不到2026 holdout预测文件")
            logger.error("请先运行 predict_2026_holdout.py 生成预测")
            return False
        
        # 加载预测
        phase1_pred = pd.read_csv(phase1_pred_path)
        phase1_pred['date'] = pd.to_datetime(phase1_pred['date'])
        
        phase2_pred = pd.read_csv(phase2_pred_path)
        phase2_pred['date'] = pd.to_datetime(phase2_pred['date'])
        
        logger.info(f"\nPhase 1在2026年的预测: {len(phase1_pred)} 行")
        logger.info(f"Phase 2在2026年的预测: {len(phase2_pred)} 行")
        
        # 计算IC
        phase1_ic = calculate_ic_on_2026(phase1_pred, df_2026, 'Phase 1', pred_col='prediction')
        phase2_ic = calculate_ic_on_2026(phase2_pred, df_2026, 'Phase 2', pred_col='prediction')
        
        # 计算收益
        phase1_perf = calculate_portfolio_returns(phase1_pred, df_2026, 'Phase 1', pred_col='prediction')
        phase2_perf = calculate_portfolio_returns(phase2_pred, df_2026, 'Phase 2', pred_col='prediction')
        
        # 生成对比报告
        generate_comparison_report(phase1_ic, phase2_ic, phase1_perf, phase2_perf)
        
        return True
        
    except Exception as e:
        logger.error(f"对比分析失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
