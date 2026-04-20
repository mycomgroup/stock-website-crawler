"""
Phase 2: 使用2015-2025年数据训练，在2026年测试

与Phase 1的区别：
- Phase 1: 训练2015-2023年，测试2023年holdout
- Phase 2: 训练2015-2025年，测试2026年

目标：验证加入2024-2025年数据后，模型在2026年的表现是否改善
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# 添加项目路径
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from v2.pipeline import WeakFactorPipelineV2, PipelineConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


def run_phase2():
    """运行Phase 2训练"""
    
    logger.info("=" * 80)
    logger.info("Phase 2: 训练2015-2025年数据，测试2026年")
    logger.info("=" * 80)
    
    # 配置
    config = PipelineConfig(
        csv_path=str(BASE_DIR / 'train_merged_all_with_2026.csv'),
        holdout_periods=52,  # 保留2026年作为测试集（约52周）
        random_state=42,
    )
    
    logger.info(f"数据文件: {config.csv_path}")
    logger.info(f"Holdout期: {config.holdout_periods}周")
    logger.info("=" * 80)
    
    # 创建pipeline
    pipeline = WeakFactorPipelineV2(config)
    
    # 运行pipeline（使用research数据，不访问holdout）
    logger.info("\n开始训练...")
    result = pipeline.run(use_holdout=False)
    
    # 保存结果
    output_dir = BASE_DIR / 'output' / 'phase2'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"\n保存结果到: {output_dir}")
    
    # 保存OOF预测
    oof_predictions = result['oof_predictions']
    oof_df = oof_predictions.reset_index()
    oof_df.columns = ['date', 'stock_id', 'oof_prediction']
    oof_path = output_dir / 'oof_predictions_phase2.csv'
    oof_df.to_csv(oof_path, index=False)
    logger.info(f"  OOF预测已保存: {oof_path}")
    
    # 保存运行快照
    snapshot = {
        'run_id': 'phase2',
        'timestamp': datetime.now().isoformat(),
        'random_state': config.random_state,
        'config': {
            'csv_path': str(config.csv_path),
            'holdout_periods': config.holdout_periods,
            'use_family_map': {k: v for k, v in config.use_family_map.items()},
        },
        'family_beta': {k: float(v) for k, v in result['family_beta'].items()},
    }
    
    snapshot_path = output_dir / 'run_snapshot_phase2.json'
    with open(snapshot_path, 'w') as f:
        json.dump(snapshot, f, indent=2)
    logger.info(f"  运行快照已保存: {snapshot_path}")
    
    logger.info("\n" + "=" * 80)
    logger.info("Phase 2训练完成!")
    logger.info("=" * 80)
    
    return result


if __name__ == "__main__":
    try:
        result = run_phase2()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Phase 2训练失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
