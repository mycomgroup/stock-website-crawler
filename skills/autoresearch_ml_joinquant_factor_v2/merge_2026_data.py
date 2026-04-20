"""
合并2026年数据到训练集

将weekly_factors中的2026年数据合并到train_merged_all.csv，
生成train_merged_all_with_2026.csv用于Phase 2训练。
"""

import pandas as pd
import glob
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "weekly_factors"
TRAIN_FILE = BASE_DIR / "train_merged_all.csv"
OUTPUT_FILE = BASE_DIR / "train_merged_all_with_2026.csv"


def load_2026_data():
    """加载2026年的weekly_factors数据"""
    logger.info("加载2026年数据...")
    
    files_2026 = sorted(glob.glob(str(DATA_DIR / "factors_2026*.csv")))
    logger.info(f"找到 {len(files_2026)} 个2026年数据文件")
    
    if not files_2026:
        raise FileNotFoundError("未找到2026年数据文件")
    
    dfs = []
    for file_path in files_2026:
        df = pd.read_csv(file_path)
        # 从文件名提取日期
        date_str = Path(file_path).stem.split('_')[1]
        df['date'] = pd.to_datetime(date_str)
        dfs.append(df)
        logger.info(f"  加载 {Path(file_path).name}: {len(df)} 行")
    
    df_2026 = pd.concat(dfs, ignore_index=True)
    
    # 重命名列
    if 'Unnamed: 0' in df_2026.columns:
        df_2026 = df_2026.rename(columns={'Unnamed: 0': 'stock_id'})
    
    logger.info(f"2026年数据总计: {len(df_2026)} 行, {df_2026['date'].nunique()} 个日期")
    
    return df_2026


def merge_data():
    """合并数据"""
    logger.info("=" * 80)
    logger.info("开始合并数据...")
    logger.info("=" * 80)
    
    # 加载现有训练数据
    logger.info(f"\n加载现有训练数据: {TRAIN_FILE}")
    df_train = pd.read_csv(TRAIN_FILE)
    logger.info(f"  行数: {len(df_train)}")
    logger.info(f"  列数: {len(df_train.columns)}")
    logger.info(f"  日期范围: {df_train['date'].min()} ~ {df_train['date'].max()}")
    
    # 加载2026年数据
    df_2026 = load_2026_data()
    
    # 检查列是否匹配
    train_cols = set(df_train.columns)
    data_2026_cols = set(df_2026.columns)
    
    missing_in_2026 = train_cols - data_2026_cols
    missing_in_train = data_2026_cols - train_cols
    
    if missing_in_2026:
        logger.warning(f"\n2026年数据缺少的列 ({len(missing_in_2026)}): {sorted(list(missing_in_2026))[:10]}...")
    
    if missing_in_train:
        logger.warning(f"\n训练数据缺少的列 ({len(missing_in_train)}): {sorted(list(missing_in_train))[:10]}...")
    
    # 对齐列
    common_cols = sorted(list(train_cols & data_2026_cols))
    logger.info(f"\n共同列数: {len(common_cols)}")
    
    # 确保包含stock_id或Unnamed: 0
    if 'Unnamed: 0' in train_cols:
        stock_id_col = 'Unnamed: 0'
    elif 'stock_id' in train_cols:
        stock_id_col = 'stock_id'
    else:
        raise ValueError("训练数据中没有找到stock_id列")
    
    if stock_id_col not in common_cols:
        common_cols.append(stock_id_col)
        # 如果2026数据中没有这个列，需要从另一个列名复制
        if stock_id_col == 'Unnamed: 0' and 'stock_id' in df_2026.columns:
            df_2026['Unnamed: 0'] = df_2026['stock_id']
        elif stock_id_col == 'stock_id' and 'Unnamed: 0' in df_2026.columns:
            df_2026['stock_id'] = df_2026['Unnamed: 0']
    
    common_cols = sorted(common_cols)
    logger.info(f"最终共同列数（包含{stock_id_col}）: {len(common_cols)}")
    
    df_train_aligned = df_train[common_cols]
    df_2026_aligned = df_2026[common_cols]
    
    # 合并
    logger.info("\n合并数据...")
    df_merged = pd.concat([df_train_aligned, df_2026_aligned], ignore_index=True)
    
    # 转换日期类型
    df_merged['date'] = pd.to_datetime(df_merged['date'])
    
    logger.info(f"  合并后行数: {len(df_merged)}")
    logger.info(f"  合并后列数: {len(df_merged.columns)}")
    logger.info(f"  日期范围: {df_merged['date'].min()} ~ {df_merged['date'].max()}")
    
    # 检查日期分布
    logger.info("\n日期分布:")
    for year in sorted(df_merged['date'].dt.year.unique()):
        count = (df_merged['date'].dt.year == year).sum()
        logger.info(f"  {year}年: {count} 行")
    
    # 保存
    logger.info(f"\n保存到: {OUTPUT_FILE}")
    df_merged.to_csv(OUTPUT_FILE, index=False)
    logger.info(f"  文件大小: {OUTPUT_FILE.stat().st_size / 1024 / 1024:.2f} MB")
    
    logger.info("\n" + "=" * 80)
    logger.info("数据合并完成!")
    logger.info("=" * 80)
    
    return df_merged


def main():
    """主函数"""
    try:
        df_merged = merge_data()
        
        # 验证
        logger.info("\n验证合并结果:")
        logger.info(f"  总行数: {len(df_merged)}")
        logger.info(f"  总列数: {len(df_merged.columns)}")
        logger.info(f"  唯一日期数: {df_merged['date'].nunique()}")
        logger.info(f"  唯一股票数: {df_merged['Unnamed: 0'].nunique() if 'Unnamed: 0' in df_merged.columns else 'N/A'}")
        
        # 检查2026年数据
        df_2026 = df_merged[pd.to_datetime(df_merged['date']).dt.year == 2026]
        logger.info(f"\n2026年数据:")
        logger.info(f"  行数: {len(df_2026)}")
        logger.info(f"  日期数: {df_2026['date'].nunique()}")
        logger.info(f"  日期范围: {df_2026['date'].min()} ~ {df_2026['date'].max()}")
        
        return True
        
    except Exception as e:
        logger.error(f"合并失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
