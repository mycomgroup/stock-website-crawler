"""
Unit tests for keep/rollback file update logic in run_iteration.py
"""
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from run_iteration_wizard import load_json, save_json, append_tsv, _write_result, _update_state, TSV_HEADER


def _make_exp_dir(tmp_path):
    """Helper: create a minimal experiment directory."""
    exp_dir = tmp_path / "exp"
    history_dir = exp_dir / "history"
    history_dir.mkdir(parents=True)
    return exp_dir, history_dir


def test_keep_updates_wizard_config(tmp_path):
    exp_dir, history_dir = _make_exp_dir(tmp_path)

    old_config = {"name": "old", "maxHoldingNum": 10}
    new_config = {"name": "new", "maxHoldingNum": 20}

    wizard_config_path = exp_dir / "wizard_config.json"
    save_json(wizard_config_path, old_config)

    # Simulate keep: save new_config to wizard_config.json
    save_json(wizard_config_path, new_config)

    loaded = load_json(wizard_config_path)
    assert loaded == new_config
    assert loaded["maxHoldingNum"] == 20


def test_rollback_restores_wizard_config(tmp_path):
    exp_dir, history_dir = _make_exp_dir(tmp_path)

    current_config = {"name": "current", "maxHoldingNum": 20}
    champion_config = {"name": "champion", "maxHoldingNum": 15}

    wizard_config_path = exp_dir / "wizard_config.json"
    save_json(wizard_config_path, current_config)

    # Save champion config in history
    champion_config_path = history_dir / "0001_config.json"
    save_json(champion_config_path, champion_config)

    # Simulate rollback: restore wizard_config.json from champion
    restored = load_json(champion_config_path)
    save_json(wizard_config_path, restored)

    loaded = load_json(wizard_config_path)
    assert loaded == champion_config
    assert loaded["maxHoldingNum"] == 15


def test_write_result_creates_json(tmp_path):
    exp_dir, history_dir = _make_exp_dir(tmp_path)

    start_time = datetime.now()
    _write_result(
        base=exp_dir,
        iter_id="0001",
        backtest_id="7973201",
        status="finished",
        annual_return=0.15,
        max_drawdown=0.12,
        sharpe=1.2,
        sortino=1.5,
        information_ratio=0.8,
        score=1.234,
        decision="keep",
        reason="new_score > champion_score",
        mutation="add_filter: pe_ratio < 20",
        mutation_type="add_filter",
        start_time=start_time,
    )

    result_path = history_dir / "0001.json"
    assert result_path.exists()

    record = load_json(result_path)
    assert record["iter"] == "0001"
    assert record["backtest_id"] == "7973201"
    assert record["status"] == "finished"
    assert record["annual_return"] == 0.15
    assert record["score"] == 1.234
    assert record["decision"] == "keep"
    assert record["mutation_type"] == "add_filter"


def test_update_state_keep(tmp_path):
    exp_dir, _ = _make_exp_dir(tmp_path)

    state = {
        "current_iter": 0,
        "strategy_id": "123456",
        "champion_score": float("-inf"),
        "champion_iter": "",
        "champion_config": None,
        "champion_metrics": None,
        "consecutive_failures": 2,
        "last_update": "",
    }
    save_json(exp_dir / "state.json", state)

    _update_state(
        state=state,
        base=exp_dir,
        iter_n=0,
        decision="keep",
        new_champion_score=1.5,
        new_champion_iter="0000",
        new_champion_metrics={"annual_return": 0.15, "max_drawdown": 0.12},
    )

    assert state["current_iter"] == 1
    assert state["champion_score"] == 1.5
    assert state["champion_iter"] == "0000"
    assert state["consecutive_failures"] == 0


def test_update_state_rollback(tmp_path):
    exp_dir, _ = _make_exp_dir(tmp_path)

    state = {
        "current_iter": 3,
        "strategy_id": "123456",
        "champion_score": 1.5,
        "champion_iter": "0001",
        "champion_config": None,
        "champion_metrics": None,
        "consecutive_failures": 2,
        "last_update": "",
    }
    save_json(exp_dir / "state.json", state)

    _update_state(
        state=state,
        base=exp_dir,
        iter_n=3,
        decision="rollback",
        new_champion_score=1.5,
        new_champion_iter=None,
        new_champion_metrics=None,
    )

    assert state["current_iter"] == 4
    assert state["consecutive_failures"] == 3
