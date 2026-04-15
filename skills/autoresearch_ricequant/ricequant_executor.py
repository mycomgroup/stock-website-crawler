#!/usr/bin/env python3
"""
RiceQuant 平台回测执行器

直接通过 HTTP API 与 RiceQuant 交互，读取 session 文件获取认证 cookie。
不依赖 Node.js 脚本的文本输出解析。

Session 文件路径: skills/ricequant_strategy/data/session.json

⚠️  此文件为基础设施文件，agent 不可修改。只改 strategy.py。
"""

import json
import os
import subprocess
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── 路径配置 ──────────────────────────────────────────────────────────────────
RICEQUANT_STRATEGY_DIR = Path(
    "/Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy"
)
SESSION_FILE = Path(
    "/Users/fengzhi/Downloads/git/testlixingren/skills/.sessions/ricequant.json"
)
RUN_SKILL_JS = RICEQUANT_STRATEGY_DIR / "run-skill.js"

RQ_BASE = "https://www.ricequant.com"
DEFAULT_START_DATE = "2021-01-01"
DEFAULT_END_DATE = "2025-03-28"
DEFAULT_CAPITAL = "100000"
DEFAULT_FREQ = "day"
DEFAULT_BENCHMARK = "000300.XSHG"
DEFAULT_POLL_INTERVAL = 15
DEFAULT_MAX_WAIT_SECONDS = 600


class RiceQuantExecutorError(Exception):
    pass


class BacktestTimeoutError(RiceQuantExecutorError):
    pass


class BacktestFailedError(RiceQuantExecutorError):
    pass


# ── Session / HTTP 工具 ───────────────────────────────────────────────────────


SESSION_DURATION_MS = 7 * 24 * 60 * 60 * 1000
AUTO_LOGIN_JS = RICEQUANT_STRATEGY_DIR / "auto-login.js"


def _is_session_valid(session: Dict) -> bool:
    if not session or not session.get("cookies"):
        return False
    cookies = session.get("cookies", [])
    has_valid = any(
        c.get("name") in ("sid", "rqjwt", "access_token")
        or "session" in c.get("name", "").lower()
        or "token" in c.get("name", "").lower()
        for c in cookies
    )
    if not has_valid:
        return False
    timestamp = session.get("timestamp", 0)
    if time.time() * 1000 - timestamp > SESSION_DURATION_MS:
        return False
    return True


def _auto_login() -> Dict[str, Any]:
    print("[auto-login] Session 无效，正在自动登录...")
    if not AUTO_LOGIN_JS.exists():
        raise RiceQuantExecutorError(
            f"自动登录脚本不存在: {AUTO_LOGIN_JS}\n请手动运行: node auto-login.js"
        )
    result = subprocess.run(
        ["node", str(AUTO_LOGIN_JS)],
        cwd=str(RICEQUANT_STRATEGY_DIR),
        capture_output=True,
        text=True,
        timeout=180,
    )
    if result.returncode != 0:
        raise RiceQuantExecutorError(f"自动登录失败: {result.stderr}")
    print("[auto-login] 登录成功")
    return _load_session(auto_login=False)


def _load_session(auto_login: bool = True) -> Dict[str, Any]:
    """读取 session 文件，如果无效则自动登录"""
    if not SESSION_FILE.exists():
        if auto_login:
            return _auto_login()
        raise RiceQuantExecutorError(
            f"Session 文件不存在: {SESSION_FILE}\n"
            "请先运行: node create_rq_strategy.js 或 browser/capture-session.js 登录"
        )
    with open(SESSION_FILE, encoding="utf-8") as f:
        session = json.load(f)
    if auto_login and not _is_session_valid(session):
        return _auto_login()
    return session


def _cookie_header(session: Dict) -> str:
    cookies = session.get("cookies", [])
    return "; ".join(f"{c['name']}={c['value']}" for c in cookies)


