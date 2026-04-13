"""
Unit tests for setup.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from init_experiment import _make_initial_state, TSV_HEADER


def test_initial_state_fields():
    state = _make_initial_state("123456")
    assert state["current_iter"] == 0
    assert state["strategy_id"] == "123456"
    assert state["champion_score"] == -1e308
    assert state["champion_iter"] == ""
    assert state["champion_config"] is None
    assert state["champion_metrics"] is None
    assert state["consecutive_failures"] == 0
    assert "last_update" in state


def test_tsv_header_format():
    assert TSV_HEADER.startswith("iter\t")
    columns = TSV_HEADER.strip().split("\t")
    expected = ["iter", "backtest_id", "status", "annual_return", "max_drawdown", "sharpe", "score", "decision", "mutation"]
    assert columns == expected


def test_experiment_directory_creation(tmp_path):
    # Create directory structure manually (simulating what init_experiment.main() does)
    exp_dir = tmp_path / "experiments" / "test_exp"
    history_dir = exp_dir / "history"
    history_dir.mkdir(parents=True)

    # Load seed config from actual seed file
    seed_path = Path(__file__).parent.parent / "seed_wizard_config.json"
    with open(seed_path, encoding="utf-8") as f:
        seed_config = json.load(f)

    # Write wizard_config.json
    wizard_config_path = exp_dir / "wizard_config.json"
    with open(wizard_config_path, "w", encoding="utf-8") as f:
        json.dump(seed_config, f, ensure_ascii=False, indent=2)

    # Write state.json
    state = _make_initial_state("654321")
    state_path = exp_dir / "state.json"
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    # Write history/0000_config.json
    snapshot_path = history_dir / "0000_config.json"
    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump(seed_config, f, ensure_ascii=False, indent=2)

    # Write history/iterations.tsv with header
    tsv_path = history_dir / "iterations.tsv"
    with open(tsv_path, "w", encoding="utf-8") as f:
        f.write(TSV_HEADER)

    # Verify all files exist
    assert wizard_config_path.exists()
    assert state_path.exists()
    assert snapshot_path.exists()
    assert tsv_path.exists()

    # Verify wizard_config.json content
    with open(wizard_config_path, encoding="utf-8") as f:
        loaded_config = json.load(f)
    assert loaded_config == seed_config

    # Verify state.json content
    with open(state_path, encoding="utf-8") as f:
        loaded_state = json.load(f)
    assert loaded_state["current_iter"] == 0
    assert loaded_state["strategy_id"] == "654321"
    assert loaded_state["champion_score"] == -1e308

    # Verify history/0000_config.json matches seed
    with open(snapshot_path, encoding="utf-8") as f:
        loaded_snapshot = json.load(f)
    assert loaded_snapshot == seed_config

    # Verify iterations.tsv has correct header
    with open(tsv_path, encoding="utf-8") as f:
        content = f.read()
    assert content == TSV_HEADER
