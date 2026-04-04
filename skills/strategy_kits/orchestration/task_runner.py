"""Unified task runner for skill-driven single-strategy research."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Mapping, Optional, Type

import pandas as pd

from ..contracts import validate_prediction_frame
from ..core import get_logger, log_kv
from ..core.errors import ErrorCode, StrategyKitsError
from ..execution.backtrader_runtime import BacktraderConfig, run_backtest
from ..integrations.factorhub import (
    load_pool_panel,
    load_score_panel,
    pool_panel_to_prediction_frame,
    score_panel_to_prediction_frame,
)
from ..strategy_templates.presets import (
    DirectExecutionStrategy,
    EqualWeightStrategy,
    WeightedTopNStrategy,
)
from .artifacts import persist_platform_artifacts, persist_task_artifacts
from .task_schema import validate_strategy_task_spec

_logger = get_logger("orchestration.task_runner")


_TEMPLATE_REGISTRY: dict[str, Type] = {
    "WeightedTopNStrategy": WeightedTopNStrategy,
    "EqualWeightStrategy": EqualWeightStrategy,
    "DirectExecutionStrategy": DirectExecutionStrategy,
}


def _resolve_strategy_template(name: str) -> Type:
    if name in _TEMPLATE_REGISTRY:
        return _TEMPLATE_REGISTRY[name]
    raise StrategyKitsError(
        ErrorCode.CONTRACT_INVALID_VALUE,
        f"Unknown strategy template: {name}",
        details={"available_templates": sorted(_TEMPLATE_REGISTRY.keys())},
    )


def _load_local_prediction_frame(path: str | Path) -> pd.DataFrame:
    file_path = Path(path)
    suffix = file_path.suffix.lower()
    if suffix == ".csv":
        df = pd.read_csv(file_path)
    elif suffix in {".parquet", ".pq"}:
        df = pd.read_parquet(file_path)
    elif suffix == ".json":
        df = pd.read_json(file_path)
    else:
        raise StrategyKitsError(
            ErrorCode.CONTRACT_INVALID_VALUE,
            f"Unsupported prediction_path suffix: {suffix}",
            details={"path": str(file_path)},
        )
    return validate_prediction_frame(df)


def build_prediction_frame_from_task(spec: Mapping[str, Any]) -> pd.DataFrame:
    """Build template-ready prediction frame from normalized task spec."""
    data = dict(spec["data"])
    pipeline = dict(spec.get("pipeline", {}))

    panel_type = data["panel_type"]
    top_n = int(pipeline.get("top_n", 20))
    weight_mode = str(pipeline.get("weight_mode", "score"))

    if panel_type == "pool_panel":
        panel = load_pool_panel(data["panel_path"])
        pred_df = pool_panel_to_prediction_frame(panel, top_n=top_n, weight_mode=weight_mode)  # type: ignore[arg-type]
    elif panel_type == "score_panel":
        panel = load_score_panel(data["panel_path"])
        pred_df = score_panel_to_prediction_frame(panel, top_n=top_n, weight_mode=weight_mode)  # type: ignore[arg-type]
    elif panel_type == "local_features":
        prediction_path = data.get("prediction_path")
        if not isinstance(prediction_path, str):
            raise StrategyKitsError(
                ErrorCode.CONTRACT_MISSING_COLUMN,
                "data.prediction_path is required when panel_type=local_features",
            )
        pred_df = _load_local_prediction_frame(prediction_path)
    else:
        raise StrategyKitsError(
            ErrorCode.CONTRACT_INVALID_VALUE,
            f"Unsupported panel_type: {panel_type}",
            details={"panel_type": panel_type},
        )

    log_kv(
        _logger,
        20,
        "prediction_frame_built",
        panel_type=panel_type,
        rows=len(pred_df),
        unique_codes=pred_df["code"].nunique() if "code" in pred_df.columns else 0,
    )
    return pred_df


def run_strategy_task(
    raw_spec: Mapping[str, Any],
    data_bundle: Optional[dict[str, Any]] = None,
    persist_artifacts: Optional[bool] = None,
) -> dict[str, Any]:
    """Validate task spec and execute template backtest.

    Supports two execution engines:
    - platform.engine = "local"      → backtrader (default)
    - platform.engine = "joinquant"  → JoinQuant cloud backtest
    - platform.engine = "ricequant"  → RiceQuant cloud backtest
    """
    spec = validate_strategy_task_spec(raw_spec)
    engine = spec.get("platform", {}).get("engine", "local")

    if engine in {"joinquant", "ricequant"}:
        return _run_platform_task(spec, persist_artifacts)

    # ── local backtrader path ─────────────────────────────────────────────────
    pred_df = build_prediction_frame_from_task(spec)
    if pred_df.empty:
        raise StrategyKitsError(
            ErrorCode.CONTRACT_INVALID_VALUE,
            "prediction frame is empty after preprocessing",
        )

    strategy_name = spec["backtest"]["template"]
    strategy_cls = _resolve_strategy_template(strategy_name)

    symbols = sorted(pred_df["code"].astype(str).unique().tolist()) if data_bundle is None else []
    cfg = BacktraderConfig(
        start_date=spec["data"]["start_date"],
        end_date=spec["data"]["end_date"],
        symbols=symbols,
        initial_cash=float(spec["backtest"]["initial_cash"]),
        benchmark=spec["backtest"].get("benchmark"),
        printlog=bool(spec["backtest"].get("printlog", False)),
        tradehistory=bool(spec["backtest"].get("tradehistory", False)),
        strategy_params={
            "pred_df": pred_df,
            "rebalance_threshold": float(spec["backtest"]["rebalance_threshold"]),
            "hold_days": int(spec["backtest"]["hold_days"]),
            "top_n_stocks": int(spec["pipeline"]["top_n"]),
        },
    )

    log_kv(
        _logger,
        20,
        "strategy_task_started",
        task_id=spec["task"]["task_id"],
        strategy_name=spec["task"]["strategy_name"],
        template=strategy_name,
        start_date=spec["data"]["start_date"],
        end_date=spec["data"]["end_date"],
        prediction_rows=len(pred_df),
    )
    result = run_backtest(cfg, strategy_cls, data_bundle=data_bundle)
    result["task_spec"] = spec
    result["pred_df"] = pred_df

    should_persist = spec["output"]["save_artifacts"] if persist_artifacts is None else bool(persist_artifacts)
    if should_persist:
        artifact_manifest = persist_task_artifacts(
            result=result,
            spec=spec,
            artifact_dir=spec["output"]["artifact_dir"],
        )
        result["artifact_manifest"] = artifact_manifest

    log_kv(
        _logger,
        20,
        "strategy_task_finished",
        task_id=spec["task"]["task_id"],
        portfolio_value=float(result.get("portfolio_value", 0.0)),
        persisted_artifacts=should_persist,
    )
    return result


# ── 云平台执行路径 ─────────────────────────────────────────────────────────────

_PLATFORM_SKILL_DIRS = {
    "joinquant": Path(__file__).parent.parent.parent / "joinquant_strategy",
    "ricequant": Path(__file__).parent.parent.parent / "ricequant_strategy",
}


def _run_platform_task(
    spec: Mapping[str, Any],
    persist_artifacts: Optional[bool] = None,
) -> dict[str, Any]:
    """Execute strategy on a cloud platform via run-skill.js."""
    platform_cfg = dict(spec.get("platform", {}))
    engine = platform_cfg["engine"]
    strategy_id = platform_cfg["strategy_id"]
    strategy_file = platform_cfg["strategy_file"]
    start_date = spec["data"]["start_date"]
    end_date = spec["data"]["end_date"]
    capital = str(int(spec["backtest"]["initial_cash"]))
    freq = platform_cfg.get("freq", "day")

    skill_dir = _PLATFORM_SKILL_DIRS.get(engine)
    if skill_dir is None or not skill_dir.exists():
        raise StrategyKitsError(
            ErrorCode.CONTRACT_INVALID_VALUE,
            f"Platform skill directory not found for engine: {engine}",
            details={"expected_dir": str(skill_dir)},
        )

    if not Path(strategy_file).exists():
        raise StrategyKitsError(
            ErrorCode.CONTRACT_INVALID_VALUE,
            f"strategy_file not found: {strategy_file}",
        )

    cmd = [
        "node", "run-skill.js",
        "--id", strategy_id,
        "--file", str(Path(strategy_file).resolve()),
        "--start", start_date,
        "--end", end_date,
        "--capital", capital,
        "--freq", freq,
    ]

    log_kv(
        _logger,
        20,
        "platform_task_started",
        engine=engine,
        task_id=spec["task"]["task_id"],
        strategy_id=strategy_id,
        start_date=start_date,
        end_date=end_date,
    )

    try:
        proc = subprocess.run(
            cmd,
            cwd=str(skill_dir),
            capture_output=True,
            text=True,
            timeout=platform_cfg.get("timeout_seconds", 600),
        )
    except subprocess.TimeoutExpired as exc:
        raise StrategyKitsError(
            ErrorCode.CONTRACT_INVALID_VALUE,
            f"Platform backtest timed out after {platform_cfg.get('timeout_seconds', 600)}s",
        ) from exc

    stdout = proc.stdout or ""
    stderr = proc.stderr or ""

    if proc.returncode != 0:
        raise StrategyKitsError(
            ErrorCode.CONTRACT_INVALID_VALUE,
            f"Platform run-skill.js exited with code {proc.returncode}",
            details={"stderr": stderr[-2000:], "stdout": stdout[-2000:]},
        )

    # 解析终端输出里的关键指标
    metrics = _parse_platform_stdout(stdout)

    result: dict[str, Any] = {
        "engine": engine,
        "strategy_id": strategy_id,
        "stdout": stdout,
        "stderr": stderr,
        "returncode": proc.returncode,
        "metrics": metrics,
        "portfolio_value": metrics.get("portfolio_value", 0.0),
        "task_spec": spec,
    }

    # 尝试找最新的 output JSON 文件
    output_dir = skill_dir / "output"
    if output_dir.exists():
        json_files = sorted(output_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        if json_files:
            try:
                result["platform_report"] = json.loads(json_files[0].read_text(encoding="utf-8"))
                result["platform_report_path"] = str(json_files[0])
            except Exception:
                pass

    should_persist = spec["output"]["save_artifacts"] if persist_artifacts is None else bool(persist_artifacts)
    if should_persist:
        artifact_manifest = persist_platform_artifacts(
            result=result,
            spec=spec,
            artifact_dir=spec["output"]["artifact_dir"],
        )
        result["artifact_manifest"] = artifact_manifest

    log_kv(
        _logger,
        20,
        "platform_task_finished",
        engine=engine,
        task_id=spec["task"]["task_id"],
        returncode=proc.returncode,
        metrics=metrics,
    )
    return result


def _parse_platform_stdout(stdout: str) -> dict[str, Any]:
    """从 run-skill.js 的终端输出里提取关键指标。"""
    metrics: dict[str, Any] = {}
    for line in stdout.splitlines():
        line = line.strip()
        # JoinQuant / RiceQuant 输出格式：  "Total Return: 12.34 %"
        for key, patterns in {
            "total_return": ["Total Return:", "总收益:"],
            "annual_return": ["Annual Return:", "年化收益:"],
            "max_drawdown": ["Max Drawdown:", "最大回撤:"],
            "sharpe": ["Sharpe Ratio:", "夏普比率:"],
        }.items():
            for pat in patterns:
                if pat in line:
                    try:
                        val_str = line.split(pat, 1)[1].strip().rstrip("%").strip()
                        metrics[key] = float(val_str)
                    except (ValueError, IndexError):
                        pass
        # Backtest ID
        if "Backtest started! ID:" in line or "回测ID:" in line:
            try:
                metrics["backtest_id"] = line.split(":", 1)[1].strip()
            except IndexError:
                pass
    return metrics
