#!/usr/bin/env python3
"""独立执行器：尽量在本地执行 strategy.py 并解析最后一行 JSON。"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


def execute_strategy(strategy_path: str, timeout_ms: int = 600000, notebook_dir: str | None = None):
    strategy = Path(strategy_path)
    if not strategy.exists():
        return {"success": False, "error": f"strategy_not_found: {strategy}"}

    cwd = Path(notebook_dir) if notebook_dir else strategy.parent
    try:
        proc = subprocess.run(
            ["python", str(strategy)],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=max(1, timeout_ms // 1000),
        )
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "timeout"}
    except Exception as e:
        return {"success": False, "error": f"exec_error: {e}"}

    stdout = (proc.stdout or "").strip().splitlines()
    stderr = (proc.stderr or "").strip()

    if proc.returncode != 0:
        return {
            "success": False,
            "error": f"returncode={proc.returncode}",
            "stderr": stderr,
            "stdout_tail": stdout[-5:],
        }

    if not stdout:
        return {"success": False, "error": "empty_stdout", "stderr": stderr}

    try:
        payload = json.loads(stdout[-1])
    except Exception:
        return {
            "success": False,
            "error": "invalid_json_output",
            "stdout_tail": stdout[-5:],
            "stderr": stderr,
        }

    return {
        "success": True,
        "score": payload.get("score", 0.0),
        "payload": payload,
        "stderr": stderr,
    }
