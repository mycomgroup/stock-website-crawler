"""
对2026年holdout数据生成预测

Phase 1: 使用2015-2023训练的模型预测2026
Phase 2: 使用2015-2025训练的模型预测2026

需要重新加载模型并对2026数据进行预测
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import logging
import pickle

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / 'output'


def load_2026_data():
    """加载2026年数据"""
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


def load_phase_snapshot(phase_name):
    """加载Phase的snapshot配置"""
    snapshot_path = OUTPUT_DIR / phase_name / f'run_snapshot_{phase_name}.json'
    
    if not snapshot_path.exists():
        logger.error(f"找不到{phase_name}的snapshot: {snapshot_path}")
        return None
    
    with open(snapshot_path, 'r') as f:
        snapshot = json.load(f)
    
    # 如果snapshot没有family_beta，尝试从analysis summary加载
    if 'family_beta' not in snapshot:
        analysis_path = OUTPUT_DIR / 'analysis' / f'{phase_name}_analysis_summary.json'
        if analysis_path.exists():
            with open(analysis_path, 'r') as f:
                analysis = json.load(f)
                if 'family_weights' in analysis:
                    snapshot['family_beta'] = analysis['family_weights']
                    logger.info(f"  从analysis summary加载了{phase_name}的family_beta")
    
    return snapshot


def predict_with_family_weights(df_2026, snapshot, phase_name):
    """使用family权重对2026数据进行预测"""
    logger.info(f"\n使用{phase_name}的family权重预测2026...")
    
    family_beta = snapshot['family_beta']
    family_map = snapshot['config']['use_family_map']
    
    # 准备因子列表
    all_factors = []
    for family, factors in family_map.items():
        all_factors.extend(factors)
    
    # 检查哪些因子在数据中存在
    available_factors = [f for f in all_factors if f in df_2026.columns]
    missing_factors = [f for f in all_factors if f not in df_2026.columns]
    
    logger.info(f"  可用因子: {len(available_factors)}/{len(all_factors)}")
    if missing_factors:
        logger.warning(f"  缺失因子: {len(missing_factors)} 个")
    
    # 对每个family计算加权得分
    df_pred = df_2026[['date', 'stock_id', 'pchg']].copy()
    df_pred['prediction'] = 0.0
    
    for family, beta in family_beta.items():
        if family not in family_map:
            continue
        
        family_factors = [f for f in family_map[family] if f in df_2026.columns]
        
        if len(family_factors) == 0:
            continue
        
        # 标准化family内的因子
        family_data = df_2026[family_factors].copy()
        
        # 按日期分组标准化
        for date in df_2026['date'].unique():
            date_mask = df_2026['date'] == date
            date_data = family_data[date_mask]
            
            # 标准化
            mean = date_data.mean()
            std = date_data.std()
            std[std == 0] = 1  # 避免除零
            
            normalized = (date_data - mean) / std
            
            # 计算family得分（所有因子的平均）
            family_score = normalized.mean(axis=1)
            
            # 加权到总预测
            df_pred.loc[date_mask, 'prediction'] += beta * family_score.values
    
    logger.info(f"  预测完成: {len(df_pred)} 行")
    logger.info(f"  预测范围: [{df_pred['prediction'].min():.4f}, {df_pred['prediction'].max():.4f}]")
    
    return df_pred


def main():
    """主函数"""
    try:
        # 加载2026数据
        df_2026 = load_2026_data()
        
        # Phase 1预测
        logger.info("\n" + "=" * 80)
        logger.info("Phase 1: 使用2015-2023训练的模型预测2026")
        logger.info("=" * 80)
        
        phase1_snapshot = load_phase_snapshot('phase1')
        if phase1_snapshot is None:
            return False
        
        phase1_pred = predict_with_family_weights(df_2026, phase1_snapshot, 'Phase 1')
        
        # 保存Phase 1预测
        phase1_output = OUTPUT_DIR / 'phase1' / 'predictions_2026_holdout.csv'
        phase1_pred.to_csv(phase1_output, index=False)
        logger.info(f"\nPhase 1预测已保存: {phase1_output}")
        
        # Phase 2预测
        logger.info("\n" + "=" * 80)
        logger.info("Phase 2: 使用2015-2025训练的模型预测2026")
        logger.info("=" * 80)
        
        phase2_snapshot = load_phase_snapshot('phase2')
        if phase2_snapshot is None:
            return False
        
        phase2_pred = predict_with_family_weights(df_2026, phase2_snapshot, 'Phase 2')
        
        # 保存Phase 2预测
        phase2_output = OUTPUT_DIR / 'phase2' / 'predictions_2026_holdout.csv'
        phase2_pred.to_csv(phase2_output, index=False)
        logger.info(f"\nPhase 2预测已保存: {phase2_output}")
        
        logger.info("\n✅ 2026 holdout预测完成")
        logger.info(f"   Phase 1: {phase1_output}")
        logger.info(f"   Phase 2: {phase2_output}")
        
        return True
        
    except Exception as e:
        logger.error(f"预测失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