def _rq_get(path: str, session: Dict) -> Dict:
    url = RQ_BASE + path
    req = urllib.request.Request(
        url,
        headers={
            "Cookie": _cookie_header(session),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": url,
            "Origin": RQ_BASE,
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def _rq_post(path: str, body: Dict, session: Dict) -> Dict:
    url = RQ_BASE + path
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Cookie": _cookie_header(session),
            "Content-Type": "application/json",
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


def _get_workspace_id(
    session: Dict, max_retries: int = 3, retry_interval: int = 3
) -> str:
    for attempt in range(max_retries):
        result = _rq_get("/api/user/v1/workspaces", session)
        workspaces = result.get("data", [])
        if workspaces:
            return workspaces[0]["id"]
        if attempt < max_retries - 1:
            time.sleep(retry_interval)
    raise RiceQuantExecutorError("No workspace found")


# ── 核心 API ──────────────────────────────────────────────────────────────────


def run_backtest(
    strategy_id: str,
    strategy_file: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    capital: Optional[str] = None,
    freq: Optional[str] = None,
    benchmark: Optional[str] = None,
    no_wait: bool = False,
    **kwargs,
) -> Dict[str, Any]:
    """
    提交回测。先用 run-skill.js 上传策略代码，再通过 HTTP API 提交回测。
    返回 {"backtest_id": str, "status": "submitted"}
    """
    if not os.path.exists(strategy_file):
        raise RiceQuantExecutorError(f"策略文件不存在: {strategy_file}")

    # 确保 strategy_file 是绝对路径（subprocess 的 cwd 不是项目目录）
    strategy_file = str(Path(strategy_file).resolve())

    # 提交前记录当前最新 backtest_id，用于 fallback 时验证新 ID
    _pre_submit_id = _get_latest_backtest_id(str(strategy_id))

    # 用 run-skill.js 提交（它负责上传代码 + 触发回测）
    cmd = [
        "node",
        str(RUN_SKILL_JS),
        "--id",
        str(strategy_id),
        "--file",
        strategy_file,
    ]
    if start_date:
        cmd += ["--start", start_date]
    if end_date:
        cmd += ["--end", end_date]
    if capital:
        cmd += ["--capital", str(capital)]
    if freq:
        cmd += ["--freq", freq]
    if benchmark:
        cmd += ["--benchmark", benchmark]
    if no_wait:
        cmd.append("--no-wait")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=180
        if no_wait
        else 900,  # no-wait 模式快速返回；否则等回测完成最多 15min
        cwd=str(RICEQUANT_STRATEGY_DIR),
    )
    output = result.stdout + result.stderr

    # 从输出里提取 backtest_id（run-skill.js 会打印）
    backtest_id = _extract_backtest_id(output)
    if not backtest_id:
        # 解析失败，打印输出便于排查，等待平台入库后重试
        print(
            f"[run_backtest] _extract_backtest_id 失败，输出末尾:\n{output[-300:]}",
            flush=True,
        )
        # 轮询等待新 ID 出现（最多 30s，每 5s 查一次）
        for _wait in range(6):
            time.sleep(5)
            candidate = _get_latest_backtest_id(str(strategy_id))
            if candidate and candidate != _pre_submit_id:
                backtest_id = candidate
                print(
                    f"[run_backtest] fallback 拿到新 backtest_id={backtest_id}",
                    flush=True,
                )
                break
        if not backtest_id:
            # 最后兜底：即使和旧 ID 相同也用（可能是第一次提交）
            backtest_id = _get_latest_backtest_id(str(strategy_id))

    if not backtest_id:
        raise RiceQuantExecutorError(f"无法获取 backtest_id\noutput:\n{output[:500]}")

    return {
        "backtest_id": str(backtest_id),
        "status": "submitted",
        "raw_output": output,
    }


def _extract_backtest_id(output: str) -> Optional[str]:
    """从 run-skill.js 输出里提取 backtest_id，按优先级匹配多种格式"""
    import re

    for line in output.split("\n"):
        # 格式1（最高优先级）: "   ✓ Backtest started! ID: 7973201"
        if "Backtest started" in line and "ID:" in line:
            after_id = line.split("ID:")[-1].strip().strip("\"' ,")
            if after_id.isdigit():
                return after_id

        # 格式2: JSON 行，如 {"backtestId": "7973999"} 或 {"backtest_id": "..."}
        if "{" in line:
            try:
                data = json.loads(line[line.index("{") :])
                bid = (
                    data.get("backtest_id") or data.get("backtestId") or data.get("_id")
                )
                if bid and str(bid).strip().isdigit():
                    return str(bid).strip()
            except Exception:
                pass

        # 格式3: "Backtest ID: 7973112"（精确匹配，避免误匹配 Strategy ID）
        m = re.search(r"\bBacktest\s+ID[:\s]+(\d{5,})", line, re.IGNORECASE)
        if m:
            return m.group(1)

        # 格式4: "backtest_id: 7973112"（key=value 格式）
        m = re.search(r"\bbacktest_id[:\s=]+(\d{5,})", line, re.IGNORECASE)
        if m:
            return m.group(1)

    return None


def _get_latest_backtest_id(
    strategy_id: str, max_retries: int = 3, retry_interval: int = 3
) -> Optional[str]:
    """通过 API 获取策略最新回测 ID，带重试"""
    for attempt in range(max_retries):
        try:
            session = _load_session()
            workspace_id = _get_workspace_id(session)
            url = f"/api/backtest/v1/workspaces/{workspace_id}/backtests?strategy_id={strategy_id}"
            result = _rq_get(url, session)
            backtests = result.get("backtests", [])
            if backtests:
                latest = sorted(
                    backtests, key=lambda b: b.get("create_at", ""), reverse=True
                )[0]
                bid = str(latest.get("backtest_id") or latest.get("_id") or "").strip()
                if bid:
                    return bid
        except Exception as e:
            print(f"[_get_latest_backtest_id] attempt {attempt + 1}/{max_retries}: {e}")
        if attempt < max_retries - 1:
            time.sleep(retry_interval)
    return None


def wait_for_completion(
    strategy_id: str,
    backtest_id: str,
    max_wait_seconds: int = DEFAULT_MAX_WAIT_SECONDS,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
    **kwargs,
) -> Dict[str, Any]:
    """
    直接通过 HTTP API 轮询回测状态。
    超时后标记为失败（RiceQuant 无取消接口，平台会自动清理）。
    """
    session = _load_session()
    workspace_id = _get_workspace_id(session)
    url = f"/api/backtest/v1/workspaces/{workspace_id}/backtests/{backtest_id}?extra_fields=summary"

    # RiceQuant 成功状态集合
    SUCCESS_STATUSES = {"finished", "normal_exit"}
    FAIL_STATUSES = {"error_exit", "failed", "error", "cancelled"}

    start = time.time()
    _session_refresh_at = start  # 每 5 分钟刷新一次 session
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
        if elapsed > max_wait_seconds:
            # 超时前最后查一次，如果已经完成就还是拿结果
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
            raise BacktestTimeoutError(
                f"回测超时（{max_wait_seconds}s），标记为失败。"
                f"backtest_id={backtest_id}，平台回测仍在运行，下次提交会自动排队。"
            )

        try:
            data = _rq_get(url, session)
            status = (data.get("status") or "").lower()
            progress = data.get("progress", 0)
            print(
                f"[等待回测] backtest_id={backtest_id} status={status} progress={progress}% elapsed={elapsed:.0f}s",
                flush=True,
            )

            if status in SUCCESS_STATUSES:
                summary = data.get("summary") or {}
                return {
                    "backtest_id": backtest_id,
                    "status": status,
                    "summary": summary,
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


def fetch_results(
    strategy_id: str,
    backtest_id: Optional[str] = None,
    save_dir: Optional[str] = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    获取回测完整结果（含 summary + risk）。
    如果 backtest_id 为 None，获取最新一次。
    """
    session = _load_session()
    workspace_id = _get_workspace_id(session)

    if not backtest_id:
        backtest_id = _get_latest_backtest_id(str(strategy_id))
    if not backtest_id:
        raise RiceQuantExecutorError(f"找不到 strategy {strategy_id} 的回测记录")

    result_url = f"/api/backtest/v1/workspaces/{workspace_id}/backtests/{backtest_id}?extra_fields=summary"
    risk_url = (
        f"/api/backtest/v1/workspaces/{workspace_id}/backtests/{backtest_id}/risk"
    )

    result_data = _rq_get(result_url, session)
    try:
        risk_data = _rq_get(risk_url, session)
    except Exception:
        risk_data = {}

    summary = result_data.get("summary") or {}

    output = {
        "backtest_id": backtest_id,
        "status": result_data.get("status", ""),
        "summary": summary,
        "risk": risk_data,
        "full_result": result_data,
        # 把 RiceQuant snake_case 字段映射成 scorer.py 期望的 camelCase
        "annualReturn": summary.get("annualized_returns"),
        "totalReturn": summary.get("total_returns"),
        "maxDrawdown": summary.get("max_drawdown"),
        "sharpe": summary.get("sharpe"),
        "sortino": summary.get("sortina") or summary.get("sortino"),
        "informationRatio": summary.get("information_ratio"),
        "alpha": summary.get("alpha"),
        "beta": summary.get("beta"),
    }

    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        with open(
            os.path.join(save_dir, "fetch_result.json"), "w", encoding="utf-8"
        ) as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

    return output
