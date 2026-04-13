#!/usr/bin/env python3
"""
RiceQuant 向导式策略执行器

通过 subprocess 调用 Node.js ricequant-wizard skill（run-skill.js）来更新策略和触发回测，
使用 HTTP 轮询获取回测状态。Session 读取和 HTTP 工具逻辑复用自 ricequant_executor.py。

⚠️  此文件为基础设施文件，agent 不可修改。只改 wizard_config.json。

环境变量：
- WIZARD_MOCK_MODE=1: 启用 Mock 模式，跳过实际 API 调用，返回模拟数据
"""

import json
import os
import random
import re
import subprocess
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Dict, Optional

# ── 路径常量 ──────────────────────────────────────────────────────────────────
WIZARD_SKILL_DIR = Path("/Users/fengzhi/Downloads/git/testlixingren/skills/ricequant-wizard")
SESSION_FILE = Path(
    "/Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy/data/session.json"
)

RQ_BASE = "https://www.ricequant.com"
DEFAULT_POLL_INTERVAL = 15
DEFAULT_MAX_WAIT_SECONDS = 600

# Mock 模式开关
MOCK_MODE = os.environ.get("WIZARD_MOCK_MODE", "0") == "1"


# ── 异常类 ────────────────────────────────────────────────────────────────────


class WizardExecutorError(Exception):
    pass


class BacktestTimeoutError(WizardExecutorError):
    pass


class BacktestFailedError(WizardExecutorError):
    pass


# ── Session / HTTP 工具（复用自 ricequant_executor.py） ───────────────────────


def _load_session() -> Dict[str, Any]:
    """读取 session 文件，返回 {cookies, workspaceId}"""
    if not SESSION_FILE.exists():
        raise WizardExecutorError(
            f"Session 文件不存在: {SESSION_FILE}\n"
            "请先运行: node create_rq_strategy.js 或 browser/capture-session.js 登录"
        )
    with open(SESSION_FILE, encoding="utf-8") as f:
        return json.load(f)


def _cookie_header(session: Dict) -> str:
    cookies = session.get("cookies", [])
    return "; ".join(f"{c['name']}={c['value']}" for c in cookies)


