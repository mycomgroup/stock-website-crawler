#!/usr/bin/env python3
"""
JoinQuant 平台回测执行器

直接通过 HTTP API 与 JoinQuant 交互，读取 session 文件获取认证 cookie。
不依赖 Node.js 脚本等待回测完成。

Session 文件路径: skills/joinquant_strategy/data/session.json

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

JQ_STRATEGY_DIR = Path(
    "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy"
)
SESSION_FILE = JQ_STRATEGY_DIR / "data" / "session.json"
QUICK_SUBMIT_JS = JQ_STRATEGY_DIR / "jq-quick-submit.js"

JQ_BASE = "https://www.joinquant.com"
DEFAULT_START_DATE = "2021-01-01"
DEFAULT_END_DATE = "2025-03-28"
DEFAULT_CAPITAL = "100000"
DEFAULT_FREQ = "day"
DEFAULT_BENCHMARK = "000300.XSHG"
DEFAULT_POLL_INTERVAL = 15
DEFAULT_MAX_WAIT_SECONDS = 600


class JoinQuantExecutorError(Exception):
    pass


class BacktestTimeoutError(JoinQuantExecutorError):
    pass


class BacktestFailedError(JoinQuantExecutorError):
    pass


def _load_session() -> Dict[str, Any]:
    """读取 session 文件，返回 {cookies}"""
    if not SESSION_FILE.exists():
        raise JoinQuantExecutorError(
            f"Session 文件不存在: {SESSION_FILE}\n"
            "请先运行: node browser/capture-session.js 登录"
        )
    with open(SESSION_FILE, encoding="utf-8") as f:
        return json.load(f)


def _cookie_header(session: Dict) -> str:
    cookies = session.get("cookies", [])
    return "; ".join(f"{c['name']}={c['value']}" for c in cookies)


def _jq_get(path: str, session: Dict) -> str:
    url = JQ_BASE + path
    req = urllib.request.Request(
        url,
        headers={
            "Cookie": _cookie_header(session),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode()


def _jq_post(path: str, body: Dict, session: Dict) -> Dict:
    url = JQ_BASE + path
    data = urllib.parse.urlencode(body).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Cookie": _cookie_header(session),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        text = resp.read().decode()
        try:
            return json.loads(text)
        except:
            return {"raw": text}


def _extract_xsrf_token(session: Dict) -> str:
    """从 cookies 中提取 _xsrf token"""
    cookies = session.get("cookies", [])
    for c in cookies:
        if c.get("name") == "_xsrf":
            value = c.get("value", "")
            parts = value.split("|")
            if len(parts) >= 3:
                return parts[2]
    return ""


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
    提交回测。使用 jq-quick-submit.js 快速上传代码并启动回测。
    返回 {"backtest_id": str, "status": "submitted"}
    """
    if not os.path.exists(strategy_file):
        raise JoinQuantExecutorError(f"策略文件不存在: {strategy_file}")

    strategy_file = str(Path(strategy_file).resolve())

    cmd = [
        "node",
        str(QUICK_SUBMIT_JS),
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

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=60,  # 快速返回，不等待回测完成
        cwd=str(JQ_STRATEGY_DIR),
    )
    output = result.stdout + result.stderr

    # 从输出中提取 backtest_id
    backtest_id = _extract_backtest_id(output)
    if not backtest_id:
        print(
            f"[run_backtest] _extract_backtest_id 失败，尝试从 API 获取最新回测",
            flush=True,
        )
        time.sleep(3)  # 等待回测启动
        backtest_id = _get_latest_backtest_id(str(strategy_id))

    if not backtest_id:
        print(f"[run_backtest] 输出末尾:\n{output[-500:]}", flush=True)
        raise JoinQuantExecutorError(f"无法获取 backtest_id")

    print(
        f"[run_backtest] algorithmId={strategy_id}, backtestId={backtest_id}",
        flush=True,
    )
    return {
        "backtest_id": str(backtest_id),
        "status": "submitted",
        "raw_output": output,
    }


def _extract_backtest_id(output: str) -> Optional[str]:
    """从 jq-quick-submit.js 输出里提取 backtest_id"""
    import re

    for line in output.split("\n"):
        # JSON 格式: {"backtest_id": "xxx", ...}
        if "{" in line:
            try:
                data = json.loads(line[line.index("{") :])
                bid = data.get("backtest_id") or data.get("backtestId")
                if bid:
                    return str(bid)
            except:
                pass

    # 备用：正则匹配 32位十六进制
    m = re.search(r"([a-f0-9]{32})", output)
    if m:
        return m.group(1)

    return None


