"""生成小型测试数据集 (Task 8.4 辅助)

生成与 train_merged_all.csv 结构完全一致的小型合成数据，
用于在不加载完整大文件的情况下跑通整个 pipeline。

生成规格：
- 100 只股票
- 300 个截面日期（约 5.8 年，周频）
- 260 个因子列（与真实 CSV 完全一致）
- 包含 pchg 标签（有微弱信号，便于验证 IC > 0）

使用方法：
    python -m skills.autoresearch_ml_joinquant_factor_v2.v2.generate_test_data
    # 生成文件：skills/autoresearch_ml_joinquant_factor_v2/test_data_small.csv
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# 输出路径
OUTPUT_PATH = Path(__file__).parent.parent / "test_data_small.csv"

# 生成参数
N_STOCKS = 100
N_DATES = 300       # 约 5.8 年周频
RANDOM_SEED = 42
SIGNAL_STRENGTH = 0.05  # 微弱信号强度（确保 IC > 0）


def generate_small_dataset(
    n_stocks: int = N_STOCKS,
    n_dates: int = N_DATES,
    seed: int = RANDOM_SEED,
    output_path: str | Path = OUTPUT_PATH,
) -> pd.DataFrame:
    """生成小型合成数据集。

    Parameters
    ----------
    n_stocks : int
        股票数量（默认 100）。
    n_dates : int
        截面日期数量（默认 300，周频）。
    seed : int
        随机种子（默认 42）。
    output_path : str | Path
        输出 CSV 路径。

    Returns
    -------
    pd.DataFrame
        生成的数据集（与 train_merged_all.csv 结构一致）。
    """
    # 导入实际因子列名
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
    from skills.autoresearch_ml_joinquant_factor_v2.v2.family.family_map import ALL_FACTORS

    rng = np.random.default_rng(seed)
    logger.info(
        "生成小型测试数据：%d 只股票 × %d 个截面 × %d 个因子",
        n_stocks, n_dates, len(ALL_FACTORS),
    )

    # 生成日期序列（周频，从 2015-01-01 开始）
    base_date = pd.Timestamp("2015-01-01")
    dates = pd.date_range(base_date, periods=n_dates, freq="W-FRI")

    # 生成股票代码（模拟 A 股格式）
    stocks = [f"{600000 + i:06d}.XSHG" for i in range(n_stocks)]

    # 生成因子数据
    n_total = n_stocks * n_dates
    logger.info("生成 %d 行数据...", n_total)

    # 为每个因子生成有轻微时序相关性的截面数据
    # 使用向量化操作避免循环
    factor_data = {}

    # 生成一个"真实信号"因子（用于构造 pchg 的微弱相关性）
    signal_matrix = rng.standard_normal((n_dates, n_stocks))

    for factor_name in ALL_FACTORS:
        # 每个因子 = 信号 * 随机权重 + 噪声
        weight = rng.uniform(-0.3, 0.3)
        noise = rng.standard_normal((n_dates, n_stocks))
        factor_matrix = weight * signal_matrix + noise

        # 随机引入约 5% 的 NaN（模拟真实数据缺失）
        nan_mask = rng.random((n_dates, n_stocks)) < 0.05
        factor_matrix[nan_mask] = np.nan

        factor_data[factor_name] = factor_matrix.flatten()

    # 生成 pchg（下期收益）：与信号有微弱相关性
    # pchg[t] = signal_strength * signal[t] + noise
    pchg_matrix = SIGNAL_STRENGTH * signal_matrix + rng.standard_normal((n_dates, n_stocks)) * 0.05
    # 随机引入约 2% 的 NaN
    pchg_nan = rng.random((n_dates, n_stocks)) < 0.02
    pchg_matrix[pchg_nan] = np.nan

    # 构建 DataFrame
    date_col = np.repeat(dates.strftime("%Y-%m-%d"), n_stocks)
    stock_col = np.tile(stocks, n_dates)

    df = pd.DataFrame({
        "Unnamed: 0": stock_col,
        "date": date_col,
        "pchg": pchg_matrix.flatten(),
        **factor_data,
    })

    # 按 [date, stock_id] 排序
    df = df.sort_values(["date", "Unnamed: 0"]).reset_index(drop=True)

    logger.info("数据生成完成：shape=%s", df.shape)
    logger.info("日期范围：%s ~ %s", df["date"].min(), df["date"].max())
    logger.info("pchg 统计：mean=%.4f, std=%.4f", df["pchg"].mean(), df["pchg"].std())

    # 保存
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info("已保存到：%s（%.1f MB）", output_path, output_path.stat().st_size / 1e6)

    return df


if __name__ == "__main__":
    df = generate_small_dataset()
    print(f"\n✓ 小型测试数据已生成：{OUTPUT_PATH}")
    print(f"  Shape: {df.shape}")
    print(f"  日期范围: {df['date'].min()} ~ {df['date'].max()}")
    print(f"  股票数: {df['Unnamed: 0'].nunique()}")
    print(f"  因子数: {df.shape[1] - 3}")  # 减去 Unnamed:0, date, pchg
