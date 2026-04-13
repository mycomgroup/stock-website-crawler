"""
Unit tests for TSV format of iterations.tsv in run_iteration.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from run_iteration_wizard import append_tsv, TSV_HEADER


def test_tsv_header_columns():
    columns = TSV_HEADER.strip().split("\t")
    expected = ["iter", "backtest_id", "status", "annual_return", "max_drawdown", "sharpe", "score", "decision", "mutation"]
    assert len(columns) == 9
    assert columns == expected


def test_append_tsv_creates_file_with_header(tmp_path):
    exp_dir = tmp_path / "exp"
    history_dir = exp_dir / "history"
    history_dir.mkdir(parents=True)

    row = {
        "iter": "0001",
        "backtest_id": "7973201",
        "status": "finished",
        "annual_return": 0.15,
        "max_drawdown": 0.12,
        "sharpe": 1.2,
        "score": 1.234,
        "decision": "keep",
        "mutation": "add_filter: pe_ratio < 20",
    }

    append_tsv(exp_dir, row)

    tsv_path = history_dir / "iterations.tsv"
    assert tsv_path.exists()

    lines = tsv_path.read_text(encoding="utf-8").splitlines()
    assert lines[0] == TSV_HEADER.strip()
    assert "0001" in lines[1]
    assert "7973201" in lines[1]


def test_append_tsv_multiple_rows(tmp_path):
    exp_dir = tmp_path / "exp"
    history_dir = exp_dir / "history"
    history_dir.mkdir(parents=True)

    for i in range(3):
        row = {
            "iter": f"{i:04d}",
            "backtest_id": f"100{i}",
            "status": "finished",
            "annual_return": 0.10 + i * 0.01,
            "max_drawdown": 0.10,
            "sharpe": 1.0,
            "score": 1.0 + i * 0.1,
            "decision": "keep",
            "mutation": f"mutation_{i}",
        }
        append_tsv(exp_dir, row)

    content = (history_dir / "iterations.tsv").read_text(encoding="utf-8")
    lines = [l for l in content.splitlines() if l.strip()]
    # 1 header + 3 data rows
    assert len(lines) == 4


def test_tsv_row_format(tmp_path):
    exp_dir = tmp_path / "exp"
    history_dir = exp_dir / "history"
    history_dir.mkdir(parents=True)

    row = {
        "iter": "0001",
        "backtest_id": "9999",
        "status": "finished",
        "annual_return": 0.15,
        "max_drawdown": 0.08,
        "sharpe": 1.5,
        "score": 1.234,
        "decision": "keep",
        "mutation": "adjust_holding_num: 15 → 20",
    }

    append_tsv(exp_dir, row)

    lines = (history_dir / "iterations.tsv").read_text(encoding="utf-8").splitlines()
    data_line = lines[1]
    fields = data_line.split("\t")

    assert len(fields) == 9
    # annual_return formatted as 4 decimal places
    assert fields[3] == "0.1500"
    # score formatted as 6 decimal places
    assert fields[6] == "1.234000"
