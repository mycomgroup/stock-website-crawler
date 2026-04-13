"""
Unit tests for _recover_state function in run_iteration.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from run_iteration_wizard import _recover_state, load_json, save_json


def _make_exp_dir(tmp_path):
    """Helper: create a minimal experiment directory."""
    exp_dir = tmp_path / "exp"
    history_dir = exp_dir / "history"
    history_dir.mkdir(parents=True)
    return exp_dir, history_dir


def test_recover_consistent_state(tmp_path):
    """State is consistent: current_iter=2, history/0001.json exists."""
    exp_dir, history_dir = _make_exp_dir(tmp_path)

    state = {
        "current_iter": 2,
        "strategy_id": "123456",
        "champion_score": 1.5,
        "champion_iter": "0001",
        "champion_config": None,
        "champion_metrics": None,
        "consecutive_failures": 0,
        "last_update": "",
    }
    save_json(exp_dir / "state.json", state)

    # Create history/0001.json (champion history)
    save_json(history_dir / "0001.json", {"iter": "0001", "score": 1.5})
    # Create history/0001_config.json (champion config)
    save_json(history_dir / "0001_config.json", {"name": "champion"})
    # Create history/0001.json for current_iter-1 = 1
    # (already created above as 0001.json)

    result = _recover_state(exp_dir, state)

    # State should not be modified
    assert result["current_iter"] == 2


def test_recover_missing_last_iter_json(tmp_path):
    """current_iter=3 but history/0002.json is missing → roll back to 2."""
    exp_dir, history_dir = _make_exp_dir(tmp_path)

    state = {
        "current_iter": 3,
        "strategy_id": "123456",
        "champion_score": 1.5,
        "champion_iter": "0001",
        "champion_config": None,
        "champion_metrics": None,
        "consecutive_failures": 0,
        "last_update": "",
    }
    save_json(exp_dir / "state.json", state)

    # Create champion history files
    save_json(history_dir / "0001.json", {"iter": "0001", "score": 1.5})
    save_json(history_dir / "0001_config.json", {"name": "champion"})
    # Do NOT create history/0002.json

    result = _recover_state(exp_dir, state)

    assert result["current_iter"] == 2


def test_recover_missing_champion_history(tmp_path):
    """champion_iter=0001 but history/0001.json is missing → clear champion info."""
    exp_dir, history_dir = _make_exp_dir(tmp_path)

    state = {
        "current_iter": 2,
        "strategy_id": "123456",
        "champion_score": 1.5,
        "champion_iter": "0001",
        "champion_config": None,
        "champion_metrics": None,
        "consecutive_failures": 0,
        "last_update": "",
    }
    save_json(exp_dir / "state.json", state)

    # Create history/0001.json for current_iter-1 check (iter 1)
    # but do NOT create history/0001.json for champion check
    # Note: current_iter=2, so _recover_state checks history/0001.json for both
    # the last-iter check AND the champion check. We need to be careful here.
    # current_iter-1 = 1, so it checks history/0001.json for last iter.
    # champion_iter = "0001", so it also checks history/0001.json for champion.
    # Since we don't create it, both checks fail.
    # The last-iter check runs first and rolls back current_iter to 1.
    # Then champion check runs and clears champion info.

    result = _recover_state(exp_dir, state)

    assert result["champion_score"] == float("-inf")
    assert result["champion_iter"] == ""


def test_recover_restores_wizard_config(tmp_path):
    """Missing last iter json triggers rollback and restores wizard_config from champion."""
    exp_dir, history_dir = _make_exp_dir(tmp_path)

    champion_config = {"name": "champion_config", "maxHoldingNum": 15}

    state = {
        "current_iter": 2,
        "strategy_id": "123456",
        "champion_score": 1.5,
        "champion_iter": "0001",
        "champion_config": None,
        "champion_metrics": None,
        "consecutive_failures": 0,
        "last_update": "",
    }
    save_json(exp_dir / "state.json", state)

    # Create champion config in history
    save_json(history_dir / "0001_config.json", champion_config)
    # Create champion history json so champion check passes
    save_json(history_dir / "0001.json", {"iter": "0001", "score": 1.5})
    # Do NOT create history/0001.json for last iter (current_iter-1=1)
    # Wait - 0001.json IS created above. Let's use current_iter=3 instead.

    # Redo with current_iter=3 so last iter check looks for 0002.json
    state["current_iter"] = 3
    save_json(exp_dir / "state.json", state)

    # Write a current (non-champion) wizard_config
    save_json(exp_dir / "wizard_config.json", {"name": "current", "maxHoldingNum": 20})

    # Do NOT create history/0002.json → triggers rollback
    result = _recover_state(exp_dir, state)

    # wizard_config.json should be restored from champion
    loaded = load_json(exp_dir / "wizard_config.json")
    assert loaded == champion_config
    assert loaded["maxHoldingNum"] == 15