def _get_latest_backtest_id(
    algorithm_id: str, max_retries: int = 5, retry_interval: int = 3
) -> Optional[str]:
    """通过 API 获取策略最新回测 ID"""
    for attempt in range(max_retries):
        try:
            session = _load_session()
            url = f"/algorithm/backtest/list?algorithmId={algorithm_id}"
            html = _jq_get(url, session)

            import re

            # 提取所有 backtestId，返回第一个（最新的）
            matches = re.findall(r'_backtestId="([^"]+)"', html)
            if matches:
                # 去重，返回第一个
                seen = set()
                for bid in matches:
                    if bid not in seen:
                        seen.add(bid)
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
    JoinQuant 状态: status=0 完成, status=-1 运行中, status=-2 失败
    """
    session = _load_session()
    xsrf_token = _extract_xsrf_token(session)

    start = time.time()
    _session_refresh_at = start

    while True:
        elapsed = time.time() - start

        if time.time() - _session_refresh_at > 300:
            try:
                session = _load_session()
                xsrf_token = _extract_xsrf_token(session)
                _session_refresh_at = time.time()
            except Exception as e:
                print(f"[等待回测] session 刷新失败: {e}", flush=True)

        if elapsed > max_wait_seconds:
            raise BacktestTimeoutError(
                f"回测超时（{max_wait_seconds}s），backtest_id={backtest_id}"
            )

        try:
            html = _jq_get(
                f"/algorithm/backtest/list?algorithmId={strategy_id}", session
            )

            import re

            status_match = re.search(
                r'_backtestId="{}"[^>]*_status="(\d+)"'.format(backtest_id), html
            )

            if status_match:
                status_code = int(status_match.group(1))

                # JoinQuant 状态码：-1=运行中, 0/2=完成, -2=失败
                if status_code in (0, 2):
                    print(
                        f"[等待回测] backtest_id={backtest_id} 完成 elapsed={elapsed:.0f}s",
                        flush=True,
                    )
                    result = _get_backtest_result(backtest_id, session, xsrf_token)
                    return {
                        "backtest_id": backtest_id,
                        "status": "finished",
                        "result": result,
                        "elapsed_seconds": elapsed,
                    }
                elif status_code == -2:
                    raise BacktestFailedError(
                        f"回测失败 backtest_id={backtest_id} status=-2"
                    )
                else:
                    print(
                        f"[等待回测] backtest_id={backtest_id} status={status_code} elapsed={elapsed:.0f}s",
                        flush=True,
                    )
        except (BacktestFailedError, BacktestTimeoutError):
            raise
        except Exception as e:
            print(f"[等待回测] 轮询异常: {e}", flush=True)

        time.sleep(poll_interval)


def _get_backtest_result(backtest_id: str, session: Dict, xsrf_token: str) -> Dict:
    """获取回测结果"""
    url = f"/algorithm/backtest/result?backtestId={backtest_id}&offset=0&ajax=1"
    body = {"token": xsrf_token, "ajax": "1"}
    result = _jq_post(url, body, session)
    return result


def _get_backtest_stats(backtest_id: str, session: Dict, xsrf_token: str) -> Dict:
    """获取回测统计数据"""
    url = f"/algorithm/backtest/stats?backtestId={backtest_id}&ajax=1"
    body = {"token": xsrf_token, "ajax": "1"}
    result = _jq_post(url, body, session)
    return result.get("data", {})


def fetch_results(
    strategy_id: str,
    backtest_id: Optional[str] = None,
    save_dir: Optional[str] = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    获取回测完整结果（含 stats）。
    如果 backtest_id 为 None，获取最新一次。
    """
    session = _load_session()
    xsrf_token = _extract_xsrf_token(session)

    if not backtest_id:
        backtest_id = _get_latest_backtest_id(str(strategy_id))
    if not backtest_id:
        raise JoinQuantExecutorError(f"找不到 strategy {strategy_id} 的回测记录")

    result_data = _get_backtest_result(backtest_id, session, xsrf_token)
    stats_data = _get_backtest_stats(backtest_id, session, xsrf_token)

    stats = stats_data
    result_dict = result_data.get("data", {}).get("result", {})

    output = {
        "backtest_id": backtest_id,
        "status": "finished" if result_data.get("status") == 0 else "running",
        "stats": stats,
        "result": result_dict,
        "annualReturn": stats.get("annual_return", 0),
        "totalReturn": stats.get("total_return", 0),
        "maxDrawdown": stats.get("max_drawdown", 0),
        "sharpe": stats.get("sharpe", 0),
        "alpha": stats.get("alpha", 0),
        "beta": stats.get("beta", 0),
        "sortino": stats.get("sortino", 0),
        "informationRatio": stats.get("information_ratio", 0),
    }

    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        with open(
            os.path.join(save_dir, "fetch_result.json"), "w", encoding="utf-8"
        ) as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

    return output
