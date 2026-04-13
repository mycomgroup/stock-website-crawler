#!/usr/bin/env python3
"""
问财公式回测执行器

通过 subprocess 调用 10jqka_backtest skill（Node.js run-skill.js）执行回测，
解析标准化 JSON 输出并返回指标。

环境变量：
- JQKA_MOCK_MODE=1: 启用 Mock 模式，跳过实际 API 调用，返回模拟数据
"""

import json
import os
import random
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, Optional


JQKA_SKILL_DIR = Path(__file__).parent.parent / "10jqka_backtest"
RUN_SKILL_JS = JQKA_SKILL_DIR / "run-skill.js"

MOCK_MODE = os.environ.get("JQKA_MOCK_MODE", "0") == "1"


class JqkaExecutorError(Exception):
    pass


class BacktestTimeoutError(JqkaExecutorError):
    pass


class BacktestFailedError(JqkaExecutorError):
    pass


class SessionInvalidError(JqkaExecutorError):
    pass


def run_backtest(config: dict, timeout: int = 120) -> dict:
    """
    通过 10jqka_backtest skill 执行回测。

    Args:
        config: 公式策略配置，包含 formula, daysForSaleStrategy, startDate 等字段
        timeout: 最大等待秒数

    Returns:
        {
            "status": "ok",
            "backtest_id": str,
            "summary": {
                "annualReturn": float,
                "maxDrawdown": float,
                "winRate": float,
                "informationRatio": float,
                "sharpe": float,
                "sortino": float,
                "avgHoldingDays": float,
                "tradeCount": int,
                "totalReturn": float
            },
            "full_result": dict
        }

    Raises:
        JqkaExecutorError: 回测失败时抛出
        BacktestTimeoutError: 回测超时时抛出
        SessionInvalidError: Session 无效时抛出
    """
    if MOCK_MODE:
        return _run_mock_backtest(config)

    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        config_file = f.name

    try:
        cmd = ["node", str(RUN_SKILL_JS), config_file]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(JQKA_SKILL_DIR),
        )

        output = result.stdout + result.stderr

        if result.returncode != 0:
            if "noauth" in output.lower() or "401" in output or "未授权" in output:
                raise SessionInvalidError(
                    f"Session 无效，请重新登录\ncd skills/10jqka_backtest && node browser/manual-login-capture.js"
                )
            raise BacktestFailedError(f"回测失败 (exit={result.returncode})\n{output[:1000]}")

        import re

        try:
            saved_match = re.search(r"结果已保存:\s*(.+\.json)", output)
            if saved_match:
                result_file_path = saved_match.group(1).strip()
                if Path(result_file_path).exists():
                    result_data = json.loads(Path(result_file_path).read_text())
                else:
                    raise ValueError(f"结果文件不存在: {result_file_path}")
            else:
                json_start = output.rfind("\n{")
                if json_start == -1:
                    json_start = output.rfind("{")
                if json_start == -1:
                    raise ValueError("输出中未找到 JSON")

                remaining = output[json_start:]
                if remaining.startswith("\n"):
                    remaining = remaining[1:]

                brace_count = 0
                json_end = 0
                for i, c in enumerate(remaining):
                    if c == "{":
                        brace_count += 1
                    elif c == "}":
                        brace_count -= 1
                        if brace_count == 0:
                            json_end = i + 1
                            break

                if json_end == 0:
                    raise ValueError("无法找到完整的 JSON 对象")

                json_str = remaining[:json_end]
                result_data = json.loads(json_str)

        except (json.JSONDecodeError, ValueError) as e:
            raise BacktestFailedError(f"解析回测结果失败: {e}\n输出:\n{output[:500]}")

        if result_data.get("status") != "ok":
            error_msg = result_data.get("message", result_data.get("error", "Unknown error"))
            raise BacktestFailedError(f"回测失败: {error_msg}")

        metrics = result_data.get("metrics", {})

        return {
            "status": "ok",
            "backtest_id": result_data.get("backtest_id", ""),
            "summary": {
                "annualReturn": metrics.get("annualReturn", 0),
                "maxDrawdown": metrics.get("maxDrawdown", 0),
                "winRate": metrics.get("winRate", 0),
                "informationRatio": metrics.get("informationRatio", 0),
                "sharpe": metrics.get("sharpe", 0),
                "sortino": metrics.get("sortino", metrics.get("sharpe", 0) * 1.2),
                "avgHoldingDays": metrics.get("avgHoldingDays", 0),
                "tradeCount": metrics.get("tradeCount", 0),
                "totalReturn": metrics.get("totalReturn", 0),
            },
            "full_result": result_data,
        }

    finally:
        try:
            os.unlink(config_file)
        except Exception:
            pass


def _run_mock_backtest(config: dict) -> dict:
    """
    模拟回测（用于测试）。

    Args:
        config: 公式策略配置

    Returns:
        模拟的回测结果
    """
    time.sleep(2)

    formula_count = len(config.get("formula", []))
    complexity = formula_count

    base_return = 0.08 + random.uniform(0, 0.17)
    complexity_factor = max(0.7, 1.0 - complexity * 0.02)
    annual_return = base_return * complexity_factor

    max_drawdown = abs(annual_return * random.uniform(0.3, 0.6))

    sharpe = random.uniform(1.0, 2.5)
    sortino = sharpe * random.uniform(1.1, 1.4)
    information_ratio = random.uniform(0.5, 1.5)

    win_rate = random.uniform(0.5, 0.7)
    avg_holding_days = float(config.get("daysForSaleStrategy", "2,3").split(",")[0] or 2)
    avg_holding_days = avg_holding_days + random.uniform(0, 5)

    trade_count = random.randint(50, 200)
    total_return = annual_return * 5

    backtest_id = f"mock_{int(time.time())}"

    return {
        "status": "ok",
        "backtest_id": backtest_id,
        "summary": {
            "annualReturn": round(annual_return, 4),
            "maxDrawdown": round(max_drawdown, 4),
            "winRate": round(win_rate, 4),
            "informationRatio": round(information_ratio, 4),
            "sharpe": round(sharpe, 4),
            "sortino": round(sortino, 4),
            "avgHoldingDays": round(avg_holding_days, 2),
            "tradeCount": trade_count,
            "totalReturn": round(total_return, 4),
        },
        "full_result": {
            "status": "ok",
            "backtest_id": backtest_id,
            "metrics": {
                "annualReturn": round(annual_return, 4),
                "maxDrawdown": round(max_drawdown, 4),
                "winRate": round(win_rate, 4),
                "informationRatio": round(information_ratio, 4),
                "sharpe": round(sharpe, 4),
                "sortino": round(sortino, 4),
                "avgHoldingDays": round(avg_holding_days, 2),
                "tradeCount": trade_count,
                "totalReturn": round(total_return, 4),
            },
        },
    }


def validate_config(config: dict) -> bool:
    """
    验证配置合法性。

    Args:
        config: 公式策略配置

    Returns:
        bool: 配置是否合法
    """
    required_fields = ["formula", "startDate", "endDate"]
    for field in required_fields:
        if field not in config:
            return False

    if not isinstance(config.get("formula"), list):
        if not isinstance(config.get("formula"), str):
            return False

    try:
        start_date = config.get("startDate", "")
        end_date = config.get("endDate", "")
        if len(start_date) < 8 or len(end_date) < 8:
            return False
    except Exception:
        return False

    return True
