"""
Ledger and Audit System - Records all execution details.

This module provides the台账 (ledger) functionality for the strategy autoresearch system,
recording every iteration's input, modification, execution, output, and decision.

References:
    - Design document section 13: 过程记录与可追溯性
    - Design document section 18.6: 台账与审计
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

# Import ParsedMetrics from scorer to keep definitions unified
from scorer import ParsedMetrics


@dataclass
class IterationRecord:
    """Complete record for a single iteration.

    Attributes:
        iter_id: Iteration identifier (e.g., "0001", "baseline")
        parent_iter_id: Parent iteration ID (empty for baseline)
        champion_source: Source of champion strategy ("baseline" or "iter_xxxx")
        strategy_before_path: Path to strategy script before modification
        strategy_after_path: Path to strategy script after modification
        diff_summary: Summary of changes made
        mutation_summary: Description of mutation applied
        command: Execution command that was run
        start_time: Iteration start timestamp (ISO format)
        end_time: Iteration end timestamp (ISO format)
        backtest_id: Platform backtest ID
        platform_result_path: Path to raw platform result file
        parsed_metrics: Parsed performance metrics
        score: Composite score from objective function
        decision: Decision made ("keep", "rollback", or "crash")
        decision_reason: Reason for the decision
        failure_type: Type of failure if any
            - "code_failure": Syntax error, variable undefined, encoding error
            - "platform_failure": error_exit, save failed, backtest failed
            - "session_failure": Login expired, cookie expired, browser session error
            - "result_failure": Missing metrics, empty result, data anomaly
    """
    iter_id: str
    parent_iter_id: str
    champion_source: str
    strategy_before_path: str
    strategy_after_path: str
    diff_summary: str
    mutation_summary: str
    command: str
    start_time: str
    end_time: str
    backtest_id: str
    platform_result_path: str
    parsed_metrics: ParsedMetrics
    score: float
    decision: str  # keep / rollback / crash
    decision_reason: str
    failure_type: Optional[str] = None  # code_failure / platform_failure / session_failure / result_failure


@dataclass
class ExecutionTimeline:
    """Timeline of execution events for a single iteration.

    Records the timing of key events during iteration execution,
    useful for performance analysis and debugging.

    Attributes:
        copy_env_time: Timestamp when environment was copied
        modify_script_time: Timestamp when strategy script was modified
        submit_platform_time: Timestamp when platform backtest was submitted
        backtest_id_obtained_time: Timestamp when backtest ID was obtained
        result_fetched_time: Timestamp when backtest result was fetched
        decision_made_time: Timestamp when decision was made
    """
    copy_env_time: Optional[str] = None
    modify_script_time: Optional[str] = None
    submit_platform_time: Optional[str] = None
    backtest_id_obtained_time: Optional[str] = None
    result_fetched_time: Optional[str] = None
    decision_made_time: Optional[str] = None


# =============================================================================
# Constants
# =============================================================================

# TSV header for iterations.tsv
TSV_HEADER = (
    "iter_id\tparent_iter_id\tchampion_source\tstrategy_before_path\t"
    "strategy_after_path\tdiff_summary\tmutation_summary\tcommand\t"
    "start_time\tend_time\tbacktest_id\tplatform_result_path\t"
    "annual_return\tmax_drawdown\tsharpe\twin_rate\talpha\tbeta\tstatus\t"
    "score\tdecision\tdecision_reason\tfailure_type"
)

# TSV fields corresponding to header
TSV_FIELDS = [
    "iter_id", "parent_iter_id", "champion_source", "strategy_before_path",
    "strategy_after_path", "diff_summary", "mutation_summary", "command",
    "start_time", "end_time", "backtest_id", "platform_result_path",
    "annual_return", "max_drawdown", "sharpe", "win_rate", "alpha", "beta",
    "status", "score", "decision", "decision_reason", "failure_type"
]


# =============================================================================
# Helper Functions
# =============================================================================

def _format_str_for_tsv(s: str) -> str:
    """Escape a string for TSV output.

    Replaces tabs and newlines with spaces to maintain TSV integrity.
    Handles None values gracefully.

    Args:
        s: Input string (can be None)

    Returns:
        Escaped string safe for TSV
    """
    if s is None:
        return ""
    return str(s).replace("\t", " ").replace("\n", " ").replace("\r", " ")


def _escape_markdown(s: str) -> str:
    """Escape special markdown characters in a string.

    Args:
        s: Input string

    Returns:
        String with markdown special chars escaped
    """
    special_chars = ["\\", "`", "*", "_", "[", "]", "(", ")", "#", "+", "-", ".", "!"]
    result = s
    for char in special_chars:
        result = result.replace(char, "\\" + char)
    return result


def _get_trace_dir(base_path: Path, iter_id: str) -> Path:
    """Get the trace directory for a specific iteration.

    Args:
        base_path: Base directory of the autoresearch project
        iter_id: Iteration ID

    Returns:
        Path to the trace directory
    """
    return base_path / "runs" / f"iter_{iter_id}" / "trace"


def _get_metrics_field(record: IterationRecord, field_name: str) -> str:
    """Get a metrics field value as string.

    Args:
        record: IterationRecord containing parsed_metrics
        field_name: Name of the metrics field

    Returns:
        String representation of the field value
    """
    if hasattr(record.parsed_metrics, field_name):
        value = getattr(record.parsed_metrics, field_name)
        return str(value) if value is not None else ""
    return ""


def _record_to_tsv_row(record: IterationRecord) -> str:
    """Convert an IterationRecord to a TSV row.

    Args:
        record: IterationRecord to convert

    Returns:
        TSV-formatted row string
    """
    metrics = record.parsed_metrics
    values = [
        _format_str_for_tsv(record.iter_id),
        _format_str_for_tsv(record.parent_iter_id),
        _format_str_for_tsv(record.champion_source),
        _format_str_for_tsv(record.strategy_before_path),
        _format_str_for_tsv(record.strategy_after_path),
        _format_str_for_tsv(record.diff_summary),
        _format_str_for_tsv(record.mutation_summary),
        _format_str_for_tsv(record.command),
        _format_str_for_tsv(record.start_time),
        _format_str_for_tsv(record.end_time),
        _format_str_for_tsv(record.backtest_id),
        _format_str_for_tsv(record.platform_result_path),
        str(metrics.annual_return) if metrics.annual_return is not None else "",
        str(metrics.max_drawdown) if metrics.max_drawdown is not None else "",
        str(metrics.sharpe) if metrics.sharpe is not None else "",
        str(metrics.win_rate) if metrics.win_rate is not None else "",
        str(metrics.alpha) if metrics.alpha is not None else "",
        str(metrics.beta) if metrics.beta is not None else "",
        _format_str_for_tsv(metrics.status),
        str(record.score) if record.score is not None else "",
        _format_str_for_tsv(record.decision),
        _format_str_for_tsv(record.decision_reason),
        _format_str_for_tsv(record.failure_type or ""),
    ]
    return "\t".join(values)


def _record_to_json(record: IterationRecord) -> dict:
    """Convert an IterationRecord to a JSON-serializable dict.

    Args:
        record: IterationRecord to convert

    Returns:
        Dictionary suitable for JSON serialization
    """
    result = asdict(record)
    # parsed_metrics is already a dict from asdict
    return result


def _record_to_decision_log(record: IterationRecord) -> str:
    """Generate decision log entry for an iteration.

    Args:
        record: IterationRecord to convert

    Returns:
        Markdown-formatted decision log entry
    """
    metrics = record.parsed_metrics
    annual_return = f"{metrics.annual_return:.2%}" if metrics.annual_return is not None else "N/A"
    max_drawdown = f"{metrics.max_drawdown:.2%}" if metrics.max_drawdown is not None else "N/A"
    sharpe = f"{metrics.sharpe:.3f}" if metrics.sharpe is not None else "N/A"
    score = f"{record.score:.4f}" if record.score is not None else "N/A"

    entry = f"""## Iteration {record.iter_id}