def _rq_get(path: str, session: Dict) -> Dict:
    url = RQ_BASE + path
    req = urllib.request.Request(
        url,
        headers={
            "Cookie": _cookie_header(session),
            "Accept": "application/json",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def _get_workspace_id(session: Dict) -> str:
    result = _rq_get("/api/user/v1/workspaces", session)
    workspaces = result.get("data", [])
    if not workspaces:
        raise WizardExecutorError("No workspace found")
    return workspaces[0]["id"]


# ── 核心 API ──────────────────────────────────────────────────────────────────


def _estimate_candidate_pool_size(config: Dict) -> int:
    """
    预估候选池数量（启发式方法）。

    基于：
    - universe 基础池大小
    - filters 数量和严格程度
    - 每个 filter 对池大小的缩减比例

    Returns:
        int: 预估的候选池数量（筛选后、排序前）
    """
    universe_size_map = {
        "000300.XSHG": 300,  # 沪深300
        "000905.XSHG": 500,  # 中证500
        "000852.XSHG": 1000,  # 中证1000
        "*": 5000,  # 全市场
    }

    universe_list = config.get("universe", ["000300.XSHG"])
    universe = universe_list[0] if universe_list else "000300.XSHG"
    base_size = universe_size_map.get(universe, 300)

    filters = config.get("filters", [])
    if not filters:
        return base_size

    candidate_size = base_size

    for f in filters:
        operator = f.get("operator", "")
        rhs = f.get("rhs", 10)

        reduction_factor = 0.8

        if operator == "less_than":
            threshold_ratio = rhs / 100
            reduction_factor = max(0.2, min(0.9, 0.3 + threshold_ratio * 0.6))
        elif operator == "greater_than":
            threshold_ratio = rhs / 100
            reduction_factor = max(0.2, min(0.9, 0.9 - threshold_ratio * 0.5))
        elif operator == "in_range":
            range_width = (rhs[1] - rhs[0]) / 100 if isinstance(rhs, list) else 0.2
            reduction_factor = max(0.2, min(0.9, 0.4 + range_width * 0.4))

        candidate_size *= reduction_factor

    return int(candidate_size)


def _generate_mock_metrics(config_path: str) -> Dict[str, Any]:
    """
    基于配置生成模拟回测指标。

    简单策略：根据配置的复杂度生成合理的收益和风险指标。
    """
    try:
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)

        num_filters = len(config.get("filters", []))
        num_sorting = len(config.get("sorting", []))
        complexity = num_filters + num_sorting * 0.5

        base_return = 0.08 + random.uniform(0, 0.17)
        complexity_factor = max(0.7, 1.0 - complexity * 0.05)
        annual_return = base_return * complexity_factor

        max_drawdown = abs(annual_return * random.uniform(0.3, 0.6))

        sharpe = random.uniform(1.0, 2.5)
        sortino = sharpe * random.uniform(1.1, 1.4)
        information_ratio = random.uniform(0.5, 1.5)
        alpha = annual_return * random.uniform(0.3, 0.7)
        beta = random.uniform(0.8, 1.2)
        total_return = annual_return * 5

        candidate_pool_size = _estimate_candidate_pool_size(config)

        return {
            "annualReturn": round(annual_return, 4),
            "totalReturn": round(total_return, 4),
            "maxDrawdown": round(max_drawdown, 4),
            "sharpe": round(sharpe, 4),
            "sortino": round(sortino, 4),
            "informationRatio": round(information_ratio, 4),
            "alpha": round(alpha, 4),
            "beta": round(beta, 4),
            "candidatePoolSize": candidate_pool_size,
        }
    except Exception as e:
        print(f"[Mock] 生成模拟指标失败: {e}，使用默认值")
        return {
            "annualReturn": 0.12,
            "totalReturn": 0.60,
            "maxDrawdown": 0.08,
            "sharpe": 1.5,
            "sortino": 2.0,
            "informationRatio": 1.0,
            "alpha": 0.05,
            "beta": 1.0,
            "candidatePoolSize": 50,
        }


def update_strategy(strategy_id: str, config_path: str) -> None:
    """
    通过 Node.js run-skill.js 更新向导式策略配置。

    Args:
        strategy_id: RiceQuant 策略 ID
        config_path: wizard_config.json 的路径（绝对或相对路径）

    Raises:
        WizardExecutorError: Node.js 脚本退出码非零时抛出
    """
    if MOCK_MODE:
        print(f"[Mock] update_strategy: strategy_id={strategy_id}, config={config_path}")
        time.sleep(0.5)  # 模拟网络延迟
        return

    config_path = str(Path(config_path).resolve())
    cmd = [
        "node",
        "run-skill.js",
        "--update",
        "--id",
        str(strategy_id),
        "--config",
        config_path,
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(WIZARD_SKILL_DIR),
    )
    if result.returncode != 0:
        output = result.stdout + result.stderr
        raise WizardExecutorError(
            f"update_strategy 失败 (exit={result.returncode})\n{output[:1000]}"
        )


def run_backtest(strategy_id: str, bt_config: Dict) -> Dict[str, Any]:
    """
    通过 Node.js run-skill.js 触发回测，从输出中提取 backtestId。

    Args:
        strategy_id: RiceQuant 策略 ID
        bt_config: 回测配置，包含 start_date, end_date, capital 等字段

    Returns:
        {"backtest_id": str, "status": "submitted"}

    Raises:
        WizardExecutorError: 无法获取 backtest_id 时抛出
    """
    if MOCK_MODE:
        mock_backtest_id = f"mock_{int(time.time())}"
        print(f"[Mock] run_backtest: strategy_id={strategy_id}, backtest_id={mock_backtest_id}")
        time.sleep(1)  # 模拟提交延迟
        return {"backtest_id": mock_backtest_id, "status": "submitted"}

    start_date = bt_config.get("start_date", "2021-01-01")
    end_date = bt_config.get("end_date", "2025-03-28")
    capital = str(bt_config.get("capital", "100000"))

    cmd = [
        "node",
        "run-skill.js",
        "--run",
        "--id",
        str(strategy_id),
        "--start",
        start_date,
        "--end",
        end_date,
        "--capital",
        capital,
        "--wait",
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=900,
        cwd=str(WIZARD_SKILL_DIR),
    )
    output = result.stdout + result.stderr

    backtest_id = _extract_backtest_id(output)
    if not backtest_id:
        raise WizardExecutorError(f"无法从输出中提取 backtest_id\noutput:\n{output[:500]}")

    return {"backtest_id": str(backtest_id), "status": "submitted"}


def _extract_backtest_id(output: str) -> Optional[str]:
    """
    从 Node.js run-skill.js 输出中提取 backtestId。

    主要格式：「回测已启动: <id>」（纯数字）
    备用格式：JSON 行解析

    Args:
        output: Node.js 脚本的 stdout+stderr 合并输出

    Returns:
        backtestId 字符串，或 None（未找到时）
    """
    for line in output.split("\n"):
        # 主要格式：「回测已启动: <id>」
        m = re.search(r"回测已启动[：:]\s*(\d+)", line)
        if m:
            return m.group(1)

        # 备用格式：JSON 行，如 {"backtestId": "7973999"} 或 {"backtest_id": "..."}
        if "{" in line:
            try:
                data = json.loads(line[line.index("{") :])
                bid = data.get("backtest_id") or data.get("backtestId") or data.get("_id")
                if bid and str(bid).strip().isdigit():
                    return str(bid).strip()
            except Exception:
                pass

    return None


def wait_for_completion(
    backtest_id: str,
    max_wait: int = DEFAULT_MAX_WAIT_SECONDS,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
) -> Dict[str, Any]:
    """
    通过 HTTP 轮询等待回测完成。

    Args:
        backtest_id: 回测 ID
        max_wait: 最大等待秒数（默认 600）
        poll_interval: 轮询间隔秒数（默认 15）

    Returns:
        {"backtest_id": str, "status": str, "summary": dict, ...}

    Raises:
        BacktestTimeoutError: 超时时抛出
        BacktestFailedError: 回测以 error_exit 结束时抛出
    """
    if MOCK_MODE:
        print(f"[Mock] wait_for_completion: backtest_id={backtest_id}")
        time.sleep(2)  # 模拟回测运行时间
        # 从 backtest_id 中提取配置路径（如果可能）
        mock_metrics = {
            "annualReturn": round(random.uniform(0.08, 0.25), 4),
            "totalReturn": round(random.uniform(0.40, 1.25), 4),
            "maxDrawdown": round(random.uniform(0.05, 0.15), 4),
            "sharpe": round(random.uniform(1.0, 2.5), 4),
            "sortino": round(random.uniform(1.5, 3.0), 4),
            "informationRatio": round(random.uniform(0.5, 1.5), 4),
            "alpha": round(random.uniform(0.02, 0.10), 4),
            "beta": round(random.uniform(0.8, 1.2), 4),
        }
        return {
            "backtest_id": backtest_id,
            "status": "finished",
            "summary": mock_metrics,
            "full_result": {"status": "finished", "summary": mock_metrics},
            "elapsed_seconds": 2,
        }

    session = _load_session()
    workspace_id = _get_workspace_id(session)
    url = f"/api/backtest/v1/workspaces/{workspace_id}/backtests/{backtest_id}?extra_fields=summary"

    SUCCESS_STATUSES = {"finished", "normal_exit"}
    FAIL_STATUSES = {"error_exit", "failed", "error", "cancelled"}

    start = time.time()
    _session_refresh_at = start

    while True:
        elapsed = time.time() - start

        # 定期刷新 session，防止长时间轮询时 cookie 过期
        if time.time() - _session_refresh_at > 300:
            try:
                session = _load_session()
                workspace_id = _get_workspace_id(session)
                url = f"/api/backtest/v1/workspaces/{workspace_id}/backtests/{backtest_id}?extra_fields=summary"
                _session_refresh_at = time.time()
            except Exception as e:
                print(f"[等待回测] session 刷新失败: {e}", flush=True)

        if elapsed > max_wait:
            # 超时前最后查一次
            try:
                data = _rq_get(url, session)
                status = (data.get("status") or "").lower()
                if status in SUCCESS_STATUSES:
                    print(
                        f"[等待回测] 超时但回测已完成，取结果 status={status}",
                        flush=True,
                    )
                    return {
                        "backtest_id": backtest_id,
                        "status": status,
                        "summary": data.get("summary") or {},
                        "full_result": data,
                        "elapsed_seconds": elapsed,
                    }
            except Exception:
                pass
            raise BacktestTimeoutError(f"回测超时（{max_wait}s），backtest_id={backtest_id}")

        try:
            data = _rq_get(url, session)
            status = (data.get("status") or "").lower()
            progress = data.get("progress", 0)
            print(
                f"[等待回测] backtest_id={backtest_id} status={status} "
                f"progress={progress}% elapsed={elapsed:.0f}s",
                flush=True,
            )

            if status in SUCCESS_STATUSES:
                return {
                    "backtest_id": backtest_id,
                    "status": status,
                    "summary": data.get("summary") or {},
                    "full_result": data,
                    "elapsed_seconds": elapsed,
                }
            if status in FAIL_STATUSES:
                raise BacktestFailedError(
                    f"回测失败 backtest_id={backtest_id} status={status} "
                    f"exception={data.get('exception', '')}"
                )
        except (BacktestFailedError, BacktestTimeoutError):
            raise
        except Exception as e:
            print(f"[等待回测] 轮询异常: {e}", flush=True)

        time.sleep(poll_interval)


def fetch_results(strategy_id: str, backtest_id: str) -> Dict[str, Any]:
    """
    获取回测结果，映射字段到 scorer.py 期望的 camelCase 格式。

    Args:
        strategy_id: RiceQuant 策略 ID（保留参数，与 ricequant_executor 接口一致）
        backtest_id: 回测 ID

    Returns:
        包含 annualReturn, maxDrawdown, sharpe, sortino, informationRatio,
        alpha, beta, totalReturn, status, backtest_id 的 dict
    """
    if MOCK_MODE:
        print(f"[Mock] fetch_results: strategy_id={strategy_id}, backtest_id={backtest_id}")
        mock_metrics = {
            "annualReturn": round(random.uniform(0.08, 0.25), 4),
            "totalReturn": round(random.uniform(0.40, 1.25), 4),
            "maxDrawdown": round(random.uniform(0.05, 0.15), 4),
            "sharpe": round(random.uniform(1.0, 2.5), 4),
            "sortino": round(random.uniform(1.5, 3.0), 4),
            "informationRatio": round(random.uniform(0.5, 1.5), 4),
            "alpha": round(random.uniform(0.02, 0.10), 4),
            "beta": round(random.uniform(0.8, 1.2), 4),
        }
        return {
            "backtest_id": backtest_id,
            "status": "finished",
            "summary": mock_metrics,
            "full_result": {"status": "finished", "summary": mock_metrics},
            **mock_metrics,
        }

    session = _load_session()
    workspace_id = _get_workspace_id(session)

    result_url = (
        f"/api/backtest/v1/workspaces/{workspace_id}/backtests/{backtest_id}?extra_fields=summary"
    )
    result_data = _rq_get(result_url, session)
    summary = result_data.get("summary") or {}

    return {
        "backtest_id": backtest_id,
        "status": result_data.get("status", ""),
        "summary": summary,
        "full_result": result_data,
        "annualReturn": summary.get("annualized_returns"),
        "totalReturn": summary.get("total_returns"),
        "maxDrawdown": summary.get("max_drawdown"),
        "sharpe": summary.get("sharpe"),
        "sortino": summary.get("sortina") or summary.get("sortino"),
        "informationRatio": summary.get("information_ratio"),
        "alpha": summary.get("alpha"),
        "beta": summary.get("beta"),
    }


def _main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="向导式策略执行器 CLI")
    parser.add_argument("--strategy-id", required=True, help="RiceQuant 策略 ID")
    parser.add_argument("--config", required=True, help="wizard_config.json 路径")
    parser.add_argument("--start-date", default="2020-01-01", help="回测开始日期")
    parser.add_argument("--end-date", default="2025-03-28", help="回测结束日期")
    parser.add_argument("--capital", type=int, default=100000, help="初始资金")
    parser.add_argument("--benchmark", default="000300.XSHG", help="基准指数")
    args = parser.parse_args()

    bt_config = {
        "start_date": args.start_date,
        "end_date": args.end_date,
        "capital": args.capital,
        "benchmark": args.benchmark,
    }

    update_strategy(args.strategy_id, args.config)
    result = run_backtest(args.strategy_id, bt_config)
    backtest_id = result["backtest_id"]

    completed = wait_for_completion(backtest_id)
    final_result = fetch_results(args.strategy_id, backtest_id)

    output = {
        "backtest_id": backtest_id,
        "status": completed.get("status", "unknown"),
        "metrics": {
            "annual_return": final_result.get("annualReturn"),
            "total_return": final_result.get("totalReturn"),
            "max_drawdown": final_result.get("maxDrawdown"),
            "sharpe": final_result.get("sharpe"),
            "sortino": final_result.get("sortino"),
            "information_ratio": final_result.get("informationRatio"),
            "alpha": final_result.get("alpha"),
            "beta": final_result.get("beta"),
        },
        "elapsed_seconds": completed.get("elapsed_seconds", 0),
    }

    print(json.dumps(output))


if __name__ == "__main__":
    _main()
