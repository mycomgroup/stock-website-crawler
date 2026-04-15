#!/usr/bin/env python
# coding: utf-8
"""
Notebook 执行适配器
调用 joinquant_notebook 执行策略，支持创建和复用 Notebook
"""

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, Optional


DEFAULT_SESSION_FILE = str(
    Path(__file__).parent.parent / "joinquant_notebook" / "data" / "session.json"
)
DEFAULT_NOTEBOOK_URL = (
    "https://www.joinquant.com/user/notebook?url=/user/21333940833/notebooks/test.ipynb"
)


def find_notebook_executor() -> Optional[str]:
    """查找 joinquant_notebook 的 run-strategy.js"""
    possible_paths = [
        Path(__file__).parent.parent / "joinquant_notebook" / "run-strategy.js",
        Path(__file__).parent / "joinquant_notebook" / "run-strategy.js",
        Path(os.environ.get("JOINQUANT_NOTEBOOK_DIR", "")) / "run-strategy.js",
    ]

    for p in possible_paths:
        if p.exists():
            return str(p)

    return None


def _run_node(cmd: list, timeout: int = 120) -> Dict:
    """运行 node 命令并解析结果文件"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        output = result.stdout + result.stderr

        # 从输出中找到结果文件路径
        match = re.search(r"结果文件:\s*(.+\.json)", output)
        if match:
            result_file = match.group(1).strip()
            if Path(result_file).exists():
                with open(result_file, "r") as f:
                    return json.load(f)

        return {
            "success": False,
            "error": "找不到结果文件",
            "output": output[-500:],
        }

    except subprocess.TimeoutExpired:
        return {"success": False, "error": "执行超时"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_notebook(
    notebook_name: str,
    notebook_dir: str = None,
) -> Dict:
    """
    创建一个新的 Notebook

    Args:
        notebook_name: Notebook 名称
        notebook_dir: joinquant_notebook 目录路径

    Returns:
        {
            "success": bool,
            "notebook_path": str,
            "notebook_url": str,
            "error": str (if failed)
        }
    """
    if notebook_dir:
        executor = Path(notebook_dir) / "run-strategy.js"
    else:
        executor = find_notebook_executor()

    if not executor or not Path(executor).exists():
        return {
            "success": False,
            "error": f"找不到 run-strategy.js: {executor}",
        }

    init_code = f"# {notebook_name} - 初始化\nprint('Notebook created')"

    cmd = [
        "node",
        str(executor),
        "--cell-source",
        init_code,
        "--notebook-base-name",
        notebook_name,
        "--create-new",
        "true",
        "--session-file",
        DEFAULT_SESSION_FILE,
        "--notebook-url",
        DEFAULT_NOTEBOOK_URL,
    ]

    data = _run_node(cmd, timeout=120)

    if data.get("newNotebookCreated") or data.get("reuseNotebook"):
        return {
            "success": True,
            "notebook_path": data.get("notebookPath", ""),
            "notebook_url": data.get("notebookUrl", ""),
            "reused": data.get("reuseNotebook", False),
        }

    return {
        "success": False,
        "error": data.get("error", "创建失败"),
        "output": data.get("output", ""),
    }


def execute_strategy(
    strategy_file: str,
    notebook_url: str = None,
    timeout_ms: int = 600000,
    notebook_dir: str = None,
) -> Dict:
    """
    通过 Notebook 执行策略文件

    Args:
        strategy_file: 策略文件路径
        notebook_url: Notebook URL（复用）
        timeout_ms: 超时时间（毫秒）
        notebook_dir: joinquant_notebook 目录路径

    Returns:
        {
            "success": bool,
            "score": float,
            "metrics": dict,
            "factors": list,
            "error": str (if failed)
        }
    """
    if notebook_dir:
        executor = Path(notebook_dir) / "run-strategy.js"
    else:
        executor = find_notebook_executor()

    if not executor or not Path(executor).exists():
        return {
            "success": False,
            "error": f"找不到 run-strategy.js: {executor}",
        }

    cmd = [
        "node",
        str(executor),
        "--strategy",
        str(strategy_file),
        "--timeout-ms",
        str(timeout_ms),
        "--session-file",
        DEFAULT_SESSION_FILE,
        "--notebook-url",
        notebook_url or DEFAULT_NOTEBOOK_URL,
    ]

    data = _run_node(cmd, timeout=timeout_ms // 1000 + 60)

    # 从 executions 中提取策略输出
    if data.get("executions"):
        for exec in data["executions"]:
            if "textOutput" in exec:
                text = exec["textOutput"]
                # 查找包含 "factors" 和 "score" 的 JSON
                start = text.find('{"factors"')
                if start < 0:
                    start = text.find('{"score"')
                if start >= 0:
                    # 从 start 开始找匹配的 }
                    depth = 0
                    end = start
                    for i in range(start, len(text)):
                        if text[i] == "{":
                            depth += 1
                        elif text[i] == "}":
                            depth -= 1
                            if depth == 0:
                                end = i + 1
                                break
                    try:
                        strategy_result = json.loads(text[start:end])
                        return {
                            "success": True,
                            "score": strategy_result.get("score", 0),
                            "metrics": strategy_result.get("metrics", {}),
                            "factors": strategy_result.get("factors", []),
                            "diversity": strategy_result.get("diversity", 0),
                        }
                    except json.JSONDecodeError:
                        pass

    return {
        "success": False,
        "error": data.get("error", "无法解析策略输出"),
        "raw_output": data.get("output", ""),
    }
