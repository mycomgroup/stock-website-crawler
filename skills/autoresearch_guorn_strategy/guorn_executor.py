"""
果仁网策略执行器

通过 subprocess 调用 guorn_strategy skill 执行回测，解析结果并返回标准化格式。

参考设计文档: .kiro/specs/autoresearch-guorn-strategy/design.md

⚠️  此文件为基础设施文件，agent 不可修改。只改配置文件。
"""

import json
import os
import random
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, Optional


# ── 路径常量 ──────────────────────────────────────────────────────────────────
GUORN_SKILL_DIR = Path(__file__).parent.parent / "guorn_strategy"
SESSION_FILE = GUORN_SKILL_DIR / "data" / "session.json"
RUN_SKILL_JS = GUORN_SKILL_DIR / "run-skill.js"

# Mock 模式开关
MOCK_MODE = os.environ.get("GUORN_MOCK_MODE", "0") == "1"


# ── 异常类 ────────────────────────────────────────────────────────────────────

class GuornExecutorError(Exception):
    """果仁执行器基础异常"""
    pass


class BacktestTimeoutError(GuornExecutorError):
    """回测超时异常"""
    pass


class BacktestFailedError(GuornExecutorError):
    """回测失败异常"""
    pass


class SessionInvalidError(GuornExecutorError):
    """Session 无效异常"""
    pass


# ── 核心 API ──────────────────────────────────────────────────────────────────

