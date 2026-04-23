from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from common import Thresholds, write_json, dataclass_to_dict


@dataclass
class BaselineConfig:
    strategy_name: str
    universe: list[str]
    rebalance_freq: str
    hold_count_max: int
    risk_budget: float
    thresholds: Thresholds
    fallback_to_cash: bool


def freeze_baseline_config() -> BaselineConfig:
    """子任务1：主仓底座统一与冻结。"""
    return BaselineConfig(
        strategy_name="low_freq_main_base_v1",
        universe=["HS300", "CSI500"],
        rebalance_freq="monthly",
        hold_count_max=15,
        risk_budget=1.0,
        thresholds=Thresholds(),
        fallback_to_cash=True,
    )


def export_baseline(config: BaselineConfig, output_path: str) -> None:
    payload: dict[str, Any] = dataclass_to_dict(config)
    payload["thresholds"] = dataclass_to_dict(config.thresholds)
    write_json(payload, output_path)