### 修改内容
{record.mutation_summary}

### 执行命令
```
{record.command}
```

### 执行时间
{record.start_time} - {record.end_time}

### 回测结果
- backtest_id: {record.backtest_id}
- 年化收益: {annual_return}
- 最大回撤: {max_drawdown}
- 夏普: {sharpe}
- 得分: {score}

### 决策
{record.decision}: {record.decision_reason}
"""
    return entry


# =============================================================================
# Core Functions
# =============================================================================

def init_ledger(base_path: str | Path) -> None:
    """Initialize the ledger directory and files.

    Creates the following files:
        - ledger/iterations.tsv (with header)
        - ledger/iterations.jsonl (empty, ready for append)
        - ledger/decision_log.md (with title)

    Args:
        base_path: Base directory of the autoresearch project
            (e.g., /path/to/strategy_autoresearch_rfscore7/)

    Raises:
        OSError: If directory creation fails or permission denied
    """
    base_path = Path(base_path)
    ledger_dir = base_path / "ledger"

    # Create ledger directory if it doesn't exist
    ledger_dir.mkdir(parents=True, exist_ok=True)

    # Create iterations.tsv with header
    tsv_path = ledger_dir / "iterations.tsv"
    if not tsv_path.exists():
        with open(tsv_path, "w", encoding="utf-8") as f:
            f.write(TSV_HEADER + "\n")

    # Create iterations.jsonl (empty file, ready for append)
    jsonl_path = ledger_dir / "iterations.jsonl"
    if not jsonl_path.exists():
        jsonl_path.touch()

    # Create decision_log.md with title
    decision_log_path = ledger_dir / "decision_log.md"
    if not decision_log_path.exists():
        with open(decision_log_path, "w", encoding="utf-8") as f:
            f.write("# Decision Log\n\n")
            f.write("This log records all iteration decisions and their rationale.\n\n")


def append_iteration(base_path: str | Path, record: IterationRecord) -> None:
    """Append an iteration record to all ledger files.

    Appends the record to:
        - ledger/iterations.tsv (tab-separated)
        - ledger/iterations.jsonl (one JSON object per line)
        - ledger/decision_log.md (markdown entry)

    Args:
        base_path: Base directory of the autoresearch project
        record: IterationRecord to append

    Raises:
        FileNotFoundError: If ledger files don't exist (call init_ledger first)
        OSError: If file write fails
    """
    base_path = Path(base_path)
    ledger_dir = base_path / "ledger"

    tsv_path = ledger_dir / "iterations.tsv"
    jsonl_path = ledger_dir / "iterations.jsonl"
    decision_log_path = ledger_dir / "decision_log.md"

    # Validate files exist
    if not all(p.exists() for p in [tsv_path, jsonl_path, decision_log_path]):
        raise FileNotFoundError(
            "Ledger files not found. Call init_ledger() first to initialize the ledger."
        )

    # Append to iterations.tsv
    tsv_row = _record_to_tsv_row(record)
    with open(tsv_path, "a", encoding="utf-8") as f:
        f.write(tsv_row + "\n")

    # Append to iterations.jsonl
    json_record = _record_to_json(record)
    with open(jsonl_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(json_record, ensure_ascii=False) + "\n")

    # Append to decision_log.md
    decision_entry = _record_to_decision_log(record)
    with open(decision_log_path, "a", encoding="utf-8") as f:
        f.write(decision_entry + "\n")


def save_execution_timeline(
    base_path: str | Path,
    iter_id: str,
    timeline: ExecutionTimeline
) -> None:
    """Save execution timeline for a specific iteration.

    Saves to: runs/iter_xxxx/trace/execution_timeline.json

    Args:
        base_path: Base directory of the autoresearch project
        iter_id: Iteration ID (e.g., "0001", "baseline")
        timeline: ExecutionTimeline to save

    Raises:
        OSError: If directory creation or file write fails
    """
    base_path = Path(base_path)
    trace_dir = _get_trace_dir(base_path, iter_id)

    # Create trace directory if it doesn't exist
    trace_dir.mkdir(parents=True, exist_ok=True)

    # Save execution_timeline.json
    timeline_path = trace_dir / "execution_timeline.json"
    timeline_dict = asdict(timeline)

    with open(timeline_path, "w", encoding="utf-8") as f:
        json.dump(timeline_dict, f, indent=2, ensure_ascii=False)


def load_execution_timeline(
    base_path: str | Path,
    iter_id: str
) -> ExecutionTimeline:
    """Load execution timeline for a specific iteration.

    Args:
        base_path: Base directory of the autoresearch project
        iter_id: Iteration ID (e.g., "0001", "baseline")

    Returns:
        ExecutionTimeline object loaded from file

    Raises:
        FileNotFoundError: If timeline file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
    """
    base_path = Path(base_path)
    timeline_path = _get_trace_dir(base_path, iter_id) / "execution_timeline.json"

    if not timeline_path.exists():
        raise FileNotFoundError(f"Timeline file not found: {timeline_path}")

    with open(timeline_path, "r", encoding="utf-8") as f:
        timeline_dict = json.load(f)

    return ExecutionTimeline(**timeline_dict)


def load_iterations(base_path: str | Path) -> list[IterationRecord]:
    """Load all iteration records from the ledger.

    Reads from ledger/iterations.jsonl and returns a list of IterationRecord objects.

    Args:
        base_path: Base directory of the autoresearch project

    Returns:
        List of IterationRecord objects, ordered as they appear in the file

    Raises:
        FileNotFoundError: If ledger file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
    """
    base_path = Path(base_path)
    jsonl_path = base_path / "ledger" / "iterations.jsonl"

    if not jsonl_path.exists():
        raise FileNotFoundError(f"Ledger file not found: {jsonl_path}")

    records = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record_dict = json.loads(line)
            # parsed_metrics is nested dict, convert to ParsedMetrics
            if "parsed_metrics" in record_dict:
                record_dict["parsed_metrics"] = ParsedMetrics(**record_dict["parsed_metrics"])
            records.append(IterationRecord(**record_dict))

    return records


def get_champion_iter_id(base_path: str | Path) -> str | None:
    """Get the iteration ID of the current champion.

    Returns the iter_id of the most recent 'keep' decision.

    Args:
        base_path: Base directory of the autoresearch project

    Returns:
        Iteration ID of champion, or None if no champion found
    """
    try:
        records = load_iterations(base_path)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    # Find most recent 'keep' decision
    champion_id = None
    for record in records:
        if record.decision == "keep":
            champion_id = record.iter_id

    return champion_id


def get_latest_iter_id(base_path: str | Path) -> str | None:
    """Get the iteration ID of the most recent iteration.

    Args:
        base_path: Base directory of the autoresearch project

    Returns:
        Most recent iteration ID, or None if no iterations exist
    """
    try:
        records = load_iterations(base_path)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    if not records:
        return None

    # Sort by iter_id and return the last one
    # Assuming iter_id format like "0001", "0002", etc.
    sorted_records = sorted(records, key=lambda r: r.iter_id)
    return sorted_records[-1].iter_id