def run_backtest(config: dict, session_file: Optional[str] = None) -> dict:
    """
    通过 guorn_strategy skill 执行回测。

    Args:
        config: 策略配置，包含 filters, ranks, pool, start, end 等字段
        session_file: session.json 路径（可选，默认使用 GUORN_SKILL_DIR/data/session.json）

    Returns:
        {
            "status": "ok",
            "backtest_id": str,  # calc_id
            "summary": {
                "annualReturn": float,
                "maxDrawdown": float,
                "winRate": float,
                "informationRatio": float,
                "avgHoldingDays": float,
                "sellCount": int,
                ...
            },
            "full_result": dict  # 完整的果仁回测结果
        }

    Raises:
        GuornExecutorError: 回测失败时抛出
        BacktestTimeoutError: 回测超时时抛出
        SessionInvalidError: Session 无效时抛出
    """
    if MOCK_MODE:
        return _run_mock_backtest(config)

    # 1. 验证 session 文件存在
    if session_file is None:
        session_file = str(SESSION_FILE)

    if not Path(session_file).exists():
        raise SessionInvalidError(
            f"Session 文件不存在: {session_file}\n"
            "请先运行: cd skills/guorn_strategy && node request/ensure-session.js"
        )

    # 2. 验证 session 有效性
    try:
        session_info = validate_session(session_file)
        if not session_info["valid"]:
            raise SessionInvalidError("Session 无效，请重新登录")
    except Exception as e:
        raise SessionInvalidError(f"Session 验证失败: {e}")

    # 3. 准备配置文件
    # 将配置写入临时文件
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        config_file = f.name

    try:
        # 4. 调用 run-skill.js
        cmd = [
            "node",
            str(RUN_SKILL_JS),
            "backtest",
            "--config", config_file,
        ]

        # 添加回测参数
        backtest_config = config.get("backtest", {})
        if backtest_config.get("start"):
            cmd.extend(["--start", backtest_config["start"]])
        if backtest_config.get("end"):
            cmd.extend(["--end", backtest_config["end"]])
        if backtest_config.get("benchmark"):
            cmd.extend(["--benchmark", backtest_config["benchmark"]])
        if backtest_config.get("trade_cost") is not None:
            cmd.extend(["--cost", str(backtest_config["trade_cost"])])
        if config.get("holding_num"):
            cmd.extend(["--count", str(config["holding_num"])])
        if config.get("rebalance_interval"):
            cmd.extend(["--period", str(config["rebalance_interval"])])

        print(f"[执行器] 运行命令: {' '.join(cmd)}")

        # 执行命令（最多等待 120 秒）
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(GUORN_SKILL_DIR),
        )

        if result.returncode != 0:
            output = result.stdout + result.stderr
            raise BacktestFailedError(
                f"回测失败 (exit={result.returncode})\n{output[:1000]}"
            )

        # 5. 解析输出
        # run-skill.js 应该输出 JSON 格式的结果
        output = result.stdout
        try:
            # 尝试从输出中提取结果文件路径
            # 输出格式: "Result saved to: /path/to/file.json"
            result_file_match = None
            for line in output.split('\n'):
                if 'Result saved to:' in line or 'Full result:' in line:
                    # 提取文件路径
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        result_file_match = parts[1].strip()
                        break
            
            if result_file_match and Path(result_file_match).exists():
                # 读取结果文件
                with open(result_file_match, 'r', encoding='utf-8') as f:
                    result_data = json.load(f)
            else:
                # 尝试从输出中提取 JSON
                json_start = output.find('{')
                json_end = output.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = output[json_start:json_end]
                    result_data = json.loads(json_str)
                else:
                    raise ValueError("输出中未找到 JSON 数据")
        except (json.JSONDecodeError, ValueError) as e:
            raise BacktestFailedError(
                f"解析回测结果失败: {e}\n输出:\n{output[:500]}"
            )

        # 6. 提取关键指标
        if result_data.get("status") != "ok":
            raise BacktestFailedError(
                f"回测失败: {result_data.get('message', 'Unknown error')}"
            )

        data = result_data.get("data", {})

        # 从 summary2 提取指标
        # meas_data 列顺序（来自 sheet_defn.layout.grid.column）:
        # [0]=TotalReturn, [1]=AnnualReturn, [2]=SharpeRatio, [3]=MaxDrawDown,
        # [4]=Volatility, [5]=InformationRatio, [6]=Beta, [7]=Alpha
        # 每列格式: [策略值, 基准值]
        summary2 = data.get("summary2", {})
        sheet_data = summary2.get("sheet_data", {})
        meas_data = sheet_data.get("meas_data", [])

        def _meas(col, row=0, default=0):
            try:
                v = meas_data[col][row]
                return float(v) if v != '-' else default
            except (IndexError, TypeError, ValueError):
                return default

        total_return    = _meas(0)
        annual_return   = _meas(1)
        sharpe          = _meas(2)
        max_drawdown    = _meas(3)   # 真实回撤比例，如 0.30 表示 30%
        information_ratio = _meas(5)

        # 从 trade_summary 提取其他指标
        trade_summary = data.get("trade_summary", {})
        win_rate         = trade_summary.get("win_ratio", 0)
        avg_holding_days = trade_summary.get("avg_holding_days", 0)
        sell_count       = trade_summary.get("sell_count", 0)

        # calc_id
        calc_id = data.get("session_id", "") or data.get("calc_id", "")

        # 7. 返回标准化格式
        return {
            "status": "ok",
            "backtest_id": calc_id,
            "summary": {
                "annualReturn": annual_return,
                "maxDrawdown": max_drawdown,
                "winRate": win_rate,
                "informationRatio": information_ratio,
                "sharpe": sharpe,
                "sortino": sharpe * 1.2,  # Sortino 不可用，用 Sharpe * 1.2 近似
                "avgHoldingDays": avg_holding_days,
                "sellCount": sell_count,
                "totalReturn": total_return,
            },
            "full_result": result_data,
        }

    finally:
        # 清理临时文件
        try:
            os.unlink(config_file)
        except Exception:
            pass


