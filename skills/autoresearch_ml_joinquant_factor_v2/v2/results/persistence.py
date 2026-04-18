"""结果落盘模块 (Task 8.2, 8.3)

实现 OOF 预测、inner loop 结果、outer loop 结果分别保存，
以及参数快照（参数配置、数据版本、随机种子）。

**Validates: Requirements 12**
"""

from __future__ import annotations

import hashlib
import json
import logging
import pickle
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Task 8.2: 结果落盘
# ---------------------------------------------------------------------------


def save_oof_predictions(
    predictions: pd.Series,
    output_dir: str | Path,
    run_id: str | None = None,
) -> Path:
    """保存 OOF 预测结果。

    Parameters
    ----------
    predictions : pd.Series
        OOF 预测，indexed by (date, stock_id)。
    output_dir : str | Path
        输出目录。
    run_id : str | None
        运行 ID（默认使用时间戳）。

    Returns
    -------
    Path
        保存的文件路径。
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    run_id = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = output_dir / f"oof_predictions_{run_id}.csv"

    # Convert MultiIndex Series to DataFrame for CSV
    df = predictions.reset_index()
    df.columns = ["date", "stock_id", "oof_prediction"]
    df.to_csv(filepath, index=False)

    logger.info("OOF 预测已保存：%s（%d 行）", filepath, len(df))
    return filepath


def save_inner_loop_results(
    results: list[dict],
    output_dir: str | Path,
    run_id: str | None = None,
) -> Path:
    """保存 inner loop 超参数选择结果。

    Parameters
    ----------
    results : list[dict]
        每个 outer fold 的 inner loop 结果列表。
        每个元素包含：fold_index, best_params, best_score, all_scores。
    output_dir : str | Path
        输出目录。
    run_id : str | None
        运行 ID。

    Returns
    -------
    Path
        保存的文件路径。
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    run_id = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = output_dir / f"inner_loop_results_{run_id}.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)

    logger.info("Inner loop 结果已保存：%s（%d 个 fold）", filepath, len(results))
    return filepath


def save_outer_loop_results(
    results: list[dict],
    output_dir: str | Path,
    run_id: str | None = None,
) -> Path:
    """保存 outer loop 评估结果。

    Parameters
    ----------
    results : list[dict]
        每个 outer fold 的评估结果列表。
        每个元素包含：fold_index, train_dates, test_dates, metrics。
    output_dir : str | Path
        输出目录。
    run_id : str | None
        运行 ID。

    Returns
    -------
    Path
        保存的文件路径。
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    run_id = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = output_dir / f"outer_loop_results_{run_id}.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)

    logger.info("Outer loop 结果已保存：%s（%d 个 fold）", filepath, len(results))
    return filepath


# ---------------------------------------------------------------------------
# Task 8.3: 参数快照
# ---------------------------------------------------------------------------


@dataclass
class RunSnapshot:
    """运行参数快照，确保完全可复现。

    **Validates: Requirements 12.3**
    """

    run_id: str
    timestamp: str
    random_state: int
    data_version: str  # CSV 文件的 MD5 哈希
    config: dict
    git_commit: str | None = None
    python_version: str | None = None
    package_versions: dict | None = None


def compute_data_version(csv_path: str | Path) -> str:
    """计算数据文件的 MD5 哈希，作为数据版本标识。

    Parameters
    ----------
    csv_path : str | Path
        CSV 文件路径。

    Returns
    -------
    str
        MD5 哈希字符串（前 16 位）。
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        logger.warning("数据文件不存在：%s，使用 'unknown' 作为版本", csv_path)
        return "unknown"

    md5 = hashlib.md5()
    with open(csv_path, "rb") as f:
        # 只读取前 10MB 计算哈希（避免大文件耗时过长）
        chunk = f.read(10 * 1024 * 1024)
        md5.update(chunk)

    return md5.hexdigest()[:16]


def save_run_snapshot(
    config: Any,
    output_dir: str | Path,
    run_id: str | None = None,
    csv_path: str | Path | None = None,
) -> Path:
    """保存运行参数快照。

    Parameters
    ----------
    config : Any
        Pipeline 配置对象（dataclass 或 dict）。
    output_dir : str | Path
        输出目录。
    run_id : str | None
        运行 ID（默认使用时间戳）。
    csv_path : str | Path | None
        数据文件路径（用于计算数据版本）。

    Returns
    -------
    Path
        保存的快照文件路径。
    """
    import sys

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    run_id = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")

    # 序列化 config
    if hasattr(config, "__dataclass_fields__"):
        config_dict = asdict(config)
    elif isinstance(config, dict):
        config_dict = config
    else:
        config_dict = {"config": str(config)}

    # 计算数据版本
    data_version = "unknown"
    if csv_path is not None:
        data_version = compute_data_version(csv_path)
    elif "csv_path" in config_dict:
        data_version = compute_data_version(config_dict["csv_path"])

    # 获取 Python 版本
    python_version = sys.version

    # 获取关键包版本
    package_versions = {}
    for pkg in ["pandas", "numpy", "sklearn", "scipy"]:
        try:
            import importlib
            mod = importlib.import_module(pkg)
            package_versions[pkg] = getattr(mod, "__version__", "unknown")
        except ImportError:
            package_versions[pkg] = "not installed"

    # 获取 git commit（可选）
    git_commit = None
    try:
        import subprocess
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            git_commit = result.stdout.strip()
    except Exception:
        pass

    snapshot = RunSnapshot(
        run_id=run_id,
        timestamp=datetime.now().isoformat(),
        random_state=config_dict.get("random_state", 42),
        data_version=data_version,
        config=config_dict,
        git_commit=git_commit,
        python_version=python_version,
        package_versions=package_versions,
    )

    filepath = output_dir / f"run_snapshot_{run_id}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(asdict(snapshot), f, ensure_ascii=False, indent=2, default=str)

    logger.info(
        "运行快照已保存：%s（run_id=%s, data_version=%s）",
        filepath,
        run_id,
        data_version,
    )
    return filepath


def load_run_snapshot(snapshot_path: str | Path) -> RunSnapshot:
    """加载运行参数快照。

    Parameters
    ----------
    snapshot_path : str | Path
        快照文件路径。

    Returns
    -------
    RunSnapshot
        运行参数快照对象。
    """
    with open(snapshot_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return RunSnapshot(**data)