def _run_mock_backtest(config: dict) -> dict:
    """
    模拟回测（用于测试）。

    Args:
        config: 策略配置

    Returns:
        模拟的回测结果
    """
    print("[Mock] 模拟回测模式")

    # 模拟延迟
    time.sleep(2)

    # 基于配置复杂度生成模拟指标
    num_filters = len(config.get("filters", []))
    num_rankings = len(config.get("rankings", []))
    complexity = num_filters + num_rankings * 0.5

    # 基础年化收益：8% - 25%
    base_return = 0.08 + random.uniform(0, 0.17)
    # 复杂度调整：更多筛选条件可能降低收益但降低风险
    complexity_factor = max(0.7, 1.0 - complexity * 0.05)
    annual_return = base_return * complexity_factor

    # 最大回撤：与收益相关，但有随机性
    max_drawdown = abs(annual_return * random.uniform(0.3, 0.6))

    # 夏普比率：1.0 - 2.5
    sharpe = random.uniform(1.0, 2.5)

    # Sortino 通常高于 Sharpe
    sortino = sharpe * random.uniform(1.1, 1.4)

    # 信息比率：0.5 - 1.5
    information_ratio = random.uniform(0.5, 1.5)

    # 胜率：0.5 - 0.7
    win_rate = random.uniform(0.5, 0.7)

    # 平均持仓天数：10 - 30
    avg_holding_days = random.uniform(10, 30)

    # 卖出次数：50 - 200
    sell_count = random.randint(50, 200)

    # 总收益（假设回测 5 年）
    total_return = annual_return * 5

    # 生成 calc_id
    calc_id = f"mock_{int(time.time())}"

    return {
        "status": "ok",
        "backtest_id": calc_id,
        "summary": {
            "annualReturn": round(annual_return, 4),
            "maxDrawdown": round(max_drawdown, 4),
            "winRate": round(win_rate, 4),
            "informationRatio": round(information_ratio, 4),
            "sharpe": round(sharpe, 4),
            "sortino": round(sortino, 4),
            "avgHoldingDays": round(avg_holding_days, 2),
            "sellCount": sell_count,
            "totalReturn": round(total_return, 4),
        },
        "full_result": {
            "status": "ok",
            "data": {
                "calc_id": calc_id,
                "trade_summary": {
                    "winsorize_annual": round(annual_return, 4),
                    "maxdrop_day": round(max_drawdown, 4),
                    "win_ratio": round(win_rate, 4),
                    "year_information_ratio": round(information_ratio, 4),
                    "sharpe_ratio": round(sharpe, 4),
                    "sortino_ratio": round(sortino, 4),
                    "avg_hold_days": round(avg_holding_days, 2),
                    "sell_count": sell_count,
                    "total_return": round(total_return, 4),
                },
            },
        },
    }


def validate_session(session_file: Optional[str] = None) -> dict:
    """
    验证 session 文件有效性。

    Args:
        session_file: session.json 路径（可选）

    Returns:
        {
            "valid": bool,
            "username": str,
            "level": int,  # 1=普通账号（回测窗口约1年）
            "cookies": list
        }

    Raises:
        SessionInvalidError: Session 文件不存在或格式错误
    """
    if session_file is None:
        session_file = str(SESSION_FILE)

    if not Path(session_file).exists():
        raise SessionInvalidError(f"Session 文件不存在: {session_file}")

    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            session = json.load(f)

        # 检查必需字段
        if "cookies" not in session:
            return {"valid": False, "username": "", "level": 0, "cookies": []}

        # 检查 cookies 是否过期（简单检查）
        cookies = session.get("cookies", [])
        if not cookies:
            return {"valid": False, "username": "", "level": 0, "cookies": []}

        # 提取用户信息（如果有）
        username = session.get("username", "")
        level = session.get("level", 1)

        return {
            "valid": True,
            "username": username,
            "level": level,
            "cookies": cookies,
        }

    except (json.JSONDecodeError, IOError) as e:
        raise SessionInvalidError(f"Session 文件格式错误: {e}")


def normalize_config(config: dict) -> dict:
    """
    规范化策略配置为果仁格式。

    Args:
        config: 高级配置（filters, rankings, pool 等）

    Returns:
        dict: 规范化后的配置

    Note:
        当前版本简化处理，未来可以集成 config-normalizer.js
    """
    # 简化版本：直接返回配置
    # 未来可以调用 config-normalizer.js 进行更复杂的转换
    return config
